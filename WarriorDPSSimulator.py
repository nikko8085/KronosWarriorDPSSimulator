# Version 1.1.1 (in progress)

# Goal: Add many (or all) keywords. Optimize Trinket Usage algorithm. Fix GUI issues. Add pre-popping CD's possibility.

# Changes from v1.0:
# - Massive overhaul from global variables
# - Changed heroic strike usage criteria
# - Implemented user-safeguards. (No wrong values allowed anymore).
# - Whirlwind can only hit 4 targets now
# - Maladath now correctly gives +4 Sword Skill
# - Slayers Crest now a recognized (and functioning) trinket
# - Added OH Crit Stone option
# - Fixed Unbridled Wrath to have correct proc rate down from 60%
# - Added Unbridled Wrath to talent options
# - Load now correctly loads settings for Juju Flurry Usage
# - Added easy adding of on-hit procs
# - Fixed Hand of Justice proc now dealing damage
# - Added Perditions Blade with 3.9% proc rate

# Changes from v1.1:
# - Fixed OH Weapon swinging for its own damage, not MH weapon damage

# Known Bugs: 
# - Result window not closing when closing GUI
# - Result window opening many times if closing GUI first
# - GUI freezing on big calculations
# - User-safeguards missing. (Wrong type inputs still allowed).
# - GUI rescaling not possible
# - 2H weapon speed normalization factor not 3.3

# Missing features: 
# - Pre-popping CDs
# - Parallel Processing
# - Optimization
# - Not recalculating the damage reduction from mob armor at every hit

# Missing keywords: 
# - Diamond Flask
# - Misplaced Servo Arm
# - Deathbringer
# - Many More

if __name__ == '__main__':
	from tkinter import *
	from tkinter import messagebox
	from tkinter.filedialog import askopenfilename,asksaveasfile
	from tkinter.ttk import Progressbar
	import pandas as pd
	import os
	import sys
	import numpy as np
	from dataclasses import dataclass,field,fields
	import matplotlib.pyplot as plt
	import time

	# Gui functionality #
	def resource_path(relative_path):
		try: #""" Get absolute path to resource, works for dev and for PyInstaller """
			# PyInstaller creates a temp folder and stores path in _MEIPASS
			base_path = sys._MEIPASS
		except Exception:
			base_path = os.path.abspath(".")
		return os.path.join(base_path, relative_path)
	def scrollfunction(event):
		canvas.configure(scrollregion=canvas.bbox("all"),width=975,height=490)
	def mouse_wheel(event):
		canvas.yview_scroll(int(-1*(event.delta/30)),"units")
	def UpdateProgressBar(handle,val,gui):
		handle.set(val)
		gui.update_idletasks()

	filename = resource_path('GearList.xlsx')
	data = pd.read_excel(filename, sheet_name = None)

	root=Tk(screenName="Warrior DPS Simulator v1p1",className=" Warrior DPS Simulator v1p1")
	root.geometry("1000x500")

	myframe=Frame(root,relief=GROOVE,width=975,height=490,bd=1)
	myframe.place(x=2,y=2)

	canvas=Canvas(myframe)
	frame=Frame(canvas)
	myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
	canvas.configure(yscrollcommand=myscrollbar.set)

	myscrollbar.pack(side="right",fill="y")
	canvas.pack(side="left")
	canvas.create_window((0,0),window=frame,anchor='nw')
	frame.bind("<Configure>",scrollfunction)

	root.bind("<MouseWheel>", mouse_wheel)
	root.bind("<Button-4>", mouse_wheel) # Linux support
	root.bind("<Button-5>", mouse_wheel) # Linux support

	## Buffs and Debuffs ##
	label_Buffs = Label(frame,text = "Buffs and Debuffs", font = "bold")
	label_Buffs.grid(row=1,column=0)

	val_Zandalar = IntVar()
	val_Zandalar.set(1)
	label_Zaldalar = Label(frame,text = "Zandalar").grid(row=2,column=0)
	checkbox_Zaldalar = Checkbutton(frame,text=" ",variable = val_Zandalar).grid(row=2,column=1)
	val_Dragonslayer = IntVar()
	val_Dragonslayer.set(1)
	label_Dragonslayer = Label(frame,text = "Dragonslayer").grid(row=3,column=0)
	checkbox_Dragonslayer = Checkbutton(frame,text=" ",variable = val_Dragonslayer).grid(row=3,column=1)
	val_DMT = IntVar()
	val_DMT.set(1)
	label_DMT = Label(frame,text = "DMT").grid(row=4,column=0)
	checkbox_DMT = Checkbutton(frame,text=" ",variable = val_DMT).grid(row=4,column=1)
	val_SilithusSand = IntVar()
	val_SilithusSand.set(0)
	label_SilithusSand = Label(frame,text = "Silithus Sand").grid(row=5,column=0)
	checkbox_SilithusSand = Checkbutton(frame,text=" ",variable = val_SilithusSand).grid(row=5,column=1)
	val_Songflower = IntVar()
	val_Songflower.set(1)
	label_Songflower = Label(frame,text = "Songflower").grid(row=6,column=0)
	checkbox_Songflower = Checkbutton(frame,text=" ",variable = val_Songflower).grid(row=6,column=1)
	val_Kings = IntVar()
	val_Kings.set(1)
	label_Kings = Label(frame,text = "BoK").grid(row=7,column=0)
	checkbox_Kings = Checkbutton(frame,text=" ",variable = val_Kings).grid(row=7,column=1)
	val_BoM = IntVar()
	val_BoM.set(1)
	label_BoM = Label(frame,text = "BoM").grid(row=8,column=0)
	checkbox_BoM = Checkbutton(frame,text=" ",variable = val_BoM).grid(row=8,column=1)
	val_Trueshot = IntVar()
	val_Trueshot.set(1)
	label_Trueshot = Label(frame,text = "Trueshot").grid(row=9,column=0)
	checkbox_Trueshot = Checkbutton(frame,text=" ",variable = val_Trueshot).grid(row=9,column=1)
	val_MotW = IntVar()
	val_MotW.set(1)
	label_MotW = Label(frame,text = "MotW").grid(row=10,column=0)
	checkbox_MotW = Checkbutton(frame,text=" ",variable = val_MotW).grid(row=10,column=1)
	val_PackLeader = IntVar()
	val_PackLeader.set(0)
	label_PackLeader = Label(frame,text = "Pack Leader").grid(row=11,column=0)
	checkbox_PackLeader = Checkbutton(frame,text=" ",variable = val_PackLeader).grid(row=11,column=1)
	val_GiftOfArthas = IntVar()
	val_GiftOfArthas.set(0)
	label_GiftOfArthas = Label(frame,text = "Gift Of Arthas").grid(row=12,column=0)
	checkbox_GiftOfArthas = Checkbutton(frame,text=" ",variable = val_GiftOfArthas).grid(row=12,column=1)
	val_Chicken = IntVar()
	val_Chicken.set(1)
	label_Chicken = Label(frame,text = "Chicken").grid(row=13,column=0)
	checkbox_Chicken = Checkbutton(frame,text=" ",variable = val_Chicken).grid(row=13,column=1)
	val_Battleshout = IntVar()
	val_Battleshout.set(1)
	label_Battleshout = Label(frame,text = "Battleshout").grid(row=14,column=0)
	checkbox_Battleshout = Checkbutton(frame,text=" ",variable = val_Battleshout).grid(row=14,column=1)
	val_FaerieFire = IntVar()
	val_FaerieFire.set(1)
	label_FaerieFire = Label(frame,text = "Faerie Fire").grid(row=15,column=0)
	checkbox_FaerieFire = Checkbutton(frame,text=" ",variable = val_FaerieFire).grid(row=15,column=1)
	val_CoR = IntVar()
	val_CoR.set(1)
	label_CoR = Label(frame,text = "CoR").grid(row=16,column=0)
	checkbox_CoR = Checkbutton(frame,text=" ",variable = val_CoR).grid(row=16,column=1)
	val_ZerkerStance = IntVar()
	val_ZerkerStance.set(1)
	label_ZerkerStance = Label(frame,text = "Berserker Stance").grid(row=17,column=0)
	checkbox_ZerkerStance = Checkbutton(frame,text=" ",variable = val_ZerkerStance).grid(row=17,column=1)
	val_DMF = IntVar()
	val_DMF.set(0)
	label_DMF = Label(frame,text = "DMF").grid(row=18,column=0)
	entry_DMF = Entry(frame,textvar=val_DMF,width=3).grid(row=18,column=1)
	val_Sunders = IntVar()
	val_Sunders.set(5)
	label_sunders = Label(frame,text = "Sunders").grid(row=19,column=0)
	entry_sunders = Entry(frame,textvar=val_Sunders,width=3).grid(row=19,column=1)
	val_Annihilator = IntVar()
	val_Annihilator.set(3)
	label_annihilators = Label(frame,text = "Annihilators").grid(row=20,column=0)
	entry_annihilators = Entry(frame,textvar=val_Annihilator,width=3).grid(row=20,column=1)

	## Consumables ##
	label_Consumables = Label(frame,text = "Consumables",font = "bold").grid(row=1,column=2)
	val_JujuMight = IntVar()
	val_JujuMight.set(1)
	label_JujuMight = Label(frame,text = "Juju Might").grid(row=2,column=2)
	checkbox_JujuMight = Checkbutton(frame,text=" ",variable = val_JujuMight).grid(row=2,column=3)
	val_JujuPower = IntVar()
	val_JujuPower.set(1)
	label_JujuPower = Label(frame,text = "Juju Power").grid(row=3,column=2)
	checkbox_JujuPower = Checkbutton(frame,text=" ",variable = val_JujuPower).grid(row=3,column=3)
	val_Mongoose = IntVar()
	val_Mongoose.set(1)
	label_Mongoose = Label(frame,text = "Mongoose").grid(row=4,column=2)
	checkbox_Mongoose = Checkbutton(frame,text=" ",variable = val_Mongoose).grid(row=4,column=3)
	val_Dumpling = IntVar()
	val_Dumpling.set(1)
	label_Dumpling = Label(frame,text = "Dumpling").grid(row=5,column=2)
	checkbox_Dumpling = Checkbutton(frame,text=" ",variable = val_Dumpling).grid(row=5,column=3)
	val_MHCritStone = IntVar()
	val_MHCritStone.set(1)
	label_MHCritStone = Label(frame,text = "MH Crit Stone").grid(row=6,column=2)
	checkbox_MHCritStone = Checkbutton(frame,text=" ",variable = val_MHCritStone).grid(row=6,column=3)
	val_OHCritStone = IntVar()
	val_OHCritStone.set(0)
	label_OHCritStone = Label(frame,text = "OH Crit Stone").grid(row=7,column=2)
	checkbox_OHCritStone = Checkbutton(frame,text=" ",variable = val_OHCritStone).grid(row=7,column=3)
	val_MHStone = IntVar()
	val_MHStone.set(0)
	label_MHStone = Label(frame,text = "MH Stone").grid(row=8,column=2)
	checkbox_MHStone = Checkbutton(frame,text=" ",variable = val_MHStone).grid(row=8,column=3)
	val_OHStone = IntVar()
	val_OHStone.set(1)
	label_OHStone = Label(frame,text = "OH Stone").grid(row=9,column=2)
	checkbox_OHStone = Checkbutton(frame,text=" ",variable = val_OHStone).grid(row=9,column=3)
	val_UseSapper = IntVar()
	val_UseSapper.set(1)
	label_UseSapper = Label(frame,text = "Sapper").grid(row=10,column=2)
	checkbox_UseSapper = Checkbutton(frame,text=" ",variable = val_UseSapper).grid(row=10,column=3)
	val_UseRagePot = IntVar()
	val_UseRagePot.set(1)
	label_UseRagePot = Label(frame,text = "Rage Potion").grid(row=11,column=2)
	checkbox_UseRagePot = Checkbutton(frame,text=" ",variable = val_UseRagePot).grid(row=11,column=3)
	val_UseJujuFlurry = IntVar()
	val_UseJujuFlurry.set(1)
	label_UseJujuFlurry = Label(frame,text = "Juju Flurry").grid(row=12,column=2)
	checkbox_UseJujuFlurry = Checkbutton(frame,text=" ",variable = val_UseJujuFlurry).grid(row=12,column=3)

	## Abilities ##
	label_Abilities = Label(frame,text = "Abilities",font="bold").grid(row=13,column=2)
	val_HeroicStrike = IntVar()
	val_HeroicStrike.set(1)
	label_HeroicStrike = Label(frame,text = "Heroic Strike").grid(row=14,column=2)
	checkbox_HeroicStrike = Checkbutton(frame,text=" ",variable = val_HeroicStrike).grid(row=14,column=3)
	val_Cleave = IntVar()
	val_Cleave.set(1)
	label_Cleave = Label(frame,text = "Cleave").grid(row=15,column=2)
	checkbox_Cleave = Checkbutton(frame,text=" ",variable = val_Cleave).grid(row=15,column=3)
	val_Bloodthirst = IntVar()
	val_Bloodthirst.set(1)
	label_Bloodthirst = Label(frame,text = "Bloodthirst").grid(row=16,column=2)
	checkbox_Bloodthirst = Checkbutton(frame,text=" ",variable = val_Bloodthirst).grid(row=16,column=3)
	val_Whirlwind = IntVar()
	val_Whirlwind.set(1)
	label_Whirlwind = Label(frame,text = "Whirlwind").grid(row=17,column=2)
	checkbox_Whirlwind = Checkbutton(frame,text=" ",variable = val_Whirlwind).grid(row=17,column=3)
	val_Hamstring = IntVar()
	val_Hamstring.set(1)
	label_Hamstring = Label(frame,text = "Hamstring").grid(row=18,column=2)
	checkbox_Hamstring = Checkbutton(frame,text=" ",variable = val_Hamstring).grid(row=18,column=3)
	val_Bloodrage = IntVar()
	val_Bloodrage.set(1)
	label_Bloodrage = Label(frame,text = "Bloodrage").grid(row=19,column=2)
	checkbox_Bloodrage = Checkbutton(frame,text=" ",variable = val_Bloodrage).grid(row=19,column=3)
	val_Execute = IntVar()
	val_Execute.set(1)
	label_Execute = Label(frame,text = "Execute").grid(row=20,column=2)
	checkbox_Execute = Checkbutton(frame,text=" ",variable = val_Execute).grid(row=20,column=3)
	val_Deathwish = IntVar()
	val_Deathwish.set(1)
	label_Deathwish = Label(frame,text = "Deathwish").grid(row=21,column=2)
	checkbox_Deathwish = Checkbutton(frame,text=" ",variable = val_Deathwish).grid(row=21,column=3)
	val_Reckless = IntVar()
	val_Reckless.set(0)
	label_Reckless = Label(frame,text = "Recklessness").grid(row=22,column=2)
	checkbox_Reckless = Checkbutton(frame,text=" ",variable = val_Reckless).grid(row=22,column=3)

	## Talents ##
	label_Talents = Label(frame,text = "Talents",font="bold").grid(row=1,column = 4)

	val_OHSpecializationTalent = IntVar()
	val_OHSpecializationTalent.set(5)
	label_OHSpecializationTalent = Label(frame,text = "Offhand Specialization").grid(row=2,column = 4)
	entry_OHSpecializationTalent = Entry(frame,textvar=val_OHSpecializationTalent,width=3).grid(row=2,column = 5)
	val_CritDamageTalent = IntVar()
	val_CritDamageTalent.set(2)
	label_CritDamageTalent = Label(frame,text = "Impale").grid(row=3,column = 4)
	entry_CritDamageTalent = Entry(frame,textvar=val_CritDamageTalent,width=3).grid(row=3,column = 5)
	val_ImpHeroicStrike = IntVar()
	val_ImpHeroicStrike.set(3)
	label_ImpHeroicStrike = Label(frame,text = "Improved Heroic Strike").grid(row=4,column = 4)
	entry_ImpHeroicStrike = Entry(frame,textvar=val_ImpHeroicStrike,width=3).grid(row=4,column = 5)
	val_ExecuteTalent = IntVar()
	val_ExecuteTalent.set(2)
	label_ExecuteTalent = Label(frame,text = "Improved Execute").grid(row=5,column = 4)
	entry_ExecuteTalent = Entry(frame,textvar=val_ExecuteTalent,width=3).grid(row=5,column = 5)
	val_AngerManagement = IntVar()
	val_AngerManagement.set(1)
	label_AngerManagement = Label(frame,text = "Anger Management").grid(row=6,column = 4)
	checkbox_AngerManagement = Checkbutton(frame,text=" ",variable = val_AngerManagement).grid(row=6,column = 5)
	val_Cruelty = IntVar()
	val_Cruelty.set(5)
	label_Cruelty = Label(frame,text = "Cruelty").grid(row=7,column = 4)
	entry_Cruelty = Entry(frame,textvar=val_Cruelty,width=3).grid(row=7,column = 5)
	val_ImprovedCleave = IntVar()
	val_ImprovedCleave.set(0)
	label_ImprovedCleave = Label(frame,text = "Improved Cleave").grid(row=8,column = 4)
	entry_ImprovedCleave = Entry(frame,textvar=val_ImprovedCleave,width=3).grid(row=8,column = 5)
	val_UnbridledWrath = IntVar()
	val_UnbridledWrath.set(5)
	label_UnbridledWrath = Label(frame,text = "Unbridled Wrath").grid(row=9,column = 4)
	entry_UnbridledWrath = Entry(frame,textvar=val_UnbridledWrath,width=3).grid(row=9,column = 5)

	label_SimulationSettings = Label(frame,text = "Simulation Settings",font="bold").grid(row=10,column=4)

	val_Nreps = IntVar()
	val_Nreps.set(100)
	label_Nreps = Label(frame,text = "Repititions of the simulation").grid(row=11,column=4)
	entry_Nreps = Entry(frame,textvar=val_Nreps,width=3).grid(row=11,column=5)
	val_fightduration = IntVar()
	val_fightduration.set(60)
	label_fightduration = Label(frame,text = "Fight Duration").grid(row=12,column=4)
	entry_fightduration = Entry(frame,textvar=val_fightduration,width=3).grid(row=12,column=5)
	val_executeduration = IntVar()
	val_executeduration.set(10)
	label_executeduration = Label(frame,text = "Execute Duration").grid(row=13,column=4)
	entry_executeduration = Entry(frame,textvar=val_executeduration,width=3).grid(row=13,column=5)
	val_NEnemies = IntVar()
	val_NEnemies.set(1)
	label_NEnemies = Label(frame,text = "Number of targets").grid(row=14,column=4)
	entry_NEnemies = Entry(frame,textvar=val_NEnemies,width=3).grid(row=14,column=5)
	val_MobLevel = IntVar()
	val_MobLevel.set(63)
	label_MobLevel = Label(frame,text = "Enemy Level").grid(row=15,column=4)
	entry_MobLevel = Entry(frame,textvar=val_MobLevel,width=3).grid(row=15,column=5)
	val_PlayerLevel = IntVar()
	val_PlayerLevel.set(60)
	label_PlayerLevel = Label(frame,text = "Player Level").grid(row=16,column=4)
	entry_PlayerLevel = Entry(frame,textvar=val_PlayerLevel,width=3).grid(row=16,column=5)
	val_FrontAttack = IntVar()
	val_FrontAttack.set(0)
	label_FrontAttack = Label(frame,text = "Front Attack?").grid(row=17,column=4)
	checkbox_FrontAttack = Checkbutton(frame,text="",variable = val_FrontAttack).grid(row=17,column=5)

	val_scanaxis = StringVar()
	val_scanaxis.set("none")
	choices={"none","crit","hit","AP","heroic"}
	label_scanaxis = Label(frame,text = "Axis to scan along").grid(row=18,column=4)
	OptionMenu_scanaxis = OptionMenu(frame,val_scanaxis,*choices).grid(row=18,column=5)
	def change_dropdown(*args):
		return val_scanaxis.get()
	val_scanaxis.trace('w', change_dropdown)
	val_sweeprangestart = DoubleVar()
	val_sweeprangestart.set(0)
	label_sweeprangestart = Label(frame,text = "Starting value for scan").grid(row=19,column=4)
	entry_sweeprangestart = Entry(frame,textvar=val_sweeprangestart,width=3).grid(row=19,column=5)
	val_sweeprangeend = DoubleVar()
	val_sweeprangeend.set(0)
	label_sweeprangeend = Label(frame,text = "End value for scan").grid(row=20,column=4)
	entry_sweeprangeend = Entry(frame,textvar=val_sweeprangeend,width=3).grid(row=20,column=5)
	val_sweeprangesteps = IntVar()
	val_sweeprangesteps.set(0)
	label_sweeprangesteps = Label(frame,text = "Steps in the scan").grid(row=21,column=4)
	entry_sweeprangesteps = Entry(frame,textvar=val_sweeprangesteps,width=3).grid(row=21,column=5)

	## AI settings ##
	label_AISettings = Label(frame,text = "AI Settings",font="bold").grid(row=22,column=4)
	val_heroicstrikeragelimit = IntVar()
	val_heroicstrikeragelimit.set(35)
	label_heroicstrikeragelimit = Label(frame,text = "Use Heroic Strike at rage").grid(row=23,column=4)
	entry_heroicstrikeragelimit = Entry(frame,textvar=val_heroicstrikeragelimit,width=3).grid(row=23,column=5)
	val_hamstringragelimitprimary = IntVar()
	val_hamstringragelimitprimary.set(80)
	label_hamstringragelimitprimary = Label(frame,text = "Use Hamstring at rage").grid(row=24,column=4)
	entry_hamstringragelimitprimary = Entry(frame,textvar=val_hamstringragelimitprimary,width=3).grid(row=24,column=5)
	val_hamstringragelimitsecondary = IntVar()
	val_hamstringragelimitsecondary.set(35)
	label_hamstringragelimitsecondary = Label(frame,text = "Without Crusader, use Hamstring at").grid(row=25,column=4)
	entry_hamstringragelimitsecondary = Entry(frame,textvar=val_hamstringragelimitsecondary,width=3).grid(row=25,column=5)

	## Gear List ##
	SlotItems=[]
	slotlist = ['Race','Head','Neck','Shoulder','Back','Chest','Wrist','Hand','Waist','Legs','Feet','Ring 1','Ring 2','Trinket 1','Trinket 2','Ranged','MH Weapons','OH Weapons','2H+MH Weapons','Head Enchant','Leg Enchant','Shoulder Enchant','MH Enchant','OH Enchant','Cloak Enchant','Chest Enchant','Bracers Enchant','Gloves Enchant','Boots Enchant']
	for i in slotlist:
		SlotItems.append(data[i].loc[:,"Name"])
	label_Gear = Label(frame,text = "Gear",font="bold").grid(row=1,column=6)

	val_Race = StringVar()
	val_Race.set("Human")
	choices_Race=SlotItems[0]
	label_Race = Label(frame,text = "Race").grid(row=2,column=6)
	OptionMenu_Race = OptionMenu(frame,val_Race,*choices_Race).grid(row=2,column=7)
	def change_dropdown(*args):
		return val_Race.get()
	val_Race.trace('w', change_dropdown)

	val_Head = StringVar()
	val_Head.set("None")
	choices_Head=SlotItems[1]
	label_Head = Label(frame,text = "Head").grid(row=3,column=6)
	OptionMenu_Head = OptionMenu(frame,val_Head,*choices_Head).grid(row=3,column=7)
	def change_dropdown(*args):
		return val_Head.get()
	val_Head.trace('w', change_dropdown)

	val_Neck = StringVar()
	val_Neck.set("None")
	choices_Neck=SlotItems[2]
	label_Neck = Label(frame,text = "Neck").grid(row=0-1+5,column=6)
	OptionMenu_Neck = OptionMenu(frame,val_Neck,*choices_Neck).grid(row=0-1+5,column=7)
	def change_dropdown(*args):
		return val_Neck.get()
	val_Neck.trace('w', change_dropdown)

	val_Shoulders = StringVar()
	val_Shoulders.set("None")
	choices_Shoulders=SlotItems[3]
	label_Shoulders = Label(frame,text = "Shoulders").grid(row=0-1+6,column=6)
	OptionMenu_Shoulders = OptionMenu(frame,val_Shoulders,*choices_Shoulders).grid(row=0-1+6,column=7)
	def change_dropdown(*args):
		return val_Shoulders.get()
	val_Shoulders.trace('w', change_dropdown)

	val_Cloak = StringVar()
	val_Cloak.set("None")
	choices_Cloak=SlotItems[4]
	label_Cloak = Label(frame,text = "Cloak").grid(row=0-1+7,column=6)
	OptionMenu_Cloak = OptionMenu(frame,val_Cloak,*choices_Cloak).grid(row=0-1+7,column=7)
	def change_dropdown(*args):
		return val_Cloak.get()
	val_Cloak.trace('w', change_dropdown)

	val_Chest = StringVar()
	val_Chest.set("None")
	choices_Chest=SlotItems[5]
	label_Chest = Label(frame,text = "Chest").grid(row=0-1+8,column=6)
	OptionMenu_Chest = OptionMenu(frame,val_Chest,*choices_Chest).grid(row=0-1+8,column=7)
	def change_dropdown(*args):
		return val_Chest.get()
	val_Chest.trace('w', change_dropdown)

	val_Wrist = StringVar()
	val_Wrist.set("None")
	choices_Wrist=SlotItems[6]
	label_Wrist = Label(frame,text = "Wrist").grid(row=0-1+9,column=6)
	OptionMenu_Wrist = OptionMenu(frame,val_Wrist,*choices_Wrist).grid(row=0-1+9,column=7)
	def change_dropdown(*args):
		return val_Wrist.get()
	val_Wrist.trace('w', change_dropdown)

	val_Gloves = StringVar()
	val_Gloves.set("None")
	choices_Gloves=SlotItems[7]
	label_Gloves = Label(frame,text = "Gloves").grid(row=0-1+10,column=6)
	OptionMenu_Gloves = OptionMenu(frame,val_Gloves,*choices_Gloves).grid(row=0-1+10,column=7)
	def change_dropdown(*args):
		return val_Gloves.get()
	val_Gloves.trace('w', change_dropdown)

	val_Belt = StringVar()
	val_Belt.set("None")
	choices_Belt=SlotItems[8]
	label_Belt = Label(frame,text = "Belt").grid(row=0-1+11,column=6)
	OptionMenu_Belt = OptionMenu(frame,val_Belt,*choices_Belt).grid(row=0-1+11,column=7)
	def change_dropdown(*args):
		return val_Belt.get()
	val_Belt.trace('w', change_dropdown)

	val_Legs = StringVar()
	val_Legs.set("None")
	choices_Legs=SlotItems[9]
	label_Legs = Label(frame,text = "Legs").grid(row=0-1+12,column=6)
	OptionMenu_Legs = OptionMenu(frame,val_Legs,*choices_Legs).grid(row=0-1+12,column=7)
	def change_dropdown(*args):
		return val_Legs.get()
	val_Legs.trace('w', change_dropdown)

	val_Boots = StringVar()
	val_Boots.set("None")
	choices_Boots=SlotItems[10]
	label_Boots = Label(frame,text = "Boots").grid(row=0-1+13,column=6)
	OptionMenu_Boots = OptionMenu(frame,val_Boots,*choices_Boots).grid(row=0-1+13,column=7)
	def change_dropdown(*args):
		return val_Boots.get()
	val_Boots.trace('w', change_dropdown)

	val_Ring1 = StringVar()
	val_Ring1.set("None")
	choices_Ring1=SlotItems[11]
	label_Ring1 = Label(frame,text = "Ring 1").grid(row=0-1+14,column=6)
	OptionMenu_Ring1 = OptionMenu(frame,val_Ring1,*choices_Ring1).grid(row=0-1+14,column=7)
	def change_dropdown(*args):
		return val_Ring1.get()
	val_Ring1.trace('w', change_dropdown)

	val_Ring2 = StringVar()
	val_Ring2.set("None")
	choices_Ring2=SlotItems[12]
	label_Ring2 = Label(frame,text = "Ring 2").grid(row=0-1+15,column=6)
	OptionMenu_Ring2 = OptionMenu(frame,val_Ring2,*choices_Ring2).grid(row=0-1+15,column=7)
	def change_dropdown(*args):
		return val_Ring2.get()
	val_Ring2.trace('w', change_dropdown)

	val_Trinket1 = StringVar()
	val_Trinket1.set("None")
	choices_Trinket1=SlotItems[13]
	label_Trinket1 = Label(frame,text = "Trinket 1").grid(row=0-1+16,column=6)
	OptionMenu_Trinket1 = OptionMenu(frame,val_Trinket1,*choices_Trinket1).grid(row=0-1+16,column=7)
	def change_dropdown(*args):
		return val_Trinket1.get()
	val_Trinket1.trace('w', change_dropdown)

	val_Trinket2 = StringVar()
	val_Trinket2.set("None")
	choices_Trinket2=SlotItems[14]
	label_Trinket2 = Label(frame,text = "Trinket 2").grid(row=0-1+17,column=6)
	OptionMenu_Trinket2 = OptionMenu(frame,val_Trinket2,*choices_Trinket2).grid(row=0-1+17,column=7)
	def change_dropdown(*args):
		return val_Trinket2.get()
	val_Trinket2.trace('w', change_dropdown)

	val_MHWeapon = StringVar()
	val_MHWeapon.set("None")
	choices_MHWeapon=SlotItems[18]
	label_MHWeapon = Label(frame,text = "MH Weapon").grid(row=0-1+18,column=6)
	OptionMenu_MHWeapon = OptionMenu(frame,val_MHWeapon,*choices_MHWeapon).grid(row=0-1+18,column=7)
	def change_dropdown(*args):
		return val_MHWeapon.get()
	val_MHWeapon.trace('w', change_dropdown)

	val_OHWeapon = StringVar()
	val_OHWeapon.set("None")
	choices_OHWeapon=SlotItems[17]
	label_OHWeapon = Label(frame,text = "OH Weapon").grid(row=0-1+19,column=6)
	OptionMenu_OHWeapon = OptionMenu(frame,val_OHWeapon,*choices_OHWeapon).grid(row=0-1+19,column=7)
	def change_dropdown(*args):
		return val_OHWeapon.get()
	val_OHWeapon.trace('w', change_dropdown)

	val_Ranged = StringVar()
	val_Ranged.set("None")
	choices_Ranged=SlotItems[15]
	label_Ranged = Label(frame,text = "Ranged").grid(row=0-1+20,column=6)
	OptionMenu_Ranged = OptionMenu(frame,val_Ranged,*choices_Ranged).grid(row=0-1+20,column=7)
	def change_dropdown(*args):
		return val_Ranged.get()
	val_Ranged.trace('w', change_dropdown)

	label_Enchant = Label(frame,text = "Enchants",font="bold").grid(row=0-1+21,column=6)

	val_HeadEnchant = StringVar()
	val_HeadEnchant.set("None")
	choices_HeadEnchant=SlotItems[19]
	label_HeadEnchant = Label(frame,text = "Head").grid(row=0-1+22,column=6)
	OptionMenu_HeadEnchant = OptionMenu(frame,val_HeadEnchant,*choices_HeadEnchant).grid(row=0-1+22,column=7)
	def change_dropdown(*args):
		return val_HeadEnchant.get()
	val_HeadEnchant.trace('w', change_dropdown)

	val_ShouldersEnchant = StringVar()
	val_ShouldersEnchant.set("None")
	choices_ShouldersEnchant=SlotItems[21]
	label_ShouldersEnchant = Label(frame,text = "Shoulders").grid(row=0-1+23,column=6)
	OptionMenu_ShouldersEnchant = OptionMenu(frame,val_ShouldersEnchant,*choices_ShouldersEnchant).grid(row=0-1+23,column=7)
	def change_dropdown(*args):
		return val_ShouldersEnchant.get()
	val_ShouldersEnchant.trace('w', change_dropdown)

	val_CloakEnchant = StringVar()
	val_CloakEnchant.set("None")
	choices_CloakEnchant=SlotItems[24]
	label_CloakEnchant = Label(frame,text = "Cloak").grid(row=0-1+24,column=6)
	OptionMenu_CloakEnchant = OptionMenu(frame,val_CloakEnchant,*choices_CloakEnchant).grid(row=0-1+24,column=7)
	def change_dropdown(*args):
		return val_CloakEnchant.get()
	val_CloakEnchant.trace('w', change_dropdown)

	val_ChestEnchant = StringVar()
	val_ChestEnchant.set("None")
	choices_ChestEnchant=SlotItems[25]
	label_ChestEnchant = Label(frame,text = "Chest").grid(row=0-1+25,column=6)
	OptionMenu_ChestEnchant = OptionMenu(frame,val_ChestEnchant,*choices_ChestEnchant).grid(row=0-1+25,column=7)
	def change_dropdown(*args):
		return val_ChestEnchant.get()
	val_ChestEnchant.trace('w', change_dropdown)

	val_WristEnchant = StringVar()
	val_WristEnchant.set("None")
	choices_WristEnchant=SlotItems[26]
	label_WristEnchant = Label(frame,text = "Wrist").grid(row=0-1+26,column=6)
	OptionMenu_WristEnchant = OptionMenu(frame,val_WristEnchant,*choices_WristEnchant).grid(row=0-1+26,column=7)
	def change_dropdown(*args):
		return val_WristEnchant.get()
	val_WristEnchant.trace('w', change_dropdown)

	val_GlovesEnchant = StringVar()
	val_GlovesEnchant.set("None")
	choices_GlovesEnchant=SlotItems[27]
	label_GlovesEnchant = Label(frame,text = "Gloves").grid(row=0-1+27,column=6)
	OptionMenu_GlovesEnchant = OptionMenu(frame,val_GlovesEnchant,*choices_GlovesEnchant).grid(row=0-1+27,column=7)
	def change_dropdown(*args):
		return val_GlovesEnchant.get()
	val_GlovesEnchant.trace('w', change_dropdown)

	val_LegEnchant = StringVar()
	val_LegEnchant.set("None")
	choices_LegEnchant=SlotItems[19]
	label_LegEnchant = Label(frame,text = "Leg").grid(row=0-1+28,column=6)
	OptionMenu_LegEnchant = OptionMenu(frame,val_LegEnchant,*choices_LegEnchant).grid(row=0-1+28,column=7)
	def change_dropdown(*args):
		return val_LegEnchant.get()
	val_LegEnchant.trace('w', change_dropdown)

	val_BootsEnchant = StringVar()
	val_BootsEnchant.set("None")
	choices_BootsEnchant=SlotItems[28]
	label_BootsEnchant = Label(frame,text = "Boots").grid(row=0-1+29,column=6)
	OptionMenu_BootsEnchant = OptionMenu(frame,val_BootsEnchant,*choices_BootsEnchant).grid(row=0-1+29,column=7)
	def change_dropdown(*args):
		return val_BootsEnchant.get()
	val_BootsEnchant.trace('w', change_dropdown)

	val_MHWeaponEnchant = StringVar()
	val_MHWeaponEnchant.set("None")
	choices_MHWeaponEnchant=SlotItems[22]
	label_MHWeaponEnchant = Label(frame,text = "MH Weapon").grid(row=0-1+30,column=6)
	OptionMenu_MHWeaponEnchant = OptionMenu(frame,val_MHWeaponEnchant,*choices_MHWeaponEnchant).grid(row=0-1+30,column=7)
	def change_dropdown(*args):
		return val_MHWeaponEnchant.get()
	val_MHWeaponEnchant.trace('w', change_dropdown)

	val_OHWeaponEnchant = StringVar()
	val_OHWeaponEnchant.set("None")
	choices_OHWeaponEnchant=SlotItems[23]
	label_OHWeaponEnchant = Label(frame,text = "OH Weapon").grid(row=0-1+31,column=6)
	OptionMenu_OHWeaponEnchant = OptionMenu(frame,val_OHWeaponEnchant,*choices_OHWeaponEnchant).grid(row=0-1+31,column=7)
	def change_dropdown(*args):
		return val_OHWeaponEnchant.get()
	val_OHWeaponEnchant.trace('w', change_dropdown)


	def LoadSettings():
		def SetSetting(variable,value):
			return variable.set(value)
		path = askopenfilename()
		settings=[]
		f = open(path, "r")
		settings = f.readlines()
		for i in range(len(settings)):
			settings[i]=settings[i].split("_")
			settings[i]=settings[i][:-1]
			for j in range(len(settings[i])):
				if settings[i][j].isdigit():
					if i == 6 and j > 6 and j<8:
						settings[i][j]=float(settings[i][j])
					else:
						settings[i][j]=int(settings[i][j])
		f.close()
		
		gearlist = settings[0]
		weaponlist = settings[1]
		talentlist = settings[2]
		consumablelist = settings[3]
		bufflist = settings[4]
		abilitylist = settings[5]
		simulationsettinglist = settings[6]
		aisettinglist =settings[7]

		SetSetting(val_Race,gearlist[0])
		SetSetting(val_Head,gearlist[1])
		SetSetting(val_Neck,gearlist[2])
		SetSetting(val_Shoulders,gearlist[3])
		SetSetting(val_Cloak,gearlist[4])
		SetSetting(val_Chest,gearlist[5])
		SetSetting(val_Wrist,gearlist[6])
		SetSetting(val_Gloves,gearlist[7])
		SetSetting(val_Belt,gearlist[8])
		SetSetting(val_Legs,gearlist[9])
		SetSetting(val_Boots,gearlist[10])
		SetSetting(val_Ring1,gearlist[11])
		SetSetting(val_Ring2,gearlist[12])
		SetSetting(val_Trinket1,gearlist[13])
		SetSetting(val_Trinket2,gearlist[14])
		SetSetting(val_Ranged,gearlist[15])
		SetSetting(val_HeadEnchant,gearlist[16])
		SetSetting(val_LegEnchant,gearlist[17])
		SetSetting(val_ShouldersEnchant,gearlist[18])
		SetSetting(val_MHWeaponEnchant,gearlist[19])
		SetSetting(val_OHWeaponEnchant,gearlist[20])
		SetSetting(val_CloakEnchant,gearlist[21])
		SetSetting(val_ChestEnchant,gearlist[22])
		SetSetting(val_WristEnchant,gearlist[23])
		SetSetting(val_GlovesEnchant,gearlist[24])
		SetSetting(val_BootsEnchant,gearlist[25])
		
		SetSetting(val_MHWeapon,weaponlist[0])
		SetSetting(val_OHWeapon,weaponlist[1])
		
		SetSetting(val_OHSpecializationTalent,talentlist[0])
		SetSetting(val_CritDamageTalent,talentlist[1])
		SetSetting(val_ImpHeroicStrike,talentlist[2])
		SetSetting(val_ExecuteTalent,talentlist[3])
		SetSetting(val_AngerManagement,talentlist[4])
		SetSetting(val_Cruelty,talentlist[5])
		SetSetting(val_ImprovedCleave,talentlist[6])
		SetSetting(val_UnbridledWrath,talentlist[7])
		
		SetSetting(val_JujuMight,consumablelist[0])
		SetSetting(val_JujuPower,consumablelist[1])
		SetSetting(val_Mongoose,consumablelist[2])
		SetSetting(val_Dumpling,consumablelist[3])
		SetSetting(val_OHStone,consumablelist[4])
		SetSetting(val_MHCritStone,consumablelist[5])
		SetSetting(val_MHStone,consumablelist[6])
		SetSetting(val_UseSapper,consumablelist[7])
		SetSetting(val_UseRagePot,consumablelist[8])
		SetSetting(val_UseJujuFlurry,consumablelist[9])
		SetSetting(val_OHCritStone,consumablelist[10])
		
		SetSetting(val_Zandalar,bufflist[0])
		SetSetting(val_Dragonslayer,bufflist[1])
		SetSetting(val_DMT,bufflist[2])
		SetSetting(val_DMF,bufflist[3])
		SetSetting(val_SilithusSand,bufflist[4])
		SetSetting(val_Songflower,bufflist[5])
		SetSetting(val_Kings,bufflist[6])
		SetSetting(val_BoM,bufflist[7])
		SetSetting(val_Trueshot,bufflist[8])
		SetSetting(val_MotW,bufflist[9])
		SetSetting(val_PackLeader,bufflist[10])
		SetSetting(val_GiftOfArthas,bufflist[11])
		SetSetting(val_Chicken,bufflist[12])
		SetSetting(val_Battleshout,bufflist[13])
		SetSetting(val_Sunders,bufflist[14])
		SetSetting(val_Annihilator,bufflist[15])
		SetSetting(val_FaerieFire,bufflist[16])
		SetSetting(val_CoR,bufflist[17])
		SetSetting(val_ZerkerStance,bufflist[18])
		
		SetSetting(val_HeroicStrike,abilitylist[0])
		SetSetting(val_Cleave,abilitylist[1])
		SetSetting(val_Bloodthirst,abilitylist[2])
		SetSetting(val_Whirlwind,abilitylist[3])
		SetSetting(val_Hamstring,abilitylist[4])
		SetSetting(val_Bloodrage,abilitylist[5])
		SetSetting(val_Execute,abilitylist[6])
		SetSetting(val_Deathwish,abilitylist[7])
		SetSetting(val_Reckless,abilitylist[8])
		
		SetSetting(val_Nreps,simulationsettinglist[0])
		SetSetting(val_fightduration,simulationsettinglist[1])
		SetSetting(val_executeduration,simulationsettinglist[2])
		SetSetting(val_NEnemies,simulationsettinglist[3])
		SetSetting(val_MobLevel,simulationsettinglist[4])
		SetSetting(val_PlayerLevel,simulationsettinglist[5])
		SetSetting(val_FrontAttack,simulationsettinglist[6])
		SetSetting(val_scanaxis,simulationsettinglist[7])
		SetSetting(val_sweeprangestart,simulationsettinglist[8])
		SetSetting(val_sweeprangeend,simulationsettinglist[9])
		SetSetting(val_sweeprangesteps,simulationsettinglist[10])

		SetSetting(val_heroicstrikeragelimit,aisettinglist[0])
		SetSetting(val_hamstringragelimitprimary,aisettinglist[1])
		SetSetting(val_hamstringragelimitsecondary,aisettinglist[2])
	button_load = Button(frame,text="Load", width=18, command=LoadSettings).grid(row=0,column=0)
	def SaveSettings():
		gearlist = [val_Race.get(),val_Head.get(),val_Neck.get(),val_Shoulders.get(),val_Cloak.get(),val_Chest.get(),val_Wrist.get(),val_Gloves.get(),val_Belt.get(),val_Legs.get(),val_Boots.get(),val_Ring1.get(),val_Ring2.get(),val_Trinket1.get(),val_Trinket2.get(),val_Ranged.get(),val_HeadEnchant.get(),val_LegEnchant.get(),val_ShouldersEnchant.get(),val_MHWeaponEnchant.get(),val_OHWeaponEnchant.get(),val_CloakEnchant.get(),val_ChestEnchant.get(),val_WristEnchant.get(),val_GlovesEnchant.get(),val_BootsEnchant.get()]
		weaponlist = [val_MHWeapon.get(),val_OHWeapon.get()]
		aisettinglist=[val_heroicstrikeragelimit.get(),val_hamstringragelimitprimary.get(),val_hamstringragelimitsecondary.get()]
		simulationsettinglist=[val_Nreps.get(),val_fightduration.get(),val_executeduration.get(),val_NEnemies.get(),val_MobLevel.get(),val_PlayerLevel.get(),val_FrontAttack.get(),val_scanaxis.get(),val_sweeprangestart.get(),val_sweeprangeend.get(),val_sweeprangesteps.get()]
		abilitylist=[val_HeroicStrike.get(),val_Cleave.get(),val_Bloodthirst.get(),val_Whirlwind.get(),val_Hamstring.get(),val_Bloodrage.get(),val_Execute.get(),val_Deathwish.get(),val_Reckless.get()]
		consumablelist=[val_JujuMight.get(),val_JujuPower.get(),val_Mongoose.get(),val_Dumpling.get(),val_OHStone.get(),val_MHCritStone.get(),val_MHStone.get(),val_UseSapper.get(),val_UseRagePot.get(),val_UseJujuFlurry.get(),val_OHCritStone.get()]
		bufflist = [val_Zandalar.get(),val_Dragonslayer.get(),val_DMT.get(),val_DMF.get(),val_SilithusSand.get(),val_Songflower.get(),val_Kings.get(),val_BoM.get(),val_Trueshot.get(),val_MotW.get(),val_PackLeader.get(),val_GiftOfArthas.get(),val_Chicken.get(),val_Battleshout.get(),val_Sunders.get(),val_Annihilator.get(),val_FaerieFire.get(),val_CoR.get(),val_ZerkerStance.get()]
		talentlist = [val_OHSpecializationTalent.get(),val_CritDamageTalent.get(),val_ImpHeroicStrike.get(),val_ExecuteTalent.get(),val_AngerManagement.get(),val_Cruelty.get(),val_ImprovedCleave.get(),val_UnbridledWrath.get()]
		settings = [gearlist,weaponlist,talentlist,consumablelist,bufflist,abilitylist,simulationsettinglist,aisettinglist]

		fileoptions = [('Text Document', '*.txt'),('All Files', '*.*')]
		file = asksaveasfile(filetypes = fileoptions, defaultextension = fileoptions)
		for item in settings:
			savestring = ''
			for i in item:
				savestring+=str(i)+'_'
			file.write(savestring+'\n')
		file.close()
	button_save = Button(frame,text="Save", width=18, command=SaveSettings).grid(row=0,column=2)
	
	def RunSimulation():
		GCDList = ["bloodthirst","whirlwind","deathwish","reckless","hamstring","execute"]
		ATSpeedBuffList = ['kissofthespider','jujuflurry','flurry']
		DMGFactorBuffList = ['enrage','deathwish']
		APBuffList = ['slayerscrest']
		StrBuffList = ['crusaderMH','crusaderOH','ragepot']
		CritBuffsList = ['reckless']
		## Attack calculations ##
		def GenerateAttackTable(stats,mobstats,basestats):
			atmy = AttackTableClass()
			atmw = AttackTableClass()
			atow = AttackTableClass()

			skilldiffMH = mobstats.defence - basestats.weaponskillMH
			extraskillMH = np.max([0, basestats.weaponskillMH-basestats.playerlevel*5])
			cappedskillMH = np.min([basestats.weaponskillMH,basestats.playerlevel*5])
			if basestats.weaponspeedOH==0: # not dualwielding
				dwmod = 1
			else:
				dwmod = 0.8
			## Mainhand white swings
			if skilldiffMH > 10:
				skilldiffmod = 0.002
			else:
				skilldiffmod = 0.001
			atmw.miss = np.min([1,np.max([(0.05+skilldiffMH*skilldiffmod)*dwmod+(0.2*basestats.dualwield)-basestats.hit,0])])
			atmw.dodge = np.min([1,np.max([0.05+skilldiffMH*0.001+atmw.miss,atmw.miss])])
			if basestats.frontattack == 0: # Parry is not possible
				atmw.parry = atmw.dodge
				atmw.block = atmw.parry
			else:
				atmw.parry = np.min([1,np.max([0.05+skilldiffMH*0.001+atmw.dodge,atmw.dodge])])
				atmw.block = np.min([1,0.05+atmw.parry])
			if mobstats.level-basestats.playerlevel >= 3:
				atmw.glance = np.min([1,np.max([0.1+(mobstats.defence-cappedskillMH)*0.02+atmw.block,atmw.block])])
			else:
				atmw.glance = atmw.block
			if cappedskillMH-mobstats.defence < 0:
				atmw.crit = np.min([1,np.max([stats.critMH+(cappedskillMH-mobstats.defence)*0.002+atmw.glance,atmw.glance])])
			else:
				atmw.crit = np.min([1,np.max([stats.critMH+(cappedskillMH-mobstats.defence)*0.0004+atmw.glance,atmw.glance])])
			atmw.hit = 1
			## Mainhand yellow swings
			atmy.miss = np.min([1,np.max([0.05+skilldiffMH*skilldiffmod-basestats.hit,0])])
			atmy.dodge = np.min([1,np.max([0.05+skilldiffMH*0.001+atmy.miss,atmy.miss])])
			if basestats.frontattack == 0: # Parry is not possible
				atmy.parry = atmy.dodge
				atmy.block = atmy.parry
			else:
				atmy.parry = np.min([1,np.max([0.05+skilldiffMH*0.001+atmy.dodge,atmy.dodge])])
				atmy.block = np.min([1,0.05+atmy.parry])
			atmy.glance = atmy.block # Glance is not possible
			if cappedskillMH-mobstats.defence < 0:
				atmy.crit = np.min([1,np.max([stats.critMH+(cappedskillMH-mobstats.defence)*0.002+atmy.glance,atmy.glance])])
			else:
				atmy.crit = np.min([1,np.max([stats.critMH+(cappedskillMH-mobstats.defence)*0.0004+atmy.glance,atmy.glance])])
			atmy.hit = 1
			## Offhand white swings
			skilldiffOH = mobstats.defence - basestats.weaponskillOH
			extraskillOH = np.max([0, basestats.weaponskillOH-basestats.playerlevel*5])
			cappedskillOH = np.min([basestats.weaponskillOH,basestats.playerlevel*5])
			if skilldiffOH > 10:
				skilldiffmod = 0.002
			else:
				skilldiffmod = 0.001
			atow.miss = np.min([1,np.max([(0.05+skilldiffOH*skilldiffmod)*dwmod+(0.2*basestats.dualwield)-basestats.hit,0])])
			atow.dodge = np.min([1,np.max([0.05+skilldiffOH*0.001+atow.miss,atow.miss])])
			if basestats.frontattack == 0:
				atow.parry = atow.dodge
				atow.block = atow.parry
			else:	
				atow.parry = np.min([1,np.max([0.05+skilldiffOH*0.001+atow.dodge,atow.dodge])])
				atow.block = np.min([1,0.05+atow.parry])
			if mobstats.level-basestats.playerlevel >= 3:
				atow.glance = np.min([1,np.max([0.1+(mobstats.defence-cappedskillOH)*0.02+atow.block,atow.block])])
			else:
				atow.glance = atow.block
			if cappedskillOH-mobstats.defence < 0:
				atow.crit = np.min([1,np.max([stats.critOH+(cappedskillOH-mobstats.defence)*0.002+atow.glance,atow.glance])])
			else:
				atow.crit = np.min([1,np.max([stats.critOH+(cappedskillOH-mobstats.defence)*0.0004+atow.glance,atow.glance])])
			atow.hit = 1

			return atmy,atmw,atow			
		def AttackOutcome(table):
			random=np.random.uniform()
			if random<=table.miss:
				return 0
			elif random<=table.block: # any of dodge, parry, block
				return 1
			elif random<= table.glance:
				return 2
			elif random<= table.crit:
				return 3
			elif random<= table.hit:
				return 4
		def AttackDamage(hand,Character):
			if hand == 0:
				mindamage=Character.stats_base.weaponmindamageMH+Character.stats_active.AP/14.0*Character.stats_base.weaponspeedMH
				maxdamage=Character.stats_base.weaponmaxdamageMH+Character.stats_active.AP/14.0*Character.stats_base.weaponspeedMH
			elif hand == 1:
				mindamage=(Character.stats_base.weaponmindamageOH+Character.stats_active.AP/14.0*Character.stats_base.weaponspeedOH)*(0.5+0.025*Character.stats_base.OHSpecialization)
				maxdamage=(Character.stats_base.weaponmaxdamageOH+Character.stats_active.AP/14.0*Character.stats_base.weaponspeedOH)*(0.5+0.025*Character.stats_base.OHSpecialization)
			damage=np.random.uniform(mindamage,maxdamage)
			return damage
		def GlanceFactor(hand,Character):
			if hand == 0:
				skilldiff = Character.mobstats.defence - Character.stats_base.weaponskillMH
			elif hand == 1:
				skilldiff = Character.mobstats.defence - Character.stats_base.weaponskillOH
			glancinglow = np.min([1.3-0.05*skilldiff,0.91])
			glancinghigh = np.max([0.2,np.min([1.2-0.03*skilldiff,0.99])])
			glancingfactor = np.random.uniform(glancinglow,glancinghigh)
			return glancingfactor
		def ArmorReduction(Character):
			return 1-np.min([0.75,np.max([0,Character.mobstats.armor / (Character.mobstats.armor + 400 + 85 * Character.stats_base.playerlevel)])])
		def RageFromAttack(damage):
			gain = np.round(0.03252*damage)
			return gain # rage gain
		# On attack procs
		def FlurryProc(Character):
			Character.buffs_active.flurry = 1
			Character.buffs_duration.flurry = 12
			Character.buffs_duration.flurrycharge = 3
			UpdateAttackSpeed(Character)
		def FlurryConsume(Character):
			if Character.buffs_active.flurry == 1:
				Character.buffs_duration.flurrycharge += -1
				if Character.buffs_duration.flurrycharge<=0:
					Character.buffs_active.flurry = 0
					UpdateAttackSpeed(Character)
		def CrusaderMHFunc(Character):
			if np.random.uniform()<=Character.procrate.crusader:
				Character.buffs_active.crusaderMH = 1
				Character.buffs_duration.crusaderMH = 15
				UpdateAP(Character)
			return 0
				# print('Proc from Crusader MH')
		def CrusaderOHFunc(Character):
			if np.random.uniform()<=Character.procrate.crusader:
				Character.buffs_active.crusaderOH = 1
				Character.buffs_duration.crusaderOH = 15
				UpdateAP(Character)
			return 0
		def UnbridledWrathFunc(Character):
			if np.random.uniform()<=Character.procrate.unbridledwrath:
				Character.stats_active.rage=np.min([100,Character.stats_active.rage+1])
			return 0
		def HandOfJusticeFunc(Character):
			if np.random.uniform()<Character.procrate.handofjustice:
				return MHauto(Character)
			return 0
		def NightfallFunc(Character):
			if np.random.uniform()<=Character.procrate.nightfall:
				Character.buffs_active.nightfall = 1
				Character.buffs_duration.nightfall = 5
			return 0
		def PerditionBladeFunc(Character):
			if np.random.uniform()<=Character.procrate.perditionblade:
				return np.random.randint(40,57)
			return 0
		## Abilities ##
		def Bloodthirst(Character):
			totaldamage=0
			Character.cooldown_active.bloodthirst = 6
			Character.stats_active.rage += -30
			Character.cooldown_active.gcd = Character.cooldown_max.gcd
			outcome=AttackOutcome(Character.attacktable[0])
			if outcome == 1:
				Character.stats_active.rage+= 22 # what rage regained on dodge?
			elif outcome == 3: # crit
				totaldamage+=np.floor(Character.stats_active.AP*0.45*ArmorReduction(Character)*Character.stats_active.damageinc*Character.stats_base.CritDamageBonus)+8*Character.stats_base.giftofarthas
				FlurryProc(Character)
				for f in Character.AttackProcListMH:
					totaldamage+=f(Character)
			elif outcome == 4: # hit
				totaldamage+=np.floor(Character.stats_active.AP*0.45*ArmorReduction(Character)*Character.stats_active.damageinc)+8*Character.stats_base.giftofarthas
				for f in Character.AttackProcListMH:
					totaldamage+=f(Character)
			UpdateGlobalCd(Character)
			return totaldamage
		def Whirlwind(Character):
			totaldamage=0
			Character.cooldown_active.whirlwind = 10
			Character.stats_active.rage += -25
			Character.cooldown_active.gcd = Character.cooldown_max.gcd
			for i in range(np.min([Character.stats_base.nenemies,4])):
				outcome=AttackOutcome(Character.attacktable[0])
				if outcome == 3: # crit:
					totaldamage += np.floor(np.random.uniform(Character.stats_base.weaponmindamageMH,Character.stats_base.weaponmaxdamageMH)+Character.stats_active.AP*Character.stats_base.normalizedspeed/14.0)*ArmorReduction(Character)*Character.stats_base.CritDamageBonus+8*Character.stats_base.giftofarthas
					FlurryProc(Character)
					for f in Character.AttackProcListMH:
						totaldamage+=f(Character)
				elif outcome == 4:
					totaldamage += np.floor(np.random.uniform(Character.stats_base.weaponmindamageMH,Character.stats_base.weaponmaxdamageMH)+Character.stats_active.AP*Character.stats_base.normalizedspeed/14.0)*ArmorReduction(Character)+8*Character.stats_base.giftofarthas
					for f in Character.AttackProcListMH:
						totaldamage+=f(Character)
			UpdateGlobalCd(Character)
			return totaldamage
		def Execute(Character):
			totaldamage=0
			Character.cooldown_active.gcd = Character.cooldown_max.gcd
			rageused = Character.stats_active.rage-Character.stats_base.ExecuteAbilityCost
			Character.stats_active.rage = 0
			outcome=AttackOutcome(Character.attacktable[0])
			if outcome == 1: # Dodge
				Character.stats_active.rage = np.floor(10*0.84+rageused)
			# elif outcome == 2: # Miss, nothing happens
				# Character.stats_active.rage
			elif outcome == 3: # crit
				totaldamage+=np.floor((600+rageused*15)*ArmorReduction(Character)*Character.stats_base.CritDamageBonus)+8*Character.stats_base.giftofarthas
				FlurryProc(Character)
				for f in Character.AttackProcListMH:
					totaldamage+=f(Character)
			elif outcome == 4:
				totaldamage+=np.floor((600+rageused*15)*ArmorReduction(Character))+8*Character.stats_base.giftofarthas
				for f in Character.AttackProcListMH:
					totaldamage+=f(Character)
			UpdateGlobalCd(Character)
			return totaldamage
		def Hamstring(Character):
			totaldamage=0
			Character.cooldown_active.gcd = Character.cooldown_max.gcd
			Character.cooldown_active.hamstring = Character.cooldown_max.gcd
			Character.stats_active.rage += -10
			outcome=AttackOutcome(Character.attacktable[0])
			if outcome == 1:
				Character.stats_active.rage += 7
			elif outcome == 3:
				totaldamage+=np.floor(45*ArmorReduction(Character)*Character.stats_base.CritDamageBonus)+8*Character.stats_base.giftofarthas
				FlurryProc(Character)
				for f in Character.AttackProcListMH:
					totaldamage+=f(Character)
			elif outcome == 4:
				totaldamage+=np.floor(45*ArmorReduction(Character))+8*Character.stats_base.giftofarthas
				for f in Character.AttackProcListMH:
					totaldamage+=f(Character)
			UpdateGlobalCd(Character)
			return totaldamage
		def Deathwish(Character):
			Character.stats_active.rage += -10
			Character.cooldown_active.deathwish = Character.cooldown_max.deathwish
			Character.cooldown_active.gcd = Character.cooldown_max.gcd
			Character.buffs_active.deathwish = 1
			Character.buffs_duration.deathwish = Character.buffs_maxduration.deathwish
			UpdateDamage(Character)
			UpdateGlobalCd(Character)
		def Reckless(Character):
			Character.cooldown_active.reckless = Character.cooldown_max.reckless
			Character.cooldown_active.gcd = Character.cooldown_max.gcd
			Character.buffs_active.reckless = 1
			Character.buffs_duration.reckless = Character.buffs_maxduration.reckless
			UpdateCrit(Character)
			UpdateGlobalCd(Character)
		def RagePot(Character):
			Character.stats_active.rage = np.min([Character.stats_active.rage+np.round(np.random.uniform()*30)+45,100])
			Character.cooldown_active.ragepot = Character.cooldown_max.ragepot
			Character.buffs_active.ragepot = 1
			Character.buffs_duration.ragepot = Character.buffs_maxduration.ragepot
			UpdateAP(Character)
		def Bloodrage(Character):
			Character.stats_active.rage = np.min([Character.stats_active.rage+10,100])
			Character.cooldown_active.bloodrage = Character.cooldown_max.bloodrage
			Character.buffs_active.bloodrage = 10
			Character.cooldown_active.bloodragetic = Character.cooldown_max.bloodragetic # reset cooldown to 1 sec before next tic
		def Bloodragetic(Character):
			Character.cooldown_active.bloodragetic = Character.cooldown_max.bloodragetic # reset cooldown to 1 sec before next tic
			Character.buffs_active.bloodrage += -1 # Consume a bloodrage tic
			Character.stats_active.rage = np.min([Character.stats_active.rage+1,100])
		def AngerManagement(Character):
			Character.cooldown_active.angermanagement = Character.cooldown_max.angermanagement # reset cooldown to 1 sec before next tic
			Character.stats_active.rage = np.min([Character.stats_active.rage+1,100])
		def JujuFlurry(Character):
			Character.cooldown_active.jujuflurry = Character.cooldown_max.jujuflurry
			Character.buffs_active.jujuflurry = 1
			Character.buffs_duration.jujuflurry = Character.buffs_maxduration.jujuflurry
			UpdateAttackSpeed(Character)
		def Sapper(Character):
			Character.cooldown_active.sapper = Character.cooldown_max.sapper
			damage=np.random.randint(450,751,Character.stats_base.nenemies)
			return np.sum(damage)
		def KissOfTheSpider(Character):
			Character.cooldown_active.kissofthespider = Character.cooldown_max.kissofthespider
			Character.cooldown_active.slayerscrest = np.max([Character.cooldown_active.slayerscrest,Character.buffs_maxduration.kissofthespider])
			Character.cooldown_active.jomgabbar = np.max([Character.cooldown_active.jomgabbar,Character.buffs_maxduration.kissofthespider])
			Character.buffs_active.kissofthespider = 1
			Character.buffs_duration.kissofthespider = Character.buffs_maxduration.kissofthespider
			UpdateAttackSpeed(Character)
		def SlayersCrest(Character):
			Character.cooldown_active.slayerscrest = Character.cooldown_max.slayerscrest
			Character.cooldown_active.kissofthespider = np.max([Character.cooldown_active.kissofthespider,Character.buffs_maxduration.slayerscrest])
			Character.cooldown_active.jomgabbar = np.max([Character.cooldown_active.jomgabbar,Character.buffs_maxduration.slayerscrest])
			Character.buffs_active.slayerscrest = 1
			Character.buffs_duration.slayerscrest = Character.buffs_maxduration.slayerscrest
			UpdateAP(Character)
		def JomGabbar(Character):
			Character.cooldown_active.jomgabbar = Character.cooldown_max.jomgabbar
			Character.cooldown_active.slayerscrest = np.max([Character.cooldown_active.slayerscrest,Character.buffs_duration.jomgabbar])
			Character.cooldown_active.kissofthespider = np.max([Character.cooldown_active.kissofthespider,Character.buffs_duration.jomgabbar])
			Character.buffs_active.jomgabbar = 1
			Character.cooldown_active.jomgabbartic = Character.cooldown_max.jomgabbartic # reset cooldown to 1 sec before next tic
			UpdateAP(Character)
		def JomGabbarTic(Character):
			Character.cooldown_active.jomgabbartic = Character.cooldown_max.jomgabbartic # reset cooldown to 2 sec before next tic
			if Character.buffs_active.jomgabbar < 10:
				Character.buffs_active.jomgabbar += 1 # Consume a jomgabbar tic
			else:
				Character.buffs_active.jomgabbar = 0 # End jomgabbar
			UpdateAP(Character)
		# Core attacks #
		def MainAttack(Character):
			FlurryConsume(Character)
			if Character.stats_active.rage >= 25 and Character.stats_base.nenemies>=2 and Character.stats_base.cleave:
				totaldamage=Cleave(Character)
				# print('Used Cleave')
			elif Character.stats_active.rage >= Character.AIsettings.heroicstrikeragelimit and Character.stats_base.heroicstrike and (Character.stats_base.nenemies == 1 or Character.stats_base.cleave == 0):
				totaldamage=HeroicStrike(Character)
				# print('Used Heroic Strike')
			else:
				totaldamage=MHauto(Character)
				# print('Used MH Auto attack')
			return totaldamage
		def MHauto(Character):
			totaldamage = 0
			Character.cooldown_active.automain = Character.stats_active.weaponspeedMH # reset swing timer
			outcome=AttackOutcome(Character.attacktable[1])
			#if outcome == 0: # miss, nothing happens
			#elif outcome == 1: # dodge, nothing happens
			if outcome == 2: # glance
				totaldamage+=np.floor(AttackDamage(0,Character)*ArmorReduction(Character)*Character.stats_active.damageinc*GlanceFactor(0,Character))+8*Character.stats_base.giftofarthas
				Character.stats_active.rage=np.min([Character.stats_active.rage+RageFromAttack(totaldamage),100])
				for f in Character.AttackProcListMH:
					totaldamage+=f(Character)
				for f in Character.AttackProcListWhite:
					totaldamage+=f(Character)
			elif outcome == 3: # crit
				totaldamage+=np.floor(AttackDamage(0,Character)*ArmorReduction(Character)*Character.stats_active.damageinc*Character.stats_base.CritDamageBonus)+8*Character.stats_base.giftofarthas
				Character.stats_active.rage=np.min([Character.stats_active.rage+RageFromAttack(totaldamage),100])
				FlurryProc(Character)
				for f in Character.AttackProcListMH:
					totaldamage+=f(Character)
				for f in Character.AttackProcListWhite:
					totaldamage+=f(Character)
			elif outcome == 4: # hit
				totaldamage+=np.floor(AttackDamage(0,Character)*ArmorReduction(Character)*Character.stats_active.damageinc)+8*Character.stats_base.giftofarthas
				Character.stats_active.rage=np.min([Character.stats_active.rage+RageFromAttack(totaldamage),100])
				for f in Character.AttackProcListMH:
					totaldamage+=f(Character)
				for f in Character.AttackProcListWhite:
					totaldamage+=f(Character)
			return totaldamage
		def OHauto(Character):
			totaldamage=0
			Character.cooldown_active.autooff = Character.stats_active.weaponspeedOH # reset swing timer
			FlurryConsume(Character)
			outcome=AttackOutcome(Character.attacktable[2])
			#if outcome == 0: # miss, nothing happens
			#elif outcome == 1: # dodge, nothing happens
			if outcome == 2: # glance
				totaldamage+= np.floor(AttackDamage(1,Character)*ArmorReduction(Character)*Character.stats_active.damageinc*GlanceFactor(1,Character))+8*Character.stats_base.giftofarthas
				Character.stats_active.rage=np.min([Character.stats_active.rage+RageFromAttack(totaldamage),100])
				for f in Character.AttackProcListOH:
					totaldamage+=f(Character)
			elif outcome == 3: # crit
				totaldamage+=np.floor(AttackDamage(1,Character)*ArmorReduction(Character)*Character.stats_active.damageinc*Character.stats_base.CritDamageBonus)+8*Character.stats_base.giftofarthas
				Character.stats_active.rage=np.min([Character.stats_active.rage+RageFromAttack(totaldamage),100])
				FlurryProc(Character)
				for f in Character.AttackProcListOH:
					totaldamage+=f(Character)
			elif outcome == 4: # hit
				totaldamage+=np.floor(AttackDamage(1,Character)*ArmorReduction(Character)*Character.stats_active.damageinc)+8*Character.stats_base.giftofarthas
				Character.stats_active.rage=np.min([Character.stats_active.rage+RageFromAttack(totaldamage),100])
				for f in Character.AttackProcListOH:
					totaldamage+=f(Character)
			return totaldamage
		def HeroicStrike(Character):
			totaldamage=0
			Character.cooldown_active.automain = Character.stats_active.weaponspeedMH # reset swing timer
			Character.stats_active.rage+=-Character.stats_base.HeroicStrikeAbilityCost
			outcome=AttackOutcome(Character.attacktable[0])
			#if outcome == 0: # miss, nothing happens
			if outcome == 1: # dodge, regain some rage
				Character.stats_active.rage+=np.floor(Character.stats_base.HeroicStrikeAbilityCost*0.75)
			#if outcome == 2: # glance, not possible
			elif outcome == 3: # crit
				totaldamage += np.floor((AttackDamage(0,Character)+157)*ArmorReduction(Character)*Character.stats_active.damageinc*Character.stats_base.CritDamageBonus)+8*Character.stats_base.giftofarthas
				FlurryProc(Character)
				for f in Character.AttackProcListMH:
					totaldamage+=f(Character)
			elif outcome == 4: # hit
				totaldamage += np.floor((AttackDamage(0,Character)+157)*ArmorReduction(Character)*Character.stats_active.damageinc)+8*Character.stats_base.giftofarthas
				for f in Character.AttackProcListMH:
					totaldamage+=f(Character)
			return totaldamage
		def Cleave(Character):
			totaldamage = 0
			Character.cooldown_active.automain = Character.stats_active.weaponspeedMH # reset swing timer
			Character.stats_active.rage += -20
			# First target:
			for i in range(np.min([2,Character.stats_base.nenemies])):
				outcome=AttackOutcome(Character.attacktable[0])
				#if outcome == 0: # miss, nothing happens
				if outcome == 1 and i==0: # dodge on primary target, refund rage
					Character.stats_active.rage += 15
				#if outcome == 2: # glance, not possible
				elif outcome == 3: # crit
					totaldamage+=np.floor((AttackDamage(0,Character)+32*(1+0.4*Character.stats_base.impcleave))*ArmorReduction(Character)*Character.stats_active.damageinc*Character.stats_base.CritDamageBonus)+8*Character.stats_base.giftofarthas
					FlurryProc(Character)
					for f in Character.AttackProcListMH:
						totaldamage+=f(Character)
				elif outcome == 4: # hit
					totaldamage+=np.floor((AttackDamage(0,Character)+32*(1+0.4*Character.stats_base.impcleave))*ArmorReduction(Character)*Character.stats_active.damageinc)+8*Character.stats_base.giftofarthas
					for f in Character.AttackProcListMH:
						totaldamage+=f(Character)
			return totaldamage
		## Update stats ##
		def UpdateAttackSpeed(Character):
			attackspeedfactor = Character.stats_base.attackspeedfactor
			for i in range(len(Character.AttackSpeedBuffs)):
				if getattr(Character.buffs_active,Character.AttackSpeedBuffs[i]) == 1:
					attackspeedfactor = attackspeedfactor * getattr(Character.buffs_effect,Character.AttackSpeedBuffs[i])
			Character.stats_active.weaponspeedMH=Character.stats_base.weaponspeedMH/attackspeedfactor
			Character.stats_active.weaponspeedOH=Character.stats_base.weaponspeedOH/attackspeedfactor
			if Character.cooldown_active.automain>Character.stats_active.weaponspeedMH:
				Character.cooldown_active.automain = Character.stats_active.weaponspeedMH
			if Character.cooldown_active.autooff>Character.stats_active.weaponspeedOH:
				Character.cooldown_active.autooff = Character.stats_active.weaponspeedOH
		def UpdateAP(Character):
			strbonus = 0
			APbonus = 0
			for i in range(len(Character.StrBuffs)):
				if getattr(Character.buffs_active,Character.StrBuffs[i]) == 1:
					strbonus += getattr(Character.buffs_effect,Character.StrBuffs[i])
			for i in range(len(Character.APBuffs)):
				if getattr(Character.buffs_active,Character.APBuffs[i]) == 1:
					APbonus += getattr(Character.buffs_effect,Character.APBuffs[i])
			if Character.buffs_active.jomgabbar != 0:
				APbonus += 20*Character.buffs_active.jomgabbar
			Character.stats_active.AP = np.floor(Character.stats_base.AP+(Character.stats_base.strength+strbonus)*2*Character.stats_base.statmultiplier+APbonus)
		def UpdateCrit(Character):
			critbonus = 0
			for i in range(len(Character.CritBuffs)):
				if getattr(Character.buffs_active,Character.CritBuffs[i]) == 1:
					critbonus += getattr(Character.buffs_effect,Character.CritBuffs[i])
			Character.stats_active.critMH = Character.stats_base.critMH+critbonus
			Character.stats_active.critOH = Character.stats_base.critOH+critbonus
			UpdateAttackTable(Character)
		def UpdateDamage(Character):
			damagefactor = Character.stats_base.damageinc
			for i in range(len(Character.DamageFactorBuffs)):
				if getattr(Character.buffs_active,Character.DamageFactorBuffs[i]) == 1:
					damagefactor = damagefactor * getattr(Character.buffs_effect,Character.DamageFactorBuffs[i])
			Character.stats_active.damageinc = damagefactor
		def UpdateBuffs(timestep,Character):
			for i in range(len(Character.AttackSpeedBuffs)):
				if getattr(Character.buffs_duration,Character.AttackSpeedBuffs[i]) <= timestep:
					setattr(Character.buffs_active,Character.AttackSpeedBuffs[i],0)
					setattr(Character.buffs_duration,Character.AttackSpeedBuffs[i],0)
					UpdateAttackSpeed(Character)
				else:
					setattr(Character.buffs_duration,Character.AttackSpeedBuffs[i],getattr(Character.buffs_duration,Character.AttackSpeedBuffs[i])-timestep)
			for i in range(len(Character.DamageFactorBuffs)):
				if getattr(Character.buffs_duration,Character.DamageFactorBuffs[i]) <= timestep:
					setattr(Character.buffs_active,Character.DamageFactorBuffs[i],0)
					setattr(Character.buffs_duration,Character.DamageFactorBuffs[i],0)
					UpdateDamage(Character)
				else:
					setattr(Character.buffs_duration,Character.DamageFactorBuffs[i],getattr(Character.buffs_duration,Character.DamageFactorBuffs[i])-timestep)
			for i in range(len(Character.APBuffs)):
				if getattr(Character.buffs_duration,Character.APBuffs[i]) <= timestep:
					setattr(Character.buffs_active,Character.APBuffs[i],0)
					setattr(Character.buffs_duration,Character.APBuffs[i],0)
					UpdateAP(Character)
				else:
					setattr(Character.buffs_duration,Character.APBuffs[i],getattr(Character.buffs_duration,Character.APBuffs[i])-timestep)
			for i in range(len(Character.StrBuffs)):
				if getattr(Character.buffs_duration,Character.StrBuffs[i]) <= timestep:
					setattr(Character.buffs_active,Character.StrBuffs[i],0)
					setattr(Character.buffs_duration,Character.StrBuffs[i],0)
					UpdateAP(Character)
				else:
					setattr(Character.buffs_duration,Character.StrBuffs[i],getattr(Character.buffs_duration,Character.StrBuffs[i])-timestep)
			if Character.buffs_active.nightfall == 1:
				Character.stats_active.nightfalltime += timestep
		def UpdateGlobalCd(Character):
			for i in range(len(Character.gcdlist)):
				if getattr(Character.cooldown_active,Character.gcdlist[i]) < Character.cooldown_active.gcd:
					setattr(Character.cooldown_active,Character.gcdlist[i],Character.cooldown_active.gcd)
		def UpdateCd(timestep,Character):
			names = [x.name for x in fields(Character.cooldown_active)]
			for i in range(len(names)):
				if getattr(Character.cooldown_active,names[i]) <= timestep:
					setattr(Character.cooldown_active,names[i],0)
				else:
					setattr(Character.cooldown_active,names[i],getattr(Character.cooldown_active,names[i])-timestep)
		def UpdateAttackTable(Character):
			MHSkillDiff = Character.stats_base.cappedskillMH-Character.mobstats.defence
			OHSkillDiff = Character.stats_base.cappedskillOH-Character.mobstats.defence
			if Character.stats_base.cappedskillMH-Character.mobstats.defence < 0:
				Character.attacktable[0].crit = np.min([1,np.max([Character.stats_active.critMH+MHSkillDiff*0.002+Character.attacktable[0].glance,Character.attacktable[0].glance])])
				Character.attacktable[1].crit = np.min([1,np.max([Character.stats_active.critMH+MHSkillDiff*0.002+Character.attacktable[1].glance,Character.attacktable[1].glance])])
			else:
				Character.attacktable[0].crit = np.min([1,np.max([Character.stats_active.critMH+MHSkillDiff*0.0004+Character.attacktable[0].glance,Character.attacktable[0].glance])])
				Character.attacktable[1].crit = np.min([1,np.max([Character.stats_active.critMH+MHSkillDiff*0.0004+Character.attacktable[1].glance,Character.attacktable[1].glance])])
			if Character.stats_base.cappedskillOH-Character.mobstats.defence < 0:
				Character.attacktable[2].crit = np.min([1,np.max([Character.stats_active.critOH+OHSkillDiff*0.002+Character.attacktable[2].glance,Character.attacktable[2].glance])])
			else:
				Character.attacktable[2].crit = np.min([1,np.max([Character.stats_active.critOH+OHSkillDiff*0.0004+Character.attacktable[2].glance,Character.attacktable[2].glance])])
		# Gui to variable conversion #
		def ExtractStats(gearlist,weaponlist,data):
			def FindRow(sheet,keyword):
				count = 0
				for i in sheet['Name'].tolist():
					if i==keyword:
						return count
					count += 1
			def FindSkillKeywords(weapontype):
				weaponskillkeywords = [weapontype]
				if weapontype == "Mace" or weapontype== "Sword" or weapontype == "2H Sword" or weapontype == "2H Mace":
					weaponskillkeywords.append('Human')
				if weapontype == "Axe" or weapontype== "Sword" or weapontype == "Dagger" or weapontype == "2H Mace" or weapontype == "2H Sword":
					weaponskillkeywords.append('Edgemaster')
				return weaponskillkeywords
			weaponstatnames = ['Min Hit','Max Hit','Speed']
			weaponstatlist = [[0,0,0.0],[0,0,0.0]]
			slotlist = ['Race','Head','Neck','Shoulder','Back','Chest','Wrist','Hand','Waist','Legs','Feet','Ring 1','Ring 2','Trinket 1','Trinket 2','Ranged','Head Enchant','Leg Enchant','Shoulder Enchant','MH Enchant','OH Enchant','Cloak Enchant','Chest Enchant','Bracers Enchant','Gloves Enchant','Boots Enchant']
			statnames = ['Crit','Hit','Str','Agi','AP']
			statlist = [0,0,0,0,0]
			ItemList=[]
			specials=[]
			if len(weaponlist) == 1: # 2H Weapon list
				weaponslotlist = ['2H+MH Weapons']
				skill = [0]
			elif len(weaponlist) == 2:
				weaponslotlist = ['MH Weapons','OH Weapons']
				skill = [0,0]
			weaponskillkeywords=[] # Keywords for MH/OH weapon skill
			for i in range(len(weaponlist)): # Figure out which keywords apply to which weapon skills
				Slot = weaponslotlist[i]
				Gear = weaponlist[i]
				row = FindRow(data[Slot],Gear)
				weaponskillkeywords.append(FindSkillKeywords(data[Slot].loc[row,'Weapon Type']))
				if i == 0 and weaponskillkeywords[0][0] == 'Dagger':
					specials.append('DaggerMH')
			for i in range(len(weaponlist)):
				Slot = weaponslotlist[i]
				Gear = weaponlist[i]
				row = FindRow(data[Slot],Gear)
				specialkeyword = data[Slot].loc[row,'Keyword']
				if isinstance(specialkeyword,str):
					specials.append(specialkeyword)
				for j in range(len(weaponstatlist[i])): # Scan for weapon specific stats
					value = data[Slot].loc[row,weaponstatnames[j]]
					if np.isnan(value):
						value = 0
					weaponstatlist[i][j]+=value
				for j in range(len(statlist)): # Scan for ordinary stats
					value = data[Slot].loc[row,statnames[j]]
					if np.isnan(value):
						value = 0
					statlist[j]+=value
				for j in range(len(weaponlist)): # Scan for weapon skills
					if data[Slot].loc[row,'Type'] in weaponskillkeywords[j]: # Skill applies
						value = data[Slot].loc[row,'Skill']
						if np.isnan(value):
							value = 0
						skill[j]+=value
			for i in range(len(gearlist)): # Non-weapon 
				Slot = slotlist[i]
				Gear = gearlist[i]
				row = FindRow(data[Slot],Gear)
				specialkeyword = data[Slot].loc[row,'Keyword']
				if isinstance(specialkeyword,str):
					specials.append(specialkeyword)
				for j in range(len(statlist)): # Scan for ordinary stats
					value = data[Slot].loc[row,statnames[j]]
					if np.isnan(value):
						value = 0
					statlist[j]+=value
				for j in range(len(weaponlist)): # Scan for weapon skills
					if data[Slot].loc[row,'Type'] in weaponskillkeywords[j]: # Skill applies
						value = data[Slot].loc[row,'Skill']
						if np.isnan(value):
							value = 0
						skill[j]+=value
			for i in range(2):
				try:
					weaponstatlist[i].append(skill[i]+300)
				except:
					weaponstatlist[i].append(0)
			return statlist,weaponstatlist,specials
		def KeywordParser(keywordlist):
			KnownKeywords = ['SpeedEnchant','Kiss of the Spider','Slayers Crest','Jom Gabbar','Hand of Justice','DaggerMH','Nightfall','Crusader MH','Crusader OH','Perditions Blade','Perditions Blade OH']
			ProcMHFunctionList=[]
			ProcOHFunctionList=[]
			keywordlistout=[0]*len(KnownKeywords)
			if 'SpeedEnchant' in keywordlist:
				keywordlistout[0]=keywordlist.count('SpeedEnchant')
			if 'Kiss of the Spider' in keywordlist:
				keywordlistout[1]=1
			if 'Slayers Crest' in keywordlist:
				keywordlistout[2]=1
			if 'Jom Gabbar' in keywordlist:
				keywordlistout[3]=1
			if 'Hand of Justice' in keywordlist:
				keywordlistout[4]=1
				ProcMHFunctionList.append(HandOfJusticeFunc)
			if 'DaggerMH' in keywordlist:
				keywordlistout[5]=1
			if 'Nightfall' in keywordlist:
				keywordlistout[6]=1
				ProcMHFunctionList.append(NightfallFunc)
			if 'Crusader MH' in keywordlist:
				keywordlistout[7]=1
				ProcMHFunctionList.append(CrusaderMHFunc)
			if 'Crusader OH' in keywordlist:
				keywordlistout[8]=1
				ProcOHFunctionList.append(CrusaderOHFunc)
			if 'Perditions Blade' in keywordlist:
				keywordlistout[9]=1
				ProcMHFunctionList.append(PerditionBladeFunc)
			if 'Perditions Blade OH' in keywordlist:
				keywordlistout[10]=1
				ProcOHFunctionList.append(PerditionBladeFunc)
			boollist=[i in KnownKeywords for i in keywordlist]
			unknownkeywordlist=''
			if all(boollist) == 0:
				for i in range(len(boollist)):
					if boollist[i]==False:
						unknownkeywordlist=unknownkeywordlist+str(keywordlist[i])+', '
				unknownkeywordlist=unknownkeywordlist[:-2]
				messagebox.showwarning("Unknown Keywords", "Unknown Keywords are: "+unknownkeywordlist+'. \nThis is likely a feature not included in the simulation and its effect will be ignored. \nOften this means on-hit effects are ignored.')
			return keywordlistout,ProcMHFunctionList,ProcOHFunctionList
		

		gearlist = [val_Race.get(),val_Head.get(),val_Neck.get(),val_Shoulders.get(),val_Cloak.get(),val_Chest.get(),val_Wrist.get(),val_Gloves.get(),val_Belt.get(),val_Legs.get(),val_Boots.get(),val_Ring1.get(),val_Ring2.get(),val_Trinket1.get(),val_Trinket2.get(),val_Ranged.get(),val_HeadEnchant.get(),val_LegEnchant.get(),val_ShouldersEnchant.get(),val_MHWeaponEnchant.get(),val_OHWeaponEnchant.get(),val_CloakEnchant.get(),val_ChestEnchant.get(),val_WristEnchant.get(),val_GlovesEnchant.get(),val_BootsEnchant.get()]
		if val_OHWeapon.get()!="None":
			weaponlist = [val_MHWeapon.get(),val_OHWeapon.get()]
		else:
			weaponlist = [val_MHWeapon.get()]
		aisettinglist=[val_heroicstrikeragelimit.get(),val_hamstringragelimitprimary.get(),val_hamstringragelimitsecondary.get()]
		simulationsettinglist=[val_Nreps.get(),val_fightduration.get(),val_executeduration.get(),val_NEnemies.get(),val_MobLevel.get(),val_PlayerLevel.get(),val_FrontAttack.get(),val_scanaxis.get(),val_sweeprangestart.get(),val_sweeprangeend.get(),val_sweeprangesteps.get()]
		abilitylist=[val_HeroicStrike.get(),val_Cleave.get(),val_Bloodthirst.get(),val_Whirlwind.get(),val_Hamstring.get(),val_Bloodrage.get(),val_Execute.get(),val_Deathwish.get(),val_Reckless.get()]
		consumablelist=[val_JujuMight.get(),val_JujuPower.get(),val_Mongoose.get(),val_Dumpling.get(),val_OHStone.get(),val_MHCritStone.get(),val_MHStone.get(),val_UseSapper.get(),val_UseRagePot.get(),val_UseJujuFlurry.get(),val_OHCritStone.get()]
		bufflist = [val_Zandalar.get(),val_Dragonslayer.get(),val_DMT.get(),val_DMF.get(),val_SilithusSand.get(),val_Songflower.get(),val_Kings.get(),val_BoM.get(),val_Trueshot.get(),val_MotW.get(),val_PackLeader.get(),val_GiftOfArthas.get(),val_Chicken.get(),val_Battleshout.get(),val_Sunders.get(),val_Annihilator.get(),val_FaerieFire.get(),val_CoR.get(),val_ZerkerStance.get()]
		talentlist = [val_OHSpecializationTalent.get(),val_CritDamageTalent.get(),val_ImpHeroicStrike.get(),val_ExecuteTalent.get(),val_AngerManagement.get(),val_Cruelty.get(),val_ImprovedCleave.get(),val_UnbridledWrath.get()]
		statlist,weaponstatlist,specials=ExtractStats(gearlist,weaponlist,data)

		KeywordList,ProcMHFunctionList,ProcOHFunctionList=KeywordParser(specials)
		sweeprange = np.linspace(simulationsettinglist[8],simulationsettinglist[9],simulationsettinglist[10])

		ProcWhiteFunctionList=[]
		if talentlist[7]!=0:
			ProcWhiteFunctionList.append(UnbridledWrathFunc)
			ProcWhiteFunctionList.append(UnbridledWrathFunc)

		def UserInputChecks(simulationsettinglist,bufflist,talentlist,aisettinglist,consumablelist,abilitylist):
			# safetychecks from user inputs
			if isinstance(simulationsettinglist[1],float)==0 and isinstance(simulationsettinglist[1],int)==0:
				messagebox.showwarning("User input error","User input error","Fight duration must be a number")
				return 1 # Fight duration
			if simulationsettinglist[1]<=0.0:
				messagebox.showwarning("User input error","Fight duration must be greater than 0.")
				return 1
			if isinstance(simulationsettinglist[3],int)==0:
				messagebox.showwarning("User input error","Number of enemies must be a whole number")
				return 1# NEnemies
			if simulationsettinglist[3]<1:
				messagebox.showwarning("User input error","Number of enemies must be greater than or equal to 1.")
				return 1
			if isinstance(simulationsettinglist[2],float)==0 and isinstance(simulationsettinglist[2],int)==0:
				messagebox.showwarning("User input error","Execute duration must be a number")
				return 1 # Execute Duration
			if simulationsettinglist[2]>simulationsettinglist[1]:
				messagebox.showwarning("User input error","Execute duration must be shorter than or equal to fight duration.")
				return 1
			if isinstance(bufflist[3],int)==0:
				messagebox.showwarning("User input error","DMF must be a whole number between 0 and 10")
				return 1 # DMF
			if bufflist[3]>10 or bufflist[3] < 0:
				messagebox.showwarning("User input error","DMF must be between 0 and 10.")
				return 1
			if isinstance(bufflist[14],int)==0:
				messagebox.showwarning("User input error","Sunders must be a whole number")
				return 1 # Sunders
			if bufflist[14]>5 or bufflist[14] < 0:
				messagebox.showwarning("User input error","Sunders must be between 0 and 5")
				return 1
			if isinstance(bufflist[15],int)==0:
				messagebox.showwarning("User input error","Annihilator must be a whole number")
				return 1 # Annihilator
			if bufflist[15]>3 or bufflist[15] < 0:
				messagebox.showwarning("User input error","Annihilator must be between 0 and 3")
				return 1
			if isinstance(talentlist[0],int)==0:
				messagebox.showwarning("User input error","OH Specialization Talent must be a whole number")
				return 1 # OH Specialization
			if talentlist[0]>5 or talentlist[0] < 0:
				messagebox.showwarning("User input error","OH Specialization Talent must be between 0 and 5")
				return 1
			if isinstance(talentlist[1],int)==0:
				messagebox.showwarning("User input error","Crit Damage Talent must be a whole number")
				return 1 # Crit Damage Talent
			if talentlist[1]>2 or talentlist[1] < 0:
				messagebox.showwarning("User input error","Crit Damage Talent  must be between 0 and 2")
				return 1
			if isinstance(talentlist[2],int)==0:
				messagebox.showwarning("User input error","Imp Heroic Strike Talent must be a whole number")
				return 1 # Improved Heroic Strike
			if talentlist[2]>3 or talentlist[2] < 0:
				messagebox.showwarning("User input error","Improved Heroic Strik Talent must be between 0 and 3")
				return 1
			if isinstance(talentlist[3],int)==0:
				messagebox.showwarning("User input error","Imp Execute Talent must be a whole number")
				return 1 # Improved Execute Talent
			if talentlist[3]>2 or talentlist[3]<0:
				messagebox.showwarning("User input error","Improved Execute Talent must be between 0 and 2")
				return 1
			if isinstance(talentlist[5],int)==0:
				messagebox.showwarning("User input error","Cruelty Talent must be a whole number")
				return 1 # Cruelty Talent
			if talentlist[5]>5 or talentlist[5] < 0:
				messagebox.showwarning("User input error","Cruelty Talent must be between 0 and 5")
				return 1
			if isinstance(talentlist[6],int)==0:
				messagebox.showwarning("User input error","Improved Cleave Talent must be a whole number")
				return 1 # Improved Cleave
			if talentlist[6]>3 or talentlist[6] <0:
				messagebox.showwarning("User input error","Improved Cleave Talent must be between 0 and 3")
				return 1
			if isinstance(simulationsettinglist[0],int)==0:
				messagebox.showwarning("User input error","Number of repetitions must be a whole number")
				return 1 # NReps
			if simulationsettinglist[0]<2:
				messagebox.showwarning("User input error","Number of repetitions must be greater than 2 for accuracy")
				return 1
			if isinstance(simulationsettinglist[4],int)==0:
				messagebox.showwarning("User input error","Mob Level must be a whole number")
				return 1 # MobLevel
			if simulationsettinglist[4]>63 or simulationsettinglist[4] < 1:
				messagebox.showwarning("User input error","Mob Level must be between 1 and 63")
				return 1
			if isinstance(simulationsettinglist[5],int)==0:
				messagebox.showwarning("User input error","Player Level must be a whole number")
				return 1 # Player Level
			if simulationsettinglist[5]>60 or simulationsettinglist[5] < 1:
				messagebox.showwarning("User input error","Player Level must be between 1 and 60")
				return 1
			if len(sweeprange)==0 and simulationsettinglist[7]!="none":
				messagebox.showwarning("User input error","Your sweep must have at least 1 step in it")
				return 1
			if isinstance(aisettinglist[0],int)==0:
				messagebox.showwarning("User input error","Heroic Strike Rage Limit must be a whole number")
				return 1 # Heroic Strike Rage Limit
			if aisettinglist[0]>100 or aisettinglist[0]<15-talentlist[2]:
				messagebox.showwarning("User input error","The lower limit for when to use Heroic Strike must be between the cost of Heroic Strike with talents and 100")
				return 1
			if abilitylist[4] == 1: # If hamstring is used
				if isinstance(aisettinglist[1],int)==0:
					messagebox.showwarning("User input error","Hamstring Primary Rage Limit must be a whole number")
					return 1# Hamstring Rage Limit Primary
				if aisettinglist[1]>100 or aisettinglist[1] <10:
					messagebox.showwarning("User input error","The lower limit for when to use Hamstring must be between 10 and 100")
					return 1
				if isinstance(aisettinglist[2],int)==0:
					messagebox.showwarning("User input error","Hamstring Secondary Rage Limit must be a whole number")
					return 1 # Hamstring Rage Limit Secondary
				if aisettinglist[2]>100 or aisettinglist[2]<10:
					messagebox.showwarning("User input error","The lower limit for when to use Hamstring when Crusader proc from the MH is not up must be between 10 and 100")
					return 1
			if consumablelist[10]==1 and consumablelist[4]==1: # OH Crit stone and OH Stone
				messagebox.showwarning("User input error","Offhand cannot have both a crit and damage stone applied.")
				return 1
			if consumablelist[5]==1 and consumablelist[6]==1:
				messagebox.showwarning("User input error","Mainhand cannot have both a crit and damage stone applied.")
				return 1 # MH Crit stone and MH Stone
			if abilitylist[3] == 1 and bufflist[18] == 0: # Whirlwind and Zerker Stance
				messagebox.showwarning("User input error","Whirlwind use requires Berzerker Stance active")
				return 1
			if abilitylist[8] == 1 and bufflist[18] == 0: # Reckless and Zerker Stance
				messagebox.showwarning("User input error","Recklessness use requires Berzerker Stance active")
				return 1
			return 0
		if UserInputChecks(simulationsettinglist,bufflist,talentlist,aisettinglist,consumablelist,abilitylist):
			exit() # Wrong user input is given, do not continue.

		@dataclass
		class ActiveStatsClass: # Stats varied during combat
			AP: int = 0
			critMH: float = 0
			critOH: float = 0
			weaponspeedMH: float = 0
			weaponspeedOH: float = 0
			rage: int = 0
			damageinc: float = 1
			nightfalltime: float = 0
		@dataclass
		class BaseStatsClass: # Base stats not varied during combat
			AP: int = 0
			strength: int = 0
			critMH: float = 0
			critOH: float = 0
			hit: float = 0
			weaponskillMH: int = 300
			weaponmindamageMH: int = 0
			weaponmaxdamageMH: int = 0
			weaponspeedMH: float = 0
			weaponskillOH: int = 300
			weaponmindamageOH: int = 0
			weaponmaxdamageOH: int = 0
			weaponspeedOH: float = 0
				# Talents
			OHSpecialization: float = 0
			CritDamageBonus: float = 2
			angermanagement: bool = 0
			HeroicStrikeAbilityCost: int = 15
			ExecuteAbilityCost: int = 15
			impcleave: int = 0
				# Initial conditions
			rage: int = 0
			playerlevel: int = 60
			frontattack: bool = 0
			nenemies: int = 1
			cappedskillMH: int = 300
			cappedskillOH: int = 300
			normalizedspeed: float = 2.4
			attackspeedfactor: float = 1
			dualwield: bool = 0
			nightfall: bool = 0
			giftofarthas: bool = 0
				# Buffs
			damageinc: float = 1
			statmultiplier: float = 1
				# Abilities
			sapper: bool = 0
			ragepot: bool = 0
			jujuflurry: bool = 0
			bloodthirst: bool = 0
			bloodrage: bool = 0
			whirlwind: bool = 0
			hamstring: bool = 0
			execute: bool = 0
			deathwish: bool = 0
			reckless: bool = 0
			heroicstrike: bool = 0
			cleave: bool = 0
			crusaderMH: bool = 0
			# crusaderOH: bool = 0
				# Trinkets
			kissofthespider: bool = 0
			slayerscrest: bool = 0
			handofjustice: bool = 0
			jomgabbar: bool = 0
			def Fill(self,statlist,weaponstatlist,bufflist,consumablelist,talentlist,abilitylist,simulationsettinglist,KeywordList):
				self.AP: int = np.floor(statlist[4] + 222*bufflist[7] + 40*consumablelist[0] + bufflist[1]*140 + bufflist[13]*290 + bufflist[2]*200 + 100*bufflist[8])
				self.strength: int = np.floor(statlist[2] + 20*consumablelist[3] + 15*bufflist[5] +30*consumablelist[1] + 16*bufflist[9])
				self.critMH: float = float(statlist[0])/100 + 0.03*bufflist[18] + 0.02*consumablelist[2] + 0.05*bufflist[1] + 0.05*bufflist[5] + 0.03*bufflist[10] + 0.01*talentlist[5] + ((statlist[3] + 25*consumablelist[2] + 15*bufflist[5]+16*bufflist[9])*(1+0.1*bufflist[6])*(1+0.15*bufflist[0]))*1.0/2000 + 0.02*consumablelist[5]
				self.critOH: float = float(statlist[0])/100 + 0.03*bufflist[18] + 0.02*consumablelist[2] + 0.05*bufflist[1] + 0.05*bufflist[5] + 0.03*bufflist[10] + 0.01*talentlist[5] + ((statlist[3] + 25*consumablelist[2] + 15*bufflist[5]+16*bufflist[9])*(1+0.1*bufflist[6])*(1+0.15*bufflist[0]))*1.0/2000 + 0.02*consumablelist[10]
				self.hit: float = float(statlist[1])/100
				self.weaponskillMH: int = weaponstatlist[0][3]
				self.weaponmindamageMH: int = weaponstatlist[0][0] + 8*consumablelist[6]
				self.weaponmaxdamageMH: int = weaponstatlist[0][1] + 8*consumablelist[6]
				self.weaponspeedMH: float = weaponstatlist[0][2]
				self.weaponskillOH: int = weaponstatlist[1][3]
				self.weaponmindamageOH: int = weaponstatlist[1][0] + 8*consumablelist[4]
				self.weaponmaxdamageOH: int = weaponstatlist[1][1] + 8*consumablelist[4]
				self.weaponspeedOH: float = weaponstatlist[1][2]
					# Talents
				self.OHSpecialization: float = talentlist[0]
				self.CritDamageBonus: float = 2+0.1*talentlist[1]
				self.angermanagement: bool = talentlist[4]
				self.HeroicStrikeAbilityCost: int = 15 - talentlist[2]
				if talentlist[3] == 2:
					self.ExecuteAbilityCost: int = 10
				elif talentlist[3] == 1:
					self.ExecuteAbilityCost: int = 13
				else:
					self.ExecuteAbilityCost: int = 15
				self.impcleave: int = talentlist[6]
					# Initial conditions
				self.rage: int = 0
				self.playerlevel: int = simulationsettinglist[5]
				self.frontattack: bool = simulationsettinglist[6]
				self.nenemies: int = simulationsettinglist[3]
				self.cappedskillMH: int = np.min([weaponstatlist[0][3],simulationsettinglist[5]*5])
				self.cappedskillOH: int = np.min([weaponstatlist[1][3],simulationsettinglist[5]*5])
				attackspeedfactor = 1
				if KeywordList[0] != 0:
					self.attackspeedfactor=attackspeedfactor*(1+0.01*KeywordList[0])
				if bufflist[12] == 1:
					self.attackspeedfactor=attackspeedfactor*1.05
				if KeywordList[5] == 1:
					self.normalizedspeed: float = 1.7
				else:
					self.normalizedspeed: float = 2.4
				self.attackspeedfactor: float = attackspeedfactor
				if weaponstatlist[1][2] == 0:
					self.dualwield: bool = 0
				else:
					self.dualwield: bool = 1
				self.nightfall: bool = KeywordList[6]
				self.giftofarthas: bool = bufflist[11]
					# Buffs
				self.damageinc: float = 1 * (1+0.01*bufflist[3]) * (1+0.05*bufflist[4])
				self.statmultiplier: float = 1 * (1+0.1*bufflist[6]) * (1+0.15*bufflist[0])
					# Abilities
				self.sapper: bool = consumablelist[7]
				self.ragepot: bool = consumablelist[8]
				self.jujuflurry: bool = consumablelist[9]
				self.bloodthirst: bool = abilitylist[2]
				self.bloodrage: bool = abilitylist[5]
				self.whirlwind: bool = abilitylist[3]
				self.hamstring: bool = abilitylist[4]
				self.execute: bool = abilitylist[6]
				self.deathwish: bool = abilitylist[7]
				self.reckless: bool = abilitylist[8]
				self.heroicstrike: bool = abilitylist[0]
				self.cleave: bool = abilitylist[1]
				self.crusaderMH: bool = KeywordList[7]
				# self.crusaderOH: bool = KeywordList[8]
					# Trinkets
				self.kissofthespider: bool = KeywordList[1]
				self.slayerscrest: bool = KeywordList[2]
				self.handofjustice: bool = KeywordList[4]
				self.jomgabbar: bool = KeywordList[3]
		@dataclass
		class AbilityCooldownClass: # Current cooldown of abilities
			bloodthirst: float = 0
			whirlwind: float = 0
			gcd: float = 0
			ragepot: float = 0
			deathwish: float = 0
			jujuflurry: float = 0
			bloodrage: float = 0
			reckless: float = 0
			automain: float = 0
			autooff: float = 0
			hamstring: float = 0
			execute: float = 0
			bloodragetic: float = 0
			angermanagement: float = 0
			sapper: float = 0
			kissofthespider: float = 0
			slayerscrest: float = 0
			jomgabbar: float = 0
			jomgabbartic: float = 0
		@dataclass
		class BuffsClass: # Which buffs are active
			flurry: bool = 0
			ragepot: bool = 0
			jujuflurry: bool = 0
			enrage: bool = 0
			crusaderMH: bool = 0
			crusaderOH: bool = 0
			deathwish: bool = 0
			reckless: bool = 0
			bloodrage: bool = 0
			kissofthespider: bool = 0
			slayerscrest: bool = 0
			jomgabbar: int = 0
			Zandalar: bool = 0
			Kings: bool = 0
			nightfall: bool = 0
			def Fill(self,bufflist):
				self.Zandalar: bool = bufflist[0]
				self.Kings: bool = bufflist[6]
		@dataclass
		class buffs_durationClass: # Active buffs current duration
			flurry: float = 0
			flurrycharge: int = 0
			ragepot: float = 0
			jujuflurry: float = 0
			enrage: float = 0
			enragecharge: int = 0
			crusaderMH: float = 0
			crusaderOH: float = 0
			deathwish: float = 0
			reckless: float = 0
			kissofthespider: float = 0
			slayerscrest: float = 0
			bloodrageinitiated: float = 0
			angermanagement: float = 0
			jomgabbar: float = 0
			jomgabbartic: float = 0
		@dataclass
		class buffs_durationBaseClass: # Duration of each buff
			flurry: float = 12
			flurrycharge: int = 3
			ragepot: float = 20
			jujuflurry: float = 20
			enrage: float = 15
			enragecharge: int = 12
			crusaderMH: float = 15
			crusaderOH: float = 15
			deathwish: float = 30
			reckless: float = 15
			jomgabbar: float = 20
			bloodrage: float = 10
			kissofthespider: float = 15
			slayerscrest: float = 20
		@dataclass
		class CooldownDurationBaseClass: # Maximum Cooldown of cooldowns
			whirlwind: int = 10
			bloodthirst: int = 6
			bloodrage: int = 60
			deathwish: int = 180
			reckless: int = 1800
			jujuflurry: int = 120
			ragepot: int = 120
			bloodragetic: int = 1
			angermanagement: int = 3
			sapper: int = 300
			kissofthespider: int = 120
			slayerscrest: int = 120
			jomgabbar: int = 120
			jomgabbartic: int = 2
			gcd: float = 1.5
		@dataclass
		class AttackTableClass: # Attack table template
			miss: float = 0
			dodge: float = 0
			parry: float = 0
			block: float = 0
			glance: float = 0
			crit: float = 0
			hit: float = 0
		@dataclass
		class ProcRateClass: # Proc rates
			crusader: float = 0.05 # 5% proc rate?
			handofjustice: float = 0.02 # 2% proc rate
			nightfall: float = 0.2 # 20% proc rate
			unbridledwrath: float = 0.0
			perditionblade: float = 0.039
			def Fill(self,talentlist):
				self.unbridledwrath: float = 0.08*talentlist[7]
		@dataclass
		class MobStatsClass: # Mob stats
			armor: float = 0
			level: int = 63
			defence: int = 315
			def Fill(self,bufflist,simulationsettinglist):
				self.armor: float = np.max([3761-bufflist[14]*450-bufflist[16]*505-bufflist[17]*640-bufflist[15]*200,0])
				self.level: int = simulationsettinglist[4]
				self.defence: int = simulationsettinglist[4]*5
		@dataclass
		class AISettingsClass:
			heroicstrikeragelimit: int = 30
			hamstringragelimitprimary: int = 80
			hamstringragelimitsecondary: int = 35
			def Fill(self,aisettinglist):
				self.heroicstrikeragelimit: int = aisettinglist[0]
				self.hamstringragelimitprimary: int = aisettinglist[1]
				self.hamstringragelimitsecondary: int = aisettinglist[2]
		@dataclass
		class BuffEffectClass:
			flurry: float = 1.3
			jujuflurry: float = 1.03
			kissofthespider: float = 1.2
			ragepot: int = 60
			crusaderMH: float = 100
			crusaderOH: float = 100
			slayerscrest: float = 260
			deathwish: float = 1.2
			enrage: float = 1.25
			reckless: float = 1
		@dataclass
		class CharacterClass:
			stats_base = []
			stats_active = []
			cooldown_active = []
			cooldown_max = []
			buffs_active = []
			buffs_duration = []
			buffs_maxduration = []
			buffs_effect = []
			attacktable = []
			procrate = []
			mobstats = []
			AIsettings = []
			fightduration = []
			executeduration = []
			AttackProcListMH = []
			AttackProcListOH = []
			AttackProcListWhite = []
			gcdlist = []
			AttackSpeedBuffs = []
			DamageFactorBuffs = []
			APBuffs = []
			StrBuffs = []
			CritBuffs = []
			
		## Core functionality ##
		def GeneratePriorityList(basestats): # Opimize plz
			prioritylist = []
			if basestats.jomgabbar:
				prioritylist.append('jomgabbartic')
			if basestats.angermanagement:
				prioritylist.append('angermanagement')
			if basestats.bloodrage:
				prioritylist.append('bloodragetic')
			if basestats.sapper:
				prioritylist.append('sapper')
			if basestats.kissofthespider:
				prioritylist.append('kissofthespider')
			if basestats.slayerscrest:
				prioritylist.append('slayerscrest')
			if basestats.jomgabbar:
				prioritylist.append('jomgabbar')
			if basestats.ragepot:
				prioritylist.append('ragepot')
			if basestats.jujuflurry:
				prioritylist.append('jujuflurry')
			if basestats.bloodrage:
				prioritylist.append('bloodrage')
			if basestats.reckless:
				prioritylist.append('reckless')
			if basestats.deathwish:
				prioritylist.append('deathwish')
			if basestats.bloodthirst:
				prioritylist.append('bloodthirst')
			if basestats.execute:
				prioritylist.append('execute')
			if basestats.whirlwind:
				prioritylist.append('whirlwind')
			if basestats.hamstring:
				prioritylist.append('hamstring')
			prioritylist.append('automain')
			if basestats.weaponspeedOH != 0:
				prioritylist.append('autooff')
			return prioritylist
		def SecondarySort(inlist,prioritylist):
			# Sort according to a priority list.
			timelist=[]
			for i in inlist:
				timelist.append(i[1])
			timelist = np.unique(timelist)
			shortlist = [] # Shorter list of only relevant events to be sorted
			for i in range(len(timelist)):
				shortlist.append([])
				for j in inlist:
					if j[1]==timelist[i]:
						shortlist[i].append(j)
			outlist=[]
			for k in range(len(shortlist)):
				for i in prioritylist: # Search through shortlist for element in prioritylist
					for j in shortlist[k]: # Loop over shortlist
						if i==j[0]: # 
							outlist.append(j)
			return outlist
		def FindNextEvent(Character,prioritylist,totalduration): # Convert into AI optimization procedure?
			sortedlist = sorted([(k,v) for k,v in Character.cooldown_active.__dict__.items()], key=lambda tup: tup[1])	# Sort according to time
			sortedlist=SecondarySort(sortedlist,prioritylist) # Sort according to prio list for identical times
			RemainingTime = Character.fightduration-totalduration
			for i in sortedlist:
				# All conditions are: If the ability is the next available of all events, AND conditions are met:
				if i[0] == 'angermanagement' and Character.stats_base.angermanagement == 1:
					return i[0],i[1]

				elif i[0] == 'jomgabbartic':
					if Character.buffs_active.jomgabbar != 0:
						return i[0],i[1]

				elif i[0] == 'bloodragetic':
					if Character.buffs_active.bloodrage >= 1: # tics are available
						return i[0],i[1]

				elif i[0] == 'sapper' and Character.stats_base.sapper == 1:
					if Character.stats_base.sapper:
						return i[0],i[1]

				elif i[0] == 'kissofthespider' and Character.stats_base.kissofthespider == 1:
					if RemainingTime >= Character.cooldown_max.kissofthespider+Character.buffs_maxduration.kissofthespider: # Cooldown can refresh allowing for an extra pop
						return i[0],i[1] # Time to the event and which event should be used
					elif RemainingTime<=Character.buffs_maxduration.kissofthespider: # Fight duration is less than uptime
						return i[0],i[1] # Time to the event and which event should be used

				elif i[0] == 'slayerscrest' and Character.stats_base.slayerscrest == 1:
					if Character.stats_base.kissofthespider == 1: # Slayers crest is 2nd prio

						if RemainingTime <= Character.buffs_maxduration.kissofthespider+Character.buffs_maxduration.slayerscrest:
							# If fight duration is shorter than both trinkets AND KotS , pop Slayers
							return i[0],i[1]
						elif RemainingTime >= Character.buffs_maxduration.kissofthespider+Character.cooldown_max.slayerscrest+Character.buffs_maxduration.slayerscrest: 
							# Cooldown+Active time left, allowing for an extra pop
							return i[0],i[1]
						elif Character.cooldown_active.kissofthespider >= RemainingTime-Character.buffs_maxduration.slayerscrest: # KotS will not be ready for use
							return i[0],i[1]

					else: # Slayers crest is 1st prio
						if RemainingTime >= Character.cooldown_max.slayerscrest+Character.buffs_maxduration.slayerscrest: # Cooldown can refresh allowing for an extra pop
							return i[0],i[1] # Time to the event and which event should be used
						elif RemainingTime<=Character.buffs_maxduration.slayerscrest: # Fight duration is less than uptime
							return i[0],i[1] # Time to the event and which event should be used	

				elif i[0] == 'jomgabbar' and Character.stats_base.jomgabbar == 1:
					if Character.stats_base.kissofthespider == 1 or Character.stats_base.slayerscrest == 1: # Jom Gabbar  is 2nd prio
						if Character.stats_base.kissofthespider == 1: 
							if RemainingTime <= Character.buffs_maxduration.kissofthespider+Character.buffs_maxduration.jomgabbar:
								# If fight duration is shorter than both trinkets AND KotS, pop jomgabbar
								return i[0],i[1]
							elif RemainingTime >= Character.buffs_maxduration.kissofthespider+Character.cooldown_max.jomgabbar: # Cooldown can refresh allowing for an extra pop
								return i[0],i[1]
							elif Character.cooldown_active.kissofthespider >= RemainingTime-Character.buffs_maxduration.jomgabbar: # KotS will not be ready for use
								return i[0],i[1]
						elif Character.stats_base.slayerscrest == 1:
							if RemainingTime <= Character.buffs_maxduration.slayerscrest+Character.buffs_maxduration.jomgabbar:
								# If fight duration is shorter than both trinkets AND Slayers Crest, pop jomgabbar
								return i[0],i[1]
							elif RemainingTime >= Character.buffs_maxduration.slayerscrest+Character.cooldown_max.jomgabbar: # Cooldown can refresh allowing for an extra pop
								return i[0],i[1]
							elif Character.cooldown_active.slayerscrest >= RemainingTime-Character.buffs_maxduration.jomgabbar: # KotS will not be ready for use
								return i[0],i[1]
					else: # Jom Gabbar is 1st prio
						if RemainingTime >= Character.cooldown_max.jomgabbar+Character.buffs_maxduration.jomgabbar: # Cooldown can refresh allowing for an extra pop
							return i[0],i[1] # Time to the event and which event should be used
						elif RemainingTime<=Character.buffs_maxduration.jomgabbar: # Fight duration is less than uptime
							return i[0],i[1] # Time to the event and which event should be used	
					

				elif i[0] == 'ragepot' and Character.stats_base.ragepot == 1:
					# Conditions for ragepot
					if RemainingTime >= Character.cooldown_max.ragepot+Character.buffs_maxduration.ragepot: # Cooldown can refresh allowing for an extra pop
						return i[0],i[1] # Time to the event and which event should be used
					elif RemainingTime<=Character.buffs_maxduration.ragepot: # Fight duration is less than uptime
						return i[0],i[1] # Time to the event and which event should be used

				elif i[0] == 'jujuflurry' and Character.stats_base.jujuflurry == 1:
					# Conditions for jujuflurry
					if RemainingTime >= Character.cooldown_max.jujuflurry+Character.buffs_maxduration.jujuflurry: # Cooldown can refresh allowing for an extra pop
						return i[0],i[1] # Time to the event and which event should be used
					elif RemainingTime<=Character.buffs_maxduration.jujuflurry: # Fight duration is less than uptime
						return i[0],i[1] # Time to the event and which event should be used
				
				elif i[0] == 'bloodrage':
					if Character.stats_active.rage <= 20: # Cooldown can refresh allowing for an extra pop
						return i[0],i[1] # Time to the event and which event should be used

				elif i[0] == 'reckless':
					if RemainingTime >= Character.cooldown_max.reckless+Character.buffs_maxduration.reckless: # Cooldown can refresh allowing for an extra pop
						return i[0],i[1] # Time to the event and which event should be used
					elif RemainingTime<=Character.buffs_maxduration.reckless: # Fight duration is less than uptime
						return i[0],i[1] # Time to the event and which event should be used

				elif i[0] == 'deathwish':
					if RemainingTime >= Character.cooldown_max.deathwish+Character.buffs_maxduration.deathwish and Character.stats_active.rage >= 10: # Cooldown can refresh allowing for an extra pop
						return i[0],i[1] # Time to the event and which event should be used
					elif RemainingTime<=Character.buffs_maxduration.deathwish and Character.stats_active.rage >= 10: # Fight duration is less than uptime
						return i[0],i[1] # Time to the event and which event should be used

				elif i[0] == 'bloodthirst':
					if Character.stats_active.rage >= 30:
						return i[0],i[1]
				elif i[0] == 'execute':
					if Character.stats_active.rage >= Character.stats_base.ExecuteAbilityCost and RemainingTime<=Character.executeduration:
						return i[0],i[1]

				elif i[0] == 'whirlwind':
					if Character.stats_active.rage >= 25:
						return i[0],i[1]

				elif i[0] == 'hamstring':
					bloodthirstcheck = 0
					whirlwindcheck = 0
					if Character.stats_active.rage >= Character.AIsettings.hamstringragelimitprimary: # Condition 1 for using Hamstring
						if Character.stats_base.bloodthirst:
							if Character.cooldown_active.bloodthirst>=Character.cooldown_max.gcd+i[1]: # Check for overlap with Bloodthirst
								bloodthirstcheck = 1
						else:
							bloodthirstcheck = 1
						if Character.stats_base.whirlwind: 
							if Character.cooldown_active.whirlwind>=Character.cooldown_max.gcd+i[1]: # 
								whirlwindcheck = 1
						else:
							whirlwindcheck = 1
						if bloodthirstcheck and whirlwindcheck:
							return i[0],i[1]
					elif Character.stats_base.crusaderMH: # If crusader is on the MH, check for secondary hamstring use condition
						if Character.stats_active.rage >= Character.AIsettings.hamstringragelimitsecondary and Character.buffs_active.crusaderMH == 0:
							if Character.stats_base.bloodthirst:
								if Character.cooldown_active.bloodthirst>=Character.cooldown_max.gcd+i[1]: # Check for overlap with Bloodthirst
									bloodthirstcheck = 1
							else:
								bloodthirstcheck = 1
							if Character.stats_base.whirlwind: 
								if Character.cooldown_active.whirlwind>=Character.cooldown_max.gcd+i[1]: # 
									whirlwindcheck = 1
							else:
								whirlwindcheck = 1
							if bloodthirstcheck and whirlwindcheck:
								return i[0],i[1]

				elif i[0] == 'automain':
					return i[0],i[1]

				elif i[0] == 'autooff':
					return i[0],i[1]
		def PerformEvent(event,Character): # Convert into class based calls
			damage=0
			if event == 'angermanagement':
				AngerManagement(Character)
				# print('Used AngerManagement')
			elif event == 'sapper':
				damage=Sapper(Character)
				# print('Used Sapper Charge')
			elif event == 'jomgabbar':
				JomGabbar(Character)
				# print('Used Jom Gabbar')
			elif event == 'jomgabbartic':
				JomGabbarTic(Character)
				# print('Used Jom Gabbar Tic')
			elif event == 'bloodragetic':
				Bloodragetic(Character)
				# print('Used bloodragetic')
			elif event == 'slayerscrest':
				SlayersCrest(Character)
				# print('Used Slayers Crest')
			elif event == 'kissofthespider':
				KissOfTheSpider(Character)
				# print('Used KotS')
			elif event == 'ragepot':
				RagePot(Character)
				# print('Used RagePot')
			elif event == 'jujuflurry':
				JujuFlurry(Character)
				# print('Used jujuflurry')
			elif event == 'reckless':
				Reckless(Character)
				# print('Used reckless')
			elif event == 'deathwish':
				Deathwish(Character)
				# print('Used deathwish')
			elif event == 'bloodrage':
				Bloodrage(Character)
				# print('Used bloodrage')
			elif event == 'bloodthirst':
				damage=Bloodthirst(Character)
				# print('Used bloodthirst')
			elif event == 'execute':
				damage=Execute(Character)
				# print('Used Execute')
			elif event == 'whirlwind':
				damage=Whirlwind(Character)
				# print('Used whirlwind')
			elif event == 'hamstring':
				damage=Hamstring(Character)
				# print('Used hamstring')
			elif event == 'automain':
				damage=MainAttack(Character)
				# print("Used automain")
			elif event == 'autooff':
				damage=OHauto(Character)
				# print('Used autooff')
			return damage
		def InitializeSimulation(scansetting,aisettinglist,simulationsettinglist,abilitylist,consumablelist,bufflist,talentlist,statlist,weaponstatlist,specials,KeywordList,ProcMHFunctionList,ProcOHFunctionList,sweeprange,GCDList,ATSpeedBuffList,DMGFactorBuffList,APBuffList,StrBuffList,CritBuffsList):
			AIsettings = AISettingsClass()
			AIsettings.Fill(aisettinglist)
			mobstats = MobStatsClass()
			mobstats.Fill(bufflist,simulationsettinglist)
			abilitycooldown = AbilityCooldownClass()
			procrate = ProcRateClass()
			procrate.Fill(talentlist)
			basestats = BaseStatsClass()
			basestats.Fill(statlist,weaponstatlist,bufflist,consumablelist,talentlist,abilitylist,simulationsettinglist,KeywordList)
			if simulationsettinglist[7] == "hit":
				basestats.hit = scansetting
			elif simulationsettinglist[7] == "AP":
				basestats.AP = np.floor(scansetting) + 222*bufflist[7] + 40*consumablelist[0] + 140*bufflist[1] + 290*bufflist[13] + 200*bufflist[2] + 100*bufflist[8]
			elif simulationsettinglist[7] == "crit":
				basestats.critMH = scansetting + 0.03*bufflist[18] + 0.02*consumablelist[2] + 0.05*bufflist[1] + 0.05*bufflist[5] + 0.03*bufflist[10] + 0.01*talentlist[5] + ((agility + 25*consumablelist[2] + 15*bufflist[5]+16*bufflist[9])*(1+0.1*bufflist[6])*(1+0.15*bufflist[0]))*1.0/2000 + 0.02*consumablelist[5]
				basestats.critOH = scansetting + 0.03*bufflist[18] + 0.02*consumablelist[2] + 0.05*bufflist[1] + 0.05*bufflist[5] + 0.03*bufflist[10] + 0.01*talentlist[5] + ((agility + 25*consumablelist[2] + 15*bufflist[5]+16*bufflist[9])*(1+0.1*bufflist[6])*(1+0.15*bufflist[0]))*1.0/2000 + 0.02*consumablelist[10]
			elif simulationsettinglist[7] == "heroic":
				AIsettings.heroicstrikeragelimit = scansetting
			elif simulationsettinglist[7] != "none":
				exit()
			buffs = BuffsClass()
			buffs.Fill(bufflist)
			buffeffect = BuffEffectClass()
			stats = ActiveStatsClass()
			duration = buffs_durationClass()
			cooldowntime = CooldownDurationBaseClass()
			buffs_duration = buffs_durationBaseClass()

			atmy,atmw,atow = GenerateAttackTable(stats,mobstats,basestats)
			prioritylist = GeneratePriorityList(basestats)
			
			Character = CharacterClass()
			Character.stats_base = basestats
			Character.stats_active = stats
			Character.cooldown_active = abilitycooldown
			Character.cooldown_max = cooldowntime
			Character.buffs_active = buffs
			Character.buffs_duration = duration
			Character.buffs_maxduration = buffs_duration
			Character.buffs_effect = buffeffect
			Character.attacktable = [atmy,atmw,atow]
			Character.procrate = procrate
			Character.mobstats = mobstats
			Character.AIsettings = AIsettings
			Character.fightduration = simulationsettinglist[1]
			Character.executeduration = simulationsettinglist[2]

			Character.AttackProcListMH = ProcMHFunctionList
			Character.AttackProcListOH = ProcOHFunctionList
			Character.AttackProcListWhite = ProcWhiteFunctionList

			Character.gcdlist = GCDList
			Character.AttackSpeedBuffs = ATSpeedBuffList
			Character.DamageFactorBuffs = DMGFactorBuffList
			Character.APBuffs = APBuffList
			Character.StrBuffs = StrBuffList
			Character.CritBuffs = CritBuffsList

			UpdateAttackSpeed(Character)
			UpdateDamage(Character)
			UpdateCrit(Character)
			UpdateAP(Character)
			# print(Character.stats_active.AP)
			# print(Character.stats_base.hit)
			# print(Character.stats_active.critMH)
			# print(Character.stats_active.critOH)
			# input(Character)
			return Character,prioritylist
		def RunFight(Character,prioritylist):
			totaldamage = 0.0
			totalduration = 0.0
			while totalduration<=Character.fightduration:
				event,t=FindNextEvent(Character,prioritylist,totalduration) # Identify which event is next according to cooldown time and prio.
				UpdateBuffs(t,Character)
				UpdateCd(t,Character)
				dmgbefore=totaldamage
				totaldamage+=PerformEvent(event,Character)
				totalduration+=t
				# print("Total Duration spent: %3.1f" %totalduration)
				# print(Character.cooldown_active)
				# print(Character.buffs_active)
				# print(Character.stats_active)
				# print(totaldamage-dmgbefore)
				# input('Continue \n')
			return totaldamage
		# Primary simulation
		if simulationsettinglist[7] == "none":
			sweeprange = [0]
		start = time.time()
		progressval=0
		dpslist=[]
		dpssigma=[]
		damagelist=[]
		for i in range(len(sweeprange)): # Overall parameter sweep
			damagelist.append([])
			for rep in range(simulationsettinglist[0]): # Repetition of each identical setting
				if simulationsettinglist[7] == "none":
					progressval+=100.0/simulationsettinglist[0]
				else:
					progressval+=100.0/(simulationsettinglist[0]*len(sweeprange))
				Stepsleft = simulationsettinglist[0]-rep
				TimeSpent = time.time()-start
				TimeRemaining = int(round(float(Stepsleft)/np.max([rep,1])*TimeSpent,0))
				val_progresstext.set('ETA: '+str(TimeRemaining)+' s')
				UpdateProgressBar(val_progressbar,progressval,root)

				# Initialize
				Character,prioritylist=InitializeSimulation(i,aisettinglist,simulationsettinglist,abilitylist,consumablelist,bufflist,talentlist,statlist,weaponstatlist,specials,KeywordList,ProcMHFunctionList,ProcOHFunctionList,sweeprange,GCDList,ATSpeedBuffList,DMGFactorBuffList,APBuffList,StrBuffList,CritBuffsList)				# Primary time loop
				# Run the fight
				totaldamage=RunFight(Character,prioritylist)
				damagelist[i].append(totaldamage)

			dpslist.append(np.mean(damagelist[i])/simulationsettinglist[1])
			dpssigma.append(np.std(damagelist[i])/(simulationsettinglist[1]*simulationsettinglist[0]**0.5))
		if simulationsettinglist[7] == "none":
			DPSAvg=np.mean(damagelist[i])/simulationsettinglist[1]
			DPGAvgSig=np.std(damagelist[i])/(simulationsettinglist[1]*(simulationsettinglist[0]-1)**0.5)
			fig = plt.hist([j*1.0/simulationsettinglist[1] for j in damagelist[i]])
			plt.xlabel('DPS')
			plt.ylabel('N times simulated')
			plt.title('Average DPS: %2.1f +- %2.1f' %(DPSAvg,DPGAvgSig))
			plt.show(block=False)
		else:
			fig = plt.errorbar(sweeprange,dpslist,dpssigma)
			if simulationsettinglist[7] == "hit":
				plt.xlabel('Hit Chance')
				filename = "HitSweep.txt"
			elif simulationsettinglist[7] == "crit":
				plt.xlabel('Crit Chance')
				filename = "CritSweep.txt"
			elif simulationsettinglist[7] == "AP":
				plt.xlabel('Attack Power')
				filename = "APSweep.txt"
			elif simulationsettinglist[7] == "heroic":
				plt.xlabel('Heroic strike used at rage')
				filename = "HeroicStrikeSweep.txt"
			with open(filename, 'w+') as f:
				np.savetxt(f,np.matrix([sweeprange,dpslist,dpssigma]))
			plt.ylabel('DPS')
			plt.show(block=False)
	button_Run = Button(frame,text="Run Simulation", width=18, command=RunSimulation).grid(row=0,column=4)

	val_progressbar=DoubleVar()
	val_progressbar.set(0)
	progressbar = Progressbar(frame, orient = HORIZONTAL, length = 100, mode = 'determinate',variable=val_progressbar).grid(row=0,column=5)
	val_progresstext=StringVar()
	val_progresstext.set("ETA:")
	label_progresstext = Label(frame,textvar=val_progresstext).grid(row=1,column=5)

	mainloop()
