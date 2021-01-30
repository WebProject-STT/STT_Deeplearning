from bs4 import BeautifulSoup
import requests
import re
from Writer import *
from multiprocessing import Process
import json
import os
from time import sleep

MAX_COUNT = 10000

class DictionaryCrawler(object):
    def __init__(self, dict_categories):
        self.categories = dict_categories
        self.select_categories = []
        
    def set_category(self, arg):
        # for category in arg:
        #     if category not in self.categories.keys():
        #         print(category,' is finshed crawling.')
        #         return
        self.select_categories = arg

    # totalpage는 네이버 페이지 구조를 이용해서 page=10000으로 지정해 totalpage를 알아냄
    def find_totalpage(self, url):
        temp_url = url + '&page=10000'
        total_urls = []
        html_doc = requests.get(temp_url, timeout=15, headers={'User-Agent':'Mozilla/5.0'})
        html = BeautifulSoup(html_doc.content, 'html.parser')
        headline_tag = html.find('div', {'class': 'paginate'}).find('strong')
        regex = re.compile(r'<strong>(?P<num>\d+)')
        match = regex.findall(str(headline_tag))
        for page in range(1, int(match[0])+1):
            total_urls.append(url + "&page=" + str(page))
        return total_urls

    def crawling(self, category_name):
        print(category_name + " PID: " + str(os.getpid()))
        
        # csv파일 작성 Setting
        writer = Writer(dict_categories=category_name)

        # 기사 URL 형식 지정
        nums = self.categories.get(category_name)
        url = f'https://terms.naver.com/list.nhn?cid={nums[0]}&categoryId={nums[1]}'
        total_urls = self.find_totalpage(url)
        print(category_name, "url parsing finish!")
        print(category_name, "crawling start!!")

        # 각 페이지에 있는 지식백과사전 내용들 URL 가져오기
        # 최대 저장개수 - 만개로 지정
        count = 0
        for url in total_urls:
            if count > MAX_COUNT : break
            request = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
            document = BeautifulSoup(request.content, 'html.parser')
            ul = document.find('ul', {'class' : 'content_list'})
            strong_list = ul.findAll('strong')
            post_urls = []
            for strong in strong_list:
                try:
                    post_urls.append(strong.a['href'])
                except: continue
            count += len(post_urls)

            # 지식 백과사전 URL
            for content_url in post_urls:
                sleep(0.01) # 크롤링 대기시간
                # 지식 HTML가져오기
                html = requests.get('https://terms.naver.com/'+content_url, headers={'User-Agent':'Mozilla/5.0'})
                try:
                    soup = BeautifulSoup(html.content, 'html.parser')
                except:
                    continue

                # 단어 가져오기
                try:
                    word = soup.find('h2', {'class': 'headword'})
                    new_word = re.sub('[^A-Za-z0-9가-힣]', '', word.string)
                    if not word.string: continue # 공백이면 제외
                except: continue
                
                # 본문 가져오기
                try:
                    content = soup.find('div', {'id': 'size_ct'})
                    texts = ''
                    summary = content.find('dl', {'class': 'summary_area'})
                    if summary:
                        texts = summary.text[3:]
                    else:
                        p_texts = content.findAll('p')
                        for i in range(len(p_texts)):
                            if i == 3: break # 최대 text 3개까지만 저장
                            texts += p_texts[i].text + ' '
                    
                    new_text = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', texts)
                    new_text = re.sub('\n\n', ' ', new_text)
                    new_text = re.sub('[^A-Za-z0-9가-힣.]', ' ', new_text)
                    new_text = re.sub(' +', ' ', new_text)
                except: continue
                
                if not new_text: continue # 공백이면 제외

                # CSV파일에 작성
                writer.write_row([content_url, new_word, new_text])

                del content_url
                del new_word, new_text
                del html, soup
        writer.close()
        print(category_name, "finish!!")
        return

    def start(self):
        for category_name in self.select_categories:
            proc = Process(target=self.crawling, args=(category_name, ))
            proc.start()

if __name__ == "__main__":

    # json file load
    file_name = ''
    with open(file_name, 'rt', encoding='UTF8') as json_file:
        dict_categories = json.load(json_file) # json -> dict으로 변환됨

    Crawler = DictionaryCrawler(dict_categories) # dictionary setting

    # 4개씩 multi-processing crawling할 예정
    four_categories = []
    temp = []
    for key in dict_categories.keys():
        if len(temp) == 4:
            four_categories.append(temp)
            temp = []
        temp.append(key)
    print(len(four_categories))
    #for category in four_categories:
    print(four_categories[0], " start !_!")
    # URL Setting
    Crawler.set_category(four_categories[0])
    print(Crawler.select_categories)

    # Multi-processing start
    Crawler.start()

    

    

    
