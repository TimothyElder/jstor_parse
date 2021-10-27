# jstor_parse

This repository contains code for parsing a large corpus of JSTOR articles. The code can be adapted for use with other large unparsed and nonstandard corpora, particularly those that are distributed via [zipped](https://en.wikipedia.org/wiki/ZIP_(file_format) archives. Rather than unzipping large archives, this code streams data from zipped files using the [`zipfile`](https://docs.python.org/3/library/zipfile.html) library in `python`.

Articles are then parsed using standard NLP methods with [`BeautifulSoup`](https://pypi.org/project/beautifulsoup4/). As the JSTOR corpus metadata and text files are contributed from the individual publishers, the XML formatting is not standard with certain tags missing in a large number of files. To accomodate this, the code first explores the corpus to estimate where tags are missing, selectively unzipping articles for manual inspection. 
