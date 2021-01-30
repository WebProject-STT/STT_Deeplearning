from bs4 import BeautifulSoup
import requests
import re
from Writer import *
from multiprocessing import Process
import json
import os
from time import sleep

MAX_COUNT = 100

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
        # writer = Writer(dict_categories=category_name)

        # 기사 URL 형식 지정
        nums = self.categories.get(category_name)
        url = f'https://terms.naver.com/list.nhn?cid={nums[0]}&categoryId={nums[1]}'
        if category_name != '공룡':
            total_urls = self.find_totalpage(url)
        else:
            total_urls = [url]
        print(category_name, "url parsing finish!")
        print(category_name, "crawling start!!")

        # 각 페이지에 있는 지식백과사전 내용들 URL 가져오기
        # 최대 저장개수 - 만개로 지정
        count = 0
        for url in total_urls:
            if count > MAX_COUNT : break
            request = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
            soup = BeautifulSoup(request.content, 'html.parser')
            ul = soup.find('ul', {'class' : 'content_list'})
            if category_name != '공룡':
                temp_list = ul.findAll('strong')
            else:
                print(ul)
            post_urls = []
            for tag in temp_list:
                try:
                    post_urls.append(tag.a['href'])
                except: continue
            count += len(post_urls)
            del temp_list

            # 지식 백과사전 URL
            for content_url in post_urls:
                sleep(0.01) # 크롤링 대기시간

                # 기사 HTML가져오기
                html = requests.get(content_url, headers={'User-Agent':'Mozilla/5.0'})
                try:
                    soup = BeautifulSoup(html.content, 'html.parser')
                except:
                    continue
                


                
    def start(self):
        for category_name in self.select_categories:
            proc = Process(target=self.crawling, args=(category_name, ))
            proc.start()

if __name__ == "__main__":

    # json file load
    file_name = 'C:/Users/msi/OneDrive/문서/GitHub/STT_Deeplearning/WebCrawling/지식백과사전/category.json'
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
    
    # for category in four_categories:
    #     # URL Setting
    #     Crawler.set_category(category)
    #     print(Crawler.select_categories)
    #     print()

    #     # Multi-processing start
    #     Crawler.start()
    #     break

    Crawler.set_category('공룡') # four_categories[0][0]
    Crawler.crawling('공룡')
    

    

    