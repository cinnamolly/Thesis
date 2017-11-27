import collect, count
import time
from time import gmtime, strftime

#SETTING SLEEP TIME TO 30 MINUTES
t = 1800
f = open("cumulative_info.txt", "a")

#while True:
	#gather RS network names
print "gathering nodes from Richard Spencer Network\n"
collect.main()
	#collect frequent words from the RS network
	# print "gathering frequent words\n"
	# frequent_words = count.gather_words('richardspencer_origin', False)
	# freq_words = count.maxWords(frequent_words)
	# print freq_words
	# #gather mentioned names
	# print "gathering mentioned profiles\n"
	# mentioned = count.gather_mentioned(frequent_words)
	# print mentioned
	# print "gathering mentioned tweets\n"
	# file_name = count.mentioned_tweets('mentioned_network')
	# #gather frequent words from the friend network
	# print "gathering frequent words from mentioned profiles\n"
	# mentioned_frequent_words = count.gather_words('mentioned_network', True)
	# mentioned_freq_words = count.maxWords(mentioned_frequent_words)		
	# #print mentioned_freq_words
	# #gather suspended users
	# # print "gathering trump profiles\n"
	# # c, profiles = count.gather_suspenders()
	# print suspended
	# print "gathering suspended profiles\n"
	# suspended = count.gather_suspenders()
	# print suspended
	# print "storing information\n"
	# curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	# storage = "{'time':"+ curr_time+", 'suspended':"+ str(suspended)+", 'maxwords_main':"+str(freq_words)+", 'maxwords_mentioned':"+str(mentioned_freq_words)+"}\n"
	# #print storage
	# f.write(storage)
