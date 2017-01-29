# DISCLAIMER: 
I did not personally write many of the components that I am using. I am standing on the shoulders of many other’s fine work. I’ve merely created an orchestration that I wish to share.

Based on the [mattmakai](https://github.com/mattmakai "mattmakai")/[slack-starterbot](https://github.com/mattmakai/slack-starterbot "slack-starterbot")
author: Matt Makai (matthew.makai@gmail.com) web: http://www.mattmakai.com/
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

Based on the Py-AIML or PyAIML or pyAIML or Program-Y interpreter currently cloned by [creatorrr](https://github.com/creatorrr "creatorrr")/[pyAIML](https://github.com/creatorrr/pyAIML "pyAIML")
author: Cort Stratton (cort@users.sourceforge.net) web: http://pyaiml.sourceforge.net/

# What is Slack?

[Slack.com](https://slack.com/ "Slack.com") has a video explaining all you need to know on YouTube [What is Slack?](https://youtu.be/9RJZMSsH7-g "What is Slack?")

# What or who, is Sam?

Sam is a new twist on an old favorite. The use of the [creatorrr](https://github.com/creatorrr "creatorrr")/[pyAIML](https://github.com/creatorrr/pyAIML "pyAIML") interpreter to add personality to a command capable Slackbot using Matt Makai’s [mattmakai](https://github.com/mattmakai "mattmakai")/[slack-starterbot](https://github.com/mattmakai/slack-starterbot "slack-starterbot"). Sounds simple, but the extendibility of Python and the availability of Slack means from you browser, phone, or desktop app, you can control, check and execute anything. Share the output of commands, directly with your team or family. The AIML-Slackbot is intended to leverage the power of Slack as a delivery medium for teams, personal and professional.

Sam also utilizes Twilio to add text capability to your home or office AI. I'm currently working on his Outlook client to add direct email capability will relying on Outlook to manage security and interfacing with Exchange.

He or she has the ability to;

  * Execute builds from Microsoft Team Foundation Server utilizing the [Microsoft](https://github.com/Microsoft "Microsoft")/[tfs-cli](https://github.com/Microsoft/tfs-cli "tfs-cli") tool
  * Locate my bus is utilizing the GTFS feed from my local city
  * Perform health checks on ArcGIS Server
  * Call a web service or URL to GET or POST data
  * Look up a song
  * Find a movie playing nearby
  * Ask the Wolfram|Alpha Super Computer Cluster a question
  * Pull a random gif from GIPHY using [shaunduncan](https://github.com/shaunduncan "shaunduncan")/[giphypop](https://github.com/shaunduncan/giphypop "giphypop")
  * Start/Stop/Restart services on another machine
  * Check the status of a service on another machine
  * List open files on your web server
  * List logins on your servers
  * Query your help desk(s)
  * Query your monitoring solution(s)
  * Query data from a database
  * Query data from Elasticsearch
  * Control or query your IoT devices
  * Interface with an alarm system

Anything you can script, you can enable for yourself, your team or your family and friends.

# History

The definition of artificial intelligence (AI) currently refers to intelligent agents that perceive their environment and act upon that to achieve some task. What we call chat-bots, once were called stimulated response artificial intelligence. They are either weak forms of AI with some randomness overlaid a on rule based set of actions or they employ machine learning to analyze a body of conversation to attempt to learn the appropriate conversational response to a given input. As I want Sam to perform as I expect, every time, I have over fit his actionable commands. Over fitting makes the commands less adapted in dynamic situations but ensures reliability of actions taken.

I have been a fan of the simplicity of AIML for many years. No web services to call or rely on, small, light, portable, predictable, personality! Where you want it. Sam is based on the ALICE bot of old. Here is some info on the ALICE bot (AIML) http://www.alicebot.org/about.html. It’s what the PyAIML interpreter is for. The full sets of AIML can be found here, http://www.alicebot.org/downloads/sets.html. You can always create your own custom sets or there are a few floating around the web. Some with encyclopedia like pools of facts and such.

I had the idea of wiring the two together after reading a great article on Full Stack Python by Mr. Matt Makai https://www.fullstackpython.com/blog/build-first-slack-bot-python.html.  He has provided an excellent write up of how to add your bot account to Slack and how to retrieve your token and bot ID.  The framework code is entirely from mattmakai/slack-starterbot.  

# Installation and Dependencies

Before you begin, you’ll need to install some required modules. I recommend utilizing PIP especially if you have Python 2.7.9 or greater. At that release, PIP is installed by default. You can find it separately here, https://pip.pypa.io/en/stable/. Depending on what you intend to use Sam for and how you deploy him, will affect the dependencies naturally.

I am or have successfully deployed Sam on Windows Server 2012, Windows 10, Windows 8.1, Windows 7, Raspbian Jessie, Raspbian Wheezy, Ubuntu 14.04 LTS, and Ubuntu 16.04 LTS. Using Python 2.7.8 through 2.7.13.

I have not tested on Python 3.x.

I am utilizing Advanced Message Queuing Protocol (AMQP) https://www.amqp.org/ exchanges to route messages from various sources. Utilizing them for asynchronous messages “FROM” the bot give you a means to thread heavy processes and return results later and gives the illusion that the bot is actively performing human work. In reality, the threaded process is doing what it needs and returns the response later. We are able to feed alerts to or through the bot. Alerts can be reported to the team as though they came directly from the bot.

I prefer RabbitMQ, the open source messaging queue https://www.rabbitmq.com/. The deployment, configuration, and administration of Rabbit are not part of this documentation but their website has excellent step by step examples in Python. RabbitMQ runs great on a RaspberryPi too.

I also purchased an awesome and affordable voice model with its own engine from a company called Cepstral, http://www.cepstral.com/. With their speech engine, you can have the same voice on Windows and Linux (even the Pi). This is the engine I use in the announcement service and in any other speech synthesis components.

NOTE: Installations should be performed "as administrator" in Windows or using "sudo" in Linux.

## Installing the required Py-AIML

Linux:
```
sudo python /PATH/setup.py install
```

Windows:
```
python /PATH/setup.py install
```

## Installing the Required Slack Client

Linux:
```
sudo pip install SlackClient
```

Windows:
```
python -m pip install SlackClient
```

## Installing the Optional Pika Client (to use AMPQ messaging queues)

Linux:
```
sudo pip install pika
```

Windows:
```
python -m pip install pika
```

# Running Sam

Before Sam will run, it will need to have a few edits made.

## Required edits

Edit slacksam.py and update the Slack bot ID to your Slackbot's name

```python
AT_BOT = "<@BOT_ID>"
```

Edit slacksam.py and update the Slack token to your Slack team's token

```python
slack_client = SlackClient("SLACK_TOKEN")
```

Edit slacksam.py and update the path to your AIML files and or compiled brain

Linux:
```python
saiml = "/PATH/sam/aiml/"
```

Windows:
```python
saiml = "C:\\PATH\\sam\\aiml\\"
```

## Starting Sam Up

Running only the Slackbot fairly straightforward. You execute python and pass slacksam.py as an argument.

```cmd
python slacksam.py
```

You may have to include the full path to python if you didn't include Python in your PATH environment variables.

Linux:
```sh
sudo /usr/bin/python slacksam.py
```

Windows:
```cmd
C:\PATH\python slacksam.py
```
