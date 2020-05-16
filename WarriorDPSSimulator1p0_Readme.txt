First fully functional WarriorDPSSimulator for Kronos WoW Private Server.

Goals for future version:
Speed up the process, fix bugs, add weapon and gear features.

Known bugs:
- No user input control. Number fields are not type-checking, can have values outside game values, etc.
- Missing cap on Whirlwind targets
- Possibly it's impossible to remove Crusader. Need to investigate.
- Closing the GUI before closing the result window will result in the result window popping up many times
- GUI freezes on large simulations. Numbers are still running in the background, but it gets a "non-responding" tag.
- Wrong usage of Cleave/Heroic Strike on more than 1 target
- Maladath doesn't give +4 Sword Skill
- Whirlwind not capped to 4 targets
- Unbridled Wrath has a 60% proc chance
- Juju Flurry is not loaded correctly, but tied to Sappers
- Hand of Justice proc doesn't deal damage

Missing Features:
- Many trinkets
- Many weapons
- Pre-popping CDs
- Multiprocessing utilizing all cores
- Code restructuring into more object oriented
- Smarter function calls using fewer if-statements