def ExtractStats(gearlist,weaponlist,data):
	import pandas as pd
	import numpy as np

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
	KnownKeywords = ['SpeedEnchant','Kiss of the Spider','Slayers Crest','Jom Gabbar','Hand of Justice','DaggerMH','Nightfall','Crusader MH','Crusader OH']
	if 'SpeedEnchant' in keywordlist:
		SpeedEnchants = keywordlist.count('SpeedEnchant')
	else:
		SpeedEnchants = 0
	if 'Kiss of the Spider' in keywordlist:
		KissOfTheSpider = 1
	else:
		KissOfTheSpider = 0
	if 'Slayers Crest' in keywordlist:
		SlayersCrest = 1
	else:
		SlayersCrest = 0
	if 'Jom Gabbar' in keywordlist:
		JomGabbar = 1
	else:
		JomGabbar = 0
	if 'Hand of Justice' in keywordlist:
		HandOfJustice = 1
	else:
		HandOfJustice = 0
	if 'DaggerMH' in keywordlist:
		DaggerMH = 1
	else:
		DaggerMH = 0
	if 'Nightfall' in keywordlist:
		Nightfall = 1
	else:
		Nightfall = 0
	if 'Crusader MH' in keywordlist:
		CrusaderMH = 1
	else:
		CrusaderMH = 0
	if 'Crusader OH' in keywordlist:
		CrusaderOH = 1
	else:
		CrusaderOH = 0
	boollist=[i in KnownKeywords for i in keywordlist]
	unknownkeywordlist=''
	if all(boollist) == 0:
		for i in range(len(boollist)):
			if boollist[i]==False:
				unknownkeywordlist=unknownkeywordlist+str(keywordlist[i])+', '
		unknownkeywordlist=unknownkeywordlist[:-2]
		messagebox.showwarning("Unknown Keywords", "Unknown Keywords are: "+unknownkeywordlist+'. \nThis is likely a feature not included in the simulation and its effect will be ignored. \nOften this means on-hit effects are ignored.')
	return SpeedEnchants,KissOfTheSpider,SlayersCrest,JomGabbar,HandOfJustice,DaggerMH,Nightfall,CrusaderMH,CrusaderOH
def ConsumablesParser(consumablelist):
	JujuMight = consumablelist[0]
	JujuPower = consumablelist[1]
	Mongoose = consumablelist[2]
	Dumpling = consumablelist[3]
	OHStone = consumablelist[4]
	MHCritStone = consumablelist[5]
	MHStone = consumablelist[6]
	UseSapper = consumablelist[7]
	UseRagePot = consumablelist[8]
	UseJujuFlurry = consumablelist[9]
	return JujuMight,JujuPower,Mongoose,Dumpling,OHStone,MHCritStone,MHStone,UseSapper,UseRagePot,UseJujuFlurry
def BuffsParser(bufflist):
	Zandalar = bufflist[0]
	Dragonslayer = bufflist[1]
	DMT = bufflist[2]
	DMF = bufflist[3] # 10 for maximum effect
	SilithusSand = bufflist[4]
	Songflower = bufflist[5]
	Kings = bufflist[6]
	BoM = bufflist[7]
	Trueshot = bufflist[8]
	MotW = bufflist[9]
	PackLeader = bufflist[10]
	GiftOfArthas = bufflist[11]
	Chicken = bufflist[12]
	Battleshout = bufflist[13]
	Sunders = bufflist[14] # 5 for full stacks
	Annihilator = bufflist[15] # 3 for full stacks
	FaerieFire = bufflist[16]
	CoR = bufflist[17]
	ZerkerStance = bufflist[18]
	return Zandalar,Dragonslayer,DMT,DMF,SilithusSand,Songflower,Kings,BoM,Trueshot,MotW,PackLeader,GiftOfArthas,Chicken,Battleshout,Sunders,Annihilator,FaerieFire,CoR,ZerkerStance
def AISettingParser(aisettinglist):
	heroicstrikeragelimit = aisettinglist[0]
	hamstringragelimitprimary = aisettinglist[1]
	hamstringragelimitsecondary = aisettinglist[2]
	return heroicstrikeragelimit,hamstringragelimitprimary,hamstringragelimitsecondary
def AbilityUseParser(abilitylist):
	HeroicStrike = abilitylist[0] # Heroic Strike
	Cleave = abilitylist[1] # Cleave instead of Heroic Strike if there are 2 or more mobs
	Bloodthirst = abilitylist[2]
	Whirlwind = abilitylist[3]
	Hamstring = abilitylist[4]
	Bloodrage = abilitylist[5]
	Execute = abilitylist[6]
	Deathwish = abilitylist[7]
	Reckless = abilitylist[8]
	return HeroicStrike,Cleave,Bloodthirst,Whirlwind,Hamstring,Bloodrage,Execute,Deathwish,Reckless
def SimulationSettingParser(simulationsettinglist):
	import numpy as np
	Nreps = simulationsettinglist[0]
	fightduration = simulationsettinglist[1]
	executeduration = simulationsettinglist[2]
	NEnemies = simulationsettinglist[3]
	MobLevel = simulationsettinglist[4]
	PlayerLevel = simulationsettinglist[5]
	FrontAttack = simulationsettinglist[6]
	scanaxis = simulationsettinglist[7] # AP or hit or crit or heroic or none
	sweeprange = np.linspace(simulationsettinglist[8],simulationsettinglist[9],simulationsettinglist[10])
	return Nreps,fightduration,executeduration,NEnemies,MobLevel,PlayerLevel,FrontAttack,scanaxis,sweeprange
def TalentsParser(talentlist):
	OHSpecializationTalent = talentlist[0] # 5/5 for full talent
	CritDamageTalent = talentlist[1] # 2/2 for full effect
	ImpHeroicStrike = talentlist[2] # 3/3 for full effect
	ExecuteTalent = talentlist[3]
	AngerManagement = talentlist[4]
	Cruelty = talentlist[5] # 5/5 for full effect
	ImprovedCleave = talentlist[6]
	return OHSpecializationTalent,CritDamageTalent,ImpHeroicStrike,ExecuteTalent,AngerManagement,Cruelty,ImprovedCleave

# Version 1.0

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename,asksaveasfile
from tkinter.ttk import Progressbar
import numpy as np
import pandas as pd
import os
import sys

def resource_path(relative_path):
	try: #""" Get absolute path to resource, works for dev and for PyInstaller """
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

filename = resource_path('GearList.xlsx')
data = pd.read_excel(filename, sheet_name = None)

def myfunction(event):
	canvas.configure(scrollregion=canvas.bbox("all"),width=975,height=490)

root=Tk(screenName="Warrior DPS Simulator v1.0",className=" Warrior DPS Simulator v1.0")
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
frame.bind("<Configure>",myfunction)

def mouse_wheel(event):
	canvas.yview_scroll(int(-1*(event.delta/30)),"units")

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
val_MHStone = IntVar()
val_MHStone.set(0)
label_MHStone = Label(frame,text = "MH Stone").grid(row=7,column=2)
checkbox_MHStone = Checkbutton(frame,text=" ",variable = val_MHStone).grid(row=7,column=3)
val_OHStone = IntVar()
val_OHStone.set(1)
label_OHStone = Label(frame,text = "OH Stone").grid(row=8,column=2)
checkbox_OHStone = Checkbutton(frame,text=" ",variable = val_OHStone).grid(row=8,column=3)
val_UseSapper = IntVar()
val_UseSapper.set(0)
label_UseSapper = Label(frame,text = "Sapper").grid(row=9,column=2)
checkbox_UseSapper = Checkbutton(frame,text=" ",variable = val_UseSapper).grid(row=9,column=3)
val_UseRagePot = IntVar()
val_UseRagePot.set(0)
label_UseRagePot = Label(frame,text = "Rage Potion").grid(row=10,column=2)
checkbox_UseRagePot = Checkbutton(frame,text=" ",variable = val_UseRagePot).grid(row=10,column=3)
val_UseJujuFlurry = IntVar()
val_UseJujuFlurry.set(0)
label_UseJujuFlurry = Label(frame,text = "Juju Flurry").grid(row=11,column=2)
checkbox_UseJujuFlurry = Checkbutton(frame,text=" ",variable = val_UseJujuFlurry).grid(row=11,column=3)

## Abilities ##
label_Abilities = Label(frame,text = "Abilities",font="bold").grid(row=12,column=2)
val_HeroicStrike = IntVar()
val_HeroicStrike.set(1)
label_HeroicStrike = Label(frame,text = "Heroic Strike").grid(row=13,column=2)
checkbox_HeroicStrike = Checkbutton(frame,text=" ",variable = val_HeroicStrike).grid(row=13,column=3)
val_Cleave = IntVar()
val_Cleave.set(1)
label_Cleave = Label(frame,text = "Cleave").grid(row=14,column=2)
checkbox_Cleave = Checkbutton(frame,text=" ",variable = val_Cleave).grid(row=14,column=3)
val_Bloodthirst = IntVar()
val_Bloodthirst.set(1)
label_Bloodthirst = Label(frame,text = "Bloodthirst").grid(row=15,column=2)
checkbox_Bloodthirst = Checkbutton(frame,text=" ",variable = val_Bloodthirst).grid(row=15,column=3)
val_Whirlwind = IntVar()
val_Whirlwind.set(1)
label_Whirlwind = Label(frame,text = "Whirlwind").grid(row=16,column=2)
checkbox_Whirlwind = Checkbutton(frame,text=" ",variable = val_Whirlwind).grid(row=16,column=3)
val_Hamstring = IntVar()
val_Hamstring.set(1)
label_Hamstring = Label(frame,text = "Hamstring").grid(row=17,column=2)
checkbox_Hamstring = Checkbutton(frame,text=" ",variable = val_Hamstring).grid(row=17,column=3)
val_Bloodrage = IntVar()
val_Bloodrage.set(1)
label_Bloodrage = Label(frame,text = "Bloodrage").grid(row=18,column=2)
checkbox_Bloodrage = Checkbutton(frame,text=" ",variable = val_Bloodrage).grid(row=18,column=3)
val_Execute = IntVar()
val_Execute.set(1)
label_Execute = Label(frame,text = "Execute").grid(row=19,column=2)
checkbox_Execute = Checkbutton(frame,text=" ",variable = val_Execute).grid(row=19,column=3)
val_Deathwish = IntVar()
val_Deathwish.set(1)
label_Deathwish = Label(frame,text = "Deathwish").grid(row=20,column=2)
checkbox_Deathwish = Checkbutton(frame,text=" ",variable = val_Deathwish).grid(row=20,column=3)
val_Reckless = IntVar()
val_Reckless.set(1)
label_Reckless = Label(frame,text = "Recklessness").grid(row=21,column=2)
checkbox_Reckless = Checkbutton(frame,text=" ",variable = val_Reckless).grid(row=21,column=3)

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


label_SimulationSettings = Label(frame,text = "Simulation Settings",font="bold").grid(row=9,column=4)

val_Nreps = IntVar()
val_Nreps.set(100)
label_Nreps = Label(frame,text = "Repititions of the simulation").grid(row=10,column=4)
entry_Nreps = Entry(frame,textvar=val_Nreps,width=3).grid(row=10,column=5)
val_fightduration = IntVar()
val_fightduration.set(60)
label_fightduration = Label(frame,text = "Fight Duration").grid(row=11,column=4)
entry_fightduration = Entry(frame,textvar=val_fightduration,width=3).grid(row=11,column=5)
val_executeduration = IntVar()
val_executeduration.set(10)
label_executeduration = Label(frame,text = "Execute Duration").grid(row=12,column=4)
entry_executeduration = Entry(frame,textvar=val_executeduration,width=3).grid(row=12,column=5)
val_NEnemies = IntVar()
val_NEnemies.set(1)
label_NEnemies = Label(frame,text = "Number of targets").grid(row=13,column=4)
entry_NEnemies = Entry(frame,textvar=val_NEnemies,width=3).grid(row=13,column=5)
val_MobLevel = IntVar()
val_MobLevel.set(63)
label_MobLevel = Label(frame,text = "Enemy Level").grid(row=14,column=4)
entry_MobLevel = Entry(frame,textvar=val_MobLevel,width=3).grid(row=14,column=5)
val_PlayerLevel = IntVar()
val_PlayerLevel.set(60)
label_PlayerLevel = Label(frame,text = "Player Level").grid(row=15,column=4)
entry_PlayerLevel = Entry(frame,textvar=val_PlayerLevel,width=3).grid(row=15,column=5)
val_FrontAttack = IntVar()
val_FrontAttack.set(0)
label_FrontAttack = Label(frame,text = "Front Attack?").grid(row=16,column=4)
checkbox_FrontAttack = Checkbutton(frame,text="",variable = val_FrontAttack).grid(row=16,column=5)

val_scanaxis = StringVar()
val_scanaxis.set("none")
choices={"none","crit","hit","AP","heroic"}
label_scanaxis = Label(frame,text = "Axis to scan along").grid(row=17,column=4)
OptionMenu_scanaxis = OptionMenu(frame,val_scanaxis,*choices).grid(row=17,column=5)
def change_dropdown(*args):
	return val_scanaxis.get()
val_scanaxis.trace('w', change_dropdown)
val_sweeprangestart = DoubleVar()
val_sweeprangestart.set(0)
label_sweeprangestart = Label(frame,text = "Starting value for scan").grid(row=18,column=4)
entry_sweeprangestart = Entry(frame,textvar=val_sweeprangestart,width=3).grid(row=18,column=5)
val_sweeprangeend = DoubleVar()
val_sweeprangeend.set(0)
label_sweeprangeend = Label(frame,text = "End value for scan").grid(row=19,column=4)
entry_sweeprangeend = Entry(frame,textvar=val_sweeprangeend,width=3).grid(row=19,column=5)
val_sweeprangesteps = IntVar()
val_sweeprangesteps.set(0)
label_sweeprangesteps = Label(frame,text = "Steps in the scan").grid(row=20,column=4)
entry_sweeprangesteps = Entry(frame,textvar=val_sweeprangesteps,width=3).grid(row=20,column=5)

## AI settings ##
label_AISettings = Label(frame,text = "AI Settings",font="bold").grid(row=21,column=4)
val_heroicstrikeragelimit = IntVar()
val_heroicstrikeragelimit.set(35)
label_heroicstrikeragelimit = Label(frame,text = "Use Heroic Strike at rage").grid(row=22,column=4)
entry_heroicstrikeragelimit = Entry(frame,textvar=val_heroicstrikeragelimit,width=3).grid(row=22,column=5)
val_hamstringragelimitprimary = IntVar()
val_hamstringragelimitprimary.set(80)
label_hamstringragelimitprimary = Label(frame,text = "Use Hamstring at rage").grid(row=23,column=4)
entry_hamstringragelimitprimary = Entry(frame,textvar=val_hamstringragelimitprimary,width=3).grid(row=23,column=5)
val_hamstringragelimitsecondary = IntVar()
val_hamstringragelimitsecondary.set(35)
label_hamstringragelimitsecondary = Label(frame,text = "Without Crusader, use Hamstring at").grid(row=24,column=4)
entry_hamstringragelimitsecondary = Entry(frame,textvar=val_hamstringragelimitsecondary,width=3).grid(row=24,column=5)

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
	
	SetSetting(val_JujuMight,consumablelist[0])
	SetSetting(val_JujuPower,consumablelist[1])
	SetSetting(val_Mongoose,consumablelist[2])
	SetSetting(val_Dumpling,consumablelist[3])
	SetSetting(val_OHStone,consumablelist[4])
	SetSetting(val_MHCritStone,consumablelist[5])
	SetSetting(val_MHStone,consumablelist[6])
	SetSetting(val_UseSapper,consumablelist[7])
	SetSetting(val_UseRagePot,consumablelist[8])
	SetSetting(val_UseJujuFlurry,consumablelist[8])
	
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
	talentlist = [val_OHSpecializationTalent.get(),val_CritDamageTalent.get(),val_ImpHeroicStrike.get(),val_ExecuteTalent.get(),val_AngerManagement.get(),val_Cruelty.get(),val_ImprovedCleave.get()]
	consumablelist = [val_JujuMight.get(),val_JujuPower.get(),val_Mongoose.get(),val_Dumpling.get(),val_OHStone.get(),val_MHCritStone.get(),val_MHStone.get(),val_UseSapper.get(),val_UseRagePot.get(),val_UseJujuFlurry.get()]
	bufflist = [val_Zandalar.get(),val_Dragonslayer.get(),val_DMT.get(),val_DMF.get(),val_SilithusSand.get(),val_Songflower.get(),val_Kings.get(),val_BoM.get(),val_Trueshot.get(),val_MotW.get(),val_PackLeader.get(),val_GiftOfArthas.get(),val_Chicken.get(),val_Battleshout.get(),val_Sunders.get(),val_Annihilator.get(),val_FaerieFire.get(),val_CoR.get(),val_ZerkerStance.get()]
	abilitylist = [val_HeroicStrike.get(),val_Cleave.get(),val_Bloodthirst.get(),val_Whirlwind.get(),val_Hamstring.get(),val_Bloodrage.get(),val_Execute.get(),val_Deathwish.get(),val_Reckless.get()]
	simulationsettinglist = [val_Nreps.get(),val_fightduration.get(),val_executeduration.get(),val_NEnemies.get(),val_MobLevel.get(),val_PlayerLevel.get(),val_FrontAttack.get(),val_scanaxis.get(),val_sweeprangestart.get(),val_sweeprangeend.get(),val_sweeprangesteps.get()]
	aisettinglist = [val_heroicstrikeragelimit.get(),val_hamstringragelimitprimary.get(),val_hamstringragelimitsecondary.get()]
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
	global SpeedEnchants,KissOfTheSpider,SlayersCrest,JomGabbar,HandOfJustice,DaggerMH,Nightfall,CrusaderMH,CrusaderOH,OHSpecializationTalent,CritDamageTalent,ImpHeroicStrike,ExecuteTalent,AngerManagement,Cruelty,ImprovedCleave,JujuMight,JujuPower,Mongoose,Dumpling,OHStone,MHCritStone,MHStone,UseSapper,UseRagePot,UseJujuFlurry,Zandalar,Dragonslayer,DMT,DMF,SilithusSand,Songflower,Kings,BoM,Trueshot,MotW,PackLeader,GiftOfArthas,Chicken,Battleshout,Sunders,Annihilator,FaerieFire,CoR,ZerkerStance,HeroicStrike,Cleave,Bloodthirst,Whirlwind,Hamstring,Bloodrage,Execute,Deathwish,Reckless,Nreps,fightduration,executeduration,NEnemies,MobLevel,PlayerLevel,FrontAttack,scanaxis,sweeprange,heroicstrikeragelimit,hamstringragelimitprimary,hamstringragelimitsecondary,AP,crit,hit,strength,agility,weaponskillMH,weaponmindamageMH,weaponmaxdamageMH,weaponspeedMH,weaponskillOH,weaponmindamageOH,weaponmaxdamageOH,weaponspeedOH,dpslist,dpssigma,gcdlist,AttackSpeedBuffs,DamageFactorBuffs,APBuffs,StrBuffs,CritBuffs,AIsettings,mobstats,abilitycooldown,procrate,basestats,prioritylist,buffeffect,buffs,stats,atmy,atmw,atow,duration,cooldowntime,buffdurationtotalduration,totaldamage,totalduration,totaldamage,buffduration
	gearlist = [val_Race.get(),val_Head.get(),val_Neck.get(),val_Shoulders.get(),val_Cloak.get(),val_Chest.get(),val_Wrist.get(),val_Gloves.get(),val_Belt.get(),val_Legs.get(),val_Boots.get(),val_Ring1.get(),val_Ring2.get(),val_Trinket1.get(),val_Trinket2.get(),val_Ranged.get(),val_HeadEnchant.get(),val_LegEnchant.get(),val_ShouldersEnchant.get(),val_MHWeaponEnchant.get(),val_OHWeaponEnchant.get(),val_CloakEnchant.get(),val_ChestEnchant.get(),val_WristEnchant.get(),val_GlovesEnchant.get(),val_BootsEnchant.get()]
	if val_OHWeapon.get()!="None":
		weaponlist = [val_MHWeapon.get(),val_OHWeapon.get()]
	else:
		weaponlist = [val_MHWeapon.get()]
	aisettinglist=[val_heroicstrikeragelimit.get(),val_hamstringragelimitprimary.get(),val_hamstringragelimitsecondary.get()]
	simulationsettinglist=[val_Nreps.get(),val_fightduration.get(),val_executeduration.get(),val_NEnemies.get(),val_MobLevel.get(),val_PlayerLevel.get(),val_FrontAttack.get(),val_scanaxis.get(),val_sweeprangestart.get(),val_sweeprangeend.get(),val_sweeprangesteps.get()]
	abilitylist=[val_HeroicStrike.get(),val_Cleave.get(),val_Bloodthirst.get(),val_Whirlwind.get(),val_Hamstring.get(),val_Bloodrage.get(),val_Execute.get(),val_Deathwish.get(),val_Reckless.get()]
	consumablelist=[val_JujuMight.get(),val_JujuPower.get(),val_Mongoose.get(),val_Dumpling.get(),val_OHStone.get(),val_MHCritStone.get(),val_MHStone.get(),val_UseSapper.get(),val_UseRagePot.get(),val_UseJujuFlurry.get()]
	bufflist = [val_Zandalar.get(),val_Dragonslayer.get(),val_DMT.get(),val_DMF.get(),val_SilithusSand.get(),val_Songflower.get(),val_Kings.get(),val_BoM.get(),val_Trueshot.get(),val_MotW.get(),val_PackLeader.get(),val_GiftOfArthas.get(),val_Chicken.get(),val_Battleshout.get(),val_Sunders.get(),val_Annihilator.get(),val_FaerieFire.get(),val_CoR.get(),val_ZerkerStance.get()]
	talentlist = [val_OHSpecializationTalent.get(),val_CritDamageTalent.get(),val_ImpHeroicStrike.get(),val_ExecuteTalent.get(),val_AngerManagement.get(),val_Cruelty.get(),val_ImprovedCleave.get()]
	statlist,weaponstatlist,specials=ExtractStats(gearlist,weaponlist,data)

	SpeedEnchants,KissOfTheSpider,SlayersCrest,JomGabbar,HandOfJustice,DaggerMH,Nightfall,CrusaderMH,CrusaderOH=KeywordParser(specials)
	OHSpecializationTalent,CritDamageTalent,ImpHeroicStrike,ExecuteTalent,AngerManagement,Cruelty,ImprovedCleave=TalentsParser(talentlist)
	JujuMight,JujuPower,Mongoose,Dumpling,OHStone,MHCritStone,MHStone,UseSapper,UseRagePot,UseJujuFlurry=ConsumablesParser(consumablelist)
	Zandalar,Dragonslayer,DMT,DMF,SilithusSand,Songflower,Kings,BoM,Trueshot,MotW,PackLeader,GiftOfArthas,Chicken,Battleshout,Sunders,Annihilator,FaerieFire,CoR,ZerkerStance=BuffsParser(bufflist)
	HeroicStrike,Cleave,Bloodthirst,Whirlwind,Hamstring,Bloodrage,Execute,Deathwish,Reckless=AbilityUseParser(abilitylist)
	Nreps,fightduration,executeduration,NEnemies,MobLevel,PlayerLevel,FrontAttack,scanaxis,sweeprange=SimulationSettingParser(simulationsettinglist)
	heroicstrikeragelimit,hamstringragelimitprimary,hamstringragelimitsecondary=AISettingParser(aisettinglist)


	# From gear and race:
	AP=statlist[4]
	crit=float(statlist[0]/100)
	hit=float(statlist[1]/100)
	strength = statlist[2]
	agility = statlist[3] 

	weaponskillMH=weaponstatlist[0][3]
	weaponmindamageMH=weaponstatlist[0][0]
	weaponmaxdamageMH=weaponstatlist[0][1]
	weaponspeedMH=weaponstatlist[0][2]

	weaponskillOH=weaponstatlist[1][3]
	weaponmindamageOH=weaponstatlist[1][0]
	weaponmaxdamageOH=weaponstatlist[1][1]
	weaponspeedOH=weaponstatlist[1][2]

	from dataclasses import dataclass,fields
	import numpy as np
	import matplotlib.pyplot as plt
	import time
	@dataclass
	class ActiveStatsClass: # Stats varied during combat
		AP: float = 0
		critMH: float = 0
		critOH: float = 0
		weaponspeedMH: float = 0
		weaponspeedOH: float = 0
		rage: float = 0
		damageinc: float = 1
	@dataclass
	class BaseStatsClass: # Base stats not varied during combat
		# global AP,BoM,JujuMight,Dragonslayer,Battleshout,DMT,Trueshot,strength,Dumpling,Songflower,JujuPower,MotW,crit,ZerkerStance,Mongoose,Dragonslayer,
		# Stats
		AP: float = AP + 222*BoM + 40*JujuMight + Dragonslayer*140 + Battleshout*290 + DMT*200 + 100*Trueshot
		strength: float = strength + 20*Dumpling + 15*Songflower +30*JujuPower + 16*MotW
		critMH: float = crit + 0.03*ZerkerStance + 0.02*Mongoose + 0.05*Dragonslayer + 0.05*Songflower + 0.03*PackLeader + 0.01*Cruelty + ((agility + 25*Mongoose + 15*Songflower+16*MotW)*(1+0.1*Kings)*(1+0.15*Zandalar))*1.0/2000 + 0.02*MHCritStone
		critOH: float = crit + 0.03*ZerkerStance + 0.02*Mongoose + 0.05*Dragonslayer + 0.05*Songflower + 0.03*PackLeader + 0.01*Cruelty + ((agility + 25*Mongoose + 15*Songflower+16*MotW)*(1+0.1*Kings)*(1+0.15*Zandalar))*1.0/2000
		hit: float = hit
		weaponskillMH: int = weaponskillMH
		weaponmindamageMH: int = weaponmindamageMH + 8*MHStone# + 8*GiftOfArthas
		weaponmaxdamageMH: int = weaponmaxdamageMH + 8*MHStone# + 8*GiftOfArthas
		weaponspeedMH: float = weaponspeedMH
		weaponskillOH: int = weaponskillOH
		weaponmindamageOH: int = weaponmindamageOH + 8*OHStone# + 8*GiftOfArthas
		weaponmaxdamageOH: int = weaponmaxdamageOH + 8*OHStone# + 8*GiftOfArthas
		weaponspeedOH: float = weaponspeedOH
		# Talents
		OHSpecialization: float = OHSpecializationTalent
		CritDamageBonus: float = 2+0.1*CritDamageTalent
		angermanagement: bool = AngerManagement
		HeroicStrikeAbilityCost: int = 15 - ImpHeroicStrike
		if ExecuteTalent == 2:
			ExecuteAbilityCost: int = 10
		elif ExecuteTalent == 1:
			ExecuteAbilityCost: int = 13
		else:
			ExecuteAbilityCost: int = 15
		impcleave: int = ImprovedCleave
		# Initial conditions
		rage: int = 0
		playerlevel: int = PlayerLevel
		frontattack: bool = FrontAttack
		nenemies: int = NEnemies
		cappedskillMH: int = np.min([weaponskillMH,PlayerLevel*5])
		cappedskillOH: int = np.min([weaponskillOH,PlayerLevel*5])
		attackspeedfactor = 1
		if SpeedEnchants != 0:
			attackspeedfactor=attackspeedfactor*(1+0.01*SpeedEnchants)
		if Chicken == 1:
			attackspeedfactor=attackspeedfactor*1.05
		normalizedspeed: float = 2.4*(1-DaggerMH)+1.7*DaggerMH
		attackspeedfactor: float = attackspeedfactor
		if weaponspeedOH == 0:
			dualwield = 0
		else:
			dualwield = 1
		dualwield: bool = dualwield
		nightfall: bool = Nightfall
		giftofarthas: bool = GiftOfArthas
		# Buffs
		damageinc: float = 1 * (1+0.01*DMF) * (1+0.05*SilithusSand)
		statmultiplier: float = 1 * (1+0.1*Kings) * (1+0.15*Zandalar)
		# Abilities
		sapper: bool = UseSapper
		ragepot: bool = UseRagePot
		jujuflurry: bool = UseJujuFlurry
		bloodthirst: bool = Bloodthirst
		bloodrage: bool = Bloodrage
		whirlwind: bool = Whirlwind
		hamstring: bool = Hamstring
		execute: bool = Execute
		deathwish: bool = Deathwish
		reckless: bool = Reckless
		heroicstrike: bool = HeroicStrike
		cleave: bool = Cleave
		crusaderMH: bool = CrusaderMH
		crusaderOH: bool = CrusaderOH
		# Trinkets
		kissofthespider: bool = KissOfTheSpider
		slayerscrest: bool = SlayersCrest
		handofjustice: bool = HandOfJustice
		jomgabbar: bool = JomGabbar
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
		Zandalar: bool = Zandalar
		Kings: bool = Kings
		nightfall: bool = 0
	@dataclass
	class BuffDurationClass: # Active buffs current duration
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
	class BuffDurationBaseClass: # Duration of each buff
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
		# jomgabbar: int = 120
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
	@dataclass
	class MobStatsClass: # Mob stats
		armor: float = np.max([3761-Sunders*450-FaerieFire*505-CoR*640-Annihilator*200,0])
		level: int = MobLevel
		defence: int = MobLevel*5
	@dataclass
	class AISettingsClass:
		heroicstrikeragelimit: int = heroicstrikeragelimit
		hamstringragelimitprimary: int = hamstringragelimitprimary
		hamstringragelimitsecondary: int = hamstringragelimitsecondary
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
	## Attack calculations ##
	def GenerateAttackTable():
		global stats,mobstats, basestats
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
	def AttackDamage(hand):
		global basestats,stats#,mobstats,buffs
		if hand == 0:
			mindamage=basestats.weaponmindamageMH+stats.AP/14.0*basestats.weaponspeedMH
			maxdamage=basestats.weaponmaxdamageMH+stats.AP/14.0*basestats.weaponspeedMH
		elif hand == 1:
			mindamage=(basestats.weaponmindamageMH+stats.AP/14.0*basestats.weaponspeedMH)*(0.5+0.025*basestats.OHSpecialization)
			maxdamage=(basestats.weaponmaxdamageMH+stats.AP/14.0*basestats.weaponspeedMH)*(0.5+0.025*basestats.OHSpecialization)
		damage=np.random.uniform(mindamage,maxdamage)
		return damage
	def GlanceFactor(hand):
		global mobstats,basestats
		if hand == 0:
			skilldiff = mobstats.defence - basestats.weaponskillMH
		elif hand == 1:
			skilldiff = mobstats.defence - basestats.weaponskillOH
		glancinglow = np.min([1.3-0.05*skilldiff,0.91])
		glancinghigh = np.max([0.2,np.min([1.2-0.03*skilldiff,0.99])])
		glancingfactor = np.random.uniform(glancinglow,glancinghigh)
		return glancingfactor
	def ArmorReduction():
		global mobstats,basestats
		return 1-np.min([0.75,np.max([0,mobstats.armor / (mobstats.armor + 400 + 85 * basestats.playerlevel)])])
	def RageFromAttack(damage):
		global stats
		gain = np.round(0.03252*damage)
		return gain # rage gain
	# On attack procs
	def FlurryProc():
		global buffs,duration
		buffs.flurry = 1
		duration.flurry = 12
		duration.flurrycharge = 3
		UpdateAttackSpeed()
	def FlurryConsume():
		global buffs,duration
		if buffs.flurry == 1:
			duration.flurrycharge += -1
			if duration.flurrycharge<=0:
				buffs.flurry = 0
				UpdateAttackSpeed()
	def CrusaderMH():
		global buffs,duration,procrate
		if basestats.crusaderMH:
			if np.random.uniform()<=procrate.crusader:
				buffs.crusaderMH = 1
				duration.crusaderMH = 15
				UpdateAP()
	def CrusaderOH():
		global buffs,duration,procrate
		if basestats.crusaderOH:
			if np.random.uniform()<=procrate.crusader:
				buffs.crusaderOH = 1
				duration.crusaderOH = 15
				UpdateAP()
	def UnbridledWrath():
		global stats
		if np.random.uniform()>=0.4:
			stats.rage=np.min([100,stats.rage+1])
	def HandOfJustice():
		global basestats,procrate
		if basestats.handofjustice==1:
			if np.random.uniform()<procrate.handofjustice:
				MHauto()
	def Nightfall():
		global buffs,duration,procrate
		if basestats.nightfall:
			if np.random.uniform()<=procrate.nightfall:
				buffs.nightfall = 1
				duration.nightfall = 5
	## Abilities ##
	def Bloodthirst():
		global totaldamage,stats,mobstats,buffs,duration,abilitycooldown,atmy,cooldowntime
		abilitycooldown.bloodthirst = 6
		stats.rage += -30
		abilitycooldown.gcd = cooldowntime.gcd
		outcome=AttackOutcome(atmy)
		if outcome == 1:
			stats.rage+= 22 # what rage regained on dodge?
		elif outcome == 3: # crit
			dmg = np.floor(stats.AP*0.45*ArmorReduction()*stats.damageinc*basestats.CritDamageBonus)+8*basestats.giftofarthas
			# print(dmg)
			totaldamage+= dmg
			FlurryProc()
			Nightfall()
			CrusaderMH()
			HandOfJustice()
		elif outcome == 4: # hit
			dmg = np.floor(stats.AP*0.45*ArmorReduction()*stats.damageinc)+8*basestats.giftofarthas
			# print(dmg)
			totaldamage+= dmg
			Nightfall()
			CrusaderMH()
			HandOfJustice()
		UpdateGlobalCd()
	def Whirlwind():
		global stats,mobstats,buffs,totaldamage,abilitycooldown,duration,atmy,cooldowntime
		abilitycooldown.whirlwind = 10
		stats.rage += -25
		abilitycooldown.gcd = cooldowntime.gcd
		dmg = 0
		for i in range(basestats.nenemies):
			outcome=AttackOutcome(atmy)
			if outcome == 3: # crit:
				dmg += np.floor(np.random.uniform(basestats.weaponmindamageMH,basestats.weaponmaxdamageMH)+stats.AP*basestats.normalizedspeed/14.0)*ArmorReduction()*basestats.CritDamageBonus+8*basestats.giftofarthas
				FlurryProc()
				CrusaderMH()
				HandOfJustice()
				if i==0:
					Nightfall()
			elif outcome == 4:
				dmg += np.floor(np.random.uniform(basestats.weaponmindamageMH,basestats.weaponmaxdamageMH)+stats.AP*basestats.normalizedspeed/14.0)*ArmorReduction()+8*basestats.giftofarthas
				CrusaderMH()
				HandOfJustice()
				if i==0:
					Nightfall()
			totaldamage += dmg
			# print(dmg)
		UpdateGlobalCd()
	def Execute():
		global stats,mobstats,buffs,totaldamage,abilitycooldown,duration,atmy,cooldowntime
		abilitycooldown.gcd = cooldowntime.gcd
		rageused = stats.rage-basestats.ExecuteAbilityCost
		stats.rage = 0
		outcome=AttackOutcome(atmy)
		if outcome == 1: # Dodge
			stats.rage = np.floor(10*0.84+rageused)
		# elif outcome == 2: # Miss, nothing happens
			# stats.rage
		elif outcome == 3: # crit
			dmg = np.floor((600+rageused*15)*ArmorReduction()*basestats.CritDamageBonus)+8*basestats.giftofarthas
			# print(dmg)
			totaldamage += dmg
			FlurryProc()
			CrusaderMH()
			HandOfJustice()
			Nightfall()
		elif outcome == 4:
			dmg = np.floor((600+rageused*15)*ArmorReduction())+8*basestats.giftofarthas
			# print(dmg)
			totaldamage += dmg
			CrusaderMH()
			HandOfJustice()
			Nightfall()
		UpdateGlobalCd()
	def Hamstring():
		global stats,mobstats,buffs,totaldamage,abilitycooldown,duration,atmy,cooldowntime
		abilitycooldown.gcd = cooldowntime.gcd
		abilitycooldown.hamstring = cooldowntime.gcd
		stats.rage += -10
		outcome=AttackOutcome(atmy)
		if outcome == 1:
			stats.rage += 7
		elif outcome == 3:
			dmg = np.floor(45*ArmorReduction()*basestats.CritDamageBonus)+8*basestats.giftofarthas
			# print(dmg)
			totaldamage += dmg
			FlurryProc()
			CrusaderMH()
			HandOfJustice()
			Nightfall()
		elif outcome == 4:
			dmg = np.floor(45*ArmorReduction())+8*basestats.giftofarthas
			# print(dmg)
			totaldamage += dmg
			CrusaderMH()
			HandOfJustice()
			Nightfall()
		UpdateGlobalCd()
	def Deathwish():
		global buffs,duration,abilitycooldown,cooldowntime,buffduration,stats,cooldowntime
		stats.rage += -10
		abilitycooldown.deathwish = cooldowntime.deathwish
		abilitycooldown.gcd = cooldowntime.gcd
		buffs.deathwish = 1
		duration.deathwish = buffduration.deathwish
		UpdateDamage()
		UpdateGlobalCd()
	def Reckless():
		global buffs,duration,abilitycooldown,cooldowntime,buffduration
		abilitycooldown.reckless = cooldowntime.reckless
		abilitycooldown.gcd = cooldowntime.gcd
		buffs.reckless = 1
		duration.reckless = buffduration.reckless
		UpdateCrit()
		UpdateGlobalCd()
	def RagePot():
		global buffs,duration,abilitycooldown,stats
		stats.rage = np.min([stats.rage+np.round(np.random.uniform()*30)+45,100])
		abilitycooldown.ragepot = cooldowntime.ragepot
		buffs.ragepot = 1
		duration.ragepot = buffduration.ragepot
		UpdateAP()
	def Bloodrage():
		global buffs,abilitycooldown,cooldowntime,stats
		stats.rage = np.min([stats.rage+10,100])
		abilitycooldown.bloodrage = cooldowntime.bloodrage
		buffs.bloodrage = 10
		abilitycooldown.bloodragetic = cooldowntime.bloodragetic # reset cooldown to 1 sec before next tic
	def Bloodragetic():
		global buffs,abilitycooldown,cooldowntime,stats
		abilitycooldown.bloodragetic = cooldowntime.bloodragetic # reset cooldown to 1 sec before next tic
		buffs.bloodrage += -1 # Consume a bloodrage tic
		stats.rage = np.min([stats.rage+1,100])
	def AngerManagement():
		global abilitycooldown,cooldowntime,stats
		abilitycooldown.angermanagement = cooldowntime.angermanagement # reset cooldown to 1 sec before next tic
		stats.rage = np.min([stats.rage+1,100])
	def JujuFlurry():
		global buffs,duration,abilitycooldown,cooldowntime,buffduration
		abilitycooldown.jujuflurry = cooldowntime.jujuflurry
		buffs.jujuflurry = 1
		duration.jujuflurry = buffduration.jujuflurry
		UpdateAttackSpeed()
	def Sapper():
		global abilitycooldown,basestats,totaldamage,cooldowntime
		abilitycooldown.sapper = cooldowntime.sapper
		damage=np.random.uniform(450,751,basestats.nenemies)
		# print(np.sum(damage))
		totaldamage += np.sum(damage)
	def KissOfTheSpider():
		global buffs,abilitycooldown,cooldowntime, buffduration
		abilitycooldown.kissofthespider = cooldowntime.kissofthespider
		abilitycooldown.slayerscrest = np.max([abilitycooldown.slayerscrest,buffduration.kissofthespider])
		abilitycooldown.jomgabbar = np.max([abilitycooldown.jomgabbar,buffduration.kissofthespider])
		buffs.kissofthespider = 1
		duration.kissofthespider = buffduration.kissofthespider
		UpdateAttackSpeed()
	def SlayersCrest():
		global buffs,abilitycooldown,cooldowntime, buffduration
		abilitycooldown.slayerscrest = cooldowntime.slayerscrest
		abilitycooldown.kissofthespider = np.max([abilitycooldown.kissofthespider,buffduration.slayerscrest])
		buffs.slayerscrest = 1
		duration.slayerscrest = buffduration.slayerscrest
		UpdateAP()
	def JomGabbar():
		global buffs,abilitycooldown,cooldowntime,buffduration
		abilitycooldown.jomgabbar = cooldowntime.jomgabbar
		abilitycooldown.slayerscrest = np.max([abilitycooldown.slayerscrest,buffduration.jomgabbar])
		abilitycooldown.kissofthespider = np.max([abilitycooldown.kissofthespider,buffduration.jomgabbar])
		buffs.jomgabbar = 1
		abilitycooldown.jomgabbartic = cooldowntime.jomgabbartic # reset cooldown to 1 sec before next tic
		UpdateAP()
	def JomGabbarTic():
		global buffs,abilitycooldown,cooldowntime
		abilitycooldown.jomgabbartic = cooldowntime.jomgabbartic # reset cooldown to 2 sec before next tic
		if buffs.jomgabbar < 10:
			buffs.jomgabbar += 1 # Consume a jomgabbar tic
		else:
			buffs.jomgabbar = 0 # End jomgabbar
		UpdateAP()
	# Core attacks #
	def MainAttack():
		global stats,AIsettings
		FlurryConsume()
		if stats.rage >= 25 and basestats.nenemies>=2 and basestats.cleave:
			Cleave()
			# print('Used Cleave')
		elif stats.rage >= AIsettings.heroicstrikeragelimit and basestats.nenemies == 1 and basestats.heroicstrike:
			HeroicStrike()
			# print('Used Heroic Strike')
		else:
			MHauto()
			# print('Used MH Auto Attack')
	def MHauto():
		global totaldamage,abilitycooldown,stats
		abilitycooldown.automain = stats.weaponspeedMH # reset swing timer
		outcome=AttackOutcome(atmw)
		#if outcome == 0: # miss, nothing happens
		#elif outcome == 1: # dodge, nothing happens
		if outcome == 2: # glance
			dmg = np.floor(AttackDamage(0)*ArmorReduction()*stats.damageinc*GlanceFactor(0))+8*basestats.giftofarthas
			# print(dmg)
			totaldamage+=dmg
			stats.rage=np.min([stats.rage+RageFromAttack(dmg),100])
			CrusaderMH()
			UnbridledWrath()
			Nightfall()
		elif outcome == 3: # crit
			dmg = np.floor(AttackDamage(0)*ArmorReduction()*stats.damageinc*basestats.CritDamageBonus)+8*basestats.giftofarthas
			# print(dmg)
			totaldamage+=dmg
			stats.rage=np.min([stats.rage+RageFromAttack(dmg),100])
			FlurryProc()
			CrusaderMH()
			UnbridledWrath()
			Nightfall()
		elif outcome == 4: # hit
			dmg = np.floor(AttackDamage(0)*ArmorReduction()*stats.damageinc)+8*basestats.giftofarthas
			# print(dmg)
			totaldamage+=dmg
			stats.rage=np.min([stats.rage+RageFromAttack(dmg),100])
			CrusaderMH()
			UnbridledWrath()
			Nightfall()
	def OHauto():
		global totaldamage,abilitycooldown,stats,basestats
		abilitycooldown.autooff = stats.weaponspeedOH # reset swing timer
		FlurryConsume()
		outcome=AttackOutcome(atow)
		#if outcome == 0: # miss, nothing happens
		#elif outcome == 1: # dodge, nothing happens
		if outcome == 2: # glance
			dmg = np.floor(AttackDamage(1)*ArmorReduction()*stats.damageinc*GlanceFactor(1))+8*basestats.giftofarthas
			# print(dmg)
			totaldamage+=dmg
			stats.rage=np.min([stats.rage+RageFromAttack(dmg),100])
			CrusaderOH()
			UnbridledWrath()
		elif outcome == 3: # crit
			dmg = np.floor(AttackDamage(1)*ArmorReduction()*stats.damageinc*basestats.CritDamageBonus)+8*basestats.giftofarthas
			# print(dmg)
			totaldamage+=dmg
			stats.rage=np.min([stats.rage+RageFromAttack(dmg),100])
			FlurryProc()
			CrusaderOH()
			UnbridledWrath()
		elif outcome == 4: # hit
			dmg = np.floor(AttackDamage(1)*ArmorReduction()*stats.damageinc)+8*basestats.giftofarthas
			# print(dmg)
			totaldamage+=dmg
			stats.rage=np.min([stats.rage+RageFromAttack(dmg),100])
			CrusaderOH()
			UnbridledWrath()
	def HeroicStrike():
		global totaldamage,abilitycooldown,stats,basestats
		abilitycooldown.automain = stats.weaponspeedMH # reset swing timer
		stats.rage+=-basestats.HeroicStrikeAbilityCost
		outcome=AttackOutcome(atmy)
		#if outcome == 0: # miss, nothing happens
		if outcome == 1: # dodge, regain some rage
			stats.rage+=np.floor(basestats.HeroicStrikeAbilityCost*0.75)
		#if outcome == 2: # glance, not possible
		elif outcome == 3: # crit
			dmg = np.floor((AttackDamage(0)+157)*ArmorReduction()*stats.damageinc*basestats.CritDamageBonus)+8*basestats.giftofarthas
			# print(dmg)
			totaldamage+=dmg
			FlurryProc()
			CrusaderMH()
			UnbridledWrath()
			Nightfall()
		elif outcome == 4: # hit
			dmg = np.floor((AttackDamage(0)+157)*ArmorReduction()*stats.damageinc)+8*basestats.giftofarthas
			# print(dmg)
			totaldamage+=dmg
			CrusaderMH()
			UnbridledWrath()
			Nightfall()
	def Cleave():
		global totaldamage,abilitycooldown,stats,basestats
		abilitycooldown.automain = stats.weaponspeedMH # reset swing timer
		stats.rage += -20
		# First target:
		for i in range(np.min([2,basestats.nenemies])):
			outcome=AttackOutcome(atmy)
			#if outcome == 0: # miss, nothing happens
			if outcome == 1 and i==0: # dodge on primary target, refund rage
				stats.rage += 15
			#if outcome == 2: # glance, not possible
			elif outcome == 3: # crit
				dmg = np.floor((AttackDamage(0)+32*(1+0.4*basestats.impcleave))*ArmorReduction()*stats.damageinc*basestats.CritDamageBonus)+8*basestats.giftofarthas
				# print(dmg)
				totaldamage+=dmg
				FlurryProc()
				CrusaderMH()
				UnbridledWrath()
				if i == 0:
					Nightfall()
			elif outcome == 4: # hit
				dmg = np.floor((AttackDamage(0)+32*(1+0.4*basestats.impcleave))*ArmorReduction()*stats.damageinc)+8*basestats.giftofarthas
				# print(dmg)
				totaldamage+=dmg
				CrusaderMH()
				UnbridledWrath()
				if i == 0:
					Nightfall()
	## Core functionality ##
	def GeneratePriorityList(): # Opimize plz
		global basestats
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
	def SecondarySort(inlist):
		global prioritylist
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
	def FindNextEvent(): # Convert into AI optimization procedure?
		global abilitycooldown, buffduration, stats, buffs, fightduration,executeduration,totalduration,cooldowntime,basestats,AIsettings
		sortedlist = sorted([(k,v) for k,v in abilitycooldown.__dict__.items()], key=lambda tup: tup[1])	
		sortedlist=SecondarySort(sortedlist) # Sort according to prio list for identical times
		RemainingTime = fightduration-totalduration
		for i in sortedlist:
			# All conditions are: If the ability is the next available of all events, AND conditions are met:
			if i[0] == 'angermanagement' and basestats.angermanagement == 1:
				return i[0],i[1]

			elif i[0] == 'jomgabbartic':
				if buffs.jomgabbar != 0:
					return i[0],i[1]

			elif i[0] == 'bloodragetic':
				if buffs.bloodrage >= 1: # tics are available
					return i[0],i[1]

			elif i[0] == 'sapper' and basestats.sapper == 1:
				if basestats.sapper:
					return i[0],i[1]

			elif i[0] == 'kissofthespider' and basestats.kissofthespider == 1:
				if RemainingTime >= cooldowntime.kissofthespider+buffduration.kissofthespider: # Cooldown can refresh allowing for an extra pop
					return i[0],i[1] # Time to the event and which event should be used
				elif RemainingTime<=buffduration.kissofthespider: # Fight duration is less than uptime
					return i[0],i[1] # Time to the event and which event should be used

			elif i[0] == 'slayerscrest' and basestats.slayerscrest == 1:
				if basestats.kissofthespider == 1: 
					if RemainingTime <= buffduration.kissofthespider+buffduration.slayerscrest:
						# If fight duration is shorter than both trinkets AND KotS , pop Slayers
						return i[0],i[1]
					elif RemainingTime >= buffduration.kissofthespider+cooldowntime.slayerscrest: # Cooldown can refresh allowing for an extra pop
						return i[0],i[1]
					elif abilitycooldown.kissofthespider >= RemainingTime-buffduration.slayerscrest: # KotS will not be ready for use
						return i[0],i[1]
				else: # No other trinkets to take into account
					if RemainingTime >= cooldowntime.slayerscrest+buffduration.slayerscrest: # Cooldown can refresh allowing for an extra pop
						return i[0],i[1] # Time to the event and which event should be used
					elif RemainingTime<=buffduration.slayerscrest: # Fight duration is less than uptime
						return i[0],i[1] # Time to the event and which event should be used	

			elif i[0] == 'jomgabbar' and basestats.jomgabbar == 1:
				if basestats.kissofthespider == 1 or basestats.slayerscrest == 1:
					if basestats.kissofthespider == 1: 
						if RemainingTime <= buffduration.kissofthespider+buffduration.jomgabbar:
							# If fight duration is shorter than both trinkets AND KotS, pop jomgabbar
							return i[0],i[1]
						elif RemainingTime >= buffduration.kissofthespider+cooldowntime.jomgabbar: # Cooldown can refresh allowing for an extra pop
							return i[0],i[1]
						elif abilitycooldown.kissofthespider >= RemainingTime-buffduration.jomgabbar: # KotS will not be ready for use
							return i[0],i[1]
					elif basestats.slayerscrest == 1:
						if RemainingTime <= buffduration.slayerscrest+buffduration.jomgabbar:
							# If fight duration is shorter than both trinkets AND KotS, pop jomgabbar
							return i[0],i[1]
						elif RemainingTime >= buffduration.slayerscrest+cooldowntime.jomgabbar: # Cooldown can refresh allowing for an extra pop
							return i[0],i[1]
						elif abilitycooldown.slayerscrest >= RemainingTime-buffduration.jomgabbar: # KotS will not be ready for use
							return i[0],i[1]
				else: # No other trinkets to take into account
					if RemainingTime >= cooldowntime.jomgabbar+buffduration.jomgabbar: # Cooldown can refresh allowing for an extra pop
						return i[0],i[1] # Time to the event and which event should be used
					elif RemainingTime<=buffduration.jomgabbar: # Fight duration is less than uptime
						return i[0],i[1] # Time to the event and which event should be used	
				

			elif i[0] == 'ragepot' and basestats.ragepot == 1:
				# Conditions for ragepot
				if RemainingTime >= cooldowntime.ragepot+buffduration.ragepot: # Cooldown can refresh allowing for an extra pop
					return i[0],i[1] # Time to the event and which event should be used
				elif RemainingTime<=buffduration.ragepot: # Fight duration is less than uptime
					return i[0],i[1] # Time to the event and which event should be used

			elif i[0] == 'jujuflurry' and basestats.jujuflurry == 1:
				# Conditions for jujuflurry
				if RemainingTime >= cooldowntime.jujuflurry+buffduration.jujuflurry: # Cooldown can refresh allowing for an extra pop
					return i[0],i[1] # Time to the event and which event should be used
				elif RemainingTime<=buffduration.jujuflurry: # Fight duration is less than uptime
					return i[0],i[1] # Time to the event and which event should be used
			
			elif i[0] == 'bloodrage':
				if stats.rage <= 20: # Cooldown can refresh allowing for an extra pop
					return i[0],i[1] # Time to the event and which event should be used

			elif i[0] == 'reckless':
				if RemainingTime >= cooldowntime.reckless+buffduration.reckless: # Cooldown can refresh allowing for an extra pop
					return i[0],i[1] # Time to the event and which event should be used
				elif RemainingTime<=buffduration.reckless: # Fight duration is less than uptime
					return i[0],i[1] # Time to the event and which event should be used

			elif i[0] == 'deathwish':
				if RemainingTime >= cooldowntime.deathwish+buffduration.deathwish and stats.rage >= 10: # Cooldown can refresh allowing for an extra pop
					return i[0],i[1] # Time to the event and which event should be used
				elif RemainingTime<=buffduration.deathwish and stats.rage >= 10: # Fight duration is less than uptime
					return i[0],i[1] # Time to the event and which event should be used

			elif i[0] == 'bloodthirst':
				if stats.rage >= 30:
					return i[0],i[1]
			elif i[0] == 'execute':
				if stats.rage >= basestats.ExecuteAbilityCost and RemainingTime<=executeduration:
					return i[0],i[1]

			elif i[0] == 'whirlwind':
				if stats.rage >= 25:
					return i[0],i[1]

			elif i[0] == 'hamstring':
				bloodthirstcheck = 0
				whirlwindcheck = 0
				if stats.rage >= AIsettings.hamstringragelimitprimary: # Condition 1 for using Hamstring
					if basestats.bloodthirst:
						if abilitycooldown.bloodthirst>=cooldowntime.gcd+i[1]: # Check for overlap with Bloodthirst
							bloodthirstcheck = 1
					else:
						bloodthirstcheck = 1
					if basestats.whirlwind: 
						if abilitycooldown.whirlwind>=cooldowntime.gcd+i[1]: # 
							whirlwindcheck = 1
					else:
						whirlwindcheck = 1
					if bloodthirstcheck and whirlwindcheck:
						return i[0],i[1]
				elif stats.rage >= AIsettings.hamstringragelimitsecondary and buffs.crusaderMH == 0:
					if basestats.bloodthirst:
						if abilitycooldown.bloodthirst>=cooldowntime.gcd+i[1]: # Check for overlap with Bloodthirst
							bloodthirstcheck = 1
					else:
						bloodthirstcheck = 1
					if basestats.whirlwind: 
						if abilitycooldown.whirlwind>=cooldowntime.gcd+i[1]: # 
							whirlwindcheck = 1
					else:
						whirlwindcheck = 1
					if bloodthirstcheck and whirlwindcheck:
						return i[0],i[1]

			elif i[0] == 'automain':
				return i[0],i[1]

			elif i[0] == 'autooff':
				return i[0],i[1]
	def PerformEvent(event): # Convert into class based calls
		global atmy
		if event == 'angermanagement':
			AngerManagement()
			# print('Used AngerManagement')
		elif event == 'sapper':
			Sapper()
			# print('Used Sapper Charge')
		elif event == 'jomgabbar':
			JomGabbar()
			# print('Used Jom Gabbar')
		elif event == 'jomgabbartic':
			JomGabbarTic()
			# print('Used Jom Gabbar Tic')
		elif event == 'bloodragetic':
			Bloodragetic()
			# print('Used bloodragetic')
		elif event == 'slayerscrest':
			SlayersCrest()
			# print('Used Slayers Crest')
		elif event == 'kissofthespider':
			KissOfTheSpider()
			# print('Used KotS')
		elif event == 'ragepot':
			RagePot()
			# print('Used RagePot')
		elif event == 'jujuflurry':
			JujuFlurry()
			# print('Used jujuflurry')
		elif event == 'reckless':
			Reckless()
			# print('Used reckless')
		elif event == 'deathwish':
			Deathwish()
			# print('Used deathwish')
		elif event == 'bloodrage':
			Bloodrage()
			# print('Used bloodrage')
		elif event == 'bloodthirst':
			Bloodthirst()
			# print('Used bloodthirst')
		elif event == 'execute':
			Execute()
			# print('Used Execute')
		elif event == 'whirlwind':
			Whirlwind()
			# print('Used whirlwind')
		elif event == 'hamstring':
			Hamstring()
			# print('Used hamstring')
		elif event == 'automain':
			MainAttack()
			# print("Used automain")
		elif event == 'autooff':
			OHauto()
			# print('Used autooff')
	## Update stats ##
	def UpdateAttackSpeed():
		global buffs,stats,basestats,basestats,abilitycooldown,buffeffect,AttackSpeedBuffs
		attackspeedfactor = basestats.attackspeedfactor
		for i in range(len(AttackSpeedBuffs)):
			if getattr(buffs,AttackSpeedBuffs[i]) == 1:
				attackspeedfactor = attackspeedfactor * getattr(buffeffect,AttackSpeedBuffs[i])
		stats.weaponspeedMH=basestats.weaponspeedMH/attackspeedfactor
		stats.weaponspeedOH=basestats.weaponspeedOH/attackspeedfactor
		if abilitycooldown.automain>stats.weaponspeedMH:
			abilitycooldown.automain = stats.weaponspeedMH
		if abilitycooldown.autooff>stats.weaponspeedOH:
			abilitycooldown.autooff = stats.weaponspeedOH
	def UpdateAP():
		global buffs,stats,basestats,APBuffs,StrBuffs,buffeffect
		strbonus = 0
		APbonus = 0
		for i in range(len(StrBuffs)):
			if getattr(buffs,StrBuffs[i]) == 1:
				strbonus += getattr(buffeffect,StrBuffs[i])
		for i in range(len(APBuffs)):
			if getattr(buffs,APBuffs[i]) == 1:
				APbonus += getattr(buffeffect,APBuffs[i])
		if buffs.jomgabbar != 0:
			APbonus += 20*buffs.jomgabbar
		stats.AP = np.floor(basestats.AP+(basestats.strength+strbonus)*2*basestats.statmultiplier+APbonus)
	def UpdateCrit():
		global buffs,stats,CritBuffs
		critbonus = 0
		for i in range(len(CritBuffs)):
			if getattr(buffs,CritBuffs[i]) == 1:
				critbonus += getattr(buffeffect,CritBuffs[i])
		stats.critMH = basestats.critMH+critbonus
		stats.critOH = basestats.critOH+critbonus
		UpdateAttackTable()
	def UpdateDamage():
		global stats,buffs, basestats,DamageFactorBuffs
		damagefactor = basestats.damageinc
		for i in range(len(DamageFactorBuffs)):
			if getattr(buffs,DamageFactorBuffs[i]) == 1:
				damagefactor = damagefactor * getattr(buffeffect,DamageFactorBuffs[i])
		stats.damageinc = damagefactor
	def UpdateBuffs(timestep):
		global duration,buffs,AttackSpeedBuffs,DamageFactorBuffs,APBuffs,StrBuffs
		for i in range(len(AttackSpeedBuffs)):
			if getattr(duration,AttackSpeedBuffs[i]) <= timestep:
				setattr(buffs,AttackSpeedBuffs[i],0)
				setattr(duration,AttackSpeedBuffs[i],0)
				UpdateAttackSpeed()
			else:
				setattr(duration,AttackSpeedBuffs[i],getattr(duration,AttackSpeedBuffs[i])-timestep)
		for i in range(len(DamageFactorBuffs)):
			if getattr(duration,DamageFactorBuffs[i]) <= timestep:
				setattr(buffs,DamageFactorBuffs[i],0)
				setattr(duration,DamageFactorBuffs[i],0)
				UpdateDamage()
			else:
				setattr(duration,DamageFactorBuffs[i],getattr(duration,DamageFactorBuffs[i])-timestep)
		for i in range(len(APBuffs)):
			if getattr(duration,APBuffs[i]) <= timestep:
				setattr(buffs,APBuffs[i],0)
				setattr(duration,APBuffs[i],0)
				UpdateAP()
			else:
				setattr(duration,APBuffs[i],getattr(duration,APBuffs[i])-timestep)
		for i in range(len(StrBuffs)):
			if getattr(duration,StrBuffs[i]) <= timestep:
				setattr(buffs,StrBuffs[i],0)
				setattr(duration,StrBuffs[i],0)
				UpdateAP()
			else:
				setattr(duration,StrBuffs[i],getattr(duration,StrBuffs[i])-timestep)
	def UpdateGlobalCd():
		global abilitycooldown,gcdlist
		for i in range(len(gcdlist)):
			if getattr(abilitycooldown,gcdlist[i]) < abilitycooldown.gcd:
				setattr(abilitycooldown,gcdlist[i],abilitycooldown.gcd)
	def UpdateCd(timestep):
		global abilitycooldown
		names = [x.name for x in fields(abilitycooldown)]
		for i in range(len(names)):
			if getattr(abilitycooldown,names[i]) <= timestep:
				setattr(abilitycooldown,names[i],0)
			else:
				setattr(abilitycooldown,names[i],getattr(abilitycooldown,names[i])-timestep)
	def UpdateAttackTable():
		global atmy,atmw,atow,stats,basestats,mobstats
		MHSkillDiff = basestats.cappedskillMH-mobstats.defence
		OHSkillDiff = basestats.cappedskillOH-mobstats.defence
		if basestats.cappedskillMH-mobstats.defence < 0:
			atmy.crit = np.min([1,np.max([stats.critMH+MHSkillDiff*0.002+atmy.glance,atmy.glance])])
			atmw.crit = np.min([1,np.max([stats.critMH+MHSkillDiff*0.002+atmw.glance,atmw.glance])])
		else:
			atmy.crit = np.min([1,np.max([stats.critMH+MHSkillDiff*0.0004+atmy.glance,atmy.glance])])
			atmw.crit = np.min([1,np.max([stats.critMH+MHSkillDiff*0.0004+atmw.glance,atmw.glance])])
		if basestats.cappedskillOH-mobstats.defence < 0:
			atow.crit = np.min([1,np.max([stats.critOH+OHSkillDiff*0.002+atow.glance,atow.glance])])
		else:
			atow.crit = np.min([1,np.max([stats.critOH+OHSkillDiff*0.0004+atow.glance,atow.glance])])
	# Primary simulation

	dpslist=[]
	dpssigma=[]
	gcdlist = ["bloodthirst","whirlwind","deathwish","reckless","hamstring","execute"]
	AttackSpeedBuffs = ['kissofthespider','jujuflurry','flurry']
	DamageFactorBuffs = ['enrage','deathwish']
	APBuffs = ['slayerscrest']
	StrBuffs = ['crusaderMH','crusaderOH','ragepot']
	CritBuffs = ['reckless']
	AIsettings = AISettingsClass()
	count=0
	if scanaxis == "none":
		sweeprange = [0]
	start = time.time()
	for scansetting in sweeprange:
		if scanaxis != "none":
			# print("Setting %0.2f, from %0.2f to %0.2f." %(scansetting,sweeprange[0],sweeprange[-1]))
			count+=1
			progressval=float(count-1)/len(sweeprange)*100
			if count!=1:
				Stepsleft = (len(sweeprange)-count+1)
				Stepstaken = count-1
				TimeSpent = time.time()-start
				TimeRemaining = int(round(float(Stepsleft)/Stepstaken*TimeSpent,0))
				val_progresstext.set('ETA: '+str(TimeRemaining)+' s')
			val_progressbar.set(progressval)
			root.update_idletasks()
		damagelist=[]
		if Nightfall == 1:
			NightfallTime = []
		for rep in range(Nreps):
			if scanaxis == "none":
				if rep!=0:
					Stepsleft = (Nreps-rep-1)
					Stepstaken = rep+1
					TimeSpent = time.time()-start
					TimeRemaining = int(round(float(Stepsleft)/Stepstaken*TimeSpent,0))
					val_progresstext.set('ETA: '+str(TimeRemaining)+' s')
				progressval=float(rep+1)/Nreps*100
			else:
				progressval+=1.0/Nreps*100/len(sweeprange)
			val_progressbar.set(progressval)
			root.update_idletasks()
			# Initialize
			mobstats = MobStatsClass()
			abilitycooldown = AbilityCooldownClass()
			procrate = ProcRateClass()
			basestats = BaseStatsClass()
			prioritylist = GeneratePriorityList()
			buffeffect = BuffEffectClass()

			if scanaxis == "hit":
				basestats.hit = scansetting
			elif scanaxis == "AP":
				basestats.AP = scansetting + 222*BoM + 40*JujuMight + Dragonslayer*140 + Battleshout*290 + DMT*200 + 100*Trueshot
			elif scanaxis == "crit":
				basestats.critMH: float = scansetting + 0.03*ZerkerStance + 0.02*Mongoose + 0.05*Dragonslayer + 0.05*Songflower + 0.03*PackLeader + 0.01*Cruelty + ((agility + 25*Mongoose + 15*Songflower+16*MotW)*(1+0.1*Kings)*(1+0.15*Zandalar))*1.0/2000 + 0.02*MHCritStone
				basestats.critOH: float = scansetting + 0.03*ZerkerStance + 0.02*Mongoose + 0.05*Dragonslayer + 0.05*Songflower + 0.03*PackLeader + 0.01*Cruelty + ((agility + 25*Mongoose + 15*Songflower+16*MotW)*(1+0.1*Kings)*(1+0.15*Zandalar))*1.0/2000
			elif scanaxis == "heroic":
				AIsettings.heroicstrikeragelimit = scansetting
			elif scanaxis != "none":
				exit()
				
			buffs = BuffsClass()
			stats = ActiveStatsClass()
			atmy,atmw,atow = GenerateAttackTable()
			
			
			UpdateAttackSpeed()
			UpdateDamage()
			UpdateCrit()
			UpdateAP()
			duration = BuffDurationClass()
			cooldowntime = CooldownDurationBaseClass()
			buffduration = BuffDurationBaseClass()
			totalduration = 0.0
			totaldamage = 0.0

			if basestats.nightfall:
				NightfallDowntime = 0
				NightfallUptime = 0
			# Primary time loop
			while totalduration<=fightduration:
				event,t=FindNextEvent() # Identify which event is next according to cooldown time and prio.
				if basestats.nightfall:
					if buffs.nightfall == 1:
						NightfallUptime += t
					else:
						NightfallDowntime += t
				UpdateBuffs(t)
				UpdateCd(t)
				PerformEvent(event)
				totalduration+=t
				# print("Total Duration spent: %3.1f" %totalduration)
				# print(abilitycooldown)
				# print(buffs)
				# print(stats)
				# # print(atmy,atmw,atow)
				# input('Continue \n')
			if basestats.nightfall:
				NightfallTime.append(NightfallUptime/(NightfallUptime+NightfallDowntime))
			damagelist.append(totaldamage)
		# print("Time taken to simulate: %3.1f" %(time.time()-start))
		dpslist.append(np.mean(damagelist)/fightduration)
		dpssigma.append(np.std(damagelist)/(fightduration*Nreps**0.5))
		if scanaxis == "none":
			# print("Average DPS is:")
			DPSAvg=np.mean(damagelist)/fightduration
			DPGAvgSig=np.std(damagelist)/(fightduration*(Nreps-1)**0.5)
			# print("%.2f pm %.2f" %(DPSAvg,DPGAvgSig))
			if Nightfall == 1:
				# print("Average Nightfall Uptime:")
				NightfallTimeAvg=np.mean(NightfallTime)*100.0
				NightfallTimeAvgSig=np.std(NightfallTime)*100.0
				# print("%2.2f pm %2.2f" %(NightfallTimeAvg,NightfallTimeAvgSig))
				with open('NightfallUptime.txt', 'w+') as f:
					np.savetxt(f,np.array(NightfallTime))
				plt.hist(NightfallTime,bins = 20, range=(0,1))
				plt.xlabel('Nightfall Uptime [%]')
				plt.ylabel('N times simulated')
				plt.title('Average Nightfall Uptime: %2.1f +- %2.1f' %(NightfallTimeAvg,NightfallTimeAvgSig))
				plt.show()
			plt.hist([i*1.0/fightduration for i in damagelist])
			plt.xlabel('DPS')
			plt.ylabel('N times simulated')
			plt.title('Average DPS: %2.1f +- %2.1f' %(DPSAvg,DPGAvgSig))
			plt.show()
	if scanaxis != 'none':
		plt.errorbar(sweeprange,dpslist,dpssigma)
		if scanaxis == "hit":
			plt.xlabel('Hit Chance')
			filename = "HitSweep.txt"
		elif scanaxis == "crit":
			plt.xlabel('Crit Chance')
			filename = "CritSweep.txt"
		elif scanaxis == "AP":
			plt.xlabel('Attack Power')
			filename = "APSweep.txt"
		elif scanaxis == "heroic":
			plt.xlabel('Heroic strike used at rage')
			filename = "HeroicStrikeSweep.txt"
		with open(filename, 'w+') as f:
			np.savetxt(f,np.matrix([sweeprange,dpslist,dpssigma]))
		plt.ylabel('DPS')
		plt.show()
button_Run = Button(frame,text="Run Simulation", width=18, command=RunSimulation).grid(row=0,column=4)

val_progressbar=DoubleVar()
val_progressbar.set(0)
progressbar = Progressbar(frame, orient = HORIZONTAL, length = 100, mode = 'determinate',variable=val_progressbar).grid(row=0,column=5)
val_progresstext=StringVar()
val_progresstext.set("ETA:")
label_progresstext = Label(frame,textvar=val_progresstext).grid(row=1,column=5)

mainloop()

