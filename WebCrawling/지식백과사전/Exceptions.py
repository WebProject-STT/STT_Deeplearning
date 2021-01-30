import os

# 카테고리가 올바르지 않을 때
class InvalidCategory(Exception):
    def __init__(self, category):
        self.message = f'{category} is finshed crawling.'

    def __str__(self):
        return self.message