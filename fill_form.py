from utilites import load
from rutermextract import TermExtractor

te = TermExtractor()

questions = load('questions.json')
structure = load('course_structure.json')
competencies = load('prof_competencies.json')
sentences = load('intuit_sents.json')

structure_table_dict = {}
questions_by_competence = {}

for competence in competencies.keys():
    collected_questions = {}
    for question in questions.keys():
        if questions[question][1] == competence:
            collected_questions.update({question:questions[question]})
    if len(collected_questions):
        questions_by_competence.update({competence:collected_questions})

def discipline():
    return "Администрирование информационных систем"
    
def opk():
    return [ x for x in questions_by_competence.keys() if x.startswith('ПК') ]
    
def pk():
    return [ x for x in questions_by_competence.keys() if x.startswith('ОПК') ]
    
def opk_table():
    return [ "|%s|%s|" % (x, competencies[x][0]) for x in questions_by_competence.keys() if x.startswith('ОПК') ]
    
def pk_table():
    return [ "|%s|%s|" % (x, competencies[x][0]) for x in questions_by_competence.keys() if x.startswith('ПК') ]
    
def n_task():
    return sum(structure_table_dict.values())
    
def var_1():
	return "1"

def get_questions(n):
    rez = []
    for competence in questions_by_competence.keys():
        k = 0
        for question in list(questions_by_competence[competence].keys())[n-1::4]:
            k += 1
            rez += [questions[question]]
        if n == 1: 
            structure_table_dict.update({competence:k})
    return rez

def questions_1():
	return get_questions(1)
	
def var_2():
	return "2"
	
def questions_2():
	return get_questions(2)
	
def var_3():
	return "3"
	
def questions_3():
	return get_questions(3)
	
def var_4():
	return "4"
	
def questions_4():
	return get_questions(4)
	
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
            rez += ["|%s|%s|%s|" % (head, competencies[competence][0], structure_table_dict[competence])]
    return rez
    
def i_var():
    return ""
    
def key_table():
    return ""

keys = {
    "{discipline}": discipline,
    "{opk}": opk,
    "{pk}": pk,
    "{opk_table}": opk_table,
    "{pk_table}": pk_table,
    "{var_1}":var_1,
    "{questions_1}":questions_1,
    "{var_2}":var_2,
    "{questions_2}":questions_2,
    "{var_3}":var_3,
    "{questions_3}":questions_3,
    "{var_4}":var_4,
    "{questions_4}":questions_4,
    "{structure_table}": structure_table,
    "{n_task}": n_task,
    "{key_table}": key_table,
}

for x in keys:
    print(keys[x]())