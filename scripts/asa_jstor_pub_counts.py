# This script takes the list of authors from the JSTOR corpus, standardizes
# names, creates counts of publications by author. Then taks the Faculty Names
# from the ASA data, standardizes the names, and creates a dataframe of
# publication counts using the dictionary created from the JSTOR data.

import pandas as pd
import re
import os
from Levenshtein import distance
import sys
sys.path.append('/Users/timothyelder/Documents/soc_of_soc/code')

def cleanNewlineMeta(string):

    # This function is for cleaning out extraneous newline (\n)
    # metacharacters from strings

    pattern = r'\n+' #for cleaning out extraneous new line metacharachters
    replacement = ' ' #replacement string for above new line metacharachters
    clean_string = re.sub(pattern, replacement, string)

    return clean_string

def sliceString(ListToSlice):

    # This function is for splitting up a comma delimited list of lists which is
    # converted into a string when saved as a CSV

    interests = ListToSlice
    pattern = r'\[|\]|\''
    replacement = ''
    for idx, i in enumerate(interests):
        if re.search(pattern, i) == None:
            pass
        else:
            clean_interest = re.sub(pattern, replacement, i)
            interests[idx] = clean_interest

    clean_interests = []

    for idx, i in enumerate(interests):
            temp_name = cleanNewlineMeta(i)
            clean_interests.append(temp_name.split(","))

    return clean_interests

pattern = r'(.+\,)(.+)' # regex for matching the first name and last name
aux_pattern = '(\S+)(.+)' # extra pattern for when the above doesn't match

#load complete faculty df from the ASA Guides
faculty_df = pd.read_csv("/home/timothyelder/jstor_parse/faculty_df_complete.csv")

#get names to list
asa_names = faculty_df['faculty_name'].to_list()

clean_asa_names = []


# For the ASA Network data, switching faculty name from "Last Name, First Name'
# to "First Name Last Name" for matching with the JSTOR data.

Also fixing the common error from OCR which read 'l' as '/'.



for i in asa_names:
    i = re.sub(r';|:', ',', i)
    # match regex to the file_name string
    if re.search(pattern, i) == None:
        match = re.search(aux_pattern, i)
        new_name = match.group(2) + ' ' + match.group(1)
        new_name = re.sub('\/', 'l', new_name, count=1) # replaces / for l, a common error
        new_name = re.sub('\,', '', new_name, count=1)
        new_name = new_name.lower()
        new_name = new_name.strip()

        clean_asa_names.append(new_name)

    else:
        # match regex to the file_name string
        match = re.search(pattern, i)

        new_name = match.group(2) + ' ' + match.group(1)
        new_name = re.sub('\/', 'l', new_name, count=1) # replaces / for l, a common error
        new_name = re.sub('\,', '', new_name, count=1)
        new_name = new_name.lower()
        new_name = new_name.strip()

        clean_asa_names.append(new_name)

# empty dictionary for creating counts of publications by authors
pubCounts = {}

# load JSTOR metadata
jstor_metadata = pd.read_csv("/home/timothyelder/jstor_parse/dataframes/jstor_metadata.csv")
jstor_authors = jstor_metadata['contributors'].to_list() # get names to list
doi = jstor_metadata['doi'].to_list() # get doi to list
del(jstor_metadata) # deletes jstor_metadata from working memory

clean_jstor_authors = sliceString(jstor_authors) # slice list of strings to get list of lists

# convert strings to lowercase and strip white space and errors
for idx, i in enumerate(clean_jstor_authors):
    for jdx, j in enumerate(i):
        clean = j.lower()
        clean = re.sub(r'\"', r' ', clean) # extraneous quotation marks
        clean = re.sub(r'\\xa0', r' ', clean) # error in names
        clean = re.sub(r'\s{2,10}', r' ', clean) #replacing extra white space between names with single space
        clean = clean.strip()
        clean_jstor_authors[idx][jdx] = clean # strip white space around string and replace old string in list

        # if author name in the dictionary
        if clean in pubCounts:
            # add 1 count to value for author key
            pubCounts[clean] += 1
        else:
            # otherwise, create key with 1 count value
            pubCounts[clean] = 1

# dataframe for ASA guide names
df = pd.DataFrame(list(zip(asa_names, clean_asa_names)),
columns =["asa_names", "clean_asa_names"])

# create column of zeros
df['pub_count'] = 0

for idx,i in enumerate(df["clean_asa_names"]):
    if i not in pubCounts.keys():
        pass
    else:
        df['pub_count'].loc[idx] = pubCounts[i]


df.to_csv('/home/timothyelder/jstor_parse/dataframes/pub_counts.csv', index = False)
