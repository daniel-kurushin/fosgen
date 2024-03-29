from requests import get
from bs4 import BeautifulSoup
from _constants import URL, COURSE, HOST

def get_lectures_urls(url):
    index_soup = BeautifulSoup(get(url).content, "lxml")
    for h6 in index_soup('h6'):
        if 'лекция' in h6.text.lower():
            href = "%s%s" % (HOST, h6.a['href'])
            theme = [ a.text for a in index_soup('a',{'href':h6.a['href']}) if "лекция" not in a.text.lower() ][0]
            assert href != HOST
            yield theme, href

lecture_html = ""            
for lecture, lecture_url in get_lectures_urls(URL):
    print(lecture, lecture_url)
    for page in range(1, 10):
        try:
            a_url = "%s?page=%s" % (lecture_url, page)
            print(a_url)
            lecture_soup = BeautifulSoup(get(a_url).content, "lxml")
            a_html = lecture_soup.find('div', {'id':"center-panel"})
            assert 'неправильно указали адрес страницы' not in a_html.text
            course_html = a_html.find('div', {'class':"eoi spelling-content-entity"})
            lecture_html += f'<h1>{lecture}</h1>'
            lecture_html += course_html.prettify()
        except AssertionError as e:
            break

open('in/%s.html' % COURSE,'w').write(lecture_html)
