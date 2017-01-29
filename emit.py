##########################################################################################
# Sam - Home and Office Automation Message Emitter
# (Sam Message Emitter)
#
# Version 1.0
# 
# Py-AIML or PyAIML Interpreter Personality Slackbot
# Used for both home automation and office automation
# 
##########################################################################################

import pika
import sys
import httplib
import urllib

def gethelp():
    try:
        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
        urllib.urlencode({
            "token": "PUSH_OVER_TOKEN",
            "user": "PUSH_OVER_USER",
            "message": "The alarm interface is unable to connect to the message queue. " + message,
        }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
    except:
        print "Something went horribly wrong"
try:
    credentials = pika.PlainCredentials('user', 'password')
    parameters = pika.ConnectionParameters('IP_ADDRESS', PORT, 'queue', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    message = ' '.join(sys.argv[1:]) or "Testing queue"
    channel.basic_publish(exchange='messages',
                          routing_key='',
                          body=message)
    print(" [x] Sent %r" % message)
    connection.close()
except:
    gethelp()