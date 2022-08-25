import re

from utilites import load, dump, compare, compare_phrase
from rutermextract import TermExtractor
from itertools import product
from find_wrong_answer import find_wrong_answer 

structure = load('course_structure.json')
sentences = load('intuit_sents.json')

te = TermExtractor()

questions = {}

candidates = []
for sent_id in sentences.keys():    
    text_a = sentences[sent_id]["tokens"]
    for element in structure.keys():
        text_b = structure[element]
        v = compare_phrase(text_a, text_b)
        candidates += [(v, element, sent_id)]
        
used = set()
questions = {}
        
for weight, competence, sent_id in candidates:
    if weight > 0.3:
        sentence = sentences[sent_id]["sentence"]
        sent_terms = sorted([ (x,len(x)) for x in te(sentence, strings=1) ], key=lambda x:x[1], reverse=1)
        try:
            q_term = sent_terms[0]
            q_term_words = q_term[0].split()
            sent_words = sentence.split()
            stored = sentence
            answer = []
            for a, b in product(sent_words, q_term_words):
                if compare(a, b) >= 0.5:
                    sentence = sentence.replace(a, "_", 1)
                    answer += [a]
            if stored != sentence and not re.findall("_.{6,}_", sentence):
                used |= set([sent_id])
                answer = " ".join(answer)
                wrong_answers = find_wrong_answer(answer)
                questions.update({sent_id:[sentence, competence, answer, wrong_answers]})
        except IndexError:
            pass
                
dump(questions, 'questions.json')