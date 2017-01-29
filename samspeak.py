
##########################################################################################
# Sam - Home and Office Automation SRAI Windows Speech Recognition Engine
# (Sam Windows Speech Recognition Engine)
#
# Version 1.0
# 
# Accepts spoken input utilizing Windows Speech Recognition capabilities.
#
##########################################################################################

import socket
import sys
import clr
clr.AddReference("System.Speech, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35")
from System.Speech.Recognition import (SpeechRecognitionEngine, GrammarBuilder,
        Grammar, Choices, RecognizeMode)
clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer

count = 0
lastsaid = ''


def main():
    sre = SpeechRecognitionEngine()
    sre.SetInputToDefaultAudioDevice()
    sre.UnloadAllGrammars()
    spk = SpeechSynthesizer()

    gb = GrammarBuilder()
    gb.Append(Choices('sam'))
    gb.AppendDictation()
    sre.LoadGrammar(Grammar(gb))

    HOST, PORT = "localhost", 9999

    def OnSpeechRecognized(sender, e):
        sre.RecognizeAsyncStop()
        if ((e.Result.Text[:3] == 'sam')):
            print 'Heard: %s' % (e.Result.Text[4:])
            try:
                # Connect to server and send data
                try:
                    # Create a socket (SOCK_STREAM means a TCP socket)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((HOST, PORT))
                except:
                    print "Unable to open a connection to the brain"
                try:
                    data = e.Result.Text[4:]
                except:
                    print "Unable to set captured text to data variable"
                try:
                    sock.sendall(data + "\n")
                except:
                    print "Unable to send data to the brain"
                # Receive data from the server and speak it
                try:
                    received = sock.recv(1024)
                except:
                    print "Unable to set received data to received variable"
                try:
                    sock.close()
                except:
                    print "Unable to close the connection"
                try:
                    print "Sent:     {}".format(data)
                    print "Received: {}".format(received)
                except:
                    print "Unable to print a simple line"
                try:
                    spk.Speak(received)
                except:
                    print "Unable to speak received data"
            except:
                print "Unable to communicate with the brain."
        sre.RecognizeAsync(RecognizeMode.Multiple)

    sre.SpeechRecognized += OnSpeechRecognized
    sre.RecognizeAsync(RecognizeMode.Multiple)
    raw_input('Press ENTER to quit\n\n')

if __name__ == '__main__':

    if sys.platform == 'cli':
        from System.Threading import Thread, ThreadStart
        thread = Thread(ThreadStart(main))
        thread.Start()
    else:
        main()