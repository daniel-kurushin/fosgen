from utilites import load, compare_phrase

terms = [ t.lower() for t in load('intuit_terms.json') ]

def find_wrong_answer(answer = "операционной системы"):
    return [ x[1] for x in sorted(( (compare_phrase(answer, x), x) for x in terms ), reverse=1)[3:6] ]
    

if __name__ == "__main__":
    print(find_wrong_answer())