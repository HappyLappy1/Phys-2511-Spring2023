# Importing random module depending on user decision! 
import time as tm
# Well known 32 bit LCRNG with maximum period. Use the top half, especially when multiples of 2 are involved
LCRNG_mult = 0x41C64E6D
LCRNG_add = 0x6073
# Give a cryptic means by which to enter a code
if (input("Do you believe in free will? (type Y if so, or N if not)") == "N" or input("Do you believe in free will? (type Y if so, or N if not)") == "n"):
    # If the user entered a code, use that instead
    Code = input("What is your code?")
    try:
        int(Code)
    except ValueError:
        Time = tm.localtime()
        # Slightly modified time-based initial seeding algorithm from one of my favorite video games.
        AA = int(((Time.tm_mday) * int(Time.tm_mon) + int(Time.tm_min) + int(Time.tm_sec)))
        # Day of week and day of year were initially not in this algorithm. BB ended up limiting the seed size as a result.
        BB = int((1+Time.tm_wday) * Time.tm_hour + Time.tm_yday)
        CCCC = int(int(Time.tm_year) - 2000 + ((tm.time() - int(tm.time())) * 10000000))
        Seed = ((AA << 24) + (BB << 16) + CCCC) & 0xFFFFFFFF
        RNG_State = Seed
        print("Invalid Code Formatting! Proceeding with self-randomized seed!")
    else:
        Seed = int(Code)
        RNG_State = Seed
        print("Code Accepted!")
else:
    # Seed the RNG Engine with a random value, and use sufficiently pseudorandom values from that point onward
    import random as rn
    Seed = rn.randint(0,0xFFFFFFFF)
    RNG_State = Seed
print("I am the great witch of Far Forest! Welcome to my hut in the depths of the woods.")
# Rshift of 30 forces a small delay. Ensure sleep time is never 0, mainly because that's jarring and could lose me points.
tm.sleep(max(((RNG_State >> 30)), 1))
# Advance LCRNG, as the next use will require a new state.
RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
print("It surely must have been a long journey to make it all the way here! You come from that bustling city to the far east, do you not? Why visit an old hag like me?")
tm.sleep(max(((RNG_State >> 30)), 1))
RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
print("To divine the answer to a simple yes-or-no question, you came all the way here? You must know, my fare isn't cheap!")
tm.sleep(max(((RNG_State >> 30)), 1))
RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
# A Float can be conveniently used to display currency when converted to string. This "Price" is exclusively for narrative flavor.
print("For today's divination, I require a small fee of $" + str((RNG_State>> 16) / 100) + ", is that to your liking?")
# Store the RNG State responsible for price, so the main RNG can still be used 
RNG_State_2 = RNG_State
# Only Advance RNG now, after storing the state 
RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
tm.sleep(max(((RNG_State >> 30)), 1))
RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
Verify = input("Is the price to your liking? (type Y to accept the price, or N to haggle with the witch)")
# Should haggling dialogue initiate? 
if (Verify=="N" or Verify=="n"): 
    # Only Advance RNG now, after storing the state 
    tm.sleep(max(((RNG_State >> 30)), 1))
    RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
    # Reuse RNG_State_2 with adjusted bitshift for new currency.
    # This would effectively round any new prices down to the nearest cent. 
    Dialogue_1 = ["You're right, I don't get much business these days... I should lower my prices?" +
                  " How about 50% off? That would put you at a total of: $" + str((RNG_State_2 >> 17) / 100), 
                  "That's the game we're playing? They don't call me the haggling hag for nothing you know!" + 
                  " (You doubled the price of the session in a series of haggling blunders. Your new price is: $" + 
                  str((RNG_State_2>> 15) / 100) + ")", 
                  "You don't have the funds? I accept other forms of payment than money you know." + 
                  " How does soul of your first-born child sound? Mangrove feed is hard to come by these days."]
    print(Dialogue_1[(((RNG_State >> 16) % 3))])
    RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
    tm.sleep(max(((RNG_State >> 28)), 2))
else:
    # Same total number of RNG calls regardless of whether a user haggles.
    RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
    RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
print("Excellent! Now that we've settled how you're paying for my services, what is this question you want answered so desparately?")
tm.sleep(max(((RNG_State >> 30)), 1))
RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
Question = input("Type out your question:")
print(Question)
print("Are you sure this is the question you wish me to answer?")
Verify = input("Type Y for Yes, or N for No: ")
while not(Verify=="Y" or Verify == "y"):
      print("Having second thoughts, are we? Don't be shy, what question would you like me to answer?")
      Question = input()
      print("Are you sure this is the question you wish me to answer? (Type Y for Yes, or N for No)")
      Verify = input()      
print("What a fascinating question! For such a marvelously worded question, this service is free-of-charge!")
tm.sleep(max(((RNG_State >> 30)), 1))
RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
Dialogue_2 = ["consult the stars above for the answers you seek...", "shuffle my deck of tarot cards for a reading...", 
              "peer into my Scrying Bowl as a window to the future...", 
              "shake and toss about my divination stones; an offering to those above and below...", 
              "Owwwww! I stubbed my toe on a magic 8-ball! Let us use that to resolve your query..."]
print("Have a seat, and we can begin. Let me " + Dialogue_2[(RNG_State >> 16) % 5])
# Reuse RNG_State_2 to store the state responsible for flavor dialogue. Dialogue 4 will reference Dialogue 2.
RNG_State_2 = RNG_State
RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
tm.sleep(max(((RNG_State >> 30)), 1))
RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
# Dialogue 3 will approximate how long of a delay it will take for the witch to answer the question. 
# Max delay of 255 seconds, Min delay of 2 seconds. These will display as time passes, to keep the user engaged and in suspense. 
Dialogue_3 = ["This shouldn't take long, your question is a trifle for me to answer...", 
              "Hmm, this could be tricky, I may need a minute to flip through my spell-book...",
              "BANG! Pay no heed to that dearie, it was just a minor setback, and a flesh wound...",
              "Oh drat, I need more supplies! Wait right here dearie, I need to take quick broom-trip to the market.",
              "Why don't you get comfy dearie, this ritual could take a few hours...",
              "Oh my, I don't even know where to begin with this one; this could take the whole fortnight to complete!" + 
              " Fret not dearie, I provide complimentary room and board for my paying customers..."]
print(Dialogue_3[0])
if RNG_State >> 24 > 31:
    tm.sleep(31)
    print(Dialogue_3[1])
    if RNG_State >> 24 > 63:
        tm.sleep(32)
        print(Dialogue_3[2])
        if RNG_State >> 24 > 127:
            tm.sleep(64)
            print(Dialogue_3[3])
            if RNG_State >> 24 > 191:
                tm.sleep(64)
                print(Dialogue_3[4])
                if RNG_State >> 24 > 225:
                    tm.sleep(34)
                    print(Dialogue_3[5])
                    tm.sleep((RNG_State >> 24) - 225)
                else:
                    tm.sleep((RNG_State >> 24) - 191)
            else:
                tm.sleep((RNG_State >> 24) - 127)
        else: 
            tm.sleep((RNG_State >> 24) - 63)
    else:
        tm.sleep((RNG_State >> 24) - 31)
else: 
    tm.sleep(max(((RNG_State >> 24)), 2))
RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
Dialogue_4 = ["The stars above have spoken!", "The cards lay the truth bare before me!", 
              "I see the truth within my Scrying Bowl!", "The gods of the aftertimes speak to me through these stones!", 
              "I gave the 8-ball as hearty a shake as I could muster!"] 
# Reuse stored RNG State to provide accurate dialogue
print("Aha! Yes, I see! " + Dialogue_4[(RNG_State_2 >> 16) % 5])
tm.sleep(max(((RNG_State >> 30)), 1))
RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
print("Your question is: " + Question)
tm.sleep(max(((RNG_State >> 30)), 1))
RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
# I found the 20 original responses for the patented Magic 8 Ball, and added my own twist on each. 
Responses = ["is a resounding yes; it is certain!", "is a near-perfect yes; it is decidedly so.", 
             "is indubitably a yes; without a doubt!", "is carved in stone; yes definitely!", 
             "is pseudo-statistically a yes; you may rely on it!","is a somewhat clear yes; as I see it, yes.", 
             "is a likely truth; most likely.", "things should turn out well for you; outlook good.",
             "begins with a Y, an E, then concludes with an S; yes.", "currently appears to be a yes; signs point to yes.", 
             "The curse of '63 is making my cateracts act up; reply hazy, try again.", "is still uncertain; ask again later.",
             "is... Oh me! Oh my! It would be better for both of us if I said nothing; better not tell you now.",
             "is not yet knowable; cannot predict now.", "is... oops! I forgot your question; concentrate and ask again.",
             "is pseudo-statistically improbable; don't count on it.", "is as I suspected initially; my reply is no.",
             "currently appears to be a no; my sources say no.", "seems to be as you feared; outlook not so good", 
             "is far from likely; very doubtful"]
print("The answer to your query " + Responses[(RNG_State >> 16) % 20])
RNG_State = (((RNG_State * LCRNG_mult) + LCRNG_add) & 0xFFFFFFFF)
tm.sleep(max(((RNG_State >> 30)), 1))
print("(Your secret code is: " + str(Seed) + ". Use this value to view this deterministic sequence of events identically a second time through)")
