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
    ids = [402181258]
    captured = []
    follow_trump = []

    try:
        rate_limit_status = twitter_stream.application.rate_limit_status()
        remaining = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
        if remaining<5:
            print "Sleeping (Rate Limit)"
            time.sleep(900)
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
    except Exception as e:
        print e
        print "Rate Limiting - Sleeping"
        time.sleep(900)

    for element in captured:
        try:
            rate_limit_status = twitter_stream.application.rate_limit_status()
            remaining = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
            if remaining<5:
                print "Sleeping (Rate Limit)"
                time.sleep(900)
            username = (twitter_stream.users.show(user_id=element))['screen_name']
            print username
            i1 = (twitter_stream.friends.ids(screen_name=username))
            ids_friends = i1['ids']
            i2 = (twitter_stream.followers.ids(screen_name=username))
            ids_followers = i2['ids']
            for id1 in ids_friends:
                if id1 in ids_followers:
                    if id1 not in ids:
                        ids.append(id1)
        except Exception as e:
            print e
            print "Rate Limiting - Sleeping"
            time.sleep(900)

    for person in ids:
        remaining = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
        if remaining<5:
            print "Sleeping (Rate Limit)"
            time.sleep(900)
        try:
            p = (twitter_stream.users.show(user_id=person))
            username = p['screen_name']
            protected = p['protected']
            if not protected:
                iterator = twitter_stream.statuses.user_timeline(screen_name=username,count=32000)
                print username
                if username not in read_main:
                    f_main.write(username + "\n")
                f = open("richardspencer_origin/"+ username + ".txt", "a")
                try:
                    f2 = open("richardspencer_origin/"+ username + ".txt", "r")
                    read = []
                    for line in f2:
                        line = ljson.loads(line)
                        read.append(line['id']);
                    for tweet in iterator:
                        if tweet['id'] not in read:
                            f.write(json.dumps(tweet)+'\n')
                except:
                    for tweet in iterator:
                        f.write(json.dumps(tweet)+'\n')
            f.close()
        except Exception as e:
            print e
            print "Rate Limiting - Sleeping"
            time.sleep(900)