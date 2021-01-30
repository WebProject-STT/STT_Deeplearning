import requests
from bs4 import BeautifulSoup

# 원하는 웹(URL)에서 HTML 가져오기
URL = 'https://terms.naver.com/list.nhn?cid=41708&categoryId=41708'
html_doc = requests.get(URL)

# 해당 URL의 HTML 소스코드 Parsing
html = BeautifulSoup(html_doc.text, 'html.parser')

# select 함수 사용하여 특정 부분 선택하기 -> content_list부분 가져오기
container = html.select('.content_list')

# content_list부분 중 title들과 내용 가져오기
titles = container[0].select('.title a')
new_titles = []
for i in range(len(titles)):
    if not i%2:
        new_titles.append(titles[i].string)
contents = container[0].select('p')
for i in range(len(contents)):
    contents[i] = contents[i].text
print(len(new_titles))
print(len(contents))

for title, content in zip(new_titles, contents):
    print(title, " : ", content)