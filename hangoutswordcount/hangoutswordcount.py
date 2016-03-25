# This program reads in a Google Hangouts JSON file and produces a wordcount
# Author: Pinaky Bhattacharyya 

import json     # JSON to handle Google's format
import re       # regular expressions

# CHANGE THIS. For linux/mac, use '/home/user/restofpath/'
basepath = 'C:\\Users\\Pinaky\\Desktop\\cesmd\\gmail_hangout\\'

# INPUT: This is the input file path
jsonPath = basepath + 'Hangouts.json'

# OUTPUT: These are the output file paths. dict = sorted alphabetical; freq = sorted by frequency
mainDictPath = basepath + 'hangoutdict.txt'
mainFreqPath = basepath + 'hangoutfreq.txt'

# This is the path to a temporary intermediate file
tempPath = basepath + 'hangouttemp.txt'

# Read in the JSON file
jsonFile = open(jsonPath, 'r', encoding='utf8')
outFile = open(tempPath,'w', encoding='utf8')

# 'p' is the variable that contains all the data
p = json.load(jsonFile)

c = 0   # Count the number of chat messages

# This loops through Google's weird JSON format and picks out the chat text
for n in p['conversation_state']:
    for e in n['conversation_state']['event']:
        if 'chat_message' in e:
            x = e['chat_message']['message_content']
            if 'segment' in x:
                xtype = x['segment'][0]['type']
                xtext = x['segment'][0]['text'] + u" "
                if xtype == u'TEXT':
                    # Write out the chat text to an intermediate file
                    outFile.write(xtext)
                    c += 1

print(u'Total number of chats: {0:d}'.format(c))

jsonFile.close()
outFile.close()

# The intermediate file has been written
# Now, run a wordcount

# Read in the intermediate file
inFile = open(tempPath,'r', encoding='utf8')
s = inFile.readlines()
inFile.close()

wordcount={} # The dictionary for wordcount

for l in range(len(s)):
    line = s[l].lower().strip()                 # strip unnecessary white space
    line = re.sub(u'[^A-Za-z]+', u' ', line)    # keep only alphabets and remove the rest
    for word in line.split():
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1

# Sort the wordcount like a dictionary and write to file
outFile = open(mainDictPath, 'w', encoding='utf8')
for k,v in sorted(wordcount.items()):
    outFile.write(str(k))
    outFile.write(u' ')
    outFile.write(str(v))
    outFile.write(u'\n')
outFile.close()

# Sort the wordcount in descending order of frequency and write to file
outFile = open(mainFreqPath, 'w', encoding='utf8')
for k, v in sorted(wordcount.items(), key=lambda w: w[1], reverse=True):
    outFile.write(str(k))
    outFile.write(u' ')
    outFile.write(str(v))
    outFile.write(u'\n')
outFile.close()
