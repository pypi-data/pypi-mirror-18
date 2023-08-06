from __future__ import unicode_literals

import re
import json
import sys
import copy
from random import shuffle

import matplotlib.pyplot as plt
from textblob import TextBlob
import numpy as np;
from gensim import corpora, models

print("IMPORTED LDA")

class MyLDACorpus(object):
	def __init__(self, fname, stopf = None, V = None):
		self.fname = fname;
		self.file = open(fname,"r");
		self.documentCount =  sum(1 for line in open(fname))
		
		stoplist = [];
		if stopf:
			with open(stopf,"r") as f:
				stoplist = map(lambda x: x.strip().lower(),f.readlines());
				self.st = stoplist
		self.dictionary = self.make_dict(stoplist, V);
	def rest(self):
		self.file.seek(0);
	def proc(self,line):
		return filter(lambda x: len(x) > 4, map(lambda x: x.strip(), re.sub(r'[0-9]+|\W',' ',line.strip().lower()).split()));
	def make_dict(self, stoplist = [], V = None):
		#self.reset();
		dictionary = corpora.Dictionary(self.proc(line) for line in self.read_file());
		stop_ids = [dictionary.token2id[sw] for sw in stoplist if sw in dictionary.token2id];
		dictionary.filter_tokens(stop_ids);
		dictionary.filter_extremes(5, .55);
		return dictionary;
	def dfs(self):
		return self.dictionary.dfs
	def read_file(self):
		with open(self.fname,"r") as f:
			for line in f:
				t = json.loads(line)["reviewText"]
				if (len(t.strip())> 3):
					yield t.strip();
	def __iter__(self):
		#self.reset();
		for line in self.read_file():
			bow = self.dictionary.doc2bow(self.proc(line));
			yield bow;


def generateModel(project_name, filename, stopwords, K):
	'''Runs latent dirichlet allocation to generate the model and save at filename'''
	reviewc = MyLDACorpus(filename, stopwords, 20000);

	lda = models.ldamodel.LdaModel(corpus=reviewc, id2word = reviewc.dictionary, num_topics = K, update_every = 1, chunksize = 500, passes = 1)
	
	print ("done");
	print lda.show_topics(K, formatted=True);

	for i in range(0,K):
		print("\n")
		print(lda.print_topic(i, topn=20))
	lda.save("exports/" + project_name + "/lda_states/ldapy" + str(K));	
