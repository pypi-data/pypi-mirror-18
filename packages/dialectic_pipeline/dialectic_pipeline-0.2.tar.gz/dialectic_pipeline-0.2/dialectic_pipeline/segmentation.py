import json 
import logging
import numpy as np;
import math
import operator

from gensim import corpora, models, similarities, matutils
from textblob import TextBlob
import nltk.data

nlp = None
logger = logging.getLogger(__name__)

def setNLP(nl):
	global nlp
	nlp = nl


def get_std(clusters, num_sents):
	'''standard deviation of the cluster size'''
	avg_c_size = num_sents / len(clusters)
	num = 0
	for cluster in clusters:
		num += math.pow(len(cluster) - avg_c_size, 2)
	return math.sqrt(num / len(clusters))

def cluster_sim(clusters, cluster_1, cluster_2, simMat, num_sents):
	'''clusters indices of all clusters, 
	cluster 1 indices of a cluster, cluster 2 indices of a cluster'''
	sim = 0
	for i in cluster_1:
		for j in cluster_2:
			sim += simMat[i, j]
	std = get_std(clusters, num_sents)
	sim = (2 * sim) / (math.pow((len(cluster_1) + len(cluster_2)), 2)) # - std
	return sim

def get_segments(clusters, sents):
	'''get the text'''

	print 'clusters in get_segments', clusters
	for cluster in clusters:
		for i in cluster:
			print sents[i]
		print '\n\n'

def segmentation_hac(model, corpus):
	'''segmentation algorithm'''

	with open('test.txt', 'r') as f:
		text = f.read()
	doc = nlp(unicode(text, encoding="utf-8"))

	num_sents = 0
	sents = []
	for sent in doc.sents:
		sents.append(str(sent))
		num_sents += 1

	print 'sents', sents

	'''Calc similarity matrix''' 
	simMat = np.zeros(shape = (num_sents, num_sents))
	for i, sent1 in enumerate(sents):
		for j, sent2 in enumerate(sents):
			if (j > i):
				block_lda1 = model[corpus.dictionary.doc2bow(corpus.proc(sent1))];
				block_lda2 = model[corpus.dictionary.doc2bow(corpus.proc(sent2))];
				simMat[i][j] = matutils.cossim(block_lda1, block_lda2) 
	
	'''Get initial clusters'''
	INIT_THRESH = 0.50
	clusters = []
	cluster = []
	print 'num_sents', num_sents
	for i in range(0, num_sents):
		cluster.append(i)
		if max(simMat[:, i]) < INIT_THRESH:
			clusters.append(cluster)
			print cluster
			cluster = []
	clusters.append(cluster)
	
	print 'initial clusters', clusters

	adj_similarities = []
	for i in range(0, len(clusters) - 1):
		print cluster_sim(clusters, clusters[i], clusters[i + 1], simMat, num_sents)
		adj_similarities.append(cluster_sim(clusters, clusters[i],
			clusters[i + 1], simMat, num_sents))

	while (adj_similarities and max(adj_similarities) < 0.15):
		max_index, max_value = max(enumerate(adj_similarities), key=operator.itemgetter(1))
		new_cluster = clusters[max_index] + clusters[max_index + 1]
		del clusters[max_index]
		del clusters[max_index]
		clusters.insert(max_index, new_cluster)
		print clusters
		
		adj_similarities = []
		for i in range(0, len(clusters) - 1):
			print cluster_sim(clusters, clusters[i], clusters[i + 1], simMat, num_sents)
			adj_similarities.append(cluster_sim(clusters, clusters[i],
			clusters[i + 1], simMat, num_sents))
	
	get_segments(clusters, sents)
	print clusters


class TopicTiling():
	'''We default to TopicTiling, but any segmenter can be used'''

	def __init__(self, ldamodel, corpus):
		self.lda = ldamodel
		self.reviewc = corpus
		self.W = 2
	


	def GenerateBlocks(self,sentences, s):
		'''Move window across the text and generate strings at each inde'''
		start1 = s-self.W;
		end2 = s+self.W;
		blocks = [" ".join(sentences[start1:s])," ".join(sentences[s:end2])]
		return blocks

	def ComputerSimilarityOld(self,model, corpus, blocks):
		
		#print blocks;
		#print(s);
		vectors = [];
		##There are 2 blocks, the one before the sentence and the one after
		WordProbThreshold = False;
		X=0.0012
		Z = 7;
		for block in blocks:
			#print(block);
			words = corpus.proc(block)
			topic_distribution = {};
			words_culled = [];

			#Go through all the words and generate a topic vector, see TopicTiling paper
			for word in words:
				block_lda = model[corpus.dictionary.doc2bow(corpus.proc(word))];
				topic_id = 0;
				prob = 0;

				#Find maximal topic
				for t in block_lda:
					if t[1] > prob:
						topic_id = t[0];
						prob = t[1]

				#If topic  prob is too low, ignore because no confidence
				if (prob < .1):
					continue;


				#Use another threshold to ignore words that aren't very relevant to the topic
				ppp = 0;
				word_id = corpus.dictionary.token2id[word];
				if WordProbThreshold:
					terms = model.get_topic_terms(topic_id,100000);
					for term in terms:
						if term[0] == word_id:
							ppp = term[1];

				if (ppp < X and WordProbThreshold):
					#print("CUT  " + word + "	" + str(ppp));
					continue;

				#print(word + "	" + str(ppp));
				words_culled.append(word)
				if topic_distribution.has_key(topic_id):
					topic_distribution[topic_id] = topic_distribution[topic_id]+1;
				else:
					topic_distribution[topic_id] = 1;
			#print("-------------");
				#print((topic_id, prob));

			#print(model[corpus.dictionary.doc2bow(words_culled)])
			#print(topic_distribution)
			#print("bleh")
			vectors.append(topic_distribution.items());

		#Compute similarity via cossine similarity between front and back window for index
		dot_product = matutils.cossim(vectors[0],vectors[1])
		return dot_product;


	def segment(self, line):
		global logger

		W=2
		global nlp

		js = json.loads(line)
		text = js["reviewText"]
		docfull = nlp(text)

		#Get a list of all sentences based on spacy tokenizer
		sentences = [sent.string.strip() for sent in docfull.sents]

		input_text2 = text


		text = "";
	
		#for s in range (0,8):

		datapoints = [];

		#Go through all indexes and compute dot product behind and in front
		for s in range (0,len(sentences)):
			start1 = s-W;
			end2 = s+W;
			
			if (start1 >= 0 and end2 < len(sentences)):

				blocks = self.GenerateBlocks(sentences, s);
				dot_product = self.ComputerSimilarityOld(self.lda, self.reviewc, blocks);

				datapoints.append((s,dot_product))
			else:
				datapoints.append((s,0));
		#print(datapoints)
		d = np.asarray(datapoints)
		x = d[:,0];
		y = d[:,1];
		#print (x)
		

		logger.debug("hello2?")
		# print("shape")
		# print(d.shape)
		scores = np.zeros(shape=(len(sentences),2));
		#d = np.hstack((d,scores))
		#print(scores.shape);

		#Calculate the relative depth score
		for s in range (0,len(sentences)):
			start1 = s-self.W;
			end2 = s+self.W;
			if (start1 >= 0 and end2 < len(sentences)):
				#right depth score
				hr = d[s][1];
				ri = s+1;
				while True:
					if ri >= len(sentences):
						break;
					if d[ri][1] > hr:
						hr = d[ri][1];
						ri+=1;
					else:
						#d[s][2] = hr;
						#d[s][3] = ri-1;
						break;
				#left depth score
				hl = d[s][1];
				li = s-1;
				while True:
					if li < 0:
						break;
					if d[li][1] > hl:
						hl = d[li][1];
						li-=1;
					else:
						#d[s][2] = hl;
						#d[s][3] = li+1;
						break;
				depth = 0;
				if hl==0:
					depth = hr-d[s][1];
				if hr==0:
					depth = hl-d[s][1];
				else:
					depth = 0.5 * (hl-d[s][1] + hr-d[s][1]);
				#print(s);
				scores[s][0] = depth;
				#print(depth);
		#print(scores);

		logger.debug("hello?3")

		d = np.hstack((d,scores))	
		#print();
		scoreCalc = []
		for s in range (0,len(sentences)):
			if d[s][2] != 0:
				scoreCalc.append(d[s][2])

		npp = np.asarray(scoreCalc)
		std = np.std(npp)
		mean = np.mean(npp)

		#Depth scores above this threshold denote new segments
		threshold = mean #+ std/2

		logger.debug("hello?5")
		for s in range (0,len(sentences)):
			logger.debug(d[s][2])
			if d[s][2] > threshold:
				d[s][3] = .1;
	
		documents = []

		document = "";
		predicted_seg="";
		for row in d:
			if (row[3] == .1):
				predicted_seg += "1";
	
				documents.append(document);


				document = "";
			else:
				predicted_seg+="0"

			document = document + " " + sentences[int(row[0])];

		documents.append(document);
		return documents






def generateSegments(inputs, output, segmenter):
	input_reviews = []
	global logger
	with open(inputs,'r') as f:
		for line in f:
			if (len(line) > 5):
				input_reviews.append(line)
			# if len(line) > 5 and TextBlob(line).words > 15 and json.loads(line)["helpful"][1] >= 15:
				# input_reviews.append(line);

	out = open(output,"w")
	i = 0
	for line in input_reviews:

		segments = segmenter.segment(line)
		js = json.loads(line)
		
		logger.debug(segments)
		for s in segments:
			js["reviewText"] = s
			out.write(json.dumps(js) + "\n")
		logger.debug(i)
		i+=1

	out.close()


