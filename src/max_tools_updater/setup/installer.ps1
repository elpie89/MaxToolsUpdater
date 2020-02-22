param
(
    [string]$assemblyFolder,
    [string]$enableLog,
    [string]$addAssemmblyFiles,
    [string]$removeAssemmblyFiles,
    [string]$addRootLibFiles,
    [string]$removeRootLibFiles,
    [string]$maxlocation
)

Write-Output "assemblyfolder: "$assemblyFolder
Write-Output "enable log: "$enableLog
Write-Output "assembly files to add:" $addAssemmblyFiles
Write-Output "assembly file to remove: "$removeAssemmblyFiles
Write-Output "max location: "$maxlocation
#remove feature temporarly removed
#Write-Output "root lib files to add:" $addRootLibFiles
#Write-Output "root lib file to remove: "$removeRootLibFiles

$addAssemblies = $addAssemmblyFiles.split(";")
$removeAssemblies = $removeAssemmblyFiles.split(";")
$addRootLib = $addRootLibFiles.split(";")
$removeRootLib = $removeRootLibFiles.split(";")
$maxfolder = Split-Path -Path $maxlocation

if($addAssemblies -ne "")
{
    Foreach ($file in $addAssemblies)
    {
        Write-Output "Copy-Item ($file) `n to ($assemblyFolder) `n`n"
        Copy-Item $file -Destination $assemblyFolder -Force
    }
}

if($addRootLib -ne "")
{
    Foreach ($file in $addRootLib)
    {
        Write-Output "Copy-Item ($file) `n to ($maxfolder) `n`n"
        Copy-Item $file -Destination $maxfolder -Force
    }
}

#if($removeAssemblies -ne "")
#{
#    Foreach ($file in $removeAssemblies)
#    {
#        if(($file -ne "") -and (Test-Path -Path $file))
#        {
#            Write-Output "delete ($file)"
#            Remove-Item -Path $file -Force
#        }
#    }
#}
#
#if($removeRootLib -ne "")
#{
#    Foreach ($file in $removeRootLib)
#    {
#        if(($file -ne "") -and (Test-Path -Path $file))
#        {
#            Write-Output "delete ($file)"
#            Remove-Item -Path $file -Force
#        }
#    }
#}

Start-Process -FilePath "$maxlocation"

if($enableLog.equals("True"))
{
    Write-Host -NoNewLine 'Press any key to continue...';
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
}

