# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import twitter
import time
# Variables that contains the user credentials to access Twitter API 
CONSUMER_KEY = ['0geqL4U1pwfC8JGbXilB4RtNU','CRMtmyS4l0abey0COyV4g5I9J','8LVnYvp8gpX1AdMKwq541TWqf','4aj3DnlWh9jTqpyedzqNjFGls','hzImkAb1PClT6afQy0miQCvlo','epUENTX8TVuY2kRviGYhSHIiK', 'lo9pjYRvU5P9b3hnnwx4pvP4i']
CONSUMER_SECRET = ['ZkGLWeTCfJ2qyHwleOMs4Dnvc7cm1TGR4UZItw8L5iS7AYj0vT','lmYM48LEpTvUGIcPYRqxYWtRBJoxUzS9SzHlNj9U374O0Axxm','cSOxoVGn0XxQGuJSOwQzmsDkXIaIKGCqgD28MSfetseApr5UcC','8WCMnlqFtxbJYKpOqj9caAhLO4ELsa2Vqx1bgaeRr957gWn5wf','ZMFYHq16vBTtP5EHgsmrRRXoQquBEjWQsGH1SdeW985LNEHhhA','8NbtV0BGzfhxiSEOTRRi47VYi5fiwt5JK8p3YpW93SdyrgjHpW', 'ND9osNijbp57y6rO9YzThH9nSJBdRD7sdPjlqo9guUZgB9d94U']
ACCESS_TOKEN = ['550600686-9bXQC1C0YImFREy4yYyaf5x8iDqzlBdy8mt9n6FA','29587323-4QDgoil3LrsyMejgYXqOtoDsX1tNGiil8zcQoW4dc','1081485739-LPQkkIOCiQexP6NCfXlltzeJoyqsECay60UTYTS','188476718-H3viJkcqpkejXT4yezIdFdliu6m4bQNruIMQIDvt','934598576709296128-GRb4TYnCQtQjj42UOIFntlucBCskjkQ','345699798-EmDdmFBuFiiL25RCCaM5QZpFvXIEh7h7fsXT5jOy','934509107767332867-uOYfgJUPtaUz98UzuyIhVfNhly71QfX']
ACCESS_SECRET = ['IGork6Dbls2d5IlqdJHbsSdb1xALuuLDQY4AnS8JG8BO7','vVatIUyXz0mQ87Ro2amYdHFR7KvkyeDR8cCGEtcjsDvvT','5PZU28sXW34UDbuJpZsbT23IFEtOaMdl1JbynDj4fFKxI','3vuLrTo2MEMeQvgOVJIAUVUwyqVileCeCPfDKkFahuhcV','q7UFYVObDqVTsXgHySu0nlkUzbSJ8fdlQhuqQGIiw26wq','Q3w6GYecIdFbY3JNW2piwWTWbewlsFGre5DvVCCIL7X13','GG6sGk9I0pq8Gu9m25fRtBHBPZidObESAPxvBztsJKHN4']

count = 0
oauth = OAuth(ACCESS_TOKEN[0], ACCESS_SECRET[0], CONSUMER_KEY[0], CONSUMER_SECRET[0])
twitter_stream = twitter.Twitter(auth=oauth)

def switch(count):
    print "SWITCH"
    oauth = OAuth(ACCESS_TOKEN[count], ACCESS_SECRET[count], CONSUMER_KEY[count], CONSUMER_SECRET[count])
    twitter_stream = twitter.Twitter(auth=oauth)
    try:
        info = (twitter_stream.users.show(user_id=person))
    except Exception as e:
        print "Sleeping (Rate Limit)"
        time.sleep(900)


def main():
    global count
    f_main = open("richardspencer_origin/names.txt", "a")
    f_main_read = open("richardspencer_origin/names.txt", "r")
    #f_main.write("RichardBSpencer\n")
    read_main = []
    for line in f_main_read:
        line = line.strip('\n')
        read_main.append(line);
    screen_names = []
    ids = [402181258]
    marked = []
    follow_trump = []
    limit = 0;

    #get list of names 2 levels deep
    #for x in range(0,2):
        #print x
    for person in ids:
        while limit <70:
            try:
                print "LIMIT: " + str(limit)
                if limit < 70:
                    limit+=1
                    rate_limit_status = twitter_stream.application.rate_limit_status()
                    remaining = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
                    if remaining<5:
                        if count<6:
                            count+=1
                        else:
                            count =0
                        switch(count)
                        # print "Sleeping (Rate Limit)"
                        # time.sleep(900)
                    print "about to print user name"
                    info = (twitter_stream.users.show(user_id=person))
                    username = info['screen_name']
                    protected = info['protected']
                    print username
                    if not protected:
                        i1 = (twitter_stream.friends.ids(screen_name=username))
                        ids_friends = i1['ids']
                        i2 = (twitter_stream.followers.ids(screen_name=username))
                        ids_followers = i2['ids']
                        if 25073877 in ids_friends or 25073877 in ids_followers:
                            follow_trump.append(username)
                        for id1 in ids_friends:
                            if id1 in ids_followers:
                                if id1 not in ids:
                                    ids.append(id1)
                    #marked.append(id_num)
                if not protected:
                #screen_names.append(username['screen_name'])
                    iterator = twitter_stream.statuses.user_timeline(screen_name=username,count=32000)
                    print read_main
                    if username not in read_main:
                        read_main.append(username.encode('utf-8'))
                        f_main.write(username + "\n")
                    f = open("richardspencer_origin/"+ username + ".txt", "a")
                    try:
                        f2 = open("richardspencer_origin/"+ username + ".txt", "r")
                        read = []
                        for line in f2:
                            line = line.strip('\n')
                            read.append(line);
                        for tweet in iterator:
                            if tweet not in read:
                                f.write(json.dumps(tweet)+'\n')
                    except:
                        for tweet in iterator:
                            f.write(json.dumps(tweet)+'\n')
                    f.close()
            except Exception as e:
                print e
                if count<6:
                    count+=1
                else:
                    count =0
                switch(count)
                # print "Rate Limiting - Sleeping"
                # time.sleep(900)
                continue
            break