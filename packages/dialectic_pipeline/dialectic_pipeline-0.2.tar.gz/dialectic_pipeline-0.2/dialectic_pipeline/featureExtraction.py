from string import punctuation
import json
import math
import pprint
import math
import heapq
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf8')


from sklearn.externals import joblib
from nltk.corpus import stopwords
import nltk;
from sklearn.externals import joblib
from collections import defaultdict, Counter
import operator
import re
from nltk.tokenize import TweetTokenizer

from dialectic_pipeline import apriori


sent_detector = nltk.data.load('tokenizers/punkt/english.pickle');
tk = TweetTokenizer()
NUM_DOCUMENTS = 10000.0
texts = []
stopWords = []

def setNLP(nl):
	'''Maintains a reference to the spacy model'''
	global nlp
	nlp = nl

def extractAllFeatures(project_name, corpus, stopwords, ldamodel, reviewc):
	'''Runs the entire feature extraction process'''
	#initial product feature list
	apriori_product_features(project_name, corpus,  stopwords, ldamodel, reviewc)
	#cluster this using LDA into topics
	topic_product_features(project_name, corpus,  stopwords, ldamodel, reviewc, num_topics)

	#Find the top nouns, adj, and adv (both good and bad)
	top_POS(project_name, corpus,stopwords,"NOUN")
	top_POS(project_name, corpus,stopwords,"ADJ")
	top_POS(project_name, corpus,stopwords,"ADV")


def term_Frequency(topic, product_feature):
	count = 0
	for segment in topic:

		words = tk.tokenize(segment.lower())#)re.split("; |, |\*|\n", segment.lower())
		for word in words:
			# print word
			# print product_feature[0]
			if(word == product_feature[0].decode("utf-8")):
				print("\n\n\n\n\n\n\n")
				count += 1
	return count




def pruneLexicalDiversity(all_product_features, documents, threshold):
	pruned_features = []
	'''filter based on lexical diversity '''
	featureDiversity = []

	i = 0
	for feature in all_product_features:
		i+=1
		print(i)
		print(feature)
		all_adjs = []
		for doc in documents:
			# for each sentence in the document
			for sent in doc.sents:
				#For single word features
				if (' ' not in feature):
					for token in sent:
						if feature.lower() == token.orth_.lower():
							#print(sent)
							adjs = []
							for to in sent:
								if to.pos_ == "ADJ" or to.pos_ == "VERB" or to.pos_ == "ADV":
									if str(to.orth_.lower()) not in stopWords:
										all_adjs.append(to.lemma_.lower())

				#double word features
				else:
					sentence = sent.string.strip()
					if feature in sentence:
						adjs = []
						for to in sent:
							if to.pos_ == "ADJ" or to.pos_ == "VERB" or to.pos_ == "ADV":
								if str(to.orth_.lower()) not in stopWords:
									all_adjs.append(to.lemma_.lower())


		#print(all_adjs)
		featureDiversity.append(all_adjs)
		print 'alladjs', all_adjs
		print("\n\n")

	i = 0
	for adjs in featureDiversity:
		if (len(adjs) > 0):
			score = float(len(set(adjs)))/float(len(adjs))
			word = (all_product_features[i])
			obj = {"word":word,"score":score}
			print(obj)
			json_string = json.dumps(obj)
			boost = 0
			if (' ' in word):
				boost = .2
			if score < threshold + boost:
				pruned_features.append(word)
			else:
				print('pruned')
				print(word)
		i+=1
	return pruned_features


''' Using apriori algorithm to detect product features with more than one word '''
'''featureExtraction.apriori_product_features(P, corpus,  stopwords, ldamodel, reviewc)'''
def apriori_product_features(P, filename, stopwords, model, corpus):
	Load = False  # If true then loading from old documents, else run spacy
	global texts
	global stopWords
	documents = [] # List of spacy documents


	# Add stopwords to list
	with open(stopwords) as f:
		for sw in f:
			stopWords.append(sw.strip().lower())
	i = 0


	with open(filename) as f:
		for line in f:
			i += 1
			if i % 500 == 0:
				print(i)
			if i > NUM_DOCUMENTS:
				break
			js = json.loads(line) # Load each review as json object

			if js["helpful"][1] == 0:
				continue

			score = float(js["helpful"][0])/float(js["helpful"][1])
			if score > .80 and js["helpful"][1] >= 10:
				sentences = sent_detector.tokenize(js["reviewText"].strip());
				if len(sentences) >= 2:
					texts.append(js["reviewText"])
					if Load == False:
						document = nlp((js["reviewText"])) # Actual text of review
						#print(document.count_by)
						documents.append(document)
						# print document

	all_sent_feature_words = []
	for doc in documents:
		for sent in doc.sents:
			sent_feature_words = []
			for token in sent:
				if (token.pos_=="NOUN" or token.pos_ == "ADJ") and str(token.orth_.lower()) not in stopWords:
					sent_feature_words.append(str(token))
			all_sent_feature_words.append(sent_feature_words)

	C1 = apriori.createC1(all_sent_feature_words)
	D = map(set, all_sent_feature_words)
	L1, support_data = apriori.scanD(D, C1, 0.005)
	apriori.aprioriGen(L1, 2)
	L, support_data = apriori.apriori(all_sent_feature_words, minsupport = 0.005)

	'''Get all the product features'''
	all_product_features = []
	for features in L:
		for feature in features:
			if(len(feature) is  1):
				featureString = map(str, feature)
				doc = nlp(unicode(featureString[0], encoding="utf-8"))
				for sentence in doc.sents:
					for token in sentence:
						if(token.pos_ != "ADJ"):
							all_product_features.append(map(str, feature)[0])
			else:
				all_product_features.append(" ".join(map(str, feature)))


	with open("exports/" + P + "/featuresAprioriRAW.txt",'w') as f:
		for word in all_product_features:
			f.write(word+"\n")
		f.close()

	pruned_features = pruneLexicalDiversity(all_product_features, documents, .5)

	print("PRUNED FEATURES BELOW")
	print("\n\n\n\n")
	print(pruned_features)

	with open("exports/" + P + "/featuresAprioriLexicalPruned.txt",'w') as f:
		for word in pruned_features:
			f.write(word+"\n")
		f.close()



def topic_product_features(P, filename, stopwords, model, corpus, K):
	pruned_features = []
	with open("exports/" + P + "/featuresAprioriLexicalPruned.txt",'r') as f:
		for word in f:
			pruned_features.append(word.strip())

	pruned_features2 = []
	for i in pruned_features:
		iSubFeature = False
		for j in pruned_features:
			if i != j and i in j:
				iSubFeature = True
		if not iSubFeature:
			pruned_features2.append(i)

	pruned_features = pruned_features2

	topic_documents = {}
	for i in range(0, K):
		topic_documents[i] = []

	segments = []
	with open("exports/"+P+"/all_segments.txt") as f:
		i = 0
		for line in f:
			i += 1
			if i % 500 == 0:
				print(i)
			js = json.loads(line) # Load each review as json object

			segments.append(js["reviewText"])

	''' Sort every segment into a topic '''
	for segment in segments:
		block_lda = model[corpus.dictionary.doc2bow(corpus.proc(segment))]
		#maxTopic, value = max(enumerate(block_lda), key=operator.itemgetter(1))

		topic_id = 0;
		prob = 0;
		for t in block_lda:
			if t[1] > prob:
				topic_id = t[0];
				prob = t[1]
		topic_documents[topic_id].append(segment)
		#print topic_documents[maxTopic]

	for key in topic_documents:
		print(key)
		print(len(topic_documents[key]))

	prod_feat_total_freq = {}
	
	''' For every product feature, find its total frequency '''
	for product_feature in pruned_features:
		total_freq = 0
		for segment in segments:
			total_freq += segment.count(product_feature)
		prod_feat_total_freq[product_feature] = total_freq

	# print prod_feat_total_freq


	''' For every topic, create a list of the tf-idf values of each feature '''
	tf_idfs = {}
	for i in range(0, K):
		print(i)
		print("--------------------\n\n\n\n")
		tf_idfs[i] = {}
		for product_feature in pruned_features:
			tf = 0
			for segment in topic_documents[i]:	
				if product_feature.count(" ") > 0:
					tf += segment.count(product_feature)
				else:
					tf += segment.count(product_feature) 

			tf_idf = tf * math.log(1 + NUM_DOCUMENTS / (1 + prod_feat_total_freq[product_feature]))
			tf_idfs[i][product_feature] = tf_idf

			print(product_feature)
			print(tf)
			print((1 + NUM_DOCUMENTS / (1 + prod_feat_total_freq[product_feature])))

	topic_product_features = {}
	for i in range(0, K):
		topic_product_features[i] = []
		sorted_tfidfs = sorted(tf_idfs[i].items(), key=operator.itemgetter(1), reverse=True)
		for key, val in sorted_tfidfs[:10]:
			topic_product_features[i].append(key)

		
	pprint.pprint(topic_product_features)
	with open('exports/' + P +'/topic_product_features.json', 'w') as fp:
		json.dump(topic_product_features, fp)

		

	







''' P: directory, filename: reviews, stopwords: location of stopwords '''
def product_features(P, filename, stopwords):
	Load = False  # If true then loading from old documents, else run spacy
	global texts
	global stopWords
	documents = [] # List of spacy documents

	# Add stopwords to list
	with open(stopwords) as f:
		for sw in f:
			stopWords.append(sw.strip().lower())
	i = 0
	with open(filename) as f:
		for line in f:
			i += 1
			if i % 500 == 0:
				print(i)
			if i > NUM_DOCUMENTS:
				break
			js = json.loads(line) # Load each review as json object

			if js["helpful"][1] == 0:
				continue

			score = float(js["helpful"][0])/float(js["helpful"][1])
			if score > .95 and js["helpful"][1] >= 10:
				sentences = sent_detector.tokenize(js["reviewText"].strip());
				if len(sentences) >= 2:
					texts.append(js["reviewText"])
					if Load == False:
						document = nlp((js["reviewText"])) # Actual text of review
						#print(document.count_by)
						documents.append(document)

	
	if Load==False:
		joblib.dump(documents, 'exports/' + P +'/processed_segments.p') 
	else:
		documents = joblib.load('exports/' + P + '/processed_segments.p') 


	cnt = Counter()

	#RAW FEATURE GENERATION
	# Get frequency of each noun
	for doc in documents:
		for token in doc:
			if token.pos_=="NOUN" and str(token.orth_.lower()) not in stopWords:
				cnt[token.orth_.lower()]+=1

	print("\n\n\n\n-----------------------")
	print(cnt.most_common(1000)) # 1000 most common nouns

	# Save most common ones
	with open("exports/" + P + "/featuresAutoRAW.txt",'w') as f:
		for word in cnt.most_common(200):
			output = str(word[0])
			f.write(output+"\n")
		f.close()



	''' Prune based on lexical diversity 
	Lower lexical diversity then it is product feature'''
	features = []
	with open("exports/" + P + "/featuresAutoRAW.txt",'r') as f:
		for line in f:
			features.append(line.strip())

	featureDiversity = []
	i = 0
	for feature in features:
		i+=1
		print(i)
		print(feature)
		all_adjs = []
		for doc in documents:
			# for each sentence in the document
			for sent in doc.sents:
				for token in sent:
					if feature.lower() == token.orth_.lower():
						#print(sent)
						adjs = []
						for to in sent:
							if to.pos_ == "ADJ" or to.pos_ == "VERB" or to.pos_ == "ADV":
								if str(to.orth_.lower()) not in stopWords:
									all_adjs.append(to.lemma_.lower())
		#print(all_adjs)
		featureDiversity.append(all_adjs)
		print(all_adjs)
		print("\n\n")

	i = 0

	out = open("exports/" + P + "/product_features.txt","w")
	for adjs in featureDiversity:
		if (len(adjs) > 0):
			score = float(len(set(adjs)))/float(len(adjs))
			word = (features[i])
			obj = {"word":word,"score":score}
			json_string = json.dumps(obj)
			if score < .45:
				out.write(word + "\n")
		i+=1
	out.close()


def top_POS(P,filename,stopwords,POS):
	'''Find top parts of speech, given a specific POS tag as defined by spacy'''

	i = 0
	global sent_detector
	Load = False

	global stopWords
	documents = []

	with open(stopwords) as f:
		for sw in f:
			stopWords.append(sw.strip().lower())

	documents = []
	bad_documents = []

	with open(filename) as f:
		for line in f:
			i+=1

			if i%500 == 0:
				print(i)

			js = json.loads(line)

			if js["helpful"][1] == 0:
				continue

			score = float(js["helpful"][0])/float(js["helpful"][1])
			if score > .95:
				sentences = sent_detector.tokenize(js["reviewText"].strip());
				if len(sentences) >= 2:
					texts.append(js["reviewText"])
					if Load==False:
						document = nlp((js["reviewText"]))
						#print(document.count_by)
						documents.append(document)
			if score < .55:
				sentences = sent_detector.tokenize(js["reviewText"].strip());
				if len(sentences) >= 2:
					texts.append(js["reviewText"])
					if Load==False:
						document = nlp((js["reviewText"]))
						#print(document.count_by)
						bad_documents.append(document)

	cnt = Counter()
	bad_cnt = Counter()



	#RAW FEATURE GENERATION
	for doc in documents:
			
		for token in doc:
			if token.pos_==POS and str(token.orth_.lower()) not in stopWords:
				cnt[token.orth_.lower()]+=1

	for doc in bad_documents:
			
		for token in doc:
			if token.pos_==POS and str(token.orth_.lower()) not in stopWords:
				bad_cnt[token.orth_.lower()]+=1


	words = []
	bad_words = []
	for tok in cnt.most_common(500):
		words.append(tok[0])
	for tok in bad_cnt.most_common(500):
		bad_words.append(tok[0])

	good_unique = []
	bad_unique = []

	print("good--------")
	for word in words:
		if word not in bad_words:
			good_unique.append(word)
			print(word)
	print("bad--------")
	for word in bad_words:
		if word not in words:
			bad_unique.append(word)
			print(word)

	with open("exports/" + P +"/good_" + POS + ".txt",'w') as f:
		for word in good_unique:
			f.write(word+"\n")
	with open("exports/" + P +"/bad_" + POS + ".txt",'w') as f:
		for word in bad_unique:
			f.write(word+"\n")
