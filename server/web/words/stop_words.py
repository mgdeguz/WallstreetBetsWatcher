import nltk
from pandas import read_csv
from nltk.corpus import stopwords

def all_capitalizations(word_set):
    def upper(word_set):
        return {word.upper() for word in word_set}

    def lower(word_set):
        return {word.lower() for word in word_set}

    def capitalize(word_set):
        return {word.capitalize() for word in word_set}

    def remove_apostrophe(word_set):
        return {''.join(word.split("'")) for word in word_set if "'" in word}
    
    words = upper(word_set) | lower(word_set) | capitalize(word_set)
    words_no_apostrophes = upper(remove_apostrophe(words)) | lower(remove_apostrophe(words)) | capitalize(remove_apostrophe(words))

    return words | words_no_apostrophes

COMMON_WORDS = all_capitalizations(read_csv('data/common_words.csv')['word'].head(3000).dropna().to_list())
STOP_WORDS_NLTK = all_capitalizations(stopwords.words('english') + ["I'm"])
GOVT_AGENCIES = all_capitalizations(read_csv('data/govt_acronyms.csv')['name'].tolist())
WSB_TERMINOLOGY = all_capitalizations(read_csv('data/wsb_terminology.csv')['term'].dropna().to_list())
COMMON_NAMES = all_capitalizations(read_csv('data/common_names.csv')['name'].to_list())

STOP_WORDS = COMMON_WORDS | STOP_WORDS_NLTK | GOVT_AGENCIES | WSB_TERMINOLOGY | COMMON_NAMES
