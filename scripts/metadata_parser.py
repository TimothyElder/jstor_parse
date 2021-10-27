# This script is for opening the archived zip files, 
# loading text, and then parsing the XML files, pulling 
# out the metadata of interest. It then creates a 
# dataframe and saves it as a CSV. Where data is missing 
# in the files I will insert NaN into the dataframe, which 
# in later analyses can be treated as NA or replaced with 
# another value. This script uses absolute file locations
# rather than relative ones.

import re                      
import os
import lxml 
import time
import bacchus  
import zipfile 
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

start_time = time.time()        
                 
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

                    # Load zip file
                    my_zip = zf.open(j, mode = 'r')

                    # decode file to text
                    file_text = (my_zip.read()).decode("utf-8")

                    # Parse with beautifulsoup
                    soup = BeautifulSoup(file_text, 'html')
                    
                    # temporary list for list of authors in the file text
                    temp_author_list = [] 
                    
                    # temporary list for list of author affiliations in the file text
                    temp_affiliation_list = [] 

                    # for author in the list of authors
                    for m in soup.find_all('contrib'):
                        
                        # append author to temporary list of authors
                        temp_author_list.append(cleanNewlineMeta(m.text))
                        
                        #append list of authors to main list of authors
                    list_of_authors.append(temp_author_list) 

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
                            
                            # append affiliation to temporary list of affiliations
                            temp_affiliation_list.append(l.text) 
                            
                         # append list of author's affiliations to main list of author affiliations
                        list_of_affiliations.append(temp_affiliation_list)

                    # abstracts
                    if soup.find('abstract') == None:
                        abstract.append(np.NaN)
                    else:
                        abstract.append(soup.find('abstract').text)



# packing the lists into a dataframe
df = pd.DataFrame(list(zip(file_name, doi, list_of_authors, list_of_affiliations, 
                           year_published, article_subject, article_title, 
                           journal_name, journal_id, abstract)), 
                           columns = ["file_name", "doi", "contributors", "affiliation",
                                     "year_published", "article_subject", 
                                     "article_title", "journal_name", "journal_id", 
                                      "abstract"])

df.to_csv("/home/timothyelder/jstor_parse/data/metadata.csv", index = False)

print("My program took", time.time() - start_time, "seconds to run.")

print("That is", (time.time() - start_time)/60, "minutes")
