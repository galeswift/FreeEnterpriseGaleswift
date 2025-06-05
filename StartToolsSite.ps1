if ((Test-Path env:VIRTUAL_ENV) -eq $false) { 
    if ((Test-Path ./Env/Scripts) -eq $false) {
        ./ENV/bin/activate
    }

    ./ENV/Scripts/Activate.ps1 
}
python ./fetools/tool_site.py ./ff4.rom.smc