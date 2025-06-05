if ((Test-Path env:VIRTUAL_ENV) -eq $false) { .\ENV\Scripts\Activate.ps1 }

python -m FreeEnt './ff4.rom.smc' make -f "
O1:quest_forge/2:quest_tradepink/random:1,quest,char/req:all/win:crystal 
Kmain/summon/moon 
Pkey 
Cstandard/nofree/j:abilities/spells:anti/start:fusoya
Twildish 
Sstandard 
Bstandard/alt:gauntlet 
Etoggle 
Glife/sylph/backrow 
-kit:basic -kit2:miab 
-spoon -smith:super -pushbtojump -vanilla:fusoya"