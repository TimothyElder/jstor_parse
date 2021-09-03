# This script is for opening the archived zip files, loading text, and then
# parsing the XML files, pulling out the metadata of interest. It then creates
# a dataframe and saves it as a CSV. Where data is missing in the files I will
# insert NaN into the dataframe, which in later analyses can be treated as NA
# or replaced with another value. This script uses absolute file locations
# rather than relative ones.

import time                     # for timing how long the script lastss
start_time = time.time()        # creates start time variable for knowing how long the script takes to execute
import zipfile                  # library for extracting data from zipped archives
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re                       # regex
import os
import lxml                     # xml parser for Bs4

# Functions

def cleanNewlineMeta(string):
    '''
    This function is for cleaning out extraneous newline (\n) metacharacters from strings
    '''
    pattern = r'\n+' #for cleaning out extraneous new line metacharachters
    replacement = ' ' #replacement string for above new line metacharachters
    clean_string = re.sub(pattern, replacement, string)

    return clean_string

def cleanNgram(string):
    '''
    Cleans file name strings to get the DOI number. The DOI will be the principal means of identifying the file data.
    '''
    pattern = r'\-.+' #for cleaning out extraneous new line metacharachters
    replacement = '' #replacement string for above new line metacharachters
    new_string = string.replace('_', '/', 1)
    clean_string = re.sub(pattern, replacement, new_string)

    return clean_string

pattern = '\/(journal\-article\-(.+)\.)'   #regex for pulling out DOI from file name.

# Lists for appending data from metadata files to
doi = []
file_sub_name = []
file_name = []
article_id = []
article_title = []
journal_name = []
journal_id = []
year_published = []
article_subject = []
abstract = []
list_of_authors = []
list_of_affiliations = []

#zip_location = '/Volumes/timothyelder/Downloads/receipt-id-2158941-part-016.zip'
# For  file in the Downloads directoty
for i in os.listdir('/home/timothyelder/Downloads'):

    # If file starts with receipt
     if i.startswith('receipt') == True:

            # Build string of file location
            zip_location = '/home/timothyelder/Downloads/'+i

            # Load archive of zipped files
            zf = zipfile.ZipFile(zip_location)

            # for file in files list from zipped archive
            for idx, j in enumerate(zf.namelist()):

                #if the file starts with metadata
                if j.startswith('metadata/') == True:

                    # get complete file name
                    file_name.append(j)

                    # match regex to the file_name string
                    match = re.search(pattern, j)

                    doi.append(cleanNgram(match.group(2))) # get the DOI number
                    file_sub_name.append(match.group(1)) # get the subname of the file

                    # Load zip file
                    my_zip = zf.open(j, mode = 'r')

                    # decode file to text
                    file_text = (my_zip.read()).decode("utf-8")

                    # Parse with beautifulsoup
                    soup = BeautifulSoup(file_text, 'html')
                    temp_author_list = [] # temporary list for list of authors in the file text
                    temp_affiliation_list = [] # temporary list for list of author affiliations in the file text

                    # for author in the list of authors
                    for m in soup.find_all('contrib'):
                        temp_author_list.append(cleanNewlineMeta(m.text)) # append author to temporary list of authors
                    list_of_authors.append(temp_author_list) #append list of authors to main list of authors

                    # year_published
                    if soup.find('pub-date') == None:
                        year_published.append(np.NaN)
                    else:
                        year_published.append(soup.find('pub-date').text)

                    #article_subject
                    if soup.find('subject') == None:
                        article_subject.append(np.NaN)
                    else:
                        article_subject.append(soup.find('subject').text)

                    # article titles
                    if soup.find('article-title') == None:
                        article_title.append(np.NaN)
                    else:
                        article_title.append(soup.find('article-title').text)

                    #journal_name
                    if soup.find('journal-title') == None:
                        journal_name.append(np.NaN)
                    else:
                        journal_name.append(soup.find('journal-title').text)

                    #journal_id, abbreviated and numerical
                    if soup.find('journal-id') == None:
                        journal_id.append(np.NaN)
                    else:
                        journal_id.append(soup.find('journal-id').text)

                    # author affiliations
                    if soup.find('aff') == None:
                        list_of_affiliations.append(np.NaN)
                    else:
                        for l in soup.find_all('aff'):
                            temp_affiliation_list.append(l.text) # append affiliation to temporary list of affiliations
                        list_of_affiliations.append(temp_affiliation_list) # append list of author's affiliations to main list of author affiliations

                    # abstracts
                    if soup.find('abstract') == None:
                        abstract.append(np.NaN)
                    else:
                        abstract.append(soup.find('abstract').text)


print("My program took", time.time() - start_time, "seconds to run.")

print("That is", (time.time() - start_time)/60, "minutes")

# packing the lists into a dataframe
df = pd.DataFrame(list(zip(file_name,
doi,
file_sub_name,
list_of_authors,
list_of_affiliations,
year_published,
article_subject,
article_title,
journal_name,
journal_id,
abstract)), columns =[
"file_name",
"doi",
"file_sub_name",
"contributors",
"affiliation",
"year_published",
"article_subject",
"article_title",
"journal_name",
"journal_id",
"abstract"])

df.to_csv("/home/timothyelder/jstor_parse/dataframes/jstor_metadata.csv", index = False)
