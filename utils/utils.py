from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import re


def tokenize(text):

    text = re.sub(r'[^a-zA-Z0-9]',' ',text)
    words = word_tokenize(text)
    #print(words)
    lemmed = [ WordNetLemmatizer().lemmatize(word.lower(),pos="v") for word in words if word not in stopwords.words("english")]

    return lemmed
