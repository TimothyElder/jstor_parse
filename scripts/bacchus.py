# A set of helper functions, the follow up to my Silenus module.

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


def normlizeTokens(tokenLst, stopwordLst = None, stemmer = None, lemmer = None):
    # We can use a generator here as we just need to iterate over it

    # Lowering the case and removing non-words
    workingIter = (w.lower() for w in tokenLst if w.isalpha())

    #Now we can use the stemmer, if provided
    if stemmer is not None:
        workingIter = (stemmer.stem(w) for w in workingIter)

    # And the lemmer
    if lemmer is not None:
        workingIter = (lemmer.lemmatize(w) for w in workingIter)

    #And remove the stopwords
    if stopwordLst is not None:
        workingIter = (w for w in workingIter if w not in stopwordLst)
    #We will return a list with the stopwords removed
    return list(workingIter)


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
