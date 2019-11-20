from justext import get_stoplist as get_justext_stoplist


# This method overrides get_stoplist from justext to handle chinese language
def get_stoplist(language):
    if language != 'Chinese':
        return get_justext_stoplist(language)
    else:
        stopwords = open('./' + language + '.txt', 'rb').read()
        return frozenset(w.decode("utf8").lower() for w in stopwords.splitlines())
