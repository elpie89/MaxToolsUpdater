$MAXVERSION = Read-Host -Prompt 'Prompt your 3dsMax version...2019 or superior'
$MTU_FOLDER = split-path -parent $MyInvocation.MyCommand.Definition
$3DSMAX = (Get-Item env:ADSK_3DSMAX_x64_$MAXVERSION).Value
$3DSMAXPY = "$3DSMAX\3dsmaxpy.exe"
$BUILD_FOLDER = "$MTU_FOLDER\build"
Write-Output $3DSMAXPY

New-Item  $BUILD_FOLDER -Force -ItemType Directory
Copy-Item "$MTU_FOLDER\src\max_tools_updater" -Destination "$BUILD_FOLDER\max_tools_updater" -Recurse -Force
Copy-Item "$MTU_FOLDER\src\installer.ps1" -Destination "$BUILD_FOLDER\installer.ps1" -Force
Copy-Item "$MTU_FOLDER\src\userSetup.bat" -Destination "$BUILD_FOLDER\userSetup.bat" -Force
Copy-Item $MTU_FOLDER\src\maxToolsUpdater.ms -Destination "$BUILD_FOLDER\maxToolsUpdater.ms" -Force

$Dir = Get-ChildItem "$BUILD_FOLDER" -Recurse
$PyFiles = $Dir | Where-Object {$_.extension -eq ".py"}
Foreach ($PyFile in $PyFiles)
{
    $FilePath = $PyFile.FullName
    if (Test-Path $FilePath)
    {
         # removes comments. It leaves docstrings intact
        Start-Process "$3DSMAXPY" "-m py_compile $FilePath" -RedirectStandardError  "$MTU_FOLDER\BuildError.log"
        if($PyFile.Name -ne "main.py")
        {
            Write-Output $FilePath
            Remove-Item $FilePath -Force
        }
    }
}