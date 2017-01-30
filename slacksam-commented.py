##########################################################################################
# Sam - Home and Office Automation SRAI
# (SlackSam)
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
# Based on the Py-AIML or PyAIML or pyAIML interpreter currently cloned by creatorrr
# author: Cort Stratton (cort@users.sourceforge.net) web: http://pyaiml.sourceforge.net/
# https://github.com/creatorrr/pyAIML
# 
##########################################################################################

import os
import sys
import platform
import time
from slackclient import SlackClient
import aiml
import marshal
import glob
import operator
import csv

# Optional modules to leverage
#import wikipedia
#import wolframalpha
#from giphypop import translate
#import urllib2
#import json
#import httplib
#import urllib

# Optional module for Wink API integration

#try:
#    import wink
#except ImportError as e:
#    sys.path.append(0, "..")
#    import wink  # lint:ok

# slackbot's ID
BOT_ID = "sam"

# constants
AT_BOT = "<@BOT_ID>"
EXAMPLE_COMMAND = "do"
LOOKUP_COMMAND = "look up"
HEALTH_COMMAND = "health check"
HELP_COMMAND = "help"
TEMP_COMMAND = "temperature"
PICKAMOVIE_COMMAND = "pick a movie"
SEARCHMUSIC_COMMAND = "search music for"
IDMUSIC_COMMAND = "who sings"
SEARCHFILES_COMMAND = "search files for"
SEARCHDOCS_COMMAND = "search documents for"
PICKMUSIC_COMMAND = "pick a song"
HOMEVALUE_COMMAND = "what is the house worth"
APN_COMMAND = "query parcel"
NETFLIXSEARCH_COMMAND = "search netflix for"
THEATERSEARCH_COMMAND = "find movies near"
GIPHY_COMMAND = "gif"
TELLSAM_COMMAND = "announce"

# instantiate Slack client
slack_client = SlackClient("SLACK_TOKEN")

# WolframAlpha connection
#client = wolframalpha.Client('WOLFRAM_KEY')

# AIML Directory
saiml = "/PATH/sam/aiml/"
#saiml = "C:\\PATH\\sam\\aiml\\"

# brain
k = aiml.Kernel()

# setpreds() function
def setpreds():
    with open(saiml + 'preds.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            k.setBotPredicate((row[0]), (row[1]))
    plat = platform.machine()
    osys = os.name
    print "Sam for " + osys
    print "System Architecture " + plat
    #print "Memory " + psutil.virtual_memory()
    k.setBotPredicate("architecture", plat)
    k.setBotPredicate("os", osys)


# get_oldest_file() function found on stackolverflow
def get_oldest_file(files, _invert=False):
    """ Find and return the oldest file of input file names.
    Only one wins tie. Values based on time distance from present.
    Use of `_invert` inverts logic to make this a youngest routine,
    to be used more clearly via `get_youngest_file`.
    """
    gt = operator.lt if _invert else operator.gt
    # Check for empty list.
    if not files:
        return None
    # Raw epoch distance.
    now = time.time()
    # Select first as arbitrary sentinel file, storing name and age.
    oldest = files[0], now - os.path.getmtime(files[0])
    # Iterate over all remaining files.
    for f in files[1:]:
        age = now - os.path.getmtime(f)
        if gt(age, oldest[1]):
            # Set new oldest.
            oldest = f, age
    # Return just the name of oldest file.
    return oldest[0]

# learn() function
def learn(aimlfiles):
    if not aimlfiles:
        k.learn(saiml + "xfind.aiml")
    for f in aimlfiles[1:]:
        k.learn(f)


# brain() function
def brain():
    if os.path.isfile(saiml + "sam.brn"):
        brnfiles = glob.glob(saiml + "*.brn")
        aimlfiles = glob.glob(saiml + "*.aiml")
        brn = get_oldest_file(brnfiles)
        oldage = os.path.getmtime(brn)
        youngaiml = get_youngest_file(aimlfiles)
        youngage = os.path.getmtime(youngaiml)
        testfiles = [brn, youngaiml]
        print testfiles
        oldfile = get_oldest_file(testfiles)
        print "Oldest file:", oldfile
        print 'Brain found:', brn
        print 'Brain age:', oldage
        print 'Newest AIML:', youngaiml
        print 'Newest AIML age:', youngage
        if (oldfile != (saiml + "sam.brn")):
            k.bootstrap(brainFile=saiml + "sam.brn")
        else:
            learn(aimlfiles)
    else:
        learn(aimlfiles)
        setpreds()

    if os.path.isfile(saiml + "sam.ses"):
        sessionFile = file(saiml + "sam.ses", "rb")
        session = marshal.load(sessionFile)
        sessionFile.close()
        for pred,value in session.items():
            k.setPredicate(pred, value, "sam")
    else:
        setpreds()
    k.saveBrain(saiml + "sam.brn")

# based on the slack-starterbot
def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "*"
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    elif command.startswith(HELP_COMMAND):
        try:
            response = "You need some assistance? I can perform many administrative tasks.\n"
#            response += "*look up* <KEYWORDS> - _Experimental_ _command_ to look up a topic. \n" 
#            response += "*query parcel* <APN NO DASHES> - Returns the Assessor information of a given parcel. \n"
#            response += "*what is the house worth* - Returns the Assessor information of the house. \n"
#            response += "*search files for* <KEYWORD> - Queries the home network for files with a given keyword in the filename. \n"
#            response += "*search documents for* <KEYWORD> - Queries the home network for documents with a given keyword in the filename. \n"
#            response += "*search music for* <KEYWORD> - Queries the home network for music with a given keyword in the filename. \n"
#            response += "*pick a movie* - Chooses a movie at random from the known collection of movies. \n"
#            response += "*find movies near* <ZIPCODE> - Searches for movies playing n theaters within 5 miles of the given zipcode. \n"
#            response += "*pick a song* - Chooses a song at random from the known collection of movies. \n"
#            response += "*temperature* - Returns the temperature and weather reports for the house. \n"
#            response += "*who sings* <SONG TITLE> - Queries Gracenote for all songs with a title matching the search criteria. \n"
#            response += "*gif* <KEYWORDS> - Queries GIPHY for he first gif matching the search criteria. \n"
            response += "*test* - Performs a basic SRAI test of Sam's congnitive functions. "
        except:
            response = "My help system is damaged"
#    elif command.startswith(SEARCHMUSIC_COMMAND):
#        trucommand = command
#        trucommand = trucommand.replace("search music for ", "")
#        trucommand = trucommand.replace(" ", "")
#        response = searchmusic(trucommand)
#    elif command.startswith(IDMUSIC_COMMAND):
#        trucommand = command
#        trucommand = trucommand.replace("who sings", "")
#        response = idmusic(trucommand)
#    elif command.startswith(THEATERSEARCH_COMMAND):
#        trucommand = command
#        trucommand = trucommand.replace("find movies near ", "")
#        response = searchtheater(trucommand)
#    elif command.startswith(NETFLIXSEARCH_COMMAND):
#        trucommand = command
#        trucommand = trucommand.replace("search netflix for ", "")
#        response = searchnetflix(trucommand)
#    elif command.startswith(SEARCHFILES_COMMAND):
#        trucommand = command
#        trucommand = trucommand.replace("search files for ", "")
#        trucommand = trucommand.replace(" ", "")
#        response = searchfiles(trucommand)
#    elif command.startswith(SEARCHDOCS_COMMAND):
#        trucommand = command
#        trucommand = trucommand.replace("search documents for ", "")
#        trucommand = trucommand.replace(" ", "")
#        response = searchdocs(trucommand)
#    elif command.startswith(PICKMUSIC_COMMAND):
#        response = pickmusic()
#    elif command.startswith(LOOKUP_COMMAND):
#        try:
#            trucommand = command
#            trucommand = trucommand.replace("look up ", "")
#            res = client.query(trucommand)
#            response = "According to the Wolfram|Alpha super computer...\n"
#            response += (next(res.results).text)
#        except:
#            response = "Unable to locate that topic on the Wolfram|Alpha super computer."
#    elif command.startswith(HEALTH_COMMAND):
#        trucommand = command
#        trucommand = trucommand.replace("health check", "")
#        trucommand = trucommand.replace(" ", "")
#        status = healthcheck(trucommand)
#        if status == 'True':
#            response = "The server is healthy"
#        else:
#            response = "The server is unhealthy"
#    elif command.startswith(PICKAMOVIE_COMMAND):
#        response = pickamovie()
#    elif command.startswith(APN_COMMAND):
#        trucommand = command
#        trucommand = trucommand.replace("query parcel ", "")
#        trucommand = trucommand.replace(" ", "")
#        print trucommand
#        response = lookupapn(trucommand)
#    elif command.startswith(GIPHY_COMMAND):
#        trucommand = command
#        trucommand = trucommand.replace("gif ", "")
#        print trucommand
#        response = giphyget(trucommand)
#    elif command.startswith(TELLSAM_COMMAND):
#        trucommand = command
#        trucommand = trucommand.replace("announce ", "")
#        print trucommand
#        response = tell_sam(trucommand)
#    elif command.startswith(HOMEVALUE_COMMAND):
#        trucommand = command
#        trucommand = trucommand.replace("what is the house worth", "")
#        trucommand = trucommand.replace(" ", "")
#        print trucommand
#        response = homeapn()
#    elif command.startswith(TEMP_COMMAND):
#        try:
#            howhot = tempinfo()
#            response = howhot
#        except:
#            response = "I was unable to connect to the house services"
    else:
        response = k.respond(command, "sam")
    try:
        slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
    except:
        print "Failed to send message"
        sleep(30)
        try:
            slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
        except:
            gethelp()


def gethelp():
#    try:
#        conn = httplib.HTTPSConnection("api.pushover.net:443")
#        conn.request("POST", "/1/messages.json",
#        urllib.urlencode({
#            "token": "PUSH_OVER_TOKEN",
#            "user": "PUSH_OVER_USER",
#            "message": "I am unable to use Slack, please help me.",
#        }), { "Content-type": "application/x-www-form-urlencoded" })
#        conn.getresponse()
#    except:
#        print "Failed to send help push notification"
    try:
        msg = MIMEText("Help, I can't access the internet anymore.")
        bot = "sam@youremail.com"
        person = "you@youremail.com"
        msg['Subject'] = 'Sam needs help'
        msg['From'] = bot
        msg['To'] = person
        s = smtplib.SMTP('SMTP_SERVER')
        s.sendmail(bot, [person], msg.as_string())
        s.quit()
    except:
        print "Failed to send help email"

#def tell_sam(message):
#    try:
#        send = message or "Testing queue"
#        os.system('/usr/bin/python /PATH/sam/emit.py "'+send+'"')
#        response = "Confirmed"
#        return response
#    except:
#        print "Unable to tell announce"
#        response = "Unable to tell announce"
#        return response

#def giphyget(findx):
#    try:
#        needle = findx
#        #img = translate('foo', api_key='bar')
#        try:
#            img = translate(needle)
#        except:
#            print "Unable to translate search words"
#        print (img.url)
#        reply = (img.url) + "\n"
#        print "Powered by GIPHY"
#        reply += "Powered by GIPHY"
#        return reply
#    except:
#        reply = "Giphy is blocking public API access at the moment. \n"
#        reply += "Powered by GIPHY"
#        return reply
            
#def lookupapn(apn):
#    try:
#        apnurl = "http://gis.mcassessor.maricopa.gov/arcgis/rest/services/MaricopaDynamicQueryService/MapServer/3/query?f=json&where=APN%20LIKE%20%27" + apn + "%25%27&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=APN_DASH%2COWNER_NAME%2CPHYSICAL_ADDRESS%2CMAIL_ADDRESS%2CMAIL_ADDR1%2CMAIL_CITY%2CMAIL_STATE%2CMAIL_ZIP%2CPHYSICAL_STREET_NUM%2CPHYSICAL_STREET_DIR%2CPHYSICAL_STREET_NAME%2CPHYSICAL_STREET_TYPE%2CPHYSICAL_CITY%2CPHYSICAL_ZIP%2CLATITUDE%2CLONGITUDE%2CDEED_NUMBER%2CDEED_DATE%2CDEED_CENT%2CSALE_DATE%2CSALE_PRICE%2CMCRNUM%2CMCR_BOOK%2CMCR_PAGE%2CSUBNAME%2CLAND_SIZE%2CLOT_NUM%2CSTR%2CCONST_YEAR%2CLIVING_SPACE%2CINCAREOF%2CTAX_YR_CUR%2CFCV_CUR%2CLPV_CUR%2CTAX_YR_PREV%2CFCV_PREV%2CLPV_PREV%2CAPN%2CJURISDICTION%2CCITY_ZONING%2CFLOOR%2COBJECTID_1&orderByFields=APN%20ASC&outSR=102100"
#        request = urllib2.Request(apnurl)
#        asrresponse = urllib2.urlopen(request)
#        a = json.loads(asrresponse.read())
#        response = "Owner's name: " + str(a['features'][0]['attributes']['OWNER_NAME']) + "\n"
#        response += "Address: " + str(a['features'][0]['attributes']['PHYSICAL_ADDRESS']) + "\n"
#        spaceplus = str(a['features'][0]['attributes']['PHYSICAL_ADDRESS'])
#        spaceplus = spaceplus.replace(" ", "+")
#        response += "Assessor's Website: http://mcassessor.maricopa.gov/mcs.php?q=" + apn + "\n"
#        response += "Assessor's Mapping Website: http://maps.mcassessor.maricopa.gov/?esearch=" + apn + "&slayer=0&exprnum=0" + " \n"
#        response += "Pictometry Website: http://maps.mcassessor.maricopa.gov/ipa.aspx?1=" + str(a['features'][0]['attributes']['LATITUDE']) + "&2=" + str(a['features'][0]['attributes']['LONGITUDE']) + "&a=" + spaceplus
#        print response
#        return response
#    except:
#        print "Unable to query Assessor GIS services or parse output"
#        response = "Unable to query Assessor GIS services or parse output"
#
#def homeapn():
#    try:
#        apn = 'YOUR_PARCEL_APN'
#        #apnurl = "http://gis.mcassessor.maricopa.gov/arcgis/rest/services/MaricopaDynamicQueryService/MapServer/3/query?f=json&where=APN%20LIKE%20%27" + apn + "%25%27&outFields=OWNER_NAME"
#        apnurl = "http://gis.mcassessor.maricopa.gov/arcgis/rest/services/MaricopaDynamicQueryService/MapServer/3/query?f=json&where=APN%20LIKE%20%2730443646%25%27&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=APN_DASH%2COWNER_NAME%2CPHYSICAL_ADDRESS%2CMAIL_ADDRESS%2CMAIL_ADDR1%2CMAIL_CITY%2CMAIL_STATE%2CMAIL_ZIP%2CPHYSICAL_STREET_NUM%2CPHYSICAL_STREET_DIR%2CPHYSICAL_STREET_NAME%2CPHYSICAL_STREET_TYPE%2CPHYSICAL_CITY%2CPHYSICAL_ZIP%2CLATITUDE%2CLONGITUDE%2CDEED_NUMBER%2CDEED_DATE%2CDEED_CENT%2CSALE_DATE%2CSALE_PRICE%2CMCRNUM%2CMCR_BOOK%2CMCR_PAGE%2CSUBNAME%2CLAND_SIZE%2CLOT_NUM%2CSTR%2CCONST_YEAR%2CLIVING_SPACE%2CINCAREOF%2CTAX_YR_CUR%2CFCV_CUR%2CLPV_CUR%2CTAX_YR_PREV%2CFCV_PREV%2CLPV_PREV%2CAPN%2CJURISDICTION%2CCITY_ZONING%2CFLOOR%2COBJECTID_1&orderByFields=APN%20ASC&outSR=102100"
#        request = urllib2.Request(apnurl)
#        asrresponse = urllib2.urlopen(request)
#        a = json.loads(asrresponse.read())
#        response = "For the current tax year of " + str(a['features'][0]['attributes']['TAX_YR_CUR']) + "\n"
#        response += "Current Assessor full cash value: $" + str(a['features'][0]['attributes']['FCV_CUR']) + "\n"
#        response += "Current Assessor limited property value: $" + str(a['features'][0]['attributes']['LPV_CUR']) + "\n"
#        spaceplus = str(a['features'][0]['attributes']['PHYSICAL_ADDRESS'])
#        spaceplus = spaceplus.replace(" ", "+")
#        response += "Assessor's Website: http://mcassessor.maricopa.gov/mcs.php?q=" + apn + "\n"
#        response += "Assessor's Mapping Website: http://maps.mcassessor.maricopa.gov/?esearch=" + apn + "&slayer=0&exprnum=0" + " \n"
#        response += "Pictometry Website: http://maps.mcassessor.maricopa.gov/ipa.aspx?1=" + str(a['features'][0]['attributes']['LATITUDE']) + "&2=" + str(a['features'][0]['attributes']['LONGITUDE']) + "&a=" + spaceplus
#        print response
#        return response
#    except:
#        print "Unable to query Assessor GIS services or parse output"
#        response = "Unable to query Assessor GIS services or parse output"  

#def pickamovie():
#    try:
#        # Get the movie from the movie DB
#        testurl = "http://URL/mdb/pickamovieservice.php"
#        request = urllib2.Request(testurl)
#        movresponse = urllib2.urlopen(request)
#        a = movresponse.read()
#        moviepicked = str(a)
#        print "The movie selected was " + moviepicked + "."
#        response = "The random movie is " + moviepicked + "."
#        return response
#    except:
#        print "Unable to connect to Pick-A-Movie service."
#        response = "Unable to connect to Pick-A-Movie service."
#        return response

#def healthcheck(server):
#    try:
#        testurl = "http://" + server + ".blah"
#        request = urllib2.Request(testurl)
#        agsresponse = urllib2.urlopen(request)
#        a = json.loads(agsresponse.read())
#        response = str(a["success"])
#        return response
#    except:
#        print "Unable to perform health check"

#def searchmusic(findx):
#    try:
#        searchparam = findx
#        testurl = 'http://URL/music/services/musicsearchservice.php?s=' + searchparam
#        request = urllib2.Request(testurl)
#        sbresponse = urllib2.urlopen(request)
#        h = sbresponse.read()
#        a = json.loads(h)
#        response = "I found this in your library...\n"
#        for w in a:
#            print w
#            clean = str(w)
#            #clean = '\\\\URL' + clean.replace("/","\\")
#            clean = 'file://URL' + clean.replace(' ', '%20')
#            response += clean + ' \n'
#        return response
#    except:
#        response = "I am either unable to reach the music search service or your query returned too many results for me to display here."
#        return response

#def searchnetflix(findx):
#    try:
#        searchparam = findx
#        print searchparam
#        searchparam = searchparam.replace(' ', '%20')
#        print searchparam
#        testurl = 'http://netflixroulette.net/api/api.php?title=' + searchparam
#        print testurl
#        request = urllib2.Request(testurl)
#        sbresponse = urllib2.urlopen(request)
#        h = sbresponse.read()
#        print h
#        a = json.loads(h)
#        print a
#        response = "I found...\n"
#        for w in a:
#            clean = w
#            response += clean + ' \n'
#        return response
#    except:
#        response = "I am either unable to reach the Netflix search service or your query returned results I can't display here."
#        return response

#def searchtheater(findx):
#    try:
#        searchparam = findx
#        print searchparam
#        searchparam = searchparam.replace(' ', '%20')
#        print searchparam
#        year, month, day, hour, minute = time.strftime("%Y,%m,%d,%H,%M").split(',')
#        testurl = 'http://data.tmsapi.com/v1.1/movies/showings?startDate=' + year +'-'+month+'-'+day+'&numDays=1&zip=' + searchparam + '&radius=5&units=mi&api_key=YOURKEYHERE'
#        print testurl
#        request = urllib2.Request(testurl)
#        sbresponse = urllib2.urlopen(request)
#        h = sbresponse.read()
#        print h
#        a = json.loads(h)
#        #print a
#        response = "I found the following playing near " + findx + "\n"
#        for w in a:
#            clean = w['title'] + ' - ' + w['shortDescription'] + ' ' + w['officialUrl'] + '\n'
#            response += clean + ' \n'
#        return response
#    except:
#        response = "I am either unable to reach the Gracenote search service or your query returned results I can't display here."
#        return response

#def searchfiles(findx):
#    try:
#        searchparam = findx
#        testurl = 'http://URL/file/services/filesearchservice.php?s=' + searchparam
#        request = urllib2.Request(testurl)
#        sbresponse = urllib2.urlopen(request)
#        h = sbresponse.read()
#        a = json.loads(h)
#        response = "I found this in your library...\n"
#        for w in a:
#            print w
#            clean = str(w)
#            #clean = '\\\\URL' + clean.replace("/","\\")
#            clean = 'file://URL' + clean.replace(' ', '%20')
#            response += clean + ' \n'
#        return response
#    except:
#        response = "I am either unable to reach the file search service or your query returned too many results for me to display here."
#        return response

#def idmusic(findx):
#    try:
#        searchparam = findx
#        print searchparam
#        searchparam = searchparam.replace(' ', '%20')
#        print searchparam
#        testurl = 'http://URL/php-gracenote/gracenotesearchservice.php?s=%22'+searchparam+'%22'
#        print testurl
#        request = urllib2.Request(testurl)
#        sbresponse = urllib2.urlopen(request)
#        h = sbresponse.read()
#        a = json.loads(h)
#        response = "Gracenote had the following...\n"
#        for w in a:
#            print w
#            clean = w['album_artist_name'] + ' has a track with that title on the album ' + w['album_title']
#            response += clean + ' \n'
#        return response
#    except:
#        response = "I am either unable to reach the Gracenote search service or your query returned too many results for me to display here."
#        return response
    
#def searchdocs(findx):
#    try:
#        searchparam = findx
#        testurl = 'http://URL/file/services/documentsearchservice.php?s=' + searchparam
#        request = urllib2.Request(testurl)
#        sbresponse = urllib2.urlopen(request)
#        h = sbresponse.read()
#        a = json.loads(h)
#        response = "I found this in your library...\n"
#        for w in a:
#            print w
#            clean = str(w)
#            clean = 'file://URL' + clean.replace(' ', '%20')
#            response += clean + ' \n'
#        return response
#    except:
#        response = "I am either unable to reach the document search service or your query returned too many results for me to display here."
#        return response

#def pickmusic():
#    try:
#        testurl = 'http://URL/music/services/pickmusicservice.php'
#        request = urllib2.Request(testurl)
#        sbresponse = urllib2.urlopen(request)
#        h = sbresponse.read()
#        a = json.loads(h)
#        response = "I found this in your library...\n"
#        for w in a:
#            print w
#            clean = str(w)
#            clean = 'file://URL' + clean.replace(' ', '%20')
#            response += clean + ' \n'
#        return response
#    except:
#        response = "Unable to reach the music pick service."
#        return response

#def tempinfo():
#    w = wink.init("/PATH/sam/config.cfg")
#
#    if "sensor_pod" not in w.device_types():
#        raise RuntimeError(
#            "you do not have a sensor_pod associated with your account!"
#        )
#
#    c = w.sensor_pod()
#    response = ""
#
#    try:
#        decoded = c.data.get("last_reading")
#        tempstr = (decoded['temperature']* 9/5 + 32)
#        print "The temperature in the office is " + str(tempstr) + " degrees. "
#        response += "The temperature in the office is " + str(tempstr) + " degrees. "
#    except (ValueError, KeyError, TypeError):
#        print "JSON format error"
#
#    # Get the temp upstairs
#    kurl = "http://URL/thermo/tempservice.php"
#    kreq = urllib2.Request(kurl)
#    kresponse = urllib2.urlopen(kreq)
#    thermotemp = kresponse.read()
#    print "The temperature upstairs is " + thermotemp + " degrees. "
#    response += "The temperature upstairs is " + thermotemp + " degrees. "
#
#    # Average Temperature
#    avgindrtmp = (float(thermotemp) + float((decoded['temperature']* 9/5 + 32))) / 2
#    print "The average temperature in the house is " + str(avgindrtmp) + " degrees. "
#    response += "The average temperature in the house is " + str(avgindrtmp) + " degrees. "
#
#    f = urllib2.urlopen('http://api.wunderground.com/api/KEY/geolookup/conditions/q/XX/City.json')
#    json_string = f.read()
#    parsed_json = json.loads(json_string)
#    location = parsed_json['location']['city']
#    temp_f = parsed_json['current_observation']['temp_f']
#    print "Current temperature in %s is: %s. " % (location, temp_f)
#    response += "Current temperature in %s is: %s. " % (location, temp_f)
#    f.close()
#    f = urllib2.urlopen('http://api.wunderground.com/api/KEY/geolookup/conditions/q/XX/City.json')
#    json_string = f.read()
#    parsed_json = json.loads(json_string)
#    location = parsed_json['location']['city']
#    weather = parsed_json['current_observation']['weather']
#    print "Currently %s. " % (weather)
#    response += "Currently %s. " % (weather)
#    f.close()
#    return response

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
                # return text after the @ mention, whitespace removed also .lower() removed from Matt's starter code
                return output['text'].split(AT_BOT)[1].strip(), \
                       output['channel']
    return None, None

if __name__ == "__main__":
    try:
        READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
        if slack_client.rtm_connect():
            brain()
            print("sam online and connected")
            while True:
                command, channel = parse_slack_output(slack_client.rtm_read())
                if command and channel:
                    trucommand = command.replace(": ", "")
                    trucommand = trucommand.replace(":", "")
                    handle_command(trucommand, channel)
                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
    except:
        gethelp()
        print "Slack connection has failed and the bot was closed."
