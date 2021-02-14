from utilites import load, dump, compare, compare_phrase
from rutermextract import TermExtractor

sentences = load('intuit_sents.json')
terms = load('intuit_terms.json')
competencies = load('prof_competencies.json')

te = TermExtractor()

used = []
structure = {}

for c in competencies.keys():
    text = ""
    for cc in competencies[c][1]:
        text += "%s. " % cc
    for cc in competencies[c][2]:
        text += "%s. " % cc
    contents = []
    for term in te(text, strings=1):
        if term not in used:
            contents += [term]
        used += [term]
    structure.update({c:contents})
    
dump(structure, 'course_structure.json')