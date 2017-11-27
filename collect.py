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
CONSUMER_KEY = ['mJSzhwpofJc5V2Az4NqRz2b18','0geqL4U1pwfC8JGbXilB4RtNU','1y1NlgyVoG5YKCszekhKdMTlv','8LVnYvp8gpX1AdMKwq541TWqf','4aj3DnlWh9jTqpyedzqNjFGls','hzImkAb1PClT6afQy0miQCvlo','epUENTX8TVuY2kRviGYhSHIiK', 'lo9pjYRvU5P9b3hnnwx4pvP4i']
CONSUMER_SECRET = ['SiWhNw9gkFwzl68FTbAhkBsjAyzrN72eavmIEDZ19EbKwoXYj4','ZkGLWeTCfJ2qyHwleOMs4Dnvc7cm1TGR4UZItw8L5iS7AYj0vT','vMwghzFmX3VU1mgXvoL8gYYD4LCPNiP6nFQqQ6vcDpMYqFK8Hu','cSOxoVGn0XxQGuJSOwQzmsDkXIaIKGCqgD28MSfetseApr5UcC','8WCMnlqFtxbJYKpOqj9caAhLO4ELsa2Vqx1bgaeRr957gWn5wf','ZMFYHq16vBTtP5EHgsmrRRXoQquBEjWQsGH1SdeW985LNEHhhA','8NbtV0BGzfhxiSEOTRRi47VYi5fiwt5JK8p3YpW93SdyrgjHpW', 'ND9osNijbp57y6rO9YzThH9nSJBdRD7sdPjlqo9guUZgB9d94U']
ACCESS_TOKEN = ['824623444046348288-E5zdV6s9gSRb3kxKzp5dGdhc4chgInp','550600686-9bXQC1C0YImFREy4yYyaf5x8iDqzlBdy8mt9n6FA','550600686-WINrIOdvm1DZSXyKPeSF1bWkSQT5Bp7hYcJDL1fc','1081485739-LPQkkIOCiQexP6NCfXlltzeJoyqsECay60UTYTS','188476718-H3viJkcqpkejXT4yezIdFdliu6m4bQNruIMQIDvt','934598576709296128-GRb4TYnCQtQjj42UOIFntlucBCskjkQ','345699798-EmDdmFBuFiiL25RCCaM5QZpFvXIEh7h7fsXT5jOy','934509107767332867-uOYfgJUPtaUz98UzuyIhVfNhly71QfX']
ACCESS_SECRET = ['9XMM3CrVFgTVr7eWTLX72UHm43BOLusj51HdB8A4hIoDv','IGork6Dbls2d5IlqdJHbsSdb1xALuuLDQY4AnS8JG8BO7','gEWLt5aybIedxUlSnzUtntLZd4PGhjxytTdf9FtiZMdlP','5PZU28sXW34UDbuJpZsbT23IFEtOaMdl1JbynDj4fFKxI','3vuLrTo2MEMeQvgOVJIAUVUwyqVileCeCPfDKkFahuhcV','q7UFYVObDqVTsXgHySu0nlkUzbSJ8fdlQhuqQGIiw26wq','Q3w6GYecIdFbY3JNW2piwWTWbewlsFGre5DvVCCIL7X13','GG6sGk9I0pq8Gu9m25fRtBHBPZidObESAPxvBztsJKHN4']

count = 0
oauth = OAuth(ACCESS_TOKEN[0], ACCESS_SECRET[0], CONSUMER_KEY[0], CONSUMER_SECRET[0])
twitter_stream = twitter.Twitter(auth=oauth)

def switch():
    global twitter_stream
    global count
    if count <7:
        count+=1
    else:
        count = 0
        print "Sleeping (Rate Limit: Count 0)"
        time.sleep(900)
    print "SWITCH: " + str(count)
    oauth = OAuth(ACCESS_TOKEN[count], ACCESS_SECRET[count], CONSUMER_KEY[count], CONSUMER_SECRET[count])
    twitter_stream = twitter.Twitter(auth=oauth)
    print ACCESS_TOKEN[count] 

def main():
    global twitter_stream
    global count
    f_main = open("richardspencer_origin/names.txt", "a")
    f_main_read = open("richardspencer_origin/names.txt", "r")
    #f_main.write("RichardBSpencer\n")
    read_main = []
    for line in f_main_read:
        line = line.strip('\n')
        read_main.append(line);
    ids = [402181258]
    captured = []
    follow_trump = []
    br = True
    while br:
        try:
            rate_limit_status = twitter_stream.application.rate_limit_status()
            remaining = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
            if remaining<5:
                switch()
                # print "Sleeping (Rate Limit)"
                # time.sleep(900)
            username = (twitter_stream.users.show(user_id=402181258))['screen_name']
            print username
            i1 = (twitter_stream.friends.ids(screen_name=username))
            ids_friends = i1['ids']
            i2 = (twitter_stream.followers.ids(screen_name=username))
            ids_followers = i2['ids']
            for id1 in ids_friends:
                if id1 in ids_followers:
                    if id1 not in ids:
                        ids.append(id1)
                        captured.append(id1)
            br = False
        except Exception as e:
            #print e
            switch()
            #print "Rate Limiting - Sleeping"
            #time.sleep(900)

    print "CAPTURED" + str(captured)

    new_captured =[]
    br2=True
    for x in range(0,2):
        for element in captured:
            while br2:
                try:
                    rate_limit_status = twitter_stream.application.rate_limit_status()
                    remaining = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
                    if remaining<5:
                        print "Sleeping (Rate Limit)"
                        time.sleep(900)
                    p = (twitter_stream.users.show(user_id=element))
                    username = p['screen_name']
                    protected = p['protected']
                    print username
                    if not protected:
                        i1 = (twitter_stream.friends.ids(screen_name=username))
                        ids_friends = i1['ids']
                        i2 = (twitter_stream.followers.ids(screen_name=username))
                        ids_followers = i2['ids']
                        for id1 in ids_friends:
                            if id1 in ids_followers:
                                if id1 not in ids:
                                    ids.append(id1)
                                    new_captured.append(id1)
                    br2=False
                except Exception as e:
                    print e
                    switch()
                # print "Rate Limiting - Sleeping"
                # time.sleep(900)
        captured=new_captured


    print "NOW GOING TO ITERATE: " + str(len(ids))
    read_main = []
    br3=True
    for line in f_main_read:
        line = line.strip('\n')
        read_main.append(line);
    for person in ids:
        read_main.append(person)
        remaining = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
        if remaining<5:
            switch()
            # print "Sleeping (Rate Limit)"
            # time.sleep(900)
        while br3:
            try:
                p = (twitter_stream.users.show(user_id=person))
                username = p['screen_name']
                protected = p['protected']
                if not protected:
                    iterator = twitter_stream.statuses.user_timeline(screen_name=username,count=32000)
                    if username not in read_main:
                        print "writing " + username
                        f_main.write(username + "\n")
                    f = open("richardspencer_origin/"+ username + ".txt", "a")
                    try:
                        f2 = open("richardspencer_origin/"+ username + ".txt", "r")
                        read = []
                        for line in f2:
                            line = json.loads(line)
                            read.append(line['id']);
                        for tweet in iterator:
                            if tweet['id'] not in read:
                                f.write(json.dumps(tweet)+'\n')
                    except:
                        for tweet in iterator:
                            f.write(json.dumps(tweet)+'\n')
                f.close()
                br3=False
            except Exception as e:
                print e
                switch()
            # print "Rate Limiting - Sleeping"
            # time.sleep(900)