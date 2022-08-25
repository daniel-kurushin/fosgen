import re

from rutermextract import TermExtractor
from bs4 import BeautifulSoup
from utilites import dump, load
from _constants import COURSE

def _filter_term(term):
    wrong_grammemes = {'ADJF', 'LATN', 'UNKN', 'NUMB', 'NUMR' }
    
    word = term.words[0].parsed
    
    return len(term.words) > 1 and \
           len(word.tag.grammemes & wrong_grammemes) == 0 

def _normalize_terms_weights(kw):
    import numpy as np
    res = []

    max_weight, min_weight = kw[0][1], kw[-1][1]
    a, b = np.polyfit([max_weight, min_weight], [1, 0.1], 1)
    for term, weight in kw:
        normalized_weight = max(0, a * weight + b)
        res += [[str(term), normalized_weight]]
        
    return res
    
def get_text_keywords(a_text):
    from rutermextract import TermExtractor
    te = TermExtractor()
    kw = [ (term, term.count) for term in te(a_text) if _filter_term(term) ]
    
    return _normalize_terms_weights(kw)

text = BeautifulSoup(open('in/%s.html' % COURSE).read(),'lxml').text

terms = get_text_keywords(text)
out = []
for term in terms:
    if term[1] > .2:
        out += [term[0]]
        
dump(out, 'intuit_terms.json')