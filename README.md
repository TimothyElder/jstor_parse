# jstor_parse

This repository contains code for parsing a large corpus of JSTOR articles. The code can be adapted for use with other large unparsed and nonstandard corpora, particularly those that are distributed via [zipped](https://en.wikipedia.org/wiki/ZIP_(file_format)) archives. Rather than unzipping large archives, this code streams data from zipped files using the [`zipfile`](https://docs.python.org/3/library/zipfile.html) library in `python`.

Articles are then parsed using standard NLP methods with [`BeautifulSoup`](https://pypi.org/project/beautifulsoup4/). As the JSTOR corpus metadata and text files are contributed from the individual publishers, the XML formatting is not standard with certain tags missing in a large number of files. To accommodate this, the code first explores the corpus to estimate where tags are missing, selectively unzipping articles for manual inspection. 


## Script Descriptions 

`percent_parser.py` parses all the zipped archives and inspects the XML files to see what percentage of the files have which kinds of metadata. It returns a csv with 1s and 0s depending on whether the metadata is in the file. In this way you can see what percentage of the metadata items are in the corpus.

`text_parser.py` just returns non-standardized text from all the individual files

`jstor_text_clean.py` cleans all the stems, lems and normalizes all the text files and returns a really CSV with all the text, `jstor_standard_text.csv`

`metadata_parser.py` parses all the zipped archives and returns the metadata for each file. 

`asa_jstor_pub_counts.py` returns publication counts from our faculty members in the network data. 