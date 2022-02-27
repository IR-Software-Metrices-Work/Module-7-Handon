import string
import re
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
def preprocess(text):
    cleaned_text = text.translate(str.maketrans('', '', '!"#$%&\'()*+,.<=>?@[]^`{|}~' + u'\xa0'))
    cleaned_text = cleaned_text.lower()
    cleaned_text = cleaned_text.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))

    cleaned_text = ' '.join(['#weburl' if t.startswith('http') and '/' in t else t for t in cleaned_text.split()])
    cleaned_text = ' '.join(['#number' if re.sub('[\\/;:_-]','',t).isdigit() else t for t in cleaned_text.split()])
    cleaned_text = ' '.join(['#version' if any(i.isdigit() for i in t) and t.startswith('v') else t for t in cleaned_text.split()])
    cleaned_text = ' '.join(['#localpath' if ('\\' in t or '/' in t) and ':' not in t else t for t in cleaned_text.split()])
    cleaned_text = ' '.join(['#image_size' if t.endswith('px') else t for t in cleaned_text.split()])
    cleaned_text = ' '.join(['#variable_with_underscore' if '_' in t else t for t in cleaned_text.split()])
    cleaned_text = ' '.join(['#variable_with_dash' if '-' in t else t for t in cleaned_text.split()])
    cleaned_text = ' '.join(['#long_variable_name' if len(t) > 20 else t for t in cleaned_text.split()])

    tokenized_text = word_tokenize(cleaned_text)
    stop_dict = {s: 1 for s in stopwords.words()}
    sw_removed_text = [word for word in tokenized_text if word not in stop_dict]
    sw_removed_text =[word for word in sw_removed_text if len(word) > 2]

    ps = PorterStemmer()
    stemmed_text = ' '.join([ps.stem(w) for w in sw_removed_text])

    return stemmed_text