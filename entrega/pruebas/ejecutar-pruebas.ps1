param(
    [string]$ProjectRoot = (Join-Path $PSScriptRoot '..\..'),
    [string]$JavaHome,
    [string]$OutputDirectory
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)

# PowerShell 5 representa stderr nativo como ErrorRecord. Capturarlo no debe
# convertir el texto de java -version ni un diagnóstico en excepción del script.
function Invoke-NativeCapture {
    param([string]$Executable, [string[]]$Arguments)
    $ErrorActionPreference = 'Continue'
    $lines = @(& $Executable @Arguments 2>&1 | ForEach-Object { $_.ToString() })
    return [pscustomobject]@{ Output = $lines; ExitCode = $LASTEXITCODE }
}
$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
if (-not $OutputDirectory) { $OutputDirectory = Join-Path $ProjectRoot 'entrega\evidencias' }
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$OutputDirectory = (Resolve-Path -LiteralPath $OutputDirectory).Path

if (-not $JavaHome) {
    $preferred = Join-Path $env:USERPROFILE '.jdks\ms-17.0.21.0.2'
    if (Test-Path -LiteralPath (Join-Path $preferred 'bin\javac.exe')) { $JavaHome = $preferred }
    elseif ($env:JAVA_HOME -and (Test-Path -LiteralPath (Join-Path $env:JAVA_HOME 'bin\javac.exe'))) { $JavaHome = $env:JAVA_HOME }
    else { throw 'Indique -JavaHome con la ruta de un JDK 17 o superior.' }
}
$java = Join-Path $JavaHome 'bin\java.exe'
$javac = Join-Path $JavaHome 'bin\javac.exe'
if (-not (Test-Path -LiteralPath $java) -or -not (Test-Path -LiteralPath $javac)) {
    throw "No se encontró un JDK válido en $JavaHome"
}

$classes = Join-Path $env:TEMP ('BibliotecaReservas-pruebas-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $classes | Out-Null
$sourceDirectory = Join-Path $ProjectRoot 'src\main\java\biblioteca'
$sources = @(Get-ChildItem -LiteralPath $sourceDirectory -Filter '*.java' -File | Sort-Object Name | Select-Object -ExpandProperty FullName)
if ($sources.Count -ne 21) { throw "Se esperaban 21 fuentes oficiales; se encontraron $($sources.Count)." }
$harness = Join-Path $PSScriptRoot 'PruebasBiblioteca.java'
$jsonPath = Join-Path $OutputDirectory 'resultados-pruebas.json'
$commands = @(
    "JDK: $JavaHome",
    "Compilación: & `"$javac`" --release 17 -encoding UTF-8 -Xlint:all -d `"$classes`" <21 fuentes Java oficiales> `"$harness`"",
    "Pruebas: & `"$java`" -Dfile.encoding=UTF-8 -cp `"$classes`" PruebasBiblioteca `"$jsonPath`"",
    "Main: & `"$java`" -Dfile.encoding=UTF-8 -cp `"$classes`" biblioteca.Main"
)
$commands | Set-Content -LiteralPath (Join-Path $OutputDirectory 'comandos-ejecutados.log') -Encoding UTF8

$javacVersion = ((Invoke-NativeCapture $javac @('-version')).Output | Out-String).Trim()
$javaVersion = ((Invoke-NativeCapture $java @('-version')).Output | Out-String).Trim()
$compilation = Invoke-NativeCapture $javac (@('--release', '17', '-encoding', 'UTF-8', '-Xlint:all', '-d', $classes) + $sources + @($harness))
$compileOutput = $compilation.Output
$compileExit = $compilation.ExitCode
@($javacVersion; $compileOutput; "EXIT_CODE=$compileExit") | Set-Content -LiteralPath (Join-Path $OutputDirectory 'compilacion.log') -Encoding UTF8
if ($compileExit -ne 0) { $compileOutput | Write-Output; throw "Compilación fallida ($compileExit)." }

$testRun = Invoke-NativeCapture $java @('-Dfile.encoding=UTF-8', '-cp', $classes, 'PruebasBiblioteca', $jsonPath)
$testOutput = $testRun.Output
$testExit = $testRun.ExitCode
@($testOutput; "EXIT_CODE=$testExit") | Set-Content -LiteralPath (Join-Path $OutputDirectory 'pruebas.log') -Encoding UTF8
$testOutput | Write-Output

$mainRun = Invoke-NativeCapture $java @('-Dfile.encoding=UTF-8', '-cp', $classes, 'biblioteca.Main')
$mainOutput = $mainRun.Output
$mainExit = $mainRun.ExitCode
@($mainOutput; "EXIT_CODE=$mainExit") | Set-Content -LiteralPath (Join-Path $OutputDirectory 'ejecucion-main.log') -Encoding UTF8
$mainOutput | Write-Output

$bogotaZone = [TimeZoneInfo]::FindSystemTimeZoneById('SA Pacific Standard Time')
$metadata = [ordered]@{
    ejecutadoUtc = [DateTime]::UtcNow.ToString('o')
    ejecutadoBogota = [TimeZoneInfo]::ConvertTimeFromUtc([DateTime]::UtcNow, $bogotaZone).ToString('yyyy-MM-dd HH:mm:ss')
    zonaHoraria = 'America/Bogota'
    javaHome = $JavaHome
    javaVersion = $javaVersion
    javacVersion = $javacVersion
    powershellVersion = $PSVersionTable.PSVersion.ToString()
    clasesTemporales = $classes
    fuentesOficiales = $sources.Count
    compilacionExitCode = $compileExit
    pruebasExitCode = $testExit
    mainExitCode = $mainExit
    fuentesSha256 = @(Get-FileHash -LiteralPath $sources -Algorithm SHA256 | Select-Object Path, Hash)
    harnessSha256 = (Get-FileHash -LiteralPath $harness -Algorithm SHA256).Hash
}
$metadata | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $OutputDirectory 'entorno-ejecucion.json') -Encoding UTF8
if ($testExit -ne 0 -or $mainExit -ne 0) { throw "Verificación fallida: pruebas=$testExit; Main=$mainExit. Revise los logs." }
Write-Output "Verificación completada. Evidencias: $OutputDirectory"
