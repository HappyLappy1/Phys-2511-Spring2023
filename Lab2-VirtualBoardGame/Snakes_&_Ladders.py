# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 12:54:59 2023

@author: happylappy1
"""
import time as tm
# Up Arrow: For ladders. Unicode characters are neat
down = "\u2B63"*2
# Down Arrow: For snakes. Unicode characters are neat
up = "\u2B61"*2
# triangle up arrows. they need to look different. Unicode characters are neat.
up_r = "|\u25B2"
up_l = "\u25B2|"
def roll_dice(dice_num,player):
    try:
        # Shove it pyflakes. I know RNG_State is undefined right now. That's the point!!!
        RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
    except:
        # This is a different mult and add, from a different game. I have a lot of these :P
        LCRNG_mult = 0x000343FD 
        LCRNG_add = 0x269EC3
        # Initialize RNG. Yes, this is the same algorithm as from lab 1. 32 bits should be plenty for a 2 six-sided dice.
        Time = tm.localtime()
        # Slightly modified time-based initial seeding algorithm from one of my favorite video games.
        AA = int(((Time.tm_mday) * int(Time.tm_mon) + int(Time.tm_min) + int(Time.tm_sec)))
        # Day of week and day of year were initially not in this algorithm. BB ended up limiting the seed size as a result.
        BB = int((1+Time.tm_wday) * Time.tm_hour + Time.tm_yday)
        CCCC = int(int(Time.tm_year) - 2000 + ((tm.time() - int(tm.time())) * 10000000))
        Seed = ((AA << 24) + (BB << 16) + CCCC) & 0xFFFFFFFF
        RNG_State = Seed
        RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
        # Advance LCRNG, as the next use will require a new state.
    if dice_num <1:
        dice_1 = 0
    else:
        dice_1 = ((RNG_State >> 16) % 6) + 1
        RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
    if dice_num == 2:
        dice_2 = ((RNG_State >> 16) % 6) + 1
    else:
        dice_2 = 0
    print("You rolled a "+str(dice_1)+(dice_2>0)*(" and a "+str(dice_2)))
    return dice_1 + dice_2
p1_pos = 0
p2_pos = 0
player = 1
while (p1_pos<100 and p2_pos<100):
    print("It is currently Player "+str(player)+"'s Turn!")
    tm.sleep(1)
    print("You may pass your turn, roll 1 die and be unable to pass your opponent, or roll 2 dice if you take every snake in your path.")
    tm.sleep(1)
    dice_num = int(input("How many dice would you like to roll: "))
    for i in range(2000):
        print("\b")
    movement = roll_dice(dice_num,player)
    # True when the player taking the turn is behind and they rolled one die.
    if (((p1_pos > p2_pos) ^ (player == 1)) and (p1_pos != p2_pos) and (dice_num == 1)):
        if movement >= abs(p2_pos-p1_pos) and ((p1_pos > p2_pos) ^ (player == 1)):
            tm.sleep(2)
            print("What a ruckus! Player " + str(player) + " bumped into their opponent while moving!")
            movement = abs(p2_pos-p1_pos) - 1
    if (dice_num == 2) and (movement == abs(p2_pos-p1_pos)):
        movement = movement + 1
        tm.sleep(2)
        print("What a ruckus! Player " +str(player)+" landed on the same space as their opponent!")
        tm.sleep(1)
        print("This will not do! Player " +str(player)+" will need to move an extra space!")
    # True when the player would move past tile 100. This script does not play by "bounce-back" rules.
    if (movement + p1_pos*(player == 1) + p2_pos*(player == 2) )> 100:
        movement = 0
        tm.sleep(2)
        print("Oh no! Player "+str(player)+" rolled too high to reach 100! Try again next turn!")
    snake_heads = [99, 97, 92, 88, 62, 48, 36, 32]
    snake_tails = [79, 77, 56, 24, 18, 26, 6, 10]
    
    
    if dice_num == 2:
        while movement > 0:
            if player == 1:
                p1_pos = p1_pos + 1
                for i in range(8):
                    if p1_pos == snake_heads[i]:
                        p1_pos = snake_tails[i]
                        tm.sleep(2)
                        print("Oh no! Player 1 went down a snake while in transit, with a tail at tile " + str(snake_tails[i]))
            else:
                p2_pos = p2_pos + 1
                for i in range(8):
                    if p2_pos == snake_heads[i]:
                        p2_pos = snake_tails[i]
                        tm.sleep(2)
                        print("Oh no! Player 2 went down a snake while in transit, with a tail at tile " + str(snake_tails[i]))
            movement = movement - 1
    special_tiles = [99, 97, 92, 71, 28, 88, 62, 50, 21, 48, 1, 36, 32, 8, 4]
    tiles_end = [79, 77, 56, 95, 76, 24, 18, 67, 42, 26, 38, 6, 10, 30, 14]
    snake_txt = " landed on a snake head with a tail at tile "
    ladder_txt = " landed at the foot of a ladder leading to tile "
    event = 0
    tm.sleep(1)
    if player == 1:
        p1_pos = p1_pos + movement
        for i in range(15):
            if p1_pos == special_tiles[i]:
                p1_pos = tiles_end[i]
                print("Player 1" + snake_txt*(special_tiles[i]>tiles_end[i]) + ladder_txt*(special_tiles[i]<tiles_end[i]) + str(tiles_end[i]))
                event = 1
        if event == 0:
            print("Player 1 ended on tile " + str(p1_pos))
    if player == 2:
        p2_pos = p2_pos + movement
        for i in range(15):
            if p2_pos == special_tiles[i]:
                p2_pos = tiles_end[i]
                print("Player 2" + snake_txt*(special_tiles[i]>tiles_end[i]) + ladder_txt*(special_tiles[i]<tiles_end[i]) + str(tiles_end[i]))
                event = 1
        if event == 0:
            print("Player 2 ended on tile " + str(p2_pos))        
    tm.sleep(2)
    t = []
    # Update the tiles that have player 1, 2, and are less than 2 characters in length. Tile 0 is the starting tile.
    for s in range(101):
        if (s == p1_pos):
            t.append("P1")
        elif (s == p2_pos):
            t.append("P2")
        elif (0 < s < 10):
            t.append("0"+str(s))           
        elif (s == 0):
            t.append("St")
        else:
            t.append(str(s))
    # Align the tiles in the correct grid-pattern. use pipes to cordon off tiles, and tiles that never change (such as the ends of snakes and ladders) remain static. 
    key = "\u2B63"*2+" = End of a Snake, "+"\u2B61"*2+" = End of a Ladder, Pn = Player n"
    board_row_1 = "|"+t[81]+"|"+t[82]+"|"+t[83]+"|"+t[84]+"|"+t[85]+"|"+t[86]+"|"+t[87]+"|"+t[88]+"|"+t[89]+"|"+t[90]+"|"+t[91]+"|"+t[92]+"|"+t[93]+"|"+t[94]+"|"+t[95]+"|"+t[96]+"|"+t[97]+"|"+t[98]+"|"+t[99]+"|"+t[100]+"|"
    board_row_2 = "|"+up_l+"                  |"+down+"|        |"+down+"|     |"+up+"|  |"+down+"|  |"+down+"|  "
    board_row_3 = "|"+up_l+"|99|  |97|        |24|  |95|  |56|     |71|  |77|  |79|  "
    board_row_4 = "|"+up_l+"|"+down+"|  |"+down+"|              |"+up+"|"
    board_row_5 = "|"+t[80]+"|"+t[79]+"|"+t[78]+"|"+t[77]+"|"+t[76]+"|"+t[75]+"|"+t[74]+"|"+t[73]+"|"+t[72]+"|"+t[71]+"|"+t[70]+"|"+t[69]+"|"+t[68]+"|"+t[67]+"|"+t[66]+"|"+t[65]+"|"+t[64]+"|"+t[63]+"|"+t[62]+"|"+t[61]+"|"
    board_row_6 = "            |"+up+"|                       |"+up+"|           |"+down+"|"+up_r+"|"
    board_row_7 = "            |28|           |67|        |50|  |92|     |18|"+up_r+"|"
    board_row_8 = "                           |"+up+"|              |"+down+"|         "+up_r+"|"
    board_row_9 = "|"+t[41]+"|"+t[42]+"|"+t[43]+"|"+t[44]+"|"+t[45]+"|"+t[46]+"|"+t[47]+"|"+t[48]+"|"+t[49]+"|"+t[50]+"|"+t[51]+"|"+t[52]+"|"+t[53]+"|"+t[54]+"|"+t[55]+"|"+t[56]+"|"+t[57]+"|"+t[58]+"|"+t[59]+"|"+t[60]+"|"
    board_row_10 = "|"+up_l+"|"+up+"|              |"+down+"|                                   "
    board_row_11 = "|"+up_l+"|21|              |26|           |76|  |48|  |88|     |42|"
    board_row_12 = "|"+up_l+"                                 |"+up+"|  |"+down+"|  |"+down+"|     |"+up+"|"
    board_row_13 = "|"+t[40]+"|"+t[39]+"|"+t[38]+"|"+t[37]+"|"+t[36]+"|"+t[35]+"|"+t[34]+"|"+t[33]+"|"+t[32]+"|"+t[31]+"|"+t[30]+"|"+t[29]+"|"+t[28]+"|"+t[27]+"|"+t[26]+"|"+t[25]+"|"+t[24]+"|"+t[23]+"|"+t[22]+"|"+t[21]+"|"
    board_row_14 = "      |"+up+"|  |"+down+"|        |"+down+"|  |"+up+"|                        "+up_r+"|"
    board_row_15 = "|38|  |01|14|06|36|  |30|10|32|08|                 |62|   "+up_r+"|"
    board_row_16 = "|"+up+"|     |"+up+"|  |"+down+"|  |"+up+"|  |"+down+"|                    |"+down+"|   "+up_r+"|"
    board_row_17 = "|"+t[1]+"|"+t[2]+"|"+t[3]+"|"+t[4]+"|"+t[5]+"|"+t[6]+"|"+t[7]+"|"+t[8]+"|"+t[9]+"|"+t[10]+"|"+t[11]+"|"+t[12]+"|"+t[13]+"|"+t[14]+"|"+t[15]+"|"+t[16]+"|"+t[17]+"|"+t[18]+"|"+t[19]+"|"+t[20]+"|"
    board_row_18 = "|"+t[0]+"|                                   |"+up+"|                  "
    board_row_19 = "                                       |04|                 "
    # Print the entire board. This is messy, but if I wanted a good UI, I'd be coding this in sheets. 
    print(key+"\n"+board_row_1+"\n"+board_row_2+"\n"+board_row_3+"\n"+board_row_4+"\n"+board_row_5+
          "\n"+board_row_6+"\n"+board_row_7+"\n"+board_row_8+"\n"+board_row_9+"\n"+board_row_10+
          "\n"+board_row_11+"\n"+board_row_12+"\n"+board_row_13+"\n"+board_row_14+"\n"+board_row_15+
          "\n"+board_row_16+"\n"+board_row_17+"\n"+board_row_18+"\n"+board_row_19)
    # Even with my illustrious-looking board, P1 and P2 are hard to spot amongst all the numbers.
    # That's why I'm telling both players what tile they're on in addition...
    print("Player 1: "+str(p1_pos))
    print("Player 2: "+str(p2_pos))
    # Switch turn order
    if player == 2:
        player = 1
    elif player == 1:
        player = 2

# to get here, SOMEONE won. But who? 
if p1_pos == 100:
    print("Player 1 is the winner!")
else: 
    print("Player 2 is the winner!")