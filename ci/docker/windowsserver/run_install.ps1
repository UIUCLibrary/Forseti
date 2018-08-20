﻿$MSIFILES = Get-ChildItem -Path . -Filter *.msi

# Only continue if one and only one msi file is located
try
{
    # If there are no files found, then there was a failure during the building of the docker image
    if($MSIFILES.Count -eq 0)
    {
        throw "No Files found in the docker image container."
    }

    # If there are more than one files found, then a the environment had multiple msi files during docker build
    # and needs to be properly cleaned up first
    if($MSIFILES.Count -ne 1){

        foreach ($MSIFILE in $MSIFILES)
        {
            Write-Host "Found  $MSIFILE"
        }

        throw "Found more than one msi file."
    }

}
catch
{
    Write-Host "Unable to install msi file. Quiting"
    exit 1
}

# At this point there should only be a single msi file to run
try{
    foreach ($MSIFILE in $MSIFILES) {
        echo "Running msiexec on $MSIFILE"
        msiexec /i $MSIFILE /q /lp dockerinstall.log
        $RC = $LASTEXITCODE
        if ($RC -ne 0) {
            Write-Error "Exit code is $RC ."
            throw "Problem running msiexec."
        }
    }
}
catch
{
    Write-Host "Failed to install"
    exit 1
}



