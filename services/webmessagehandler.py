##########################################################################################
# Sam - Home and Office Automation Web Message Handler
# (Sam Web Message Handler)
#
# Version 1.0
#
# Receives messages in a simple URL from other processes
# 
##########################################################################################

from flask import Flask, request, redirect
import pika

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def tell_sam():
    saywhat = request.values.get('Message', None)
    message = request.args.get('s', None)
    print saywhat

    credentials = pika.PlainCredentials('user', 'password')
    parameters = pika.ConnectionParameters('IP_ADDRESS',
                                       PORT,
                                       'queue',
                                       credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='messages', queue=queue_name)

    channel.basic_publish(exchange='messages',
                          routing_key='',
                          body=message)
    print(" [x] Sent '" + message + "'")
    connection.close()
    return "Sent to Sam :" + message

if __name__ == "__main__":
    app.run(host='IP_ADDRESS',port=PORT,debug=True)