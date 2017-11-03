try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import twitter
import os
import time
import operator
# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '550600686-9bXQC1C0YImFREy4yYyaf5x8iDqzlBdy8mt9n6FA'
ACCESS_SECRET = 'IGork6Dbls2d5IlqdJHbsSdb1xALuuLDQY4AnS8JG8BO7'
CONSUMER_KEY = '0geqL4U1pwfC8JGbXilB4RtNU'
CONSUMER_SECRET = 'ZkGLWeTCfJ2qyHwleOMs4Dnvc7cm1TGR4UZItw8L5iS7AYj0vT'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = twitter.Twitter(auth=oauth)
common_words = []
common = open("commonwords.txt", "r")
for line in common:
	common_words.append(line[:-1])

news_sources = ['@alyssa_milano','@erictrump','@foxbusiness','@sarahpalinusa','@piersmorgan','@politico','@nancypelosi','@espn','@nba','@gop','@tedcruz','@sethrogen','@abcnews','@dnc','@nbcnews','@corey_feldman','@foxnewsinsider','@chargers','@randpaul','@benaffleck','@ivankatrump','@whitehouse','@msnbc','@nra','@usatoday','@cbs','@mike_pence','@billoreilly','@fbi','@richardbspencer','@senwarren','@thedailybeast','@youtube', '@billclinton', '@harveyweinstein', '@huffpost', '@tmz', '@speakerryan','@jimmykimmellive', '@michelleobama', '@presssec', '@julianassange', '@ap','@cnn','@barackobama', '@vp', '@flotus', '@abc', '@thehill', '@wikileaks', '@nfl', '@buzzfeednews', '@potus', '@reuters', '@arianagrande', '@realdonaldtrump', '@hillaryclinton', '@bbcworldwide', '@breitbartnews', '@nytimes', '@washingtonpost', '@drudge_report']
news_sources2 = ['alyssa_milano','erictrump','foxbusiness','sarahpalinusa','piersmorgan','politico','nancypelosi','espn','nba','gop','tedcruz','sethrogen','abcnews','dnc','nbcnews','corey_feldman','foxnewsinsider','chargers','randpaul','benaffleck','ivankatrump','whitehouse','msnbc','nra','usatoday','cbs','mike_pence','billoreilly','fbi','richardbspencer','senwarren','thedailybeast','youtube','billclinton', 'harveyweinstein', 'huffpost', 'tmz', 'speakerryan','jimmykimmellive', 'michelleobama', 'presssec', 'julianassange', 'ap','cnn','barackobama', 'vp', 'flotus', 'abc', 'thehill', 'wikileaks', 'nfl', 'buzzfeednews', 'potus', 'reuters', 'arianagrande', 'realdonaldtrump', 'hillaryclinton', 'bbcworldwide', 'breitbartnews', 'nytimes', 'washingtonpost', 'drudge_report']
alt = ['jew', 'holocaust', 'holohoax', 'unbonjuif', 'juif', '1488', '1488RS', 'Heil', 'Heil Hitler', 'Cuckservative', '(((', ')))', 'Dindu Nuffin', 'Ghost Skin', 'Trumpwave', 'Deus Vult', 'Masculinist', 'God Emperor']
rate_limit_check_remaining = 180
suspended = []

#gather words from all tweets of all users from the network parameter
def gather_words(network, mentioned):
	if mentioned:
		f_main = open(network+"/used_names.txt", "r")
	else:
		f_main = open(network+"/names.txt", "r")
	alt_words = {}
	for line in f_main:
		if mentioned:
			l = line.strip('\n')
			#print l
		else:
			l = line[:-1]
		try:
			#print l
			file_name = network + '/' + l + '.txt'
			#print file_name
			with open(file_name, "r") as f_temp:
				read = []
				for line in f_temp:
					line = line.strip('\n')
					read.append(line);
				#print read
				for tweet in read:
					try:
						#print tweet
					 	t = json.loads(tweet)
					 	tweet_text = (t['text']).split()
					 	for word in tweet_text:
					 		#remove words that are from the most common list of words in the English language
					 		if word.lower() not in common_words:
						 		if word.lower() in alt_words:
						 			alt_words[word.lower()] = alt_words[word.lower()]+1
						 		else:
						 			alt_words[word.lower()] = 1
						#print alt_words
					except:
						print "Interrupted Tweet"
		except:
			#print l
			print "Account Does not Exist"
	return alt_words

#sort words by # of mentions
def maxWords(wordDict):
	return sorted(wordDict.items(), key=operator.itemgetter(1))

	# response=""
	# for key, value in sorted(wordDict.iteritems(), key=lambda (k,v): (v,k)):
	# 	response = response + ", " + ("%s: %s" % (key, value))
	# return response
#gather words that hit the "alt" words collected terms
def alt_words(wordDict):
	adj_list = {}
	for word in wordDict:
		if word.lower() in alt:
			adj_list[word] = wordDict[word]
	sortedList2 = sorted(adj_list.items(), key=operator.itemgetter(1))
	return sortedList2

#create the list usernames most frequently mentioned
def gather_mentioned(wordDict):
	f_main = open("mentioned_network/names.txt", "a")
	f_main_read = open("mentioned_network/names.txt", "r")
	read = []
	for line in f_main_read:
		line = line.strip('\n')
		read.append(line);
	#print read
	new_users={}
	for key in wordDict:
		if '@' in key:
			if wordDict[key] >100:
			#add to list of new users
				try:
					user = key.encode('utf-8')
					value = wordDict[key]
					index = user.index('@')
					user = user[index+1:]
					if ':' in user:
						user = user[:-1]
					new_users[user] = value
					#print new_users[user]
					if user not in read:
						#print user
						f_main.write(user+'\n')
				except:
					print "Unable to write"
	return new_users

#generate files corresponding to the tweets of users
def mentioned_tweets(file_name):
	global rate_limit_check_remaining
	if rate_limit_check_remaining < 5:
		print "SLEEP (rate limit)"
		rate_limit_check_remaining = 180
		time.sleep(900)
	with open(file_name+"/names.txt") as f_main:
		for line in f_main:
			f_used = open("mentioned_network/used_names.txt", "a")
			f_used_read = open("mentioned_network/used_names.txt", "r")
			read_test = []
			for l in f_used_read:
				w = l.strip('\n')
				read_test.append(w)
			#print read_test
			rate_limit_status = twitter_stream.application.rate_limit_status()
			remaining = rate_limit_status["resources"]["statuses"]["/statuses/user_timeline"]["remaining"]
			remaining2 = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
			rate_limit_check_remaining -= 1
			if remaining<5:
				print "SLEEP (rate limit of user_timeline)"
				time.sleep(900)
			elif remaining2 < 5:
				print "SLEEP (rate limit of friend list)"
				time.sleep(900)
			elif rate_limit_check_remaining<5:
				print "SLEEP (rate limit of remaining count)"
				time.sleep(900)
			username = line.strip('\n')
			if username not in news_sources2:
				try:
					if not suspension_check(username):
						p = (twitter_stream.users.show(screen_name=username))
						protected = p['protected']
						if not protected:
							if username not in read_test:
								f_used.write(username + '\n')
								#print username
							iterator = twitter_stream.statuses.user_timeline(screen_name=username,count=32000)
							print username
							f = open(file_name + "/"+ username + ".txt", "a")
							#print "here1"
							try:
								#print "here2"
								f2 = open(file_name + "/"+ username  + ".txt", "r")
								read = []
								for line in f2:
									line = line.strip('\n')
									read.append(line);
								for tweet in iterator:
									if tweet not in read:
										f.write(json.dumps(tweet)+'\n')
							except Exception as e:
								print e
								print "Unable to write"
				except:
					print "Username does not exist"
				f_used.close;

#check if a user has been suspended
def suspension_check(name):
	global suspended
	global rate_limit_check_remaining
	if rate_limit_check_remaining < 5:
		print "SLEEP (rate limit)"
		rate_limit_check_remaining = 180
		time.sleep(900)
	rate_limit_status = twitter_stream.application.rate_limit_status()
	rate_limit_check_remaining -= 1	
	remaining = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
	if remaining<5:
		print "SLEEP (rate limit)"
		time.sleep(900)
	try:
		p = twitter_stream.users.show(screen_name=name)
		#print "Not Suspended"
		return False
	except:
		print "Suspended"
		suspended.append(name)
		return True

#check if a user is protected
def protected_check(name):
	global rate_limit_check_remaining
	if rate_limit_check_remaining < 5:
		print "SLEEP (rate limit)"
		rate_limit_check_remaining = 180
		time.sleep(900)
	rate_limit_status = twitter_stream.application.rate_limit_status()
	rate_limit_check_remaining -= 1	
	remaining = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
	if remaining<5:
		print "SLEEP (rate limit)"
		time.sleep(900)
	try:
		p = twitter_stream.users.show(screen_name=name)
	except:
		print "SLEEP (except)"
		time.sleep(900)
	return p['protected']

#determine users in a network who are suspended
def gather_suspenders():
	suspended = []
	f_write = open("suspended.txt", "a")
	with open("mentioned_network/names.txt") as f_main:
		for line in f_main:
			line = line.strip('\n')
			sus = suspension_check(line)
			if sus:
				print line
				f_write.write(line + '\n')
				suspended.append(line)
	return suspended


#determine the ratio of Trump followers
def trump_check(network):
	f_main = open(network+"/names.txt", "r")
	trump_followers = []
	count = 1
	for line in f_main:
		count +=1
		username = line[:-1]
		if suspension_check(username) is False:
			if protected_check(username) is False:
				time.sleep(60)
				i1 = (twitter_stream.friends.ids(screen_name=username))
				ids_friends = i1['ids']
				for id1 in ids_friends:
					if id1 == 25073877:
						trump_followers.append(ids_friends)
	count = count*1.0
	ratio = len(trump_followers)/count
	return ratio