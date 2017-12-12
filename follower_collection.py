# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import twitter
import time
import os.path
# Variables that contains the user credentials to access Twitter API 
CONSUMER_KEY = ['gIwiGb1l1iIe8kYJMYMHNHlpD','tSruLlc8sLimHS2IFrt4unjRI','JBlopJbar2HWrA1XrR0yP5jzK','lGaSN95HzfIBen0w0Axfr0IxH','SNBMxq9QPaJo0nebjgOI9fUKA','MnydDCAY7FTG6O6v6uWwRKn7d','iUTedDiTJxDHJz9ogMC7e9Avu','zU55pVxr2jbcOD1eessizfcjz', 'XK9i2YctF94iUHQSTsXRwJ9Bg']
CONSUMER_SECRET = ['thMew6sWyjx5D5mQnZiBDoTOdQJP4Th3ewEH0lruvfBa2NPLev','fQP70F3oxq7HgX1qDmcew9cPZMQC2SuZlo1XVScxEicQHPUajB','zha98xEAlVwa3cvO0I9JWN6GTp0a50CjplznUD9lfTkiH5rAW0','kuVHapPcOGjVX8Pj1lVISFDXvmrbUCczXjJojn15ZjFBabNdBJ','OKouOO8W5vgyiIgLossSCQ2XhSVxNFtdv3z5Mxiz0S1qr8B56y','kTk1bdNCWgvMLykidplCLYljCRTvxUueE4YBaMnN3t4eghjFVc','12NjLOHdsGe6b1rs4kRqbJ1B6E2nmgZtcGy2cexuBllYgiZKXY','4eQvOfMkaCbABLGiBlG6eew7BWeR5KxTJNzkACui73Av5FFVzQ', 'hS8WC0LQsOfguo5I5ZmbQC6RhdOs0dDxisJlqiJAKYqrbOP0N0']
ACCESS_TOKEN = ['934509107767332867-8VF4Qky0RBMy468hGk6Uz7xnufLyqKR','934509107767332867-6IRuw4GwZfTOa0boFVfSXEOPrRPhTwO','934509107767332867-1MAj7Ie6ZR0gdpCoi715uF9ikMsEeOW','456179475-EgyELPuoFZAqrIYdNNS0x0PDwjarAhKRB0TvNafm','456179475-G0ALgc9AEissDQRSKoMBJBFBS9Oop33Rjoe4ybEM','456179475-Y9OQ3t2vWxMWaZhLyUiuWbZPJeEWiwnqH1JveSFF','550600686-nTcPINvxHMBB7bCAJg3e5jDaLSj7ntTDGlh1FTsB','550600686-F1LDE9Y5Nyb7jgRwCXujd7ZCy24DbgTVnmVu8hdF', '550600686-O6rdE7nvUOP4ZGzADLm4J5hwJJfW4loFjZ3RQkgo']
ACCESS_SECRET = ['IZpMPN71Is9nqF543uwiplVhtdRstXAgbaGN1w5V0byRL','VxtRDgIuFIYrDLAWWfKq9MhuCFKclkCwQQqr1hBvW77AT','eHMWvIpuIHgMeuj94rmhZZ3WE8M5mc3vJ08pECSXnUIUN','Hhh7rCiIgrIT4WpAwpx0XDspBN1mTZmzSUza9KAwXiHtA','wCDAM2KrONGgOIY8Fwac6TQm9IQvENDMhiOKdnTCEq9eK','gRRDzqNdVIz2Pk8N8aja6ZoebA96GnPBlNBEcjaCMw0p9','dmHlkCPyxG0EGszaVACMRghmSs1SMPaFUfkgwlAAoMMK4','cSAKOaoSD2bldKUX2fBl7osZZmJmQjxe7xeXvW1ejWox5', '8blOoOapcRr0SC2r7FIaUd6wHef02XYjAlWw1UlNxIqMX']

count = 0
oauth = OAuth(ACCESS_TOKEN[0], ACCESS_SECRET[0], CONSUMER_KEY[0], CONSUMER_SECRET[0])
twitter_stream = twitter.Twitter(auth=oauth)
test=0
rate_limit_check_remaining=180
def switch():
	global twitter_stream
	global count
	global rate_limit_check_remaining
	if count <8:
		count+=1
	else:
		count = 0
		print "Sleeping (Rate Limit: Count 0)"
		time.sleep(900)
	print "SWITCH: " + str(count)
	oauth = OAuth(ACCESS_TOKEN[count], ACCESS_SECRET[count], CONSUMER_KEY[count], CONSUMER_SECRET[count])
	twitter_stream = twitter.Twitter(auth=oauth)
	print ACCESS_TOKEN[count] 

def suspension_check(name):
	global twitter_stream
	global rate_limit_check_remaining
	if rate_limit_check_remaining < 5:
		print "suspension switch 1"
		rate_limit_check_remaining = 180
		switch()
	rate_limit_status = twitter_stream.application.rate_limit_status()
	rate_limit_check_remaining -= 1	
	remaining = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
	if remaining<5:
		print "suspension switch 2"
		switch()
		# print "SLEEP (rate limit)"
		# time.sleep(900)
	try:
		p = twitter_stream.users.show(screen_name=name)
		#print "Not Suspended"
		return False
	except:
		print "Suspended: " + name
		return True

def scrape_followers(main_file):
	global limit
	global twitter_stream
	global count
	global rate_limit_check_remaining
	access = 'names.txt'
	if main_file == 'mentioned_network':
		access = 'used_names.txt'
	f_main = open(main_file + "/" + access, 'r')
	for line in f_main:
		file_name = main_file + '/' + line+'.txt'
		rate_limit_status = twitter_stream.application.rate_limit_status()
		rate_limit_check_remaining-=1
		remaining = rate_limit_status["resources"]["users"]["/users/show/:id"]["remaining"]
		if remaining<5:
			switch()
		if rate_limit_check_remaining<5:
			switch()
		br = True
		while br:
			try:
				if not suspension_check(line):
					p = (twitter_stream.users.show(screen_name=line))
					id_line = p['id']
					protected = p['protected']
					if not protected:
						friends_name = 'full_network/'+str(id_line)+'_friends.txt'
						if not os.path.isfile(friends_name):
							print line + " Friends"
							f_write = open(friends_name, 'w')
							friends = (twitter_stream.friends.ids(user_id=id_line))['ids']
							for f in friends:
								f_write.write(str(f) + '\n')
						followers_name = 'full_network/'+str(id_line)+'_followers.txt'
						if not os.path.isfile(followers_name):
							print line + " Followers"
							f_write2 = open(followers_name, 'w')
							followers = (twitter_stream.followers.ids(user_id=id_line))['ids']
							for f in followers:
								f_write2.write(str(f) + '\n')
				br=False
			except Exception as e:
				print e
				if 'User not found' in e:
					print "USER NOT FOUND"
					br = False
				else:
					switch()

while True:
	scrape_followers('richardspencer_origin')
	scrape_followers('mentioned_network')