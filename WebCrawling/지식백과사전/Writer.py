import csv
import os
import platform

class Writer(object):
    def __init__(self, dict_categories):
        # dict_categories -> 주제여야함

        self.file = None
        self.initialize_file(dict_categories)
        self.csv_writer = csv.writer(self.file)
    
    def initialize_file(self, dict_categories):
        output_path = 'G:/내 드라이브/web_crawling'
        file_name = f'{output_path}/{dict_categories}.csv'
        if os.path.isfile(file_name):
            print(file_name, 'is located in', output_path)
            return
        user_os = str(platform.system())
        if user_os == "Windows":
            self.file = open(file_name, 'w', encoding='euc-kr', newline='')
    
    def write_row(self, row):
        self.csv_writer.write_row(row)
    
    def close(self):
        self.file.close()
        