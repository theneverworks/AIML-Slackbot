##########################################################################################
# Sam - Home and Office Automation SRAI
# (SlackSam)
#
# Version 1.1
# 
# Py-AIML or PyAIML Interpreter Personality Slackbot
# Used for both home automation and office automation
#
# Credits:
# Many great works of many great people are included in Sam 
# I have only stacked the legos together.
#
# Based on the slack-starterbot
# author: Matt Makai (matthew.makai@gmail.com) web: http://www.mattmakai.com/
# https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
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
from slackclient import SlackClient
import aiml
import marshal
import glob
import operator
import csv

# slackbot's ID
BOT_ID = "sam"
# list the direct message channels that you would like to allow direct messaging from, use the channel spy tool
BOTCHANNELS = "DABCDEFGHD12345678"
# list the users that are able to execute secured functions all users are default level 1, this gives them level 2
ALLOWED = "<@U12345678><@UABCDEFGH>"

# constants
AT_BOT = "<@BOT_ID>"
EXAMPLE_COMMAND = "do"
HELP_COMMAND = "help"

# instantiate Slack client
slack_client = SlackClient("SLACK_TOKEN")

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
            k.setBotPredicate((row[0]), (row[1]))
    plat = platform.machine()
    osys = os.name
    print "Sam for " + osys
    print "System Architecture " + plat
    #print "Memory " + psutil.virtual_memory()
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

    
def get_user_name(userinfo):
    # update with your BOT ID
    if userinfo != 'U12345678':
        # update with your Slack Token
        f = urllib2.urlopen('https://slack.com/api/users.info?user=' + userinfo + '&token=<PUT_YOUR_TOKEN_HERE>')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        realname = parsed_json['user']['profile']['first_name']
        return realname
    return "Sam"
    
# based on the slack-starterbot
# now available for use, security level and user's real name for personalization
def handle_command(command, channel, user, seclvl, realname):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "*"
    if (command.startswith(EXAMPLE_COMMAND) and seclvl >= 1):
        response = "Sure...write some more code then I can do that!"
    elif command.startswith(HELP_COMMAND):
        try:
            response = "You need some assistance? I can perform many administrative tasks.\n"
            response += "*test* - Performs a basic SRAI test of Sam's congnitive functions. "
        except:
            response = "My help system is damaged"
    else:
        response = k.respond(command, "sam")
    try:
        slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
    except:
        print "Failed to send message"
        sleep(30)
        try:
            slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
        except:
            gethelp()

def gethelp():
    try:
        msg = MIMEText("Help, I can't access the internet anymore.")
        bot = "sam@youremail.com"
        person = "you@youremail.com"
        msg['Subject'] = 'Sam needs help'
        msg['From'] = bot
        msg['To'] = person
        s = smtplib.SMTP('SMTP_SERVER')
        s.sendmail(bot, [person], msg.as_string())
        s.quit()
    except:
        print "Failed to send help email"

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if ((output and 'text' in output) and (AT_BOT in output['text'])):
                if (output['user'] in ALLOWED):
                    seclvl = 2
                else:
                    seclvl = 1
                return output['text'].split(AT_BOT)[1].strip(), \
                       output['channel'], \
                       output['user'], \
                       seclvl
            if ((output and 'text' in output) and (output['channel'] in BOTCHANNELS)):
                if (output['user'] in ALLOWED):
                    seclvl = 2
                else:
                    seclvl = 1
                return output['text'], \
                       output['channel'], \
                       output['user'], \
                       seclvl
    return None, None, None, None

if __name__ == "__main__":
    try:
        READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
        if slack_client.rtm_connect():
            brain()
            print("sam online and connected")
        while True:
            command, channelo, usero, seclvl = parse_slack_output(slack_client.rtm_read())
            if command and channelo:
                #print "Message: " + command
                #print "User: " + usero
                realname = get_user_name(usero)
                print "Real Name: " + realname
                # removes the colon inserted by the mobile app
                trucommand = command.replace(": ", "")
                trucommand = trucommand.replace(":", "")
                # update your bot's ID to it doesn't talk to itself
                if usero != 'U12345678':
                    handle_command(trucommand, channelo, usero, seclvl, realname)
            time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
    except:
        gethelp()
        print "Slack connection has failed and the bot was closed."