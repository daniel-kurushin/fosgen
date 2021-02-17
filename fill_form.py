from utilites import load
from rutermextract import TermExtractor
import numpy as np
import re
from _constants import COURSE, N_TASKS, N_VARS

ITEMS = "абвг"

te = TermExtractor()

questions = load('questions.json')
structure = load('course_structure.json')
competencies = load('prof_competencies.json')
sentences = load('intuit_sents.json')

structure_table_dict = {}
questions_by_competence = {}
key_table_dict = {}
used_comps = {}

for competence in competencies.keys():
    collected_questions = {}
    for question in questions.keys():
        if questions[question][1] == competence:
            collected_questions.update({question:questions[question]})
    if len(collected_questions):
        questions_by_competence.update({competence:collected_questions})

def discipline():
    return [COURSE]
    
def opk():
    return [ x for x in questions_by_competence.keys() if x.startswith('ПК') ]
    
def pk():
    return [ x for x in questions_by_competence.keys() if x.startswith('ОПК') ]
    
def opk_table():
    return [ "|%s|%s|" % (x, competencies[x][0]) for x in questions_by_competence.keys() if x.startswith('ОПК') ]
    
def pk_table():
    return [ "|%s|%s|" % (x, competencies[x][0]) for x in questions_by_competence.keys() if x.startswith('ПК') ]
    
def n_task():
    return [str(sum(structure_table_dict.values()))]
    
def get_questions(n):
    rez = []
    m = 1
    for competence in questions_by_competence.keys():
        k = 0
        for question in list(questions_by_competence[competence].keys())[n-1::4]:
            k += 1
            answers = [
                (questions[question][2], 1),
                (questions[question][3][0], 0),
                (questions[question][3][1], 0),
                (questions[question][3][2], 0),
            ]
            j, a = 0, "ъ"
            q = "%s. %s \n\n" % (m, questions[question][0])
            m += 1
            np.random.shuffle(answers)
            for item in ITEMS:
                q += "\t%s) %s \n\n" % (item, answers[j][0])
                if answers[j][1]:
                    a = item
                j += 1
            q += "\n"
            key_table_dict.update({(n,k):a})
            rez += [q]
        if n == 1: 
            structure_table_dict.update({competence:k})
        
    return rez

def variants():
    q_keys = list(questions.keys())
    needed_comps = {}
    for competence in set([ questions[q][1] for q in questions ]):
        nq = max(1, len([ q for q in questions if questions[q][1] == competence]) // N_VARS)
        needed_comps.update({competence:nq})
    np.random.shuffle(q_keys)
    rez = []
    i = 0
    for v in range(N_VARS):
        rez += ["# Тест по дисциплине «%s», вариант %s." % (COURSE, v)]
        rez += ["Выберите вариант, наиболее подходящий для заполнения пропуска."]
        for t in range(N_TASKS):
            text, competence, answer, wrong = questions[q_keys[i]]
            i += 1
            rez += ["%s. %s \n\n" % (t+1, re.sub(r"(_ )+", "___", text)) ]
            answers = [
                (answer, 1),
                (wrong[0], 0),
                (wrong[1], 0),
                (wrong[2], 0),
            ]
            np.random.shuffle(answers)
            j, a = 0, "ъ"
            for item in ITEMS:
                rez += ["\t%s) %s \n\n" % (item, answers[j][0])]
                if answers[j][1]:
                    a = item
                j += 1
            key_table_dict.update({(v,t):a})
            try:
                used_comps[competence] += 1
            except KeyError:
                used_comps.update({competence:0})
    return rez

def ball_structure():
    a, b, c, d = list(range(N_TASKS))[::round(N_TASKS/4)]
    rez =  ["0 ÷ %s баллов — «неудовлетворительно»" % b]
    rez += ["%s ÷ %s баллов — «удовлетворительно»" % (b+1, c)]
    rez += ["%s ÷ %s баллов — «хорошо»" % (c+1, d)]
    rez += ["%s ÷ %s баллов — «отлично»" % (d+1, N_TASKS)]
    
    return rez
	
def structure_table():
    rez = []
    for competence in pk() + opk():
        text = []
        n = 0
        for question in questions.keys():
            q_comp = questions[question][1]
            if q_comp == competence:
                q_sentence = sentences[question]['sentence']
                text += [q_sentence]
                n += 1
        head = ". ".join(te(" ".join(text), strings=1, limit=6)[3:])
        if n > 0:
            try:
                rez += ["|%s|%s|%s|" % (head, competencies[competence][0], used_comps[competence])]
            except KeyError:
                pass
    return rez
    
def key_table():
    rez = ["|%s|" % "|".join(["Вариант %s" % (s+1) for s in range(N_VARS)])]
    rez += ["|%s|" % "|".join([":-:" for s in range(N_VARS)])]
    for t in range(N_TASKS):    
        l = "|"
        for v in range(N_VARS):
            l += " %s) %s |" % (t+1, key_table_dict[(v,t)])
        rez += [l]
    return rez

keys = {
    "{discipline}": discipline,
    "{opk}": opk,
    "{pk}": pk,
    "{opk_table}": opk_table,
    "{pk_table}": pk_table,
    "{variants}": variants,
    "{ball_structure}": ball_structure,
    "{structure_table}": structure_table,
    "{n_task}": n_task,
    "{key_table}": key_table,
}

template = open('template/template.md').read()
for k in keys.keys():
    print(k)
    template = template.replace(k,"\n".join(keys[k]()))
open('out/%s.md' % COURSE,'w').write(template)
    