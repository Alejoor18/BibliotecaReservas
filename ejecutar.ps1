param([string]$JavaHome)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
if (-not $JavaHome) {
    $preferido = Join-Path $env:USERPROFILE '.jdks\ms-17.0.21.0.2'
    if (Test-Path (Join-Path $preferido 'bin\javac.exe')) { $JavaHome = $preferido }
    elseif ($env:JAVA_HOME) { $JavaHome = $env:JAVA_HOME }
    else { throw 'Indique -JavaHome con la ruta de un JDK 17 o superior.' }
}
$javac = Join-Path $JavaHome 'bin\javac.exe'
$java = Join-Path $JavaHome 'bin\java.exe'
if (-not (Test-Path $javac) -or -not (Test-Path $java)) { throw 'La ruta debe contener un JDK completo.' }
$salida = Join-Path $env:TEMP ('BibliotecaReservas-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $salida | Out-Null
$fuentes = @(Get-ChildItem (Join-Path $PSScriptRoot 'src\main\java\biblioteca\*.java') | Select-Object -ExpandProperty FullName)
& $javac --release 17 -encoding UTF-8 -d $salida @fuentes
if ($LASTEXITCODE -ne 0) { throw 'Compilación fallida. Se requiere JDK 17 o superior.' }
& $java '-Dfile.encoding=UTF-8' '-Dsun.stdout.encoding=UTF-8' '-Dsun.stderr.encoding=UTF-8' -cp $salida biblioteca.Main
if ($LASTEXITCODE -ne 0) { throw 'La aplicación terminó con error.' }
