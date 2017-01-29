##########################################################################################
# Sam - Home and Office Automation SRAI
# (Sam SRAI Bain)
#
# Version 1.0
# 
# Py-AIML or PyAIML Interpreter Personality Slackbot
# Used for both home automation and office automation
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

import SocketServer
import aiml
import os
import sys
import platform
import marshal
import glob
import time
import operator
import csv

# AIML Directory
saiml = "/PATH/sam/aiml/"
#saiml = "/PATH/sam/aiml/"

# SAM brain
k = aiml.Kernel()


# setpreds() function
def setpreds():
    with open(saiml + 'preds.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            k.setBotPredicate((row[0]), (row[1]))
    plat = platform.machine()
    osys = os.name
    print "Sam for " + osys
    print "System Architecture " + plat
    k.setBotPredicate("architecture", plat)
    k.setBotPredicate("os", osys)


# get_oldest_file() function found on stackolverflow
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
    if os.path.isfile(saiml + "sam.brn"):
        brnfiles = glob.glob(saiml + "*.brn")
        aimlfiles = glob.glob(saiml + "*.aiml")
        brn = get_oldest_file(brnfiles)
        oldage = os.path.getmtime(brn)
        youngaiml = get_youngest_file(aimlfiles)
        youngage = os.path.getmtime(youngaiml)
        testfiles = [brn, youngaiml]
        print testfiles
        oldfile = get_oldest_file(testfiles)
        print "Oldest file:", oldfile
        print 'Brain found:', brn
        print 'Brain age:', oldage
        print 'Newest AIML:', youngaiml
        print 'Newest AIML age:', youngage
        if (oldfile != (saiml + "sam.brn")):
            k.bootstrap(brainFile=saiml + "sam.brn")
        else:
            learn(aimlfiles)
    else:
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


# main() function


def main():
    # use sys.argv if needed
    print 'Server listening...'
    server = SocketServer.TCPServer((HOST, PORT), TCPHandler)
    server.serve_forever()


# TCPHandler class


class TCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print "{} said:".format(self.client_address[0])
        print self.data
        # Likewise, self.wfile is a file-like object used to write back
        # to the client

        if self.data:
            response = k.respond(self.data, "sam")
            self.wfile.write(response)
            if self.data == "quit":
                session = k.getSessionData("sam")
                sessionFile = file(saiml + "sam.ses", "wb")
                marshal.dump(session, sessionFile)
                sessionFile.close()
                sys.exit(0)


# call main
if __name__ == '__main__':
    HOST, PORT = "127.0.0.1", 9999
    print 'Waking sam...'
    brain()
    print 'Starting server...'
    main()
