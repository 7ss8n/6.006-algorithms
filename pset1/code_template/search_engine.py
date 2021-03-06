import os
import math
import re

def computeAngleBetweenWordFreqDicts(d1, d2):
	"""
	Computes the angle in radians between two word frequency dictionaries, d1 and d2.
	"""

	#iterate through the words in both dictionaries and add to the dot product
	dotProd = 0
	for w in d1.keys():
		try:
			dotProd+=d1[w]*d2[w]
		#if this returns an error, this means that the word "w" is not in d2, so it will contribute 0 to the dot product
		except:
			continue

	d1_magnitude = math.sqrt(math.fsum([x**2 for x in d1.values()]))
	d2_magnitude = math.sqrt(math.fsum([y**2 for y in d2.values()]))

	#now compute the angle
	angle = math.acos(float(dotProd) / float(d1_magnitude*d2_magnitude))
	return angle

def computeAngleBetweenWFIDFDicts(d1,d2,corpusIDFDict):
	"""
	Converts two WF dictionaries d1 and d2 to WFIDF dictionaries, then computes the angle between them
	"""

	#multiply every element in the word frequency dictionaries by the corresponding IDF
	d1_idf = {}
	for i in d1.keys():
		#print corpusIDFDict[i]
		#print d1[i]
		d1_idf[i] = d1[i] * corpusIDFDict[i]

	d2_idf = {}
	for j in d2.keys():
		d2_idf[j] = d2[j] *corpusIDFDict[j] 


	dotProd = 0
	for w in d1.keys():
		try:
			dotProd+=d1_idf[w]*d2_idf[w]
		#if this returns an errors, this means that the word "w" is not in d2, so it will contribute 0 to the dot product
		except:
			continue

	d1_magnitude = math.fsum([x**2 for x in d1_idf.values()])**0.5
	d2_magnitude = math.fsum([y**2 for y in d2_idf.values()])**0.5

	#now compute the angle
	angle = math.acos(float(dotProd) / (d1_magnitude*d2_magnitude))
	return angle

def buildWordFreqDict(list_of_words):
	"""
	list_of_words: a list of the words in an article
	returns: a dictionary with keys for every word in the article and values for the frequency of that word
	"""

	#initialize an empty dictionary that will contain word frequencies
	wordFreqDict = {}

	for word in list_of_words:
		#try to increment the right key in the word frequency dictionary
		try:
			wordFreqDict[word.lower()]+=1
		#if it does not exist, then create a new key, and give it the value 1
		except:
			wordFreqDict[word.lower()]=1
	return wordFreqDict

def extract_corpus(corpus_dir = "articles"):
	"""
	Returns a corpus of articles from the given directory.

	Args:
		corpus_dir (str): The location of the corpus.

	Returns:
		dict: A dictionary with key = title of the article, 
			  value = list of words in the article
	"""
	corpus = {}
	num_documents = 0
	for filename in os.listdir(corpus_dir):
		with open(os.path.join(corpus_dir, filename)) as f:
			corpus[filename] = re.sub("[^\w]", " ",  f.read()).split()
	return corpus


#title dist pair object that makes it easier to sort a list of title/distance pairs
class titleDistPair(object):
	def __init__(self, title, angle):
		self.title = title
		self.angle = angle

	def __lt__(self,other):
		if self.angle < other.angle:
			return True
		elif self.angle == other.angle:
			if self.title < other.title:
				return True

	def __eq__(self,other):
		if self.angle == other.angle and self.title == other.title:
			return True


class titleRelevancePair(object):
	def __init__(self, title, TFIDF_score):
		self.title = title
		self.tfidf_score = TFIDF_score

	def __gt__(self,other):
		if type(other)==int:
			return True

	def __lt__(self,other):
		if self.tfidf_score < other.tfidf_score:
			return True
		elif self.tfidf_score == other.tfidf_score:
			if self.title < other.title:
				return True

	def __eq__(self,other):
		if self.tfidf_score == other.tfidf_score and self.title == other.title:
			return True

	def __repr__(self):
		return "(%s,%f)" % (self.title,self.tfidf_score)

class SearchEngine(object):
	"""
	Represents an instance of a search engine. Instances of the search engine are 
	initialized with a corpus.

	Args:
		corpus (dict): A dictionary of (article title, article text) pairs.
	"""
	def __init__(self, corpus):
		# The corpus of (article title, article text) pairs.
		self.corpus = corpus

	def get_relevant_articles_doc_dist(self, title, k):
		"""
		Returns the articles most relevant to a given document, limited to at most
		k results. Uses the normal document distance score.

		Args:
			title (str): The title of the article being queried (assume it exists). 


		Returns:
			An array of the k most relevant (article title, document distance) pairs, ordered 
			by decreasing relevance. 

			Specifications:
				* Case is ignored entirely
				* If two articles have the same distance, titles should be in alphabetical order
		"""
		# TODO: Implement this for part (a)

		#as the angles betweens articles are computed, title/docdistance pairs will be appended
		titleDistPairs = []

		#get a word frequency dictionary for the queried article
		queryWordFreqDict = buildWordFreqDict(self.corpus[title])

		#for all of the other articles in the corpus, build word freqency dicts and compute angle
		for other_title in self.corpus.keys():

			#if we're looking at the query article, ignore it and move on
			if other_title == title:
				continue

			else: #this is a new article
				#build a word freq dict for the other article
				otherWordFreqDict = buildWordFreqDict(self.corpus[other_title])

				#now compute the angle between the query article and the other article
				angle = computeAngleBetweenWordFreqDicts(queryWordFreqDict,otherWordFreqDict)

				#add a new title/document-distance pair object to the list
				titleDistPairs.append(titleDistPair(other_title,angle))

		#now sort the list of title/distance pairs to find the k-nearest
		#the first k entries in the list will be the k-nearest
		titleDistPairs.sort()

		#take the k-nearest, and convert from a title/dist object to a tuple
		kClosest = [(i.title, i.angle) for i in titleDistPairs[0:k]]
		return kClosest

	def get_relevant_articles_tf_idf(self, title, k):
		"""
		Returns the articles most relevant to a given document, limited to at most
		k results. Uses the document distance with TF-IDF scores.

		Args:
			title (str): The title of the article being queried (assume it exists). 

		Returns:
			An array of the k most relevant (article title, document distance) pairs, ordered 
			by decreasing relevance. 

			Specifications:
				* Case is ignored entirely
				* If two articles have the same distance, titles should be in alphabetical order
		"""
		# TODO: Implement this for part (b)

		
		#store a word frequency dict for each article in a larger dictionary
		# STRUCTURE OF THE DICT: {article title: {word1: #, word2: #}}
		wordFreqDictDict = {}
		for t in self.corpus.keys():
			wordFreqDictDict[t] = buildWordFreqDict(self.corpus[t])
		#print wordFreqDictDict

		#now we have a dict of word freq dicts, so we can compute IDFs for each word in the corpus
		numArticles = len(wordFreqDictDict)
		corpusIDFDict = {}

		#consider every word in the corpus, and find out how many documents it occurs in
		docFreqDict = {}
		for article in wordFreqDictDict.values(): #each article, in this case, is a word frequency dictionary
			for word in article.keys():
				try:
					docFreqDict[word]+=1
				except:
					docFreqDict[word]=1

		#now build a dictionary with every word in the corpus as a key, and its IDF as a value
		for word in docFreqDict.keys():
			corpusIDFDict[word] = math.log((float(numArticles) / float(docFreqDict[word])))

		#now compute the angle between every article and the query article, and store it as a title/document-distance object
		titleDistPairs = []

		for other_title in self.corpus.keys():
			if other_title == title: #don't compare the query article to itself
				continue
			else:
				angle = computeAngleBetweenWFIDFDicts(wordFreqDictDict[title],wordFreqDictDict[other_title],corpusIDFDict)
				titleDistPairs.append(titleDistPair(other_title,angle))

		
		#now sort the list of title/distance pairs to find the k-nearest
		#the first k entries in the list will be the k-nearest
		titleDistPairs.sort()

		#take the k-nearest, and convert from a title/dist object to a tuple
		kClosest = [(i.title, i.angle) for i in titleDistPairs[0:k]]
		return kClosest

	def search(self, query, k):
		"""
		Returns the articles most relevant to a given query, limited to at most
		k results.

		Args:
			query (str): The query for the search engine. Doesn't contain any special characters.

		Returns:
			An array of the k best (article title, tf-idf score) pairs, ordered by decreasing score. 

		    Specifications: 
			    * Only consider articles with a positive tf-idf score. 
			    * If there are fewer than k results with a positive tf-idf score, return those results.
				  If there are more, return only the k best results.
			    * If two articles have the same score, titles should be in alphabetical order
		"""
		# TODO: Implement this for part (c)

		#build a word frequency dictionary for each article
		wordFreqDictDict = {}
		for article in self.corpus.keys():
			#print article
			wordFreqDictDict[article] = buildWordFreqDict(self.corpus[article])


		#now we have a dict of word freq dicts, so we can compute IDFs for each word in the corpus
		numArticles = len(wordFreqDictDict)
		corpusIDFDict = {}

		#consider every word in the corpus, and find out how many documents it occurs in
		docFreqDict = {}
		for article in wordFreqDictDict.values(): #each article, in this case, is a word frequency dictionary
			for word in article.keys():
				try:
					docFreqDict[word]+=1
				except:
					docFreqDict[word]=1

		#now build a dictionary with every word in the corpus as a key, and its IDF as a value
		for word in docFreqDict.keys():
			corpusIDFDict[word] = math.log((float(numArticles) / float(docFreqDict[word])))


		#for each article, build a TFIDF score dictionary
		TFIDFDictDict = {}
		for article in self.corpus.keys():
			wfd = wordFreqDictDict[article]
			for word in wfd:
				wfd[word]*=corpusIDFDict[word]
			TFIDFDictDict[article] = wfd

		#get the query as a list of lowercase words
		query.lower()
		parsedQueryRepeats = query.split(' ')

		#remove repeats from the parsed query
		parsedQuery = []
		for q in parsedQueryRepeats:
			if q not in parsedQuery:
				parsedQuery.append(q)

		#for each article, compute its TFIDF score based on the search
		relevanceScoreList = []
		for article in wordFreqDictDict.keys():
			TFIDF_score = 0
			for word in parsedQuery:
				try:
					#try to add the TFIDF score of the particular word in the given article
					TFIDF_score += TFIDFDictDict[article][word]
				except: #this means the word wasn't in the article
					pass

			#now add the totalled relevance score to the relevance score dict
			#print TFIDF_score
			relevanceScoreList.append((titleRelevancePair(article,TFIDF_score)))
		

		#sort the relevance score list to put the most relevant articles at the front of the list
		relevanceScoreList.sort(reverse=True)
		#relevanceScoreList = sorted(relevanceScoreList, reverse=True)

		kbest = relevanceScoreList[0:k] #take only the kbest

		#now only take the nonnegative results
		kbest_nonnegative = []
		for i in kbest:
			if i>0:
				kbest_nonnegative.append(i)

		#convert back to a tuple
		kClosest = [(i.title, i.tfidf_score) for i in kbest_nonnegative]
		return kClosest
		
if __name__ == '__main__':
	corpus = extract_corpus()
	e = SearchEngine(corpus)

	result_dd = e.get_relevant_articles_doc_dist("Apple",3)
	result_tfidf = e.get_relevant_articles_tf_idf("Apple",3)
	print "DOCDIST:", result_dd
	print "TFIDF:", result_tfidf

	"""
	print("Welcome to 6006LE! We hope you have a wonderful experience. To exit, type 'exit.'")
	print("\nSuggested searches: the yummiest fruit in the world, child prodigy, operating system, red tree, coolest algorithm....")
	while True:
		query = input('\nEnter query here: ').strip()
		if query == "exit":
			print("Good bye!")
			break
		results = e.search(query, 5)
		if len(results) == 0:
			print("There are no results for that query. :(")
		else:
			print("Top results: ")
			for title, score in e.search(query, 5):
				print ("    - %s (score %f)" % (title, score))

	"""
	
