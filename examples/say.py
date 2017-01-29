##########################################################################################
# Example using Windows Speech Synthesizer
# 
##########################################################################################

import clr
clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer

spk = SpeechSynthesizer()
spk.Speak('Hello world!')