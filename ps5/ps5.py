# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhaseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()
    def is_phrase_in(self, text):
        text = text.lower()
        for i in string.punctuation:
            text = text.replace(i, ' ')
        # print(text)
        words = text.split()
        # print(words)
        p_words = self.phrase.split()
        # print(p_words)
        ret = False
        for i in range(0, len(words)-len(p_words)+1):
            # print("LOOOOOPOPOP")
            # print (words[i]+" "+p_words[0])
            if words[i] == p_words[0]:
                # print("match")
                ret = True
                for j in range(0, len(p_words)):
                    # print(words[i+j]+" "+p_words[j])
                    if not words[i+j]==p_words[j]:
                        ret = False
                        break
        return ret

# Problem 3
class TitleTrigger(PhaseTrigger):
    def __init__(self, phrase):
        super(TitleTrigger, self).__init__(phrase)
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
class DescriptionTrigger(PhaseTrigger):
    def __init__(self, phrase):
        super(DescriptionTrigger, self).__init__(phrase)
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, time_str):
        self.time = datetime.strptime(time_str, '%d %b %Y %H:%M:%S').replace(tzinfo=pytz.timezone("EST"))

# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self, time_str):
        super(BeforeTrigger, self).__init__(time_str)
    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))<self.time

class AfterTrigger(TimeTrigger):
    def __init__(self, time_str):
        super(AfterTrigger, self).__init__(time_str)
    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))>self.time

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, o_tr):
        self.o_tr = o_tr
    def evaluate(self, story):
        return not self.o_tr.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def evaluate(self, story):
        return self.t1.evaluate(story) and self.t2.evaluate(story)

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def evaluate(self, story):
        return self.t1.evaluate(story) or self.t2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    ret = []
    for i in stories:
        for j in triggerlist:
            if j.evaluate(i):
                ret.append(i)
                break
    return ret


#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    temp = {}
    ret = []
    for line in lines:
        info = line.split(',')
        # print(info)
        name = info[0]
        t= None
        if info[1]=="TITLE":
            t=TitleTrigger(info[2])
            temp[name] = t
        if info[1]=="DESCRIPTION":
            t=DescriptionTrigger(info[2])
            temp[name] = t
        if info[1]=="BEFORE":
            t=BeforeTrigger(info[2])
            temp[name] = t
        if info[1]=="AFTER":
            t=AfterTrigger(info[2])
            temp[name] = t
        if info[1]=="NOT":
            t=NotTrigger(info[2])
            temp[name] = t
        if info[1]=="AND":
            t=AndTrigger(info[2], info[3])
            temp[name] = t
        if info[1]=="OR":
            t=OrTrigger(info[2], info[3])
            temp[name] = t
        if info[0]=="ADD":
            for i in range(1, len(info)):
                # print(info[i])
                ret.append(temp.get(info[i], None))
        
    # print(temp)
    # print(ret)
    return ret



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

