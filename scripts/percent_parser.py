'''
This code loads zipped directories, finds the metadata files for JSTOR articles then looks for the BeautifulSoup tags of interest. If the tag is found in the file, a 1 is appended to a list, if it is not found, a zero is appended. A dataframe is then constructed with the file names and the lists of zero and ones for tags. This is a rudimentary way of understanding what percentage of files have the soup tag of interest.
'''

#from zipfile import ZipFile
import zipfile
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import os
import lxml

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

    '''
    pattern = r'\-.+' #for cleaning out extraneous new line metacharachters
    replacement = '' #replacement string for above new line metacharachters
    new_string = string.replace('_', '/', 1)
    clean_string = re.sub(pattern, replacement, new_string)

    return clean_string

pattern = '\/(journal\-article\-(.+)\.)'   #regex for pulling out DOI from file name.

import time
start_time = time.time()

doi = []
doi_text = []
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

            # for file in zipped archive files list
            for idx, j in enumerate(zf.namelist()):

                #if the file starts with metadata
                if j.startswith('metadata/') == True:

                    #get file name
                    file_name.append(j)

                    match = re.search(pattern, j)
                    doi_match = match.group(2)

                    doi.append(cleanNgram(match.group(2)))
                    file_sub_name.append(match.group(1))

                    # Load zip file
                    my_zip = zf.open(j, mode = 'r')

                    # decode file to get text
                    file_text = (my_zip.read()).decode("utf-8")

                    # Parse with beautifulsoup
                    soup = BeautifulSoup(file_text, 'html')
                    temp_author_list = []
                    temp_affiliation_list = []

                    for m in soup.find_all('contrib'):
                        temp_author_list.append(cleanNewlineMeta(m.text)) #create list of contributors for article
                    list_of_authors.append(temp_author_list) #append list of contributors to main list

                    #year_published
                    if soup.find('pub-date') == None:
                        year_published.append(0)
                        filename = match.group(1)
                        file = open(r'/home/timothyelder/missing_tags/pub-date_missing/'+ filename +'xml','w')
                        file.write(file_text)
                        file.close()
                    else:
                        year_published.append(1)

                    #article_subject
                    if soup.find('subject') == None:
                        article_subject.append(0)
                        filename = match.group(1)
                        file = open(r'/home/timothyelder/missing_tags/subject_missing/'+ filename +'xml','w')
                        file.write(file_text)
                        file.close()

                    else:
                        article_subject.append(1)

                    # article titles
                    if soup.find('article-title') == None:
                        article_title.append(0)
                        filename = match.group(1)
                        file = open(r'/home/timothyelder/missing_tags/title_missing/'+ filename +'xml','w')
                        file.write(file_text)
                        file.close()
                    else:
                        article_title.append(1)

                    #journal_name
                    if soup.find('journal-title') == None:
                        journal_name.append(0)
                    else:
                        journal_name.append(1)

                    #journal_id, abbreviated and numerical
                    if soup.find('journal-id') == None:
                        journal_id.append(0)
                    else:
                        journal_id.append(1)

                    # author affiliations
                    if soup.find('aff') == None:
                        list_of_affiliations.append(0)
                        #filename = match.group(1)
                        #file = open(r'/home/timothyelder/missing_tags/subject_missing/'+ filename +'xml','w')
                        #file.write(file_text)
                        #file.close()
                    else:
                        #for l in soup.find_all('aff'):
                        #    temp_affiliation_list.append(l.text) #create list of contributors for article
                        #list_of_affiliations.append(temp_affiliation_list) #append list of contributors to main list
                        list_of_affiliations.append(1)

                    if soup.find('article-id', attrs={"pub-id-type" : "doi"}) == None:
                  #      print('doi missing')
                        doi_text.append(0)
                        #filename = match.group(1)
                        #file = open(r'/home/timothyelder/missing_tags/subject_missing/'+ filename +'xml','w')
                        #file.write(file_text)
                        #file.close()
                    else:
                        doi_text.append(1)


                    if soup.find('abstract') == None:
                  #      print('doi missing')
                        abstract.append(0)
                        #filename = match.group(1)
                        #file = open(r'/home/timothyelder/missing_tags/subject_missing/'+ filename +'xml','w')
                        #file.write(file_text)
                        #file.close()
                    else:
                        abstract.append(1)


print("My program took", time.time() - start_time, "seconds to run.")

print("That is", (time.time() - start_time)/60, "minutes")

#packing the lists into a dataframe, orders do not match up
df = pd.DataFrame(list(zip(file_name, doi, doi_text,
file_sub_name,
list_of_authors,
list_of_affiliations,
year_published,
article_subject,
article_title,
journal_name,
journal_id, abstract)), columns =["file_name", "doi", "doi_text",
"file_sub_name",
"contributors",
"affiliation",
"year_published",
"article_subject",
"article_title",
"journal_name",
"journal_id", "abstract"])

df.to_csv("/home/timothyelder/jstor_parse/dataframes/jstor_percentage_parse.csv", index = False)
