import logging
import os
import nltk
import sys


from textblob import TextBlob, Word, Blobber
from collections import Counter
from nltk.corpus import stopwords
from textblob import TextBlob



# Reads and returns the list of files from a directory
def read_directory(mypath):
    current_list_of_files = []

    while True:
        for (_, _, filenames) in os.walk(mypath):
            current_list_of_files = filenames
        logging.info("Reading the directory for the list of file names")
        return current_list_of_files



# Function you will be working with
def finding_aspects(input_review, name_of_file):
    # Your code that finds out the list of aspects present in the review and saves those aspects in a decreasing order of importance.
    # The output has to be saved in the data/output folder with the same name as data/input file
    # Note the writing to file has to be handled by you.
    
    
    review = input_review #the review contained in that file.
    sent_tokenize = nltk.tokenize.punkt.PunktSentenceTokenizer()
    
    def get_sentences(review):
    	"""
        INPUT: full text of a review
    	OUTPUT: a list of sentences
    	Given the text of a review, return a list of sentences. 
    	"""

    	if isinstance(review, str):
    		return sent_tokenize.tokenize(review)
    	else: 
    		raise TypeError('Sentence tokenizer got type %s, expected string' % type(review)) 
        
    def tokenize(sentence):
        """
    	INPUT: string (full sentence)
    	OUTPUT: list of strings
    	Given a sentence in string form, return 
    	a tokenized list of lowercased, spell corrected, lemmatized words. 
    	"""  
        sentence = str(TextBlob(sentence).correct()).lower()
        sentence = ' '.join([Word(word).lemmatize() for word in sentence.split()])
        return TextBlob(sentence).words

    def pos_tag(toked_sentence):
    	"""
    	INPUT: list of strings
    	OUTPUT: list of tuples
    	Given a tokenized sentence, return 
    	a list of tuples of form (token, POS)
    	where POS is the part of speech of token
    	"""
    	return nltk.pos_tag(toked_sentence)

    def aspects_from_tagged_sentences(tagged_sentences):
    	"""
    	INPUT: list of lists of strings
    	OUTPUT: list of aspects
    	Given a list of tokenized and pos_tagged sentences from reviews,
       return all the aspects
    	"""
    	STOPWORDS = set(stopwords.words('english'))
    
    	# find the most common nouns in the sentences
    	noun_counter = Counter()
    
    	for sent in tagged_sentences:
    		for word, pos in sent: 
    			if pos=='NNP' or pos=='NN' or pos=='NNS' or pos=='NNPS' and word not in STOPWORDS:
    				noun_counter[word] += 1
    
    	# list of tuples of form (noun, count)
    	return [noun for noun, _ in noun_counter.items()]


    #aspects extraction
    sentences = get_sentences(review)
    tokenized_sentences = [tokenize(sentence) for sentence in sentences]
    # pos tag each sentence
    tagged_sentences = [pos_tag(sentence) for sentence in tokenized_sentences]
    # from the pos tagged sentences, get a list of aspects
	aspects = aspects_from_tagged_sentences(tagged_sentences)
    
	return aspects
    
    #logging.debug("The list of input-files in the folder are {} with contents \n {}".format(name_of_file, input_review))
    
    #pass



# Main function
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

    # Folder where the input files are present
    mypath = "data/input"
    list_of_input_files = read_directory(mypath)


    #Working with each input file
    for each_file in list_of_input_files:
        with open(os.path.join(mypath, each_file), "r") as f:
            file_contents = f.read()
            finding_aspects(file_contents, each_file)
            
            #end of code