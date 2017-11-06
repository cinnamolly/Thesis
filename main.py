import collect, count, storage
import time
from time import gmtime, strftime

#SETTING SLEEP TIME TO 30 MINUTES
t = 1800
f = open("cumulative_info.txt", "a")

#gather RS network names
while True:
	# print "gathering nodes from Richard Spencer Network\n"
	# collect.main()
	#collect frequent words from the RS network
	print "gathering frequent words\n"
	frequent_words = count.gather_words('richardspencer_origin', False)
	print count.maxWords(frequent_words)
	#gather mentioned names
	print "gathering mentioned profiles\n"
	mentioned = count.gather_mentioned(frequent_words)
	print mentioned
	print "gathering mentioned tweets\n"
	file_name = count.mentioned_tweets('mentioned_network')
	#gather frequent words from the friend network
	print "gathering frequent words from mentioned profiles\n"
	mentioned_freq_words = count.gather_words('mentioned_network', True)
	#print mentioned_freq_words
	print count.maxWords(mentioned_freq_words)
	#gather suspended users
	print "gathering suspended profiles\n"
	suspended = count.gather_suspenders()
	print suspended
	print "storing information\n"
	curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	storage = storage.make_storage(curr_time, suspended, frequent_words, mentioned_freq_words)
	#print storage
	f.write(storage)
