import datetime as dt
import nltk
from nltk.corpus import stopwords
import re
from snowballstemmer import TurkishStemmer
import string

nltk.download('stopwords')
turkStem=TurkishStemmer()

def time_it(time):
    """
    Returns time data type of given string in form Y-m-d.
    Example: 2001-01-01."""
    return dt.datetime.strptime(str(time), '%Y-%m-%d')

def remove_them(x):
    """Word cleaner.
    Removes words has lenght less then 3 in given string."""
    return re.sub(r'\b\w{1,2}\b', '', x)

def remove_digit(text):
    """Digit cleaner.
    Removes digits in given string."""
    digit_pattern = str.maketrans('', '', string.digits)
    return text.translate(digit_pattern)

def lower_it(text):
    """Lowers characters in given string.
    Lowers all in string."""
    return text.lower()

def remove_punctiations(text):
    """Punction cleaner.
    Removes punctions in given string."""
    pattern = str.maketrans('', '', string.punctuation)
    return text.translate(pattern)

def remove_stopwords(text, language='turkish'):
    """Stopword cleaner.
    Removes stopwords in given string, language is set to Turkish by default."""
    st = stopwords.words(language)
    pattern = re.compile(r'\b(' + r'|'.join(st) + r')\b\s*')
    text = pattern.sub('',text)
    return text

def stem_it(x):
    """Turkish stemmer.
    Returns stemmed words in given string, uses Snowball Turkish stemmer."""
    return [turkStem.stemWord(w) for w in x.split()]

def sentence_it(x):
    """Sentence maker.
    Returns one string form of given words array."""
    sentence = ''
    for w in x: sentence += w + " "
    return sentence.strip()

def preproces(text, stemmer=False):
    """String cleaner.
    Removes digits, lowers charactes, removes punctiations and stop words in given string."""
    text = remove_digit(text)
    text = lower_it(text)
    text = remove_punctiations(text)
    text = remove_stopwords(text)
    text = remove_them(text)
    if stemmer:
        text = stem_it(text)
        text = sentence_it(text)
    return text

