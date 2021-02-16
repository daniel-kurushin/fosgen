import re
import numpy as np

from bs4 import BeautifulSoup
from utilites import dump, load
from nltk.tokenize import PunktSentenceTokenizer 
from nltk.tokenize import WordPunctTokenizer
from pymorphy2 import MorphAnalyzer

COURSE = "Администрирование информационных систем"
COURSE = "Информационные технологии и вычислительные системы"

pst = PunktSentenceTokenizer()
wpt = WordPunctTokenizer()
ma = MorphAnalyzer()

def find_stop_words(text):
    rez = []
    for word in wpt.tokenize(text):
        tags = ma.parse(word)[0].tag
        if 'UNKN' in tags or \
           'LATN' in tags or \
           'PNCT' in tags or \
           'NUMB' in tags or \
           'ROMN' in tags:
            rez += [word]
    return rez

try:
    word_normal_form  = load('word_normal_form.json')
except FileNotFoundError:
    word_normal_form = {}

text = BeautifulSoup(open('in/%s.html' % COURSE).read(),'lxml').text

try:
    stop_words = set(load('stop_words.json'))
except FileNotFoundError:
    stop_words = find_stop_words(text)
    
def get_normal_form(word):
    try:
        nf = word_normal_form[word]
    except KeyError:
        nf = sorted(ma.parse(word), key=lambda x:x.score)[-1].normal_form
        word_normal_form.update({word:nf})
    return nf

def is_word(word):
    return not word in stop_words

sentences = {}
n = 0
for sentence in [ re.sub(r"\n+|\s+", " ", x) for x in pst.tokenize(text) ]:
    sent_tokens = list(set([ get_normal_form(t) for t in wpt.tokenize(sentence) ]))
    tokens = [ t for t in sent_tokens if is_word(t) ]
    Q = len(tokens) / len(sent_tokens)
    x = {
            n:{
                "tokens": tokens,
                "sentence": sentence,
                "Q": Q,
                "len": len(tokens),
            }
    }
    sentences.update(x)
    n += 1
Q = np.array([ sentences[s]['Q'] for s in sentences ])
L = np.array([ sentences[s]['len'] for s in sentences ])

q_min, q_max = Q.mean() - Q.std(), Q.mean() + Q.std()
l_min, l_max = L.mean() - L.std(), L.mean() + L.std()

sentences = { i: sentences[i] for i in sentences if q_min <= sentences[i]['Q'] <= q_max and l_min <= sentences[i]['len'] <= l_max }

dump(sentences, 'intuit_sents.json')
dump(word_normal_form, 'word_normal_form.json')
dump(list(stop_words), 'stop_words.json')