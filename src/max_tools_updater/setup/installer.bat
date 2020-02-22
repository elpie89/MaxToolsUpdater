@ECHO off

set assemblyFolder=%1
set enableLog=%2
set maxlocation=%~3
set assembliesAdd=%~4
set assembliesRemove=%~5
set rootLibsAdd=%~6
set rootLibsRemove=%~7

taskkill  /im 3dsmax.exe /f

set installerPath="%~dp0installer.ps1"

start /wait PowerShell.exe -NoProfile -Command "& {Start-Process PowerShell.exe -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File " ""%installerPath%"" """%assemblyFolder%""" ""%enableLog%"" """%assembliesAdd%""" """%assembliesRemove%""" """%rootLibsAdd%""" """%rootLibsRemove%""" """%maxlocation%"""' -Verb RunAs}"

