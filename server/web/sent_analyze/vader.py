import nltk
import ssl
from nltk.tokenize import wordpunct_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

try:
     _create_unverified_https_context =     ssl._create_unverified_context
except AttributeError:
     pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('vader_lexicon')
nltk.download('stopwords')

SIA = SentimentIntensityAnalyzer()
