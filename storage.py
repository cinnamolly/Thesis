class Storage(object):
	time = ""
	suspended = []
	maxwords_main = []
	maxwords_mentioned = []

	def __init__(self, time, suspended, maxwords_main, maxwords_mentioned):
		self.time = time
		self.suspended = suspended
		self.maxwords_main = maxwords_main
		self.maxwords_mentioned = maxwords_mentioned

	def __str__(self):
		return "{'time':"+ self.time+", 'suspended':"+ str(self.suspended)+", 'maxwords_main':"+str(self.maxwords_main)+", 'maxwords_mentioned':"+str(self.maxwords_mentioned)+"}"

def make_storage(time, suspended, maxwords_main, maxwords_mentioned):
	storage = Storage(time, suspended, maxwords_main, maxwords_mentioned)
	return storage