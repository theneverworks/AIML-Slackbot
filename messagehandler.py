##########################################################################################
# Sam - Home and Office Automation Message Handler
# (Sam Message Handler)
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
# Based on the slack-starterbot
# author: Matt Makai (matthew.makai@gmail.com) web: http://www.mattmakai.com/
# https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
# 
##########################################################################################

import os
import sys
import time
from slackclient import SlackClient
import urllib2
import json
import httplib
import urllib
import pika

# starterbot's ID as an environment variable
BOT_ID = "sam"

# constants
AT_BOT = "<@BOT_ID>"

# instantiate Slack client
slack_client = SlackClient("SLACK_TOKEN")

def gethelp():
    try:
        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
        urllib.urlencode({
            "token": "PUSH_OVER_TOKEN",
            "user": "PUSH_OVER_USER",
            "message": "I am unable to use Slack, please help me.",
        }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
    except:
        print "Something went horribly wrong"
        
def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

def main():
    credentials = pika.PlainCredentials('user', 'password')
    parameters = pika.ConnectionParameters('IP_ADDRESS', PORT, 'queue', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='messages',
                       queue=queue_name)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] %r" % body)
        slack_client.api_call("chat.postMessage", channel="CHANNEL_ID", text=body, as_user=True)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()
    try:
        channel.start_consuming()
    except:
        print "The connection was forced closed"
        print "Waiting..."
        time.sleep(30)
        print "Attempting to reconnect"
        try:
            channel.start_consuming()
        except:
            print "Failed to reconnect"

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("online and connected")
        main()
    else:
        print("Connection failed. Invalid Slack token or bot ID?")