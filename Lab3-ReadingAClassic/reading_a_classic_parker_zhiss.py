# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 12:37:03 2023

@author: parke
"""
import matplotlib.pyplot as plt
file = open("42324.txt","r")
file_text = []
file_text = file.read()
file.close()
simple_file_chapter = file_text.split("CHAPTER ")
simple_character_names = ["Victor", "creature", "Agatha", "Caroline","De Lacey","Elizabeth","Ernest","Felix","Henry","Justine", "William"]
simple_names_per_chapter = []
for i in range(len(simple_character_names)):
    temp = []
    for j in range(len(simple_file_chapter)):
        temp.append(simple_file_chapter[j].count(simple_character_names[i]))
    simple_names_per_chapter.append(temp)
chapter = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
chapter_labels=[]
# There are a lot of character names, and I have viewed this graph on one 
for i in range(24):
    chapter_labels.append(str(chapter[i]))
fig, ax = plt.subplots()
for i in range(len(simple_character_names)//2):
    plt.plot(chapter, simple_names_per_chapter[i][:],label = simple_character_names[i])
ax.set_ylabel("Times Name Appears")
ax.set_xlabel("Chapter of Book")
ax.set_title("Simple Character Name Frequency Throughout Frankenstein by Chapter")
ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
#plt.show()

fig, ax5 = plt.subplots()
for i in range(len(simple_character_names)//2,len(simple_character_names)):
    plt.plot(chapter, simple_names_per_chapter[i][:],label = simple_character_names[i])
ax5.set_ylabel("Times Name Appears")
ax5.set_xlabel("Chapter of Book")
ax5.set_title("Simple Character Name Frequency Throughout Frankenstein by Chapter Part 2")
ax5.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
#plt.show()


# Split by chapter, store it for later use. 
chapter_text = file_text.split("CHAPTER ")
# New lines can conceal the end of a sentence or word. They need to go bye-bye!
file_text = file_text.replace("\n"," ")
# Incorrect grammatically, but the author knows best when it comes to when sentences should start
file_text = file_text.replace("--",". ")
# punctuation on either end of words make them too unique. Might miss a name because of punctuation.
file_text = file_text.replace("; "," ")
file_text = file_text.replace(":"," ")
file_text = file_text.replace("\""," ")
file_text = file_text.replace(","," ")
file_text = file_text.replace("'s","")
file_text = file_text.replace("]"," ")
# GutenbergGutenbergGutenbergGutenbergGutenbergGutenbergGutenbergGutenbergGutenbergGutenberg
# Proper Noun Blacklist
file_text = file_text.replace("Gutenberg","")
file_text = file_text.replace("Project","")
file_text = file_text.replace("Foundation","")
file_text = file_text.replace("Archive","")
file_text = file_text.replace("Literary","")
file_text = file_text.replace("License","")
file_text = file_text.replace("United States", "")
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
file_text = file_text.replace("This","")
file_text = file_text.replace("-"," ")
# Periods aren't the only way to end sentences, only the most common... 
file_text = file_text.replace("!",".")
file_text = file_text.replace("?",".")
# Double spaces make empty words, and those take up space. 
# I didn't count how many consecutive spaces there are, but this should cover 2**8 spaces: plenty
file_text = file_text.replace("  "," ")
file_text = file_text.replace("  "," ")
file_text = file_text.replace("  "," ")
file_text = file_text.replace("  "," ")
file_text = file_text.replace("  "," ")
file_text = file_text.replace("  "," ")
file_text = file_text.replace("  "," ")
file_text = file_text.replace("  "," ")
# Chapters are in the middle of my self-defined "Sentences", so I need to fix that.
file_text = file_text.replace("CHAPTER ", ". CHAPTER. ")
# This next sequence is an automated diagnostic to locate names and other proper nouns. It is not perfect, and I don't need it to be. 
# As long as I get the words I'm looking for often enough, I'm satisfied with searching those words in the text properly.
# Split the entire book into sentences. Yes, titles like Mr. and Mrs. are sentences now, and I'm not going to parse for that.
sentence_text = file_text.split(". ")
words = []
# I want to computationally generate a list of proper nouns to search the text for.
# "creature" is not a proper noun, so this search will not be able to find it. Oh well~
# I expect the data I get out of this to be pretty fuzzy, English is a complex language, after all.
# I plan to make this happen by searching words that begin with a capital letter.
# ...excuding words at the start of a sentence, and the word "I".
proper_nouns = []
for i in range(len(sentence_text)):
    # Set the current sentence to the sentence we want, split into words. 
    current_sentence = sentence_text[i].split(" ")
    # Parse every word in that sentence, skipping first word in the sentence. 
    # ... Even if it's a name.
    for j in range(1,len(current_sentence)):
        current_word = current_sentence[j]
        # Skip cases where there are 3 or more spaces or new lines (failsafes are nice), as well as words shorter than 4 characters. 
        if len(current_word)>3:
            if current_word[0].isupper() and current_word[1].islower():
                proper_nouns.append(current_sentence[j])
names = []
name_count = []
for i in proper_nouns:
    # If I don't get around to bug-fixing my filters, I'll leave this pruning segment in. 
    # Words that clearly aren't names or places are slipping through, but not frequently.
    # My heavy-handed solution is to simply remove proper nouns that aren't frequent enough in the entire text.
    # Also, having 60+ unique words makes creating a legend difficult. As a result, I'm blacklisting certain words, and enforcing a minimum count for "names". 
    if proper_nouns.count(i) > 5:    
        names.append(i)
        name_count.append(proper_nouns.count(i))
unique_names = set(names)
unique_names = list(unique_names)
true_names_per_chapter = []
print(str(len(names)) + " proper nouns found!")
print(str(len(unique_names)) + " unique proper nouns found!")
print(unique_names)
for i in range(len(unique_names)):
    temp = []
    for j in range(len(chapter_text)):
        temp.append(chapter_text[j].count(unique_names[i]))
    true_names_per_chapter.append(temp)
fig, ax1 = plt.subplots()
for i in range(len(unique_names)//4):
    plt.plot(chapter, true_names_per_chapter[i][:],label = unique_names[i])
ax1.set_ylabel("Times \"Name\" Appears")
ax1.set_xlabel("Chapter of Book")
ax1.set_title("Full \"Name\" Frequency Throughout Frankenstein by Chapter (Part 1)")
ax1.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.show()
fig, ax2 = plt.subplots()
for i in range(len(unique_names)//4,len(unique_names)//2):
    plt.plot(chapter, true_names_per_chapter[i][:],label = unique_names[i])
ax2.set_ylabel("Times \"Name\" Appears")
ax2.set_xlabel("Chapter of Book")
ax2.set_title("Full \"Name\" Frequency Throughout Frankenstein by Chapter (Part 2)")
ax2.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.show()
fig, ax3 = plt.subplots()
for i in range(len(unique_names)//2,len(unique_names)*3//4):
    plt.plot(chapter, true_names_per_chapter[i][:],label = unique_names[i])
ax3.set_ylabel("Times \"Name\" Appears")
ax3.set_xlabel("Chapter of Book")
ax3.set_title("Full \"Name\" Frequency Throughout Frankenstein by Chapter (Part 3)")
ax3.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.show()
fig, ax4 = plt.subplots()
for i in range(len(unique_names)*3//4,len(unique_names)):
    plt.plot(chapter, true_names_per_chapter[i][:],label = unique_names[i])
ax4.set_ylabel("Times \"Name\" Appears")
ax4.set_xlabel("Chapter of Book")
ax4.set_title("Full \"Name\" Frequency Throughout Frankenstein by Chapter (Part 4)")
ax4.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.show()
