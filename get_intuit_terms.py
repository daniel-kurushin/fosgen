import re

from rutermextract import TermExtractor
from bs4 import BeautifulSoup
from utilites import dump, load
from get_intuit_sentences import get_normal_form

COURSE = "Администрирование информационных систем"
COURSE = "Информационные технологии и вычислительные системы"

te = TermExtractor()

try:
    word_normal_form  = load('word_normal_form.json')
except FileNotFoundError:
    word_normal_form = {}
    
text = BeautifulSoup(open('in/%s.html' % COURSE).read(),'lxml').text

terms = te(text)
terms = [ (str(t), t.count) for t in te(text) if str(t).count(" ") > 1 and len(re.sub(r'[a-z0-9]', '', str(t)).strip())/len(str(t)) > 3/4 ]
out = []
for term in terms:
    if [ word for word in term[0].split() if len(word) < 3 ]:
        pass
    else:
       out += [term[0]]
        
dump(out, 'intuit_terms.json')