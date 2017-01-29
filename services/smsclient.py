##########################################################################################
# Sam - Home and Office Automation SMS Client
# (Sam SMS Client)
#
# Version 1.0
# 
# Py-AIML or PyAIML Interpreter Personality Slackbot
# Used for both home automation and office automation
#
# Requires paid or trial Twilio account
# 
##########################################################################################

from flask import Flask, request, redirect
import twilio.twiml
import socket

app = Flask(__name__)

# Add numbers to this list
callers = {
    "+11234567890": "Me",
    "+10987654321": "You",
}

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""

    from_number = request.values.get('From', None)
    message_body = request.values.get('Body', None)
    if from_number in callers:
        HOST, PORT = "IP_ADDRESS", PORT
        data = message_body

        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(data + "\n")

            # Receive data from the server
            message = sock.recv(1024)
            resp = twilio.twiml.Response()
            resp.message(message)
        finally:
            sock.close()
    else:
        message = "Thanks for the message!"

    return str(resp)

if __name__ == "__main__":
    app.run(host='IP_ADDRESS',port=PORT,debug=False)
