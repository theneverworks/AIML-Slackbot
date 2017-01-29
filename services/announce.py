##########################################################################################
# Sam - Home and Office Automation SRAI Announcement Service
# (Sam Windows Announcement Service)
#
# Version 1.0
# 
# Speaks out loud via Cepstral swift, messages received through message queues.
# Could be rewired to use Windows Speech Engine.
#
##########################################################################################

import os
import sys
import pika


def main():
    #!/usr/bin/env python
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
        os.system('swift ' + body)

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


if __name__ == '__main__':
    print 'Sam Voice Starting...'
    main()