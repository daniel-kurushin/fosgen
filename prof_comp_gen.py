from utilites import load, dump, compare, compare_phrase
from competencies import competencies

terms = load('intuit_terms.json')

candidates = []
for comp_key in competencies.keys():
    similarity = 0;
    similar_terms = []
    for comp in comp_key:
        for term in terms:
            v = compare_phrase(comp, term)
            if v > 0.5:
                similarity += v
                similar_terms += [term]
    if similarity > 0.65:
        candidates += [(comp_key, competencies[comp_key]['code'], similarity, similar_terms)]

candidates = sorted(candidates, key=lambda x:x[2], reverse=1)[:len(candidates)//4]

prof_competencies = {}

for candidate in candidates:
    key = candidate[0]
    code = competencies[key]["code"]
    text = competencies[key]["text"]
    terms = candidate[3]
    prof_competencies.update({code:[text, key, terms]})
    
dump(prof_competencies,'prof_competencies.json')