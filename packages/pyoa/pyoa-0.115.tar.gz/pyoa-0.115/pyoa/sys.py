# most frequently used system functions


import gzip
# gunzips a file into a variable
def unzipBook(file):
    with gzip.open(file, "rb") as f:
        text = f.read().decode('utf-8')
        return(text)

# gzips unicode text into a file
import gzip
def zipBook(data, fileName):
    with gzip.open(fileName+".metatext.gz", "wb") as f:
        f.write(data.encode('utf-8'))

# creates a folder if does not exist
def folderTest(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# round up a number based on par
# e.g., if par=20, the number will be rounded up to a closest number divisible by 20)
import math
def roundup(x, par):
    newX = int(math.ceil(int(x) / float(par)) * par)
    return(newX)

# convert AH to CE (only years)
def AHCE(ah):
    ce = int(ah)-(int(ah)/33)+622
    return(int(ce))

# convert CE to AH (only years)
def CEAH(ce):
    ah = 33/32*(int(ce)-622)
    return(int(ah))

# formatStat(annot, variable) formats statistics statements
def formatStat(annot, variable):
    formatted = '{:<25}'.format(annot) + '{0:>10}'.format(str(variable)) # + '\n'
    return print(formatted)

import textwrap
# wraps long paragraphs: helps with viewing long files
def wrapPar(paragraph, lenSymb):
    wrapped = "\n~~".join(textwrap.wrap(paragraph, lenSymb))
    return(wrapped)

# Increases counter and prints out status
def counter(counterName, printUpdate):
    counterName = counterName + 1
    if counterName % printUpdate == 0:
        counterString = "{:10,}".format(counterName)+" items processed"
        print("{:>25}".format(counterString))
    return(counterName) 
