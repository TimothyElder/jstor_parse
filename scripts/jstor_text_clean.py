# This script opens all the files in the zipped 
# archives, stems, lems and normalizes before 
# returning a really large CSV file of all the cleaned 
# text. Includes a few lines of code for getting how
# long the script takes to run. 

import time
start_time = time.time()
from nltk.corpus import stopwords
from csv import DictReader
from csv import reader
import pandas as pd
import nltk
import csv
import os
import re
import sys
csv.field_size_limit(sys.maxsize)

os.chdir('/home/timothyelder/jstor_parse')

# stop word list, generic stop word list
stop_words_nltk = stopwords.words('english')

#The stemmers and lemmers need to be initialized before being run
porter = nltk.stem.porter.PorterStemmer()
snowball = nltk.stem.snowball.SnowballStemmer('english')
wordnet = nltk.stem.WordNetLemmatizer()

tokenized_text = [] #empty list for appending tokenized text entries
normalized_tokens = [] #normalized tokens
normalized_tokens_count = [] #count of normalized tokens
normalized_tokens_POS = [] #part of speech tagger
doi = []

# iterate over each line as a ordered dictionary and print only few column by column name
with open('dataframes/jstor_text.csv', 'r') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    for idx, row in enumerate(csv_dict_reader):
        file_text = row['text']
        file_doi = row['doi']
        doi.append(file_doi)
        tokens = nltk.word_tokenize(file_text) #tokenize the entry
        tokenized_text.append(tokens) #append to the empty list

        normalized = normlizeTokens(tokens, stopwordLst = stop_words_nltk, stemmer = porter) #normal
        normalized_tokens.append(normalized)
        normalized_tokens_count.append(len(normalized))
        normalized_tokens_POS = [nltk.pos_tag(t) for t in normalized_tokens]

df = pd.DataFrame(list(zip(
doi,
tokenized_text,
normalized_tokens,
normalized_tokens_count,
normalized_tokens_POS)), columns =[
"doi",
"tokenized_text",
"normalized_tokens",
"normalized_tokens_count",
"normalized_tokens_POS"])

print("Code took", (time.time() - start_time)/60, "minutes to execute")

df.to_csv("/home/timothyelder/jstor_parse/data/jstor_standard_text.csv", index = False)
