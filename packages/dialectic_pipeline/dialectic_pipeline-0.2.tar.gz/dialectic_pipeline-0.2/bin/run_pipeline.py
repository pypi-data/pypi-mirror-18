import click
import logging
import sys
import os

from gensim import corpora, models, similarities, matutils
from spacy.en import English

from dialectic_pipeline import apriori
from dialectic_pipeline import featureExtraction
from dialectic_pipeline import generateExplainer
from dialectic_pipeline import segmentation
from dialectic_pipeline.model_trainer import ModelTrainer
from dialectic_pipeline.lda import MyLDACorpus

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

@click.command()
@click.argument("project_name")
@click.argument("num_topics")
@click.argument("corpus")
@click.argument("training")
@click.argument("testing")
@click.option('--exp', default="exports/", help='Location of export folder')
@click.option('--threshold', default=.6, help='Threshold to split data', type=float)
@click.option('--chunksize', default=20000, help='Corpus chunk size', type=int)
@click.option('--stopwords', default="inputs/stop_words.txt", help='Location of stop words')


def main(project_name,num_topics,corpus,training,testing,exp,threshold,chunksize,stopwords):
	reviewc = MyLDACorpus(corpus, stopwords, chunksize)

	#LDA topics K (#)
	num_topics = int(num_topics)

	#split count between training and test dataset
	training = int(training)
	testing = int(testing)

	#Initialize spacy
	nlp = English()

	#If there isn't a directory already for that corpus, make one
	if not os.path.exists(exp + project_name):
		os.makedirs(exp + project_name)
		os.makedirs(exp + project_name + "/lda_states")

	#Export LDA model, load, and initialize corpus
	#lda.generateModel(project_name,corpus,stopwords, num_topics)
	ldamodel = models.ldamodel.LdaModel.load(exp + project_name + "/lda_states/ldapy"+str(num_topics))
	

	explanationDump = exp + project_name + "/explanationDump.txt"

	#Train the random forest model and initialize
	trainer = ModelTrainer()
	trainer.setTrainingVars(project_name, reviewc, num_topics, testing,training)
	trainer.trainClassifier(project_name, corpus, threshold, exp + project_name + "/classifier.pkl", exp + project_name + "/vectorizer.pkl", explanationDump)

	#Generate data used for normalizing explanations of high impact features for review improvements
	generateExplainer.generateAllExplanations(project_name, exp + project_name + "/classifier.pkl", explanationDump,exp + project_name + "/scoreHistory.p")
	segmentation.setNLP(nlp)

	#Generate all segments, given a segmenter (default TopicTiling)
	segmenter = segmentation.TopicTiling(ldamodel,reviewc)
	segmentation.generateSegments(corpus,exp+project_name+"/all_segments.txt", segmenter)

	#Some features require data from the whole corpus, so we save those in advance
	featureExtraction.setNLP(nlp)
	featureExtraction.extractAllFeatures(project_name, corpus,  stopwords, ldamodel, reviewc)


if __name__ == "__main__":
	main()

