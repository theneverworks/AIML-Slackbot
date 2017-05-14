##########################################################################################
# Sam Channel Spy - Channel and user mining tool for admins to configure security
# (ChannelSpy)
#
# Version 1.0
# 
# Based on the slack-starterbot
# author: Matt Makai (matthew.makai@gmail.com) web: http://www.mattmakai.com/
# https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
#
##########################################################################################

import os
import sys
import time
import urllib2
import json
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = "sam"

# constants
AT_BOT = "<@U12345678>"
# change these to test your configuations before adding them to Sam
BOTCHANNELS = "D12345678"
ALLOWED = "<@U12345678>"

# instantiate Slack & Twilio clients
slack_client = SlackClient("TOKEN_HERE")


def handle_command(command, channel, user, seclvl):
    response = "Message"
    if (command.startswith('test') and (seclvl >= 1)):
        response = "Channel spy command test"
        slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def get_user_name(userinfo):
    # change to your bot ID
    if userinfo != 'U12345678':
        # add your token here
        f = urllib2.urlopen('https://slack.com/api/users.info?user=' + userinfo + '&token=TOKEN_HERE')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        realname = parsed_json['user']['profile']['first_name']
        return realname
    return "Sam"

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
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("channel spy online and connected")
        while True:
            command, channelo, usero, seclvl = parse_slack_output(slack_client.rtm_read())
            if command and channelo:
                print "Message: " + command
                print "User: " + usero
                realname = get_user_name(usero)
                print "Real Name: " + realname
                trucommand = command.replace(": ", "")
                trucommand = trucommand.replace(":", "")
                print "Channel: " + channelo
                #chlinfo = slack_client.api_call("channels.info", channel=channelo)
                #print chlinfo
                print "Security Level: " + str(seclvl)
                handle_command(trucommand, channelo, usero, seclvl)
            time.sleep(READ_WEBSOCKET_DELAY)