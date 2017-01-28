# DISCLAIMER: 
I did not personally write many of the components that I am using. I am standing on the shoulders of many other’s fine work. I’ve merely created an orchestration that I wish to share.

Based on the [mattmakai](https://github.com/mattmakai "mattmakai")/[slack-starterbot](https://github.com/mattmakai/slack-starterbot "slack-starterbot")
author: Matt Makai (matthew.makai@gmail.com) web: http://www.mattmakai.com/
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

Based on the Py-AIML or PyAIML or pyAIML or Program-Y interpreter currently cloned by [creatorrr](https://github.com/creatorrr "creatorrr")/[pyAIML](https://github.com/creatorrr/pyAIML "pyAIML")
author: Cort Stratton (cort@users.sourceforge.net) web: http://pyaiml.sourceforge.net/

# What or who, is Sam?

Sam is a new twist on an old favorite. The use of the [creatorrr](https://github.com/creatorrr "creatorrr")/[pyAIML](https://github.com/creatorrr/pyAIML "pyAIML") interpreter to add personality to a command capable Slackbot using Matt Makai’s [mattmakai](https://github.com/mattmakai "mattmakai")/[slack-starterbot](https://github.com/mattmakai/slack-starterbot "slack-starterbot"). Sounds simple, but the extendibility of Python and the availability of Slack means from you browser, phone, or desktop app, you can control, check and execute anything. Share the output of commands, directly with your team or family. The AIML-Slackbot is intended to leverage the power of Slack as a delivery medium for teams, personal and professional.

Sam also utilizes Twilio to add text capability to your home or office AI. I'm currently working on his Outlook client to add direct email capability will relying on Outlook to manage security and interfacing with Exchange.

He or she has the ability to;

  * Execute builds from Microsoft Team Foundation Server utilizing the [Microsoft](https://github.com/Microsoft "Microsoft")/[tfs-cli](https://github.com/Microsoft/tfs-cli "tfs-cli") tool
  * Locate my bus is utilizing the GTFS feed from my local city
  * Perform health checks on ArcGIS Server

# History

The definition of artificial intelligence (AI) currently refers to intelligent agents that perceive their environment and act upon that to achieve some task. What we call chat-bots, once were called stimulated response artificial intelligence. They are either weak forms of AI with some randomness overlaid a on rule based set of actions or they employ machine learning to analyze a body of conversation to attempt to learn the appropriate conversational response to a given input. As I want Sam to perform as I expect, every time, I have over fit his actionable commands. Over fitting makes the commands less adapted in dynamic situations but ensures reliability of actions taken.

I have been a fan of the simplicity of AIML for many years. No web services to call or rely on, small, light, portable, predictable, personality! Where you want it. Sam is based on the ALICE bot of old. Here is some info on the ALICE bot (AIML) http://www.alicebot.org/about.html. It’s what the PyAIML interpreter is for. The full sets of AIML can be found here, http://www.alicebot.org/downloads/sets.html. You can always create your own custom sets or there are a few floating around the web. Some with encyclopedia like pools of facts and such.

I had the idea of wiring the two together after reading a great article on Full Stack Python by Mr. Matt Makai https://www.fullstackpython.com/blog/build-first-slack-bot-python.html.  He has provided an excellent write up of how to add your bot account to Slack and how to retrieve your token and bot ID.  The framework code is entirely from mattmakai/slack-starterbot.  

# Installation and Dependencies

Before you begin, you’ll need to install some required modules. I recommend utilizing PIP especially if you have Python 2.7.9 or greater. At that release, PIP is installed by default. You can find it separately here, https://pip.pypa.io/en/stable/. Depending on what you intend to use Sam for and how you deploy him, will affect the dependencies naturally.

I am or have successfully deployed Sam on Windows Server 2012, Windows 10, Windows 8.1, Windows 7, Raspbian Jessie, Raspbian Wheezy, Ubuntu 14.04 LTS, and Ubuntu 16.04 LTS. Using Python 2.7.8 through 2.7.13.

I have not tested on Python 3.x.

I also purchased an awesome and affordable voice model with its own engine from a company called Cepstral, http://www.cepstral.com/. With their speech engine, you can have the same voice on Windows and Linux (even the Pi). This is the engine I use in the announcement service and in any other speech synthesis components.

## Installing the Slack Client

Linux:
```
pip install SlackClient
```

Windows:
```
python -m pip install SlackClient
```
