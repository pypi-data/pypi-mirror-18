import json
from random import shuffle 
from random import seed 
import random
from math import log
import sys
import re
import os

import numpy as np

import nltk;
import nltk.data
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib

from spacy.en import English
from textblob import TextBlob
from gensim import corpora, models, similarities, matutils
import enchant
from textstat.textstat import textstat
import matplotlib.pyplot as plt
from heapq import heappush, heappop
from reviewnlp.subject_object_extraction import extractData
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
from scipy.sparse import find

from dialectic_pipeline.lda import MyLDACorpus

class ModelTrainer(object):
	def __init__(self):


		self.wordTokenizer = TweetTokenizer()
		self.allTextInOrders = None


		self.featureLabels = []
		self.K=0
		self.lastOne = False
		self.vectorizer = None

		self.data_text = None

		self.corpus = None

		self.currentGenerator = 0

		self.lda = None #models.ldamodel.LdaModel.load("lda_states/ldapy" + segAdd + str(K));

		self.dfs = None
		self.wordweights = {}

		self.T = 50
		self.TRAIN =100

		self.product_features = []
		self.bad_words = []

		self.generateFeatures = True
		self.similarities = None

		self.clf2 = None
		self.good_adjs = []
		self.bad_adjs = []


		self.good_verbs = []
		self.bad_verbs = []

	def setTrainingVars(self, P, corp, num_topics, NTest, NTrain):
		self.T = NTest
		self.TRAIN = NTrain
		self.corpus = corp
		self.dfs = self.corpus.dfs()
		self.K= num_topics

		loc = "exports/" + P +"/lda_states/ldapy"+str(self.K)
		self.lda = models.ldamodel.LdaModel.load(loc);



		for z in range(0,self.K):
			topic = self.lda.state.get_lambda()[z]
			topic = topic / topic.sum()
			bestn = matutils.argsort(topic, 100, reverse=True)
			terms = [(id, topic[id]) for id in bestn]

			#terms = lda.get_topic_terms(z,100)
			for term in terms:
				word = corp.dictionary[term[0]].lower()
				weight = term[1]
				occurences = self.dfs[term[0]]
				#idf = log(corpus.documentCount/(1+occurences))
				if word in self.wordweights:
					if weight > self.wordweights[word]:
						self.wordweights[word] = weight #* idf
				else:
					self.wordweights[word] = weight #* idf
		#print('\n\n')


		with open("exports/"+P+"/good_ADJ.txt","r") as f:
			for line in f:
				self.good_adjs.append(line.strip());

		with open("exports/"+P+"/bad_ADJ.txt","r") as f:
			for line in f:
				self.bad_adjs.append(line.strip());


		with open("exports/"+P+"/good_NOUN.txt","r") as f:
			for line in f:
				self.good_verbs.append(line.strip());

		with open("exports/"+P+"/bad_NOUN.txt","r") as f:
			for line in f:
				self.bad_verbs.append(line.strip());


		with open("exports/"+P+"/featuresAprioriLexicalPruned.txt","r") as f:
			for line in f:
				self.product_features.append(line.strip());

		with open("inputs/badwords.txt","r") as f:
			for line in f:
				self.bad_words.append(line.decode('utf-8').strip());
		self.currentGenerator = NTrain*2


		self.nlp = English()
		self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle');		
		self.d = enchant.Dict("en_US")



	def getStats(self,head):
		for child in head.children:
			self.dependencies+=1
			self.getStats(child)

		total = self.dependencies
		return self.dependencies;

	def treeHeights(self,head, soFar):

		if soFar > 22:
			return 22

		maxHeight = 0

		numChildren = 0

		for child in head.children:
			numChildren+=1
			thisHeight = self.treeHeights(child, soFar+1)
			if self.treeHeights(child, soFar+1) > maxHeight:
				maxHeight = thisHeight

		if numChildren == 0:
			return soFar
		return maxHeight


	def addFeature(self,feature, features, name):
		if self.lastOne:
			self.featureLabels.append(name)
		features.append(feature)



	def genfeatures(self,json_review):

		reviewText = json_review["reviewText"]

		print(reviewText)


		wordCount2 = len(self.wordTokenizer.tokenize(reviewText))


		bleh = self.lda[self.corpus.dictionary.doc2bow(self.corpus.proc(reviewText))]


		helpfulSim = 0.0
		uselessSim = 0.0
		helpfulSimTopic  = 0.0
		uselessSimTopic  = 0.0
		for j in range(0,self.TRAIN*2):
			if self.similarities[self.currentGenerator][j] != 1:
				if j < self.TRAIN:
					helpfulSim += self.similarities[self.currentGenerator][j]
					#helpfulSimTopic += matutils.cossim(trainingDistributions[j], bleh)
				else:
					uselessSim += self.similarities[self.currentGenerator][j]
					#uselessSimTopic += matutils.cossim(trainingDistributions[j], bleh)

		#print("HELPFUL-SIM",helpfulSim)
		#print("USELESS-SIM",uselessSim)

		self.currentGenerator+=1
		document = self.nlp(reviewText)

		



		s = [sent.string.lower().strip() for sent in document.sents]

		iStart = 0
		iTotal = 0
		brandMention = 0
		goodAdjMention = 0.0
		badAdjMention = 0.0
		goodVerbMention = 0.0
		badVerbMention = 0.0
		lastBrand = ""

		punct = 0


		wordScore = 0
		wordCount = 0


		nounCount = 0.0
		verbCount = 0.0
		adjCount = 0.0
		detCount = 0.0
		tokenCount = 0.0


		totalDep = 0.0
		totalHeight = 0.0


		prosandcons = 0

		wordScoreList = []

		for sentence in document.sents:
			i = 0
			root = None

			startSentence = 0.0





			for token in sentence:

				

				if token.head is token:
					root = token



				if token.orth_ in self.wordweights:
					wordScore+=self.wordweights[token.orth_.lower()]
					startSentence+=self.wordweights[token.orth_.lower()]
					wordCount+=1

				if token.orth_ == 'I':
					if i == 0:
						iStart+=1
					iTotal+=1

				if token.orth_.lower() in self.good_adjs:
					goodAdjMention+=1
				if token.orth_.lower() in self.bad_adjs:
					badAdjMention+=1
				if token.orth_.lower() in self.good_verbs:
					goodVerbMention+=1
				if token.orth_.lower() in self.bad_verbs:
					badVerbMention+=1
				if token.is_punct and token.orth_ != ".":
					punct+=1
				i+=1

				if (token.pos_ == "NOUN"):
					nounCount+=1
				if (token.pos_ == "VERB"):
					verbCount+=1
				if (token.pos_ == "ADJ" or token.pos_ == "ADV"):
					adjCount+=1
				if (token.pos_ == "DET"):
					detCount+=1				

				#print(token.pos_)

				tokenCount+=1

			self.dependencies = 0
			stats = self.getStats(root)

			wordScoreList.append(startSentence)
			#print(sentence)

			#totalHeight += treeHeights(root,1)		#
			totalDep += stats
		
		print(wordScore)
		#print(wordCount)

		wordScore = wordScore * 10

		iStartNorm = float(iStart)/float(len(s))
		iTotalNorm = float(iTotal)/float(len(s))

		if len(s) ==0:
			s.append("blah.")
		C = .05





		numFeatureSentence = 0
		nPositive = 0
		nNegative = 0
		nNeutral = 0

		pOpinion = 0.0
		pPositive = 0.0
		pNegative = 0.0
		pNeutral = 0.0

		nSentencesMentionPF = 0

		

		misSpelled = 0


		noOpinion = True
		posI = 0

		senWordLengths = []


		review = reviewText.lower().replace("."," ").replace("/"," ")  # convert bytes into proper unicode
		



		compounds = []

		for sentence in s:
			#print(sentence)

			blob = TextBlob(sentence)
			vs = vaderSentiment(sentence)


			wordLength = len(blob.words)
			senWordLengths.append(wordLength)

			#b3 = [val for val in sentence if val in bad_words]
			#print(b3)
			if any(pF in sentence for pF in self.product_features):
				if (abs(vs['compound']) >= C):
					numFeatureSentence+=1
					if noOpinion:
						noOpinion = False
				if (vs['compound'] > C):
					nPositive+=1
				elif (vs['compound'] < -C):
					nNegative+=1
				else:
					nNeutral += 1

				nSentencesMentionPF+=1
			if noOpinion:
				posI+=1

			compounds.append(vs['compound'])


		if (len(senWordLengths) ==0):
			senWordLengths.append(0)

	    # 	if (d.check(word)):
	    # 		finalword.append(word)

		totalPF = 0
		totalBW = 0
		for pF in self.product_features:
			if pF in reviewText.strip().lower():
				totalPF+=1

		for pF in self.bad_words:
			if pF in reviewText.strip().lower():
				totalBW+=1
				#print(pF)

			


		avgPF = totalPF/float(len(s))

		pOpinion = numFeatureSentence/float(len(s))
		pPositive = nPositive/float(len(s))
		pNegative = nNegative/float(len(s))
		pNeutral = nNeutral/float(len(s))

		


		if numFeatureSentence == 0:
			pPositive2 = 0
			pNegative2 = 0
		else:
			pPositive2 = nPositive/float(numFeatureSentence)
			pNegative2 = nNegative/float(numFeatureSentence)


		allF = []
		
		tb = TextBlob(review)

		# corr = str(tb.correct())

		# sim = sum(a==b for a, b in zip(corr, review))



		# allF.append(sim/float(len(review)))
		# print(allF)



		self.addFeature(numFeatureSentence, allF, "Number of feature sentences")
		self.addFeature(pOpinion, allF, "percent of opinion sentences")
		self.addFeature(pPositive, allF, "percent of positive sentences")
		self.addFeature(pNeutral, allF, "percent of neutral sentences")
		self.addFeature(totalPF, allF, "total product features")
		self.addFeature(avgPF, allF, "avg product features p/sentences")
		#self.addFeature(pPositive2, allF, "percent of positive sentences x2")
		self.addFeature(nSentencesMentionPF, allF, "Number of sentences with product features in them")
		#self.addFeature((len(s) - nSentencesMentionPF)/len(s), allF, "Number of sentences with product features in them")


		#print lda.show_topics(15,50, formatted=True);
		t = 0
		

		weights = {}

		for z in range(0,self.K):
			weights[z] = 0



		tops = []

		for topic in bleh:
			t+=1
			weights[topic[0]] = topic[1]
			heappush(tops, (-topic[1], topic[0]))

		denom = 0.0

		for z in range(0,self.K):
			if weights[z] != 0:
				denom += log(weights[z])



		entropy = 0.0
		for k in range(0,self.K):
			if weights[k] != 0:
				entropy += weights[k] * log(weights[k])


		self.addFeature(-tops[0][0] * wordCount2, allF, "#1 topic proportion")
		self.addFeature(tops[0][1], allF, "#1 topic ID")
		#allF.append(-tops[0][0] * wordCount2)
		#allF.append(tops[0][1])

		
		if t > 1:
			self.addFeature(-tops[1][0] * wordCount2, allF, "#2 topic proportion")
			self.addFeature(tops[1][1], allF, "#2 topic ID")
			#allF.append(-tops[1][0]  * wordCount2)
			#allF.append(tops[1][1])
		else:
			#allF.append(0)
			#allF.append(-1)
			self.addFeature(0, allF, "#2 topic proportion")
			self.addFeature(-1, allF, "#2 topic ID")

		if t >2:
			# allF.append(-tops[2][0]  * wordCount2)
			# allF.append(tops[2][1])
			self.addFeature(-tops[2][0] * wordCount2, allF, "#3 topic proportion")
			self.addFeature(tops[2][1], allF, "#3 topic ID")
		else:
			# allF.append(0)
			# allF.append(-1)
			self.addFeature(0, allF, "#3 topic proportion")
			self.addFeature(-1, allF, "#3 topic ID")

		#allF.append((float(t)/float(len(s))));

		self.addFeature((float(t)/float(len(s))), allF, "Topic diversity/Length ratio")


		self.addFeature(tb.sentiment.polarity, allF, "text polarity")
		self.addFeature(tb.sentiment.subjectivity, allF, "text subjectivity")
		# allF.append()
		# allF.append()



		misSpell = 0

		#print(tb.words)
		for word in tb.words:
			if self.d.check(word) == False:
				misSpell+=1

		self.addFeature((misSpell/float(len(s)+1.0)), allF, "mis-spelling count")

		self.addFeature(len(reviewText), allF, "characters in text")
		self.addFeature(len(tb.words), allF, "word count")
		self.addFeature(len(s), allF, "sentence count")

		self.addFeature(4.71 * float(len(reviewText)) / float(len(tb.words)) + 0.5 * float(len(tb.words)) / float(len(s)) - 21.43, allF, "complexity measure")

		self.addFeature(textstat.flesch_kincaid_grade(reviewText), allF, "flesch kincaid")
		#allF.append()
		self.addFeature(textstat.automated_readability_index(reviewText), allF, "ARI")
		self.addFeature(textstat.coleman_liau_index(reviewText), allF, "ARI")


		self.addFeature(float(sum(1 for c in reviewText if c.isupper()))/float(len(reviewText)), allF, "Upper case percentage")


		
			#allF.append(weights[z])

		for z in range(0,self.K):
			if weights[z] != 0:
				self.addFeature(log(weights[z])/denom, allF, "weighting for topic " + str(z))
				#allF.append(weights[z])
				#weights[z] * len(wordCount2)
			else:
				self.addFeature(0, allF, "weighting for topic " + str(z))
				#allF.append(0)
			#allF.append(weights[z])

		trans = self.vectorizer.transform([reviewText])


		words = trans[0]
		ids = find(words)[1]
		weights = find(words)[2]

		net = 0
		positive = 0


		negative = 0


		for M in range(0,len(ids)):
			wordID = ids[M]
			wordWeight = weights[M]
			wordCoef = self.clf2.coef_[0][wordID]

			net += wordWeight * wordCoef

			if wordCoef > 0:
				positive += wordWeight * wordCoef
			else:
				negative += wordWeight * wordCoef

		decide = self.clf2.decision_function(trans)[0]

		
		
		
		
		#allF.append(decide)
		#make sure to add decide in a bit...
		self.addFeature(iStart, allF, "sentences that begin with I")
		self.addFeature(iTotal, allF, "total I usage")
		self.addFeature(iStartNorm, allF, "iStart normalized")
		self.addFeature(iTotalNorm, allF, "iTotal normalized")

		# allF.append(iStart)
		# allF.append(iTotal)
		# allF.append(iStartNorm)
		# allF.append(brandMention)
		# allF.append()

		# if lastBrand == "":
		# 	allF.append(-1)
		# else:calcc
		# 	allF.append(brands.index(lastBrand))

		self.addFeature(punct, allF, "punctuations")
		self.addFeature(float(punct)/float(len(s)), allF, "punctuations normalized")

		# allF.append(punct)
		# allF.append()	

		#allF.append(wordScore)
		

		#allF.append(wordCount)
		self.addFeature(float(wordCount)/float(len(s)), allF, "avg. words per sentence")
		#allF.append()
		#allF.append(net)
		#allF.append(positive)
		# allF.append(negative)


		# allF.append(nounCount/tokenCount * 100) #4th
		# #allF.append(verbCount/tokenCount * 100) #1st heaviest NOT GOOD---- 
		# allF.append(adjCount/tokenCount * 100) #3rd 
		# allF.append() #2nd heaviest  -- NEUTRAL?



		self.addFeature(adjCount/tokenCount * 100, allF, "percent of adjectives")
		self.addFeature(detCount/tokenCount * 100, allF, "percentage of dets")

		orgCount = 0.0
		productCount = 0.0
		dateCount = 0.0

		for ent in document.ents:
			if (ent.label_ == "DATE" or ent.label_ == "TIME"):
				dateCount+=1
			if (ent.label_ == "ORG"):
				orgCount+=1
			if (ent.label_ == "PRODUCT"):
				productCount+=1


		self.addFeature(orgCount/float(len(s)), allF, "organization mentions")
		self.addFeature(productCount/float(len(s)), allF, "product mentions")
		self.addFeature(dateCount/float(len(s)), allF, "date mentions")


		SVOS = extractData(document)

		for bit in SVOS:
			self.addFeature(float(bit)/float(len(s)), allF, "bits")


		self.addFeature(helpfulSim - uselessSim, allF, "TFIDF language comparison")


		self.addFeature(np.average(compounds), allF, "compounds average")
		self.addFeature(np.std(compounds), allF, "compounds std")
		self.addFeature(float(totalBW)/float(len(s)), allF, "totalBW normalized")

		#allF.append(totalHeight/float(len(document)))


		digits = 0.0
		
		digits += len(re.findall('[\d]+', reviewText))


		self.addFeature(float(goodAdjMention - badAdjMention)/float(len(s)), allF, "adjective diff")
		self.addFeature(float(goodVerbMention - badVerbMention)/float(len(s)), allF, "verb diff")
		self.addFeature(np.std(wordScoreList), allF, "word score std")
		self.addFeature(float(wordScore)/float(len(s)), allF, "word score normalized")


		#self.addFeature(json_review["overall"], allF, "overall score")

		include = [5, 17, 51, 18,  4, 1, 6, 64, 66, 12,10,8,60, 14, 63, 24, 2, 62,53, 23, 20, 22, 21, 50, 49, 13, 52, 7, 9, 11] + range(25,43)

		keep = []
		for i in range(0,len(allF)):
			if i in include:
				keep.append(allF[i])
			else:
				keep.append(0)
		return allF


	def trainClassifier(self,P, data_file, cutoff, classifierDump, vectorizerDump, explanationDump):


		helpful = []
		helpful_text = []
		unhelpful = []
		unhelpful_text = []



		helpful_exp = []
		unhelpful_exp = []
		helpful_exp_text = []
		unhelpful_exp_text = []



		banned_ids = []



		co = 0
		#with open("exports/data_segments.txt",'r') as f:
		with open(data_file,'r') as f:
			for line in f:
				js = json.loads(line)
				identifier = js["reviewerID"] + str(js["unixReviewTime"])

				if js["helpful"][1] < 15 or len(js["reviewText"]) < 10:
					continue
				# if identifier in banned_ids:
				# 	print("-----I JUST FILTERED OUT A BANNED ID------")
				# 	print(co)
				# 	co+=1
				# 	continue

				text = js["reviewText"]
				score = float(js["helpful"][0])/float(js["helpful"][1])

				s = len(self.sent_detector.tokenize(text.strip().lower()))

				if score < cutoff:
					unhelpful.append(js)
					unhelpful_text.append(text)

				elif score > cutoff:
					helpful.append(js)
					helpful_text.append(text)




		print(len(helpful))
		print(len(unhelpful))

		print("\n\n\n\n\n\n\n\n\n")

		seed(452)
		shuffle(helpful_text)
		seed(452)
		shuffle(helpful_exp)
		seed(600)
		shuffle(unhelpful_text)
		seed(600)
		shuffle(unhelpful_exp)



		for i in range(0,self.T):
			helpful_exp.append(helpful.pop())
			unhelpful_exp.append(unhelpful.pop())
			helpful_exp_text.append(helpful_text.pop())
			unhelpful_exp_text.append(unhelpful_text.pop())


		all_exp = helpful_exp + unhelpful_exp
		# file = open("exports/experimental_segments.txt", "w")
		# for l in all_exp:
		# 	file.write(json.dumps(l)+"\n")
		# file.close()


		# j = 0
		# for i in unhelpful_exp:
		# 	print(unhelpful_exp[j]["reviewerID"])
		# 	print(helpful_exp[j]["reviewerID"])
		# 	j+=1

		helpful = helpful[:self.TRAIN]
		unhelpful_text = unhelpful_text[:self.TRAIN]
		helpful_text = helpful_text[:self.TRAIN]
		unhelpful = unhelpful[:self.TRAIN]


		# file = open("exports/data.txt", "w")
		# for h in helpful:
		# 	file.write(json.dumps(h)+"\n")
		# for h in unhelpful:
		# 	file.write(json.dumps(h)+"\n")
		# for h in unhelpful_exp:
		# 	file.write(json.dumps(h)+"\n")
		# for h in helpful_exp:
		# 	file.write(json.dumps(h)+"\n")
		# file.close()

		labels = []

		for i in helpful:
			labels.append(1)
		for i in unhelpful:
			labels.append(0)

		data = helpful + unhelpful
		self.data_text = helpful_text + unhelpful_text


		X = []
		spam_test = []
		ham_test = []


		self.vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
		                                 stop_words='english')

		X2 = self.vectorizer.fit_transform(self.data_text)
		self.clf2 = SGDClassifier(loss='log', penalty='l2',alpha=1e-5, n_iter=25, random_state=42,shuffle=True)
		self.clf2.fit(X2, labels)
		vocab = my_dict2 = {y:x for x,y in self.vectorizer.vocabulary_.iteritems()}


		#clf = RandomForestClassifier(n_estimators=750)
		self.allTextInOrders = self.data_text + self.data_text + unhelpful_exp_text + helpful_exp_text


		trainingDistributions = []

		# for reviewT in data_text:
		# 	trainingDistributions.append(lda[corpus.dictionary.doc2bow(corpus.proc(reviewT))])



		mat = self.vectorizer.transform(self.allTextInOrders)
		self.similarities = (mat * mat.T).A


		indices = np.argsort(self.vectorizer.idf_)[::-1]
		features = self.vectorizer.get_feature_names()
		top_n = 250
		top_features = [features[i] for i in indices[:top_n]]
		print top_features


		print("SHAPE\n\n\n\n")
		print(self.similarities.shape)
		self.lastOne = False

		inspectFeatures = []

		if self.generateFeatures:

			i = 0
			for r in data:
				print(i)
				#print(r)
				i+=1
				fff = self.genfeatures(r)
				X.append(fff)

			for i in range(0,self.T):
				print(i)
				spam_test.append(self.genfeatures(unhelpful_exp[i]))
			for i in range(0,self.T):
				print(i)
				if i == self.T-1:
					self.lastOne = True
				ham_test.append(self.genfeatures(helpful_exp[i]))




		if self.generateFeatures==False:
			spam_test =  self.vectorizer.transform(unhelpful_exp_text);
			ham_test =  self.vectorizer.transform(helpful_exp_text);
		else:
			clf = RandomForestClassifier(n_estimators=750, random_state=42)
			clf = clf.fit(X, labels)

		predict_spam = clf.predict(spam_test)
		predict_ham = clf.predict(ham_test)
		print(predict_ham)
		print(predict_spam)





		file2=open(explanationDump,"w")

		print("----------USEFUL CORRECTLY labeled as USEFUL------\n\n\n\n\n\n")
		for i in range(0,self.T):
			if (predict_ham[i]) == 1:
				helpful_exp[i]["label"] = "useful"
				print(helpful_exp[i])

		print("----------USEFUL WRONGLY labeled as USELESS------\n\n\n\n\n")
		for i in range(0,self.T):
			if (predict_ham[i]) == 0:
				print(helpful_exp[i])
				helpful_exp[i]["label"] = "useless"

		print("----------USELESS CORRECTLY labeled as USELESS------\n\n\n\n\n\n")
		for i in range(0,self.T):
			if (predict_spam[i]) == 0:
				print(unhelpful_exp[i])
				unhelpful_exp[i]["label"] = "useless"
				print(spam_test[i])
				unhelpful_exp[i]["featureList"] = str(spam_test[i])
				#file2.write(json.dumps(unhelpful_exp[i]))
				#file2.write("\n")

		print("----------USELESS WRONGLY labeled as USEFUL------")
		for i in range(0,self.T):
			if (predict_spam[i]) == 1:
				print(unhelpful_exp[i])
				unhelpful_exp[i]["label"] = "useful"
		#file2.close()

		gather = helpful_exp + unhelpful_exp


		for i in range(0,self.T):
			oj = {"featureList":spam_test[i], "reviewText":unhelpful_exp_text[i]}
			file2.write(json.dumps(oj)+"\n")
		file2.close()

		shuffle(gather)

		# file = open("segmentLabelMTurk/segments2.txt","w")
		# for l in (gather):
		# 	file.write(json.dumps(l) + "\n")
		# file.close()

		perc1 = 0.0
		perc2 = 0.0


		if self.generateFeatures:
			importances = clf.feature_importances_
			std = np.std([tree.feature_importances_ for tree in clf.estimators_],
			             axis=0)
			indices = np.argsort(importances)[::-1]

			# Print the feature ranking
			print("Feature ranking:")

			X2 = np.asarray(X)


			for f in range(X2.shape[1]):
				print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
				print ("^ aka " + self.featureLabels[indices[f]])
				helpfuls = X[:len(X)/2]
				unhelpfuls = X[len(X)/2:]
				c1 = []
				c2 = []
				for fe in helpfuls:
					c1.append(fe[indices[f]])
				for fe in unhelpfuls:
					c2.append(fe[indices[f]])

				c1_avg = np.average(c1)
				c2_avg = np.average(c2)
				c1_std = np.std(c1)
				c2_std = np.std(c2)

				print("helpful: " + str(c1_avg) + "," + str(c1_std))
				print("unhelpful: " + str(c2_avg) + "," + str(c2_std))


			# Plot the feature importances of the forest
			# plt.figure()
			# plt.title("Feature importances")
			# plt.bar(range(X2.shape[1]), importances[indices],
			#        color="r", yerr=std[indices], align="center")
			# plt.xticks(range(X2.shape[1]), indices)
			# plt.xlim([-1, X2.shape[1]])
			I = 0
			L = 0

			true_pos = 0
			false_pos = 0
			true_neg = 0
			false_neg = 0
			# buckets = {}
			for i in range(0,self.T):

				if (predict_spam[i]) == 0:
					I+=1
					true_neg+=1
				else:
					false_neg+=1
				if (predict_ham[i]) == 1:
					true_pos+=1
					self.K+=1
				else:
					false_pos+=1

			print("FALSE POSITIVE, NEGATIVES, WHATEVER")
			print(true_pos)
			print(true_neg)
			print(false_neg)
			print(false_pos)

			print(I/float(self.T))
			print(L/float(self.T))

			perc1 = I/float(self.T)
			perc2 = L/float(self.T)

		joblib.dump(clf, classifierDump) 
		joblib.dump(self.vectorizer, vectorizerDump) 


