# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 14:33:10 2023

@author: parke
"""
'''
Preface: I personally collected all of the data used and processed here over the past 2 years.
The data I collected pertains to the Video Games Pokemon Brilliant Diamond, and Pokemon Shining Pearl, for the Nintendo Switch.
Since the aspect of the game I was investigating changed daily, I could only collect one data point per day individually (I totalled about 200 data points on my own)
I essentially lived the life of a door-to-door salesman, asking for data entries for my research from those who played the game.
Many were sympathetic to my cause, and many provided me continuous daily data points to aid my progress, matching my own contribution.
I did this on various platforms, such as Discord, Twitch, Youtube, and more. 
This is a sample data entry I received, from a user capable of providing me easily sharable video: https://imgur.com/a/qHBZi6O
The initial reference point for my data is the following spreadsheet, to which I and a collaborator on the project have edit access to: https://docs.google.com/spreadsheets/d/1qgRaKukh3i_j0lX1pFv5i5wUeeg3AO5NaUwDRtPlWno/edit?usp=sharing
After I acquired enough data points, I began attempting to reverse the source random value behind all of these linked elements.
Dataminers were able to assist me in some aspects, but were unable to glean all of the answers from Ghidra, an English-Japanese Translator, and a dump of the game.
They were able to extract indexed lists of purchasable items, and I was able to empirically derive a formula for each purchasable item over time. 
However, The items are shuffled in a deterministic way before the indexes are used. 
I later determined that a rogue Unity Heap Sort for pre-sorted indices within the game code is responsible for this entire two year journey.
Now to see if I can get more mileage out of this data...
'''
# I could not use .csv, as some of my data contains commas, pipes, and whitespace. I used google sheets formulas to join my cells with  ~~ . 
import matplotlib.pyplot as plt
import numpy as np
file = open("group_seed_data.txt","r",encoding = "UTF-8")
gs_raw_data = file.read()
file.close()
gs_lines = []
gs_lines = gs_raw_data.split("\n")
def split_buyables(input_list_chunk):
    try:
        pedestal, price = input_list_chunk.split(" | ")
        pedestal = pedestal.strip()
        if (pedestal == "?") or (pedestal == "-"):
            pedestal = None
        price = int(price.strip())
        if (price == "?") or (price == "-"):
            price = None
    except:
        price = None
        pedestal = None
    return pedestal, price
def Count_Equal(items, i):
    output = []
    
def Bool_Any(items, bools):
    any_items = []
    for i in range(len(items)):
        if bools[i] != None and type(items[i]) == int:
            any_items.append(items[i])
    return any_items
def Bool_True(items, bools):
    true_items = []
    for i in range(len(items)):
        if bools[i] == True and type(items[i]) == int:
            true_items.append(items[i])
    return true_items
def Bool_False(items, bools):
    false_items = []
    for i in range(len(items)):
        if bools[i] == False and type(items[i]) == int:
            false_items.append(items[i])
    return false_items
class GS_Data:
    def __init__(self,input_string):
        input_list = []
        input_list = input_string.split(" ~~ ")
        # name of the user who contributed the data
        GS_Data.user = input_list[0].strip()
        # If the user goes by a different name on a different platform, include that here. Most don't
        if input_list[1].strip() == "?":    
            GS_Data.alias = None
        else:
            GS_Data.alias = input_list[1].strip()
        # Badges is an index 1-8 for 8 Sinnoh Badges input badges % 10. 0 is a placeholder for unknown.
        # debug_version represents whether the game the data was sourced from is confirmed to be a debug version.
             # True or false flag derived from input badges // 10.
        # the defog tm independently impacts the data. derived from input badges // 20. 
        if input_list[2].strip() == "?":
            GS_Data.badges = 0
            GS_Data.debug_version = False
            GS_Data.obtained_defog_tm = False
        else:
            GS_Data.badges = int(input_list[2].strip()) % 10
            GS_Data.debug_version = bool((int(input_list[2].strip()) // 10) & 1)
            GS_Data.obtained_defog_tm = bool((int(input_list[2].strip()) // 20) & 1)
        # has the player obtained the national dex? true or false, input string Yes, No, or ?.
        if input_list[3].strip() == "Yes":
            GS_Data.natdex = True
        else:
            GS_Data.natdex = False
        # Text describing "evidence" collected. Not super useful, unsure if I ever need this
        GS_Data.evidence = input_list[4].strip()
        # input_list[5] is whether or not to use input_list... would be a waste of space to include
        
        # Either 32 bit or 64 bit hex "Group Seed" value. For emulated data entries, obtaining this was easy using a RAM viewer.
        # For retail entries, this master value needed to be obtained over several days after studying it's impact on the game world.
        # Only the bottom 32 bits are solveable and relevant for most games, but in the debug version, all 64 bits are used and trackable.
        if input_list[6].strip() == "?":
            GS_Data.group_seed = None
        else:
            GS_Data.group_seed = int(input_list[6].strip(),16)
        # Either 31 bit or 64 bit hex "Daily Seed" value. For emulated data entries, obtaining this was easy using a RAM viewer.
        # For retail entries, this master value needed to be obtained over several days after studying it's impact on the game world.
        # Only the bottom 31 bits are solveable and relevant for most games, but in the debug version, all 64 bits are used and trackable.
        # Typically derived from the group seed, takes the absolute value of the group seed as if it were signed.
        if input_list[7].strip() == "?":
            # I have an entry where Group and Daily seeds are exactly 0. Placeholder MUST be None.
            GS_Data.daily_seed = None
        else:
            GS_Data.daily_seed = int(input_list[7].strip(),16)
        # Numerical representation of version number. Useful for validating/generating version dependent info
        if input_list[8].strip() == "?":
            GS_Data.version = 0
            GS_Data.is_lotto_old = None 
            GS_Data.feebas_tile_red = None
        # Lottery number is super important, we knew very early on that it is a direct output of the group seed, NOT the daily seed. 
        # value between 0 and 65535 in older versions, but 0 and 99999 in newer versions (Newer than 1.1.3).
        # As my confidence grew in interpreting the other variables, I stopped asking for lottery numbers. Made people suspicious, and it was a waste of their time
        # Feebas Tile color is unobtainable in games with new lottery numbers. 
        # This tool would be used to do it, however. https://lincoln-lm.github.io/JS-Finder/Tools/BDSPFeebasOld.html
        else:
        # Easier to do it this way than index every possible version number.
            GS_Data.version = int(input_list[8].strip().replace(".",""))
            if int(input_list[8].strip().replace(".","")) < 113:
                GS_Data.is_lotto_old = True
            else:
                GS_Data.is_lotto_old = False
            if int(input_list[8].strip().replace(".","")) < 113:
                if input_list[15].strip() == "?":
                    GS_Data.feebas_tile_red = None
                elif input_list[15].strip() == "Red":
                    GS_Data.feebas_tile_red = True
                else:
                    GS_Data.feebas_tile_red = False
            else:
                GS_Data.feebas_tile_red = None
        # index 0-6. Sunday will be 0, Monday will be 1, etc. 
        weekday_index = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        for i in range(7):
            if weekday_index[i] == input_list[9].strip():
                GS_Data.day_of_week = i
        # The lottery number itself. Again, may or may not be there.
        if input_list[10].strip() == "?":
            # Lotto number 0 is possible, lotto number 100000 isn't. a numerical placeholder that won't break!
            GS_Data.lotto_number = None
        else:
            GS_Data.lotto_number = int(input_list[10].strip())
        # Are the prices of the hiker merchants at their minimum, or maximum? a coin flip from the daily seed.
        if input_list[11].strip() == "?":
            GS_Data.max_price = None
        elif input_list[11].strip() == "Max":
            GS_Data.max_price = True
        else:
            GS_Data.max_price = False
        # The first item the hikers in question have for sale is a "Digger Drill", if the player has unlocked it
        # It can be purchased either for red, blue, or green spheres at random. I will be indexing these in the order the game does, Red = 0, Blue = 1, Green = 2
        if input_list[12].strip() == "?":
            GS_Data.drill_color = 4
        elif input_list[12].strip() == "Red":
            GS_Data.drill_color = 0
        elif input_list[12].strip() == "Blue":
            GS_Data.drill_color = 1            
        else:
            GS_Data.drill_color = 2
        # The second item the hikers in question have for sale is a "Large/Small Sphere"
        # It can be purchased either for red, blue, green, prism, or pale spheres at random. 
        # I will be indexing these in the order the game does, Red = 0, Blue = 1, Green = 2, Prism = 3, Pale = 4
        if input_list[13].strip() == "?":
            GS_Data.sphere_color = 5
        elif input_list[13].strip() == "Red":
            GS_Data.sphere_color = 0
        elif input_list[13].strip() == "Blue":
            GS_Data.sphere_color = 1            
        elif input_list[13].strip() == "Green":
            GS_Data.sphere_color = 2
        elif input_list[13].strip() == "Prism":
            GS_Data.sphere_color = 3
        else:
            GS_Data.sphere_color = 4
        if input_list[14].strip() == "?":
            # Breathe a sigh of relief. I did not keep my swarms column neat...
            GS_Data.swarm_index = None
        else:
            try:
                GS_Data.swarm_index = int(input_list[14].strip())
            except:
                GS_Data.swarm_index = None
                swarm_list = ["Doduo", "Zigzagoon", "Cubone", "Nosepass", "Phanpy", "Dunsparce", "Snubbull", "Absol", "Spoink", "Drowzee", "Delibird", "Swinub", "Voltorb", "Farfetch'd", "Skitty", "Natu", "Makuhita", "Krabby", "Spinda", "Beldum", "Pidgey", "Corsola", "Surskit", "Lickitung", "Smoochum", "Electrike", "Slakoth", "Magnemite"]
                for i in range(len(swarm_list)):
                    if input_list[14].strip() == swarm_list[i]:
                        GS_Data.swarm_index = i
        GS_Data.sp1 = split_buyables(input_list[16])
        GS_Data.sp2 = split_buyables(input_list[17])
        GS_Data.sp3 = split_buyables(input_list[18])
        GS_Data.small_pedestals = [GS_Data.sp1, GS_Data.sp2, GS_Data.sp3]
        GS_Data.st1 = split_buyables(input_list[19])
        GS_Data.st2 = split_buyables(input_list[20])
        GS_Data.st3 = split_buyables(input_list[21])
        GS_Data.st4 = split_buyables(input_list[22])
        GS_Data.st5 = split_buyables(input_list[23])
        GS_Data.small_TMs = [GS_Data.st1, GS_Data.st2, GS_Data.st3, GS_Data.st4, GS_Data.st5]
        GS_Data.lp1 = split_buyables(input_list[24])
        GS_Data.lp2 = split_buyables(input_list[25])
        GS_Data.lp3 = split_buyables(input_list[26])
        GS_Data.lp4 = split_buyables(input_list[27])
        GS_Data.lp5 = split_buyables(input_list[28])
        GS_Data.large_pedestals = [GS_Data.lp1, GS_Data.lp2, GS_Data.lp3, GS_Data.lp4, GS_Data.lp5]
        GS_Data.lt1 = split_buyables(input_list[29])
        GS_Data.lt2 = split_buyables(input_list[30])
        GS_Data.lt3 = split_buyables(input_list[31])
        GS_Data.lt4 = split_buyables(input_list[32])
        GS_Data.lt5 = split_buyables(input_list[33])
        GS_Data.large_TMs = [GS_Data.lt1, GS_Data.lt2, GS_Data.lt3, GS_Data.lt4, GS_Data.lt5]        
datas = []
users = []
aliases = []
badgess = []
daily_seeds = []
days_of_week = []
debug_versions = []
drill_colors = []
evidences = []
feebas_tiles_red = []
group_seeds = []
are_lottos_old = []
beeg_TMs = []
beeg_pedestals = []
lotto_numbers = []
max_prices = []
natdexes = []
obtained_defog_tms = []
smol_TMs = []
smol_pedestals = []
sphere_colors = []
swarm_indices = []
versions = []
for i in range(2941):
    temp = GS_Data(gs_lines[i])
    datas.append(temp)
    aliases.append(temp.alias)
    badgess.append(temp.badges)
    daily_seeds.append(temp.daily_seed)
    days_of_week.append(temp.day_of_week)
    debug_versions.append(temp.debug_version)
    drill_colors.append(temp.drill_color)
    evidences.append(temp.evidence)
    feebas_tiles_red.append(temp.feebas_tile_red)
    group_seeds.append(temp.group_seed)
    are_lottos_old.append(temp.is_lotto_old)
    beeg_TMs.append(temp.large_TMs)
    beeg_pedestals.append(temp.large_pedestals)
    lotto_numbers.append(temp.lotto_number)
    max_prices.append(temp.max_price)
    natdexes.append(temp.natdex)
    obtained_defog_tms.append(temp.obtained_defog_tm)
    smol_TMs.append(temp.small_TMs)
    smol_pedestals.append(temp.small_pedestals)
    sphere_colors.append(temp.sphere_color)
    swarm_indices.append(temp.swarm_index)
    users.append(temp.user)
    versions.append(temp.version)

fig, ax = plt.subplots()
ax.hist(days_of_week,bins=7, edgecolor="white")
ax.set_ylabel("Entries collected")
ax.set_xlabel("Numerical Day of Week")
plt.show()

lotto_numbers_any = (Bool_Any(lotto_numbers,are_lottos_old))
lotto_numbers_old = (Bool_True(lotto_numbers,are_lottos_old))
lotto_numbers_new = (Bool_False(lotto_numbers,are_lottos_old))
group_seeds_old = Bool_True(group_seeds,debug_versions)
group_seeds_new  = Bool_False(group_seeds,debug_versions)
group_seeds_any  = Bool_Any(group_seeds,debug_versions)
daily_seeds_old = Bool_True(daily_seeds,debug_versions)
daily_seeds_new = Bool_False(daily_seeds,debug_versions)
fig, ax1 = plt.subplots()
lotto_numbers_list = [lotto_numbers_any,lotto_numbers_old,lotto_numbers_new]
VP = ax1.boxplot(lotto_numbers_list)
plt.xticks([1, 2, 3], ["All Lottos: " + str(len(lotto_numbers_any)), "Old Lottos: " + str(len(lotto_numbers_old)), "New Lottos: " + str(len(lotto_numbers_new))])
ax1.set_ylabel("Lottery Number Drawn")
plt.show()
fig, ax2 = plt.subplots()
plt.scatter(group_seeds_old, daily_seeds_old, s=2)
ax2.set_ylabel("Debug Daily Seeds (Decimal, x10^9)")
ax2.set_xlabel("Debug Group Seeds (Decimal, x10^9)")
plt.show()
fig, ax3 = plt.subplots()
ax3.set_ylabel("New Daily Seeds (Decimal, x10^9")
ax3.set_xlabel("New Group Seeds (Decimal, x10^9")
plt.scatter(group_seeds_new, daily_seeds_new, s=2)
plt.show()
badge_counts = []
for i in range(1,9):
    badge_counts.append(sum(1 for j in badgess if j == i))
fig, ax4 = plt.subplots()
ax4.pie(badge_counts, labels=["1 Badge","2 Badges","3 Badges","4 Badges","5 Badges","6 Badges","7 Badges","8 Badges"],autopct='%1.1f%%')
plt.show()
defoggies = []
natdexi = []
defoggies = [sum(1 for j in obtained_defog_tms if j == True),sum(1 for j in obtained_defog_tms if j == False)]
natdexi = [sum(1 for j in natdexes if j == True),sum(1 for j in natdexes if j == False)]
fig, ax4 = plt.subplots()
ax4.pie(badge_counts, labels=["1 Badge","2 Badges","3 Badges","4 Badges","5 Badges","6 Badges","7 Badges","8 Badges"],autopct='%1.1f%%')
plt.show()
fig, ax5 = plt.subplots()
ax5.pie(defoggies, labels=["No Defog","Yes Defog"],autopct='%1.1f%%')
plt.show()
fig, ax6 = plt.subplots()
ax6.pie(natdexi, labels=["No Natdex","Yes Natdex"],autopct='%1.1f%%')
plt.show()
# I doubt I'll get a chance to include more, though I definitely want to: I'd need to import the datamined indexation for the buyables under each badge count, but the graphs for some of those (which I've plotted in Sheets) are fascinating...