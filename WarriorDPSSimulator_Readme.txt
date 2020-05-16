Version 1.1

This DPS simulator tool will open a GUI guiding you through the set up process.

Goals for future version:
Speed up the process, fix (unknown) bugs, add weapon and gear features, allow pre-popping CDs.

Changes from v1.0:
- Massive overhaul from global variables to object oriented programming
- Changed heroic strike usage criteria
- Implemented user-safeguards. (No wrong values allowed anymore).
- Whirlwind can only hit 4 targets now
- Maladath now correctly gives +4 Sword Skill
- Slayers Crest now a recognized (and functioning) trinket
- Added OH Crit Stone option
- Fixed Unbridled Wrath to have correct proc rate down from 60%
- Added Unbridled Wrath to talent options
- Load now correctly loads settings for Juju Flurry Usage
- Added easy adding of on-hit procs
- Fixed Hand of Justice proc now dealing damage
- Added Perditions Blade with 3.9% proc rate

Known bugs:
- Incomplete input control. Number fields are not type-checking.
- Closing the GUI before closing the result window can result in the result window popping up many times.
- GUI freezes on large simulations. Numbers are still running in the background, but it gets a "non-responding" tag.
- Result window not closing when closing GUI.
- GUI rescaling not possible.

Missing Features:
- Many trinkets
- Many weapons
- Pre-popping CDs
- Multiprocessing utilizing all cores

Missing keywords: 
- Diamond Flask
- Misplaced Servo Arm
- Deathbringer
- Many More

Github account: nikko8085