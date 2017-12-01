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
import requests

# Variables that contains the user credentials to access Twitter API 
CONSUMER_KEY = ['fxXuwQ7nFDIZNSTvhVMAJ7Cpc','qLJrd7u7fVtFqnRgvYPaebdrz','mJSzhwpofJc5V2Az4NqRz2b18','0geqL4U1pwfC8JGbXilB4RtNU','1y1NlgyVoG5YKCszekhKdMTlv','8LVnYvp8gpX1AdMKwq541TWqf','4aj3DnlWh9jTqpyedzqNjFGls','hzImkAb1PClT6afQy0miQCvlo','epUENTX8TVuY2kRviGYhSHIiK', 'lo9pjYRvU5P9b3hnnwx4pvP4i']
CONSUMER_SECRET = ['5ZCwhLKkd1dSPnBcq24a6g1uRjDHYrsEns07TPzfMJDkefZIj0','7rVTvqAQlBVKKgKuEV6WRWoWPFoXtp0K2KStzgcQ3xHqCaiV4g','SiWhNw9gkFwzl68FTbAhkBsjAyzrN72eavmIEDZ19EbKwoXYj4','ZkGLWeTCfJ2qyHwleOMs4Dnvc7cm1TGR4UZItw8L5iS7AYj0vT','vMwghzFmX3VU1mgXvoL8gYYD4LCPNiP6nFQqQ6vcDpMYqFK8Hu','cSOxoVGn0XxQGuJSOwQzmsDkXIaIKGCqgD28MSfetseApr5UcC','8WCMnlqFtxbJYKpOqj9caAhLO4ELsa2Vqx1bgaeRr957gWn5wf','ZMFYHq16vBTtP5EHgsmrRRXoQquBEjWQsGH1SdeW985LNEHhhA','8NbtV0BGzfhxiSEOTRRi47VYi5fiwt5JK8p3YpW93SdyrgjHpW', 'ND9osNijbp57y6rO9YzThH9nSJBdRD7sdPjlqo9guUZgB9d94U']
ACCESS_TOKEN = ['935175983413506048-68cAX9prYfLo3hQm7AkupOIpWiO7TAW','935172108539367424-4RaiEEY9FNkcMmr0IDdsfQ7ntvHwHCM','824623444046348288-E5zdV6s9gSRb3kxKzp5dGdhc4chgInp','550600686-9bXQC1C0YImFREy4yYyaf5x8iDqzlBdy8mt9n6FA','550600686-WINrIOdvm1DZSXyKPeSF1bWkSQT5Bp7hYcJDL1fc','1081485739-LPQkkIOCiQexP6NCfXlltzeJoyqsECay60UTYTS','188476718-H3viJkcqpkejXT4yezIdFdliu6m4bQNruIMQIDvt','934598576709296128-GRb4TYnCQtQjj42UOIFntlucBCskjkQ','345699798-EmDdmFBuFiiL25RCCaM5QZpFvXIEh7h7fsXT5jOy','934509107767332867-uOYfgJUPtaUz98UzuyIhVfNhly71QfX']
ACCESS_SECRET = ['nZYUxVtZu69MfLVRKUDFK0T5UerH7GtCSvHnNwiKYz5yj','qvlIVS35OCf1UrzrD2aqthinOpDoWZsKc6l6ZJu881ulE','9XMM3CrVFgTVr7eWTLX72UHm43BOLusj51HdB8A4hIoDv','IGork6Dbls2d5IlqdJHbsSdb1xALuuLDQY4AnS8JG8BO7','gEWLt5aybIedxUlSnzUtntLZd4PGhjxytTdf9FtiZMdlP','5PZU28sXW34UDbuJpZsbT23IFEtOaMdl1JbynDj4fFKxI','3vuLrTo2MEMeQvgOVJIAUVUwyqVileCeCPfDKkFahuhcV','q7UFYVObDqVTsXgHySu0nlkUzbSJ8fdlQhuqQGIiw26wq','Q3w6GYecIdFbY3JNW2piwWTWbewlsFGre5DvVCCIL7X13','GG6sGk9I0pq8Gu9m25fRtBHBPZidObESAPxvBztsJKHN4']

oauth = OAuth(ACCESS_TOKEN[0], ACCESS_SECRET[0], CONSUMER_KEY[0], CONSUMER_SECRET[0])

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
deactivated = []
count = 0

def switch():
	global twitter_stream
	global count
	if count <9:
		count+=1
	else:
		count = 0
		print "Sleeping (Rate Limit: Count 0)"
		time.sleep(900)
	print "SWITCH: " + str(count)
	oauth = OAuth(ACCESS_TOKEN[count], ACCESS_SECRET[count], CONSUMER_KEY[count], CONSUMER_SECRET[count])
	twitter_stream = twitter.Twitter(auth=oauth)
	print ACCESS_TOKEN[count] 

#gather words from all tweets of all users from the network parameter
def gather_words(network, mentioned):
	if mentioned:
		f_main = open(network+"/used_names.txt", "r")
	else:
		f_main = open(network+"/names.txt", "r")
	alt_words = {}
	for line in f_main:
		print line
		if mentioned:
			l = line.strip('\n')
		else:
			l = line[:-1]
		file_name = network + '/' + l + '.txt'
		#print file_name
		try:
			with open(file_name, "r") as f_temp:
				read = []
				for line in f_temp:
					line = line.strip('\n')
					read.append(line);
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
	main_dict = {}
	for item in wordDict:
		if wordDict[item] > 100:
			main_dict[item] = wordDict[item]
	return sorted(main_dict.items(), key=operator.itemgetter(1))

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
					if user not in read:
						f_main.write(user+'\n')
				except:
					print "Unable to write"
	return new_users

#generate files corresponding to the tweets of users
def mentioned_tweets(file_name):
	global count
	global twitter_stream
	global rate_limit_check_remaining
		#time.sleep(900)
	with open(file_name+"/names.txt") as f_main:
		for line in f_main:
			if rate_limit_check_remaining < 5:
				print "top switch"
				rate_limit_check_remaining = 180
				switch()
			f_used = open("mentioned_network/used_names.txt", "a")
			f_used_read = open("mentioned_network/used_names.txt", "r")
			read_test = []
			for l in f_used_read:
				w = l.strip('\n')
				read_test.append(w)
			#print read_test
			rate_limit_status = twitter_stream.application.rate_limit_status()
			try:
				remaining = rate_limit_status["resources"]["statuses"]["/statuses/user_timeline"]["remaining"]
				remaining2 = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
			except Exception as e:
				print e
				time.sleep(900)
			rate_limit_check_remaining -= 1
			if remaining<5:
				print "switch 1"
				switch()
				# print "SLEEP (rate limit of user_timeline)"
				# time.sleep(900)
			elif remaining2 < 5:
				print "switch 2"
				switch()
				# print "SLEEP (rate limit of friend list)"
				# time.sleep(900)
			elif rate_limit_check_remaining<5:
				print "switch 3"
				switch()
				# print "SLEEP (rate limit of remaining count)"
				# time.sleep(900)
			username = line.strip('\n')
			br = True
			if "," in username:
				username.replace(",", "")
			if "!" in username:
				username.replace("!", "")
			if "." in username:
				username.replace(".", "")
			if "?" in username:
				username.replace("?", "")
			if "-" in username:
				username.replace("-", "")
			if len(username)>0:
				if username not in news_sources2:
					while br:
						try:
							if not suspension_check(username):
								p = (twitter_stream.users.show(screen_name=username))
								protected = p['protected']
								verified = p['verified']
								if not protected:
									if not verified:
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
												line = json.loads(line)
												read.append(line['id']);
											for tweet in iterator:
												if tweet['id'] not in read:
													f.write(json.dumps(tweet)+'\n')
										except Exception as e:
											print e
											print "Unable to write"
							br = False
						except Exception as e:
							print e
							print "switch exception"
							switch()
							#time.sleep(900)

					f_used.close;

#check if a user has been suspended
def suspension_check(name):
	global suspended
	global deactivated
	global twitter_stream
	global rate_limit_check_remaining
	if rate_limit_check_remaining < 5:
		switch()
		#print "SLEEP (rate limit)"
		rate_limit_check_remaining = 180
		#time.sleep(900)
	rate_limit_status = twitter_stream.application.rate_limit_status()
	rate_limit_check_remaining -= 1	
	remaining = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
	if remaining<5:
		switch()
		# print "SLEEP (rate limit)"
		# time.sleep(900)
	try:
		p = twitter_stream.users.show(screen_name=name)
		#print "Not Suspended"
		return False
	except:
		url = 'https://twitter.com/'+name
		r = requests.get(url, allow_redirects=True)
		if "suspended" in r.url:
			print "Suspended: " + name
			suspended.append(name)
		else:
			print "Deactivated: " + name
			deactivated.append(name)
		return True

#check if a user is protected
def protected_check(name):
	global rate_limit_check_remaining
	global twitter_stream
	if rate_limit_check_remaining < 5:
		print "SLEEP (rate limit)"
		rate_limit_check_remaining = 180
		time.sleep(900)
	rate_limit_status = twitter_stream.application.rate_limit_status()
	rate_limit_check_remaining -= 1	
	remaining = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
	if remaining<5:
		switch()
		# print "SLEEP (rate limit)"
		# time.sleep(900)
	br = True
	while br:
		try:
			p = twitter_stream.users.show(screen_name=name)
			br = False
		except:
			switch()
			# print "SLEEP (except)"
			# time.sleep(900)
	return p['protected']

#determine users in a network who are suspended
def gather_suspenders():
	global suspended
	global deactivated
	# suspended = []
	# f_write = open("suspended.txt", "a")
	# with open("mentioned_network/names.txt") as f_main:
	# 	for line in f_main:
	# 		line = line.strip('\n')
	# 		sus = suspension_check(line)
	# 		if sus:
	# 			print line
	# 			f_write.write(line + '\n')
	# 			suspended.append(line)
	return deactivated, suspended


#determine the ratio of Trump followers
# def trump_check(network):
# 	global twitter_stream
# 	f_main = open(network+"/names.txt", "r")
# 	trump_followers = []
# 	count = 1
# 	for line in f_main:
# 		username = line[:-1]
# 		if suspension_check(username) is False:
# 			if protected_check(username) is False:
# 				i1 = (twitter_stream.friends.ids(screen_name=username))
# 				ids_friends = i1['ids']
# 				for id1 in ids_friends:
# 					if id1 == 25073877:
# 						trump_followers.append(ids_friends)
# 	count = count*1.0
# 	ratio = len(trump_followers)/count
# 	return ratio, trump_followers