from utilites import load, dump, compare, compare_phrase

structure = load('course_structure.json')
sentences = load('intuit_sents.json')

questions = {}
for sent_id in sentences.keys():
    for element in structure.keys():
        text_a = " ".join(sentences[sent_id].tokens())
        text_b = " ".join