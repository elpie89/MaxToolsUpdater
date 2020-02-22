$MTU_FOLDER = split-path -parent $MyInvocation.MyCommand.Definition

function CopyObjects ([Int16] $MAX_CHOISE)
{
    switch ($MAX_CHOISE)
    {
       1 { $MAX_VERSION=2019;$MAX_DIR = $Env:ADSK_3DSMAX_x64_2019; break}
       2 { $MAX_VERSION=2020;$MAX_DIR = $Env:ADSK_3DSMAX_x64_2020; break}
       3 { $MAX_VERSION=2021;$MAX_DIR = $Env:ADSK_3DSMAX_x64_2021; break}
       default {"User choice not valid";return}
    }
    $INSTALL_DIR = $env:LOCALAPPDATA+="\Autodesk\3dsMax\$MAX_VERSION - 64bit\ENU\scripts\startup"

    $MAX_PROCESS = Get-Process "3dsmax" -ErrorAction SilentlyContinue
    if ($MAX_PROCESS){Stop-Process -ProcessName "3dsmax"}
    Write-Output "Max installation directory $INSTALL_DIR"
    Write-Output "Max version $MAX_VERSION"
    Write-Output "Max dir  $MAX_DIR"

#    Write-Output  "Installing PIP"
#	Start-Process "$MAX_DIR\3dsmaxpy.exe" "$MTU_FOLDER\get-pip.py --user" -Wait

	Write-Output "Installing Max Tools Updater"
	Write-Output "From: $MTU_FOLDER"
	Write-Output "To: $INSTALL_DIR"
    Copy-Item -Path "$MTU_FOLDER\maxToolsUpdater.ms " -Destination "$INSTALL_DIR\maxToolsUpdater.ms" -Force
    (Get-Content -path "$INSTALL_DIR\maxToolsUpdater.ms" -Raw) -replace "###MAXTOOLUPDATERPATH###","$MTU_FOLDER\max_tools_updater" | Set-Content "$INSTALL_DIR\maxToolsUpdater.ms"
    Start-Process "$MAX_DIR\3dsmax.exe"
}

Write-Output "Please enter your 3DSMAX version"
Write-Output "choose 1 for 2019"
Write-Output "choose 2 for 2020"
Write-Output "choose 3 for 2021"

$MAX_CHOISE = Read-Host
CopyObjects $MAX_CHOISE
