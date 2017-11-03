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
ACCESS_TOKEN = '550600686-9bXQC1C0YImFREy4yYyaf5x8iDqzlBdy8mt9n6FA'
ACCESS_SECRET = 'IGork6Dbls2d5IlqdJHbsSdb1xALuuLDQY4AnS8JG8BO7'
CONSUMER_KEY = '0geqL4U1pwfC8JGbXilB4RtNU'
CONSUMER_SECRET = 'ZkGLWeTCfJ2qyHwleOMs4Dnvc7cm1TGR4UZItw8L5iS7AYj0vT'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_stream = twitter.Twitter(auth=oauth)

def main():
    f_main = open("richardspencer_origin/names.txt", "a")
    f_main_read = open("richardspencer_origin/names.txt", "r")
    f_main.write("RichardBSpencer\n")
    read_main = []
    for line in f_main_read:
        line = line.strip('\n')
        read_main.append(line);
    screen_names = []
    ids = [402181258]
    marked = []
    follow_trump = []

    #get list of names 2 levels deep
    #for x in range(0,2):
        #print x
    for person in ids:
        try:
            #print person
            rate_limit_status = twitter_stream.application.rate_limit_status()
            remaining = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
            if remaining<5:
                print "Sleeping (Rate Limit)"
                time.sleep(900)
            username = (twitter_stream.users.show(user_id=person))['screen_name']
            print username
            i1 = (twitter_stream.friends.ids(screen_name=username))
            ids_friends = i1['ids']
            i2 = (twitter_stream.followers.ids(screen_name=username))
            ids_followers = i2['ids']
            for id1 in ids_friends:
                if id1 in ids_followers:
                    if id1 not in ids:
                        ids.append(id1)
            #print ids
            for id_num in ids:
                if id_num not in marked:
                #marked.append(id_num)
                    p = (twitter_stream.users.show(user_id=id_num))
                    username = p['screen_name']
                    protected = p['protected']
                    marked.append(id_num)
                    if not protected:
                    #screen_names.append(username['screen_name'])
                        iterator = twitter_stream.statuses.user_timeline(screen_name=username,count=32000)
                        print username
                        if username not in read_main:
                            screen_names.append(username)
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
            print "Rate Limiting - Sleeping"
            time.sleep(900)