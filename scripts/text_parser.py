print("text_parser.py running...")
import time #for timing how long the script lastss
start_time = time.time() #creates start time variable for knowing how long the script takes to execute
print("start time is", start_time)
import zipfile #library for extracting data from zipped archives
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re # regex
import os
import lxml # xml parser for Bs4

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

# lists for appending data from metadata files to
doi = []
file_sub_name = []
file_name = []

text = []

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
                if j.startswith('ocr/') == True:

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

                    # if 'page' tag not present in the file
                    if soup.find('page') == None:
                        # if 'p' tag not present in the file
                        if soup.find('p') == None:
                            text.append(np.NaN)
                        else:
                            p = soup.find_all('p')
                            paragraphs = []
                            for x in p:
                                paragraphs.append(str(x))

                            paragraphs = ' '.join(paragraphs)
                            #print(paragraphs)
                            text.append(paragraphs)
                    # if 'page' tag present
                    else:
                        # find all 'page' tags
                        p = soup.find_all('page')
                        paragraphs = [] # create paragraph list
                        for x in p:
                            paragraphs.append(str(x)) # append page tags to list
                        # concatenate the parargraph list to single string
                        paragraphs = ' '.join(paragraphs)

                        text.append(paragraphs)

print("My program took", time.time() - start_time, "seconds to run.")

print("That is", (time.time() - start_time)/60, "minutes")

# packing the lists into a dataframe
df = pd.DataFrame(list(zip(file_name,
doi,
file_sub_name,
text)), columns =[
"file_name",
"doi",
"file_sub_name",
"text",
])

df.to_csv("/home/timothyelder/jstor_parse/dataframes/jstor_text.csv", index = False)
