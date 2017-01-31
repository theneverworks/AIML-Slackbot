##########################################################################################
# Sam - Home and Office Automation SRAI
# (Sam Brain Compiler)
#
# Version 1.0
# 
# Used to compile the brain file if needed.
#
# Credits:
# Many great works of many great people are included in Sam 
# I have only stacked the legos together.
#
# Based on the Py-AIML or PyAIML or pyAIML interpreter currently cloned by creatorrr
# author: Cort Stratton (cort@users.sourceforge.net) web: http://pyaiml.sourceforge.net/
# https://github.com/creatorrr/pyAIML
# 
##########################################################################################

import os
import sys
import platform
import time
import aiml
import marshal
import glob
import time
import operator
import csv


# AIML Directory
saiml = "/PATH/sam/aiml/"
#saiml = "C:\\PATH\\sam\\aiml\\"

# brain
k = aiml.Kernel()

# setpreds() function
def setpreds():
    with open(saiml + 'preds.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            #print((row[0]), (row[1]))
            k.setBotPredicate((row[0]), (row[1]))
    plat = platform.machine()
    osys = os.name
    print "Sam for " + osys
    print "System Architecture " + plat
    #print "Memory " + psutil.virtual_memory()
    k.setBotPredicate("architecture", plat)
    k.setBotPredicate("os", osys)


# get_oldest_file() function
def get_oldest_file(files, _invert=False):
    """ Find and return the oldest file of input file names.
    Only one wins tie. Values based on time distance from present.
    Use of `_invert` inverts logic to make this a youngest routine,
    to be used more clearly via `get_youngest_file`.
    """
    gt = operator.lt if _invert else operator.gt
    # Check for empty list.
    if not files:
        return None
    # Raw epoch distance.
    now = time.time()
    # Select first as arbitrary sentinel file, storing name and age.
    oldest = files[0], now - os.path.getmtime(files[0])
    # Iterate over all remaining files.
    for f in files[1:]:
        age = now - os.path.getmtime(f)
        if gt(age, oldest[1]):
            # Set new oldest.
            oldest = f, age
    # Return just the name of oldest file.
    return oldest[0]


# learn() function
def learn(aimlfiles):
    if not aimlfiles:
        k.learn(saiml + "xfind.aiml")
    for f in aimlfiles[1:]:
        k.learn(f)


# brain() function
def brain():
    aimlfiles = glob.glob(saiml + "*.aiml")
    learn(aimlfiles)

    setpreds()

    if os.path.isfile(saiml + "sam.ses"):
        sessionFile = file(saiml + "sam.ses", "rb")
        session = marshal.load(sessionFile)
        sessionFile.close()
        for pred,value in session.items():
            k.setPredicate(pred, value, "sam")
    else:
        setpreds()
    k.saveBrain(saiml + "sam.brn")

if __name__ == "__main__":
    brain()