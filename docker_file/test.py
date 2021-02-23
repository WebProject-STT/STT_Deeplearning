from flask import Flask, request, jsonify

from keras.preprocessing import sequence
from keras.models import load_model

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import adjusted_rand_score

from collections import defaultdict
import pickle, json, os
import re

s = ['클릭', '마지막', '검색어', '눈', '오리', '피해', '호소', '최근', '폭설', '올겨울', '눈', '눈', '오리', '모양', '집계', '모양', '완성', '눈물', '피해', '사형', '삼', '인터넷', '사이트', '글', '사람', '아이', '차', '눈', '눈물', '게', '차', '눈', '오리', '세차', '보닛', '유리', '스크래치', '걸', '확인', '블랙박스', '아이', '놀이', '집계', '차', '뿌리', '녹화', '사람', '아이', '부모', '지도', '말', '보통', '바닥', '눈', '부모', '지도', '부족']

# model load
model = load_model('./docker_file/tools/Naver_dict_l3stm.h5')

# tokenizer load
with open("./docker_file/tools/tokenizer2.pickle", 'rb') as fp:
    tokenizer = pickle.load(fp)
    
topic_idx = []
sequences = tokenizer.texts_to_sequences([s])
sequences_matrix = sequence.pad_sequences(sequences, maxlen=1000)
topic_idx.append(model.predict_classes(sequences_matrix))

print(topic_idx)
