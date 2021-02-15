from flask import Flask, request, jsonify

from keras.preprocessing import sequence
from keras.models import load_model

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import adjusted_rand_score

from collections import defaultdict
import pickle, json, os
import re

from konlpy.tag import Mecab
mecab = Mecab()

app = Flask(__name__)

def rmmult(sort_):
    lili = []
    for i in range(len(sort_)):
        if (sort_[i] in lili) or (sort_[i][1] < 0.01):
            continue
        else:
            lili.append(sort_[i])
    return lili

def keyword_subjectClassifier(str_, nums):
    ############################## setting ########################################
    # model load
    model = load_model('./tools/Naver_dict_l3stm.h5')

    # tokenizer load
    with open("./tools/tokenizer3.pickle", 'rb') as fp:
        tokenizer = pickle.load(fp)

    # token load
    with open("./tools/token3.json", "r") as st_json:
        topic = json.load(st_json)

    max_word =20000
    max_len = 1000 #max_len = 500
    stop_words = [
        '가운데', '대체로', '간의', '크게', '같', '아니', '있', '되', '두', '받', '많', '크', '좋', '따르', '만들', '시키', '그러', '하나',
        '모르', '데', '자신', '어떤', '명', '앞', '번', '보이', '나', '어떻', '월', '들', '이렇', '점', '싶', '좀', '잘', '통하',
        '놓', '란', '이나', '것', '이', '그', '수', '등', '의', '때', '경우', '및', '를', '대한', '사용', '위', '때문', '약', '제', '후',
        '다른', '중', '이상', '일', '은', '위해', '가지', '시', '로', '세', '과', '다음', '두', '더', '또한', '함', '하나', '우리',
        '개', '관', '속', '가장', '모두', '점', '곳', '전', '또', '통해', '여러', '대해', '안', '즉', '모든', '내', '뒤', '보고', '이후',
        '데', '로서', '다시', '관련', '알', '비', '그것', '나', '일반', '각', '뜻', '정도', '사이', '사실', '도', '따라서', '고', '못', '예',
        '간', '동안', '매우', '정', '지금', '증', '임', '공', '해', '음', '앞', '번', '볼', '여기', '거나', '자', '부', '인', '날',
        '바로', '대부분', '기', '바', '주로', '뿐', '직접', '부터', '계속', '일부', '주', '재', '아래', '더욱', '초', '각각', '동시','권',
        '년', '곧', '온', '거의', '먼저', '비롯', '역시', '몇', '반드시', '거', '보', '단', '듯', '가장', '서로', '모든', '에 대한 ',
        ' 수 ', '모두', '의', '에', '대해', '그런데', '으로', '이것', '대로', '것', '그대로', '그리고', '것도', '수가', '이 ', '해야',
        '지금', '할 수가', '할 수', '각종', '요게', '여기', '혹시', '우리', '한번', '이번', '당신', '이렇게', '차고', '어떻게', '뭐', '깜짝', '거지',
        '싶어서', '그래서', '정말', '이런', '도저히', '거죠', '하면은', '이제', '그렇게', '그럼', '많이', '이거', '그거', '저거', '누가',
        '그래', '그냥', '바로', '누가', '다시', '그래도', '간단히', '거야', '이따', '00', '근데', '결국', '이때', '누가', '그런', '딱', '일단',
        '보면', '하나', '어디', '부터', '원', '위하', '나오', '중', '못하', '그렇', '오', '대하', '한', '지', '하']

    ########################## preprocessing ######################################
    str_ = re.sub('[^A-Za-z0-9가-힣.]', ' ', str_)
    str_ = re.sub(' +', ' ', str_)

    ########################## verb find and processing #############################
    morph = mecab.pos(str_)
    new_str = ''
    verb_1 = ['다', '요', '죠', '까', '니']
    for word, tag in morph:
        if 'EF' in tag or 'VX' in tag or 'EC' in tag:
            if word[-1] in verb_1:
                new_str += word +'.'
            else:
                new_str += word + ' '
        else:
            new_str += word + ' '

    # 형태소 분석기로 부족한 동사들 dotword로 충전
    dotword = [
        '립니다', '까요', '니다', '었다', '해요', '혔다', '였다', '든요', '거든요', '아요', 
        '습니다', '합니다', '입니다', '랍니다', '씁시다', '합시다','하죠', '보죠', '이죠', '렇죠', 
        '시죠', '었고요', '였고요', '니고요', '렇고요', '니까요', '는데>요', '니까', '이에요', '잖아요', 
        '고요', '구요','게요']
    for i in dotword:
        new_str = new_str.replace(i + ' ', i + '.')

    ###################### preprocessing 2 ########################################
    documents = new_str.split('.')
    new_docs = []
    for i in documents[:-1]:
        temp = ''
        for j in mecab.nouns(i):
            if j not in stop_words:
                temp += j + ' '
        new_docs.append(temp)

    ####################### K-Means clustering ###############################
    paragraphs = []
    paragraphs2 = []
    paragraphs3 = []
    paragraphs4 = []

    # tfidf -> 단어 vector화
    vectorizer = TfidfVectorizer(max_features = max_word)
    sp_matrix = vectorizer.fit_transform(new_docs)
    
    Kmodel = KMeans(n_clusters=nums, init='k-means++', max_iter=800, n_init=4)
    Kmodel.fit(sp_matrix)

    for i in range(nums):
        paragraphs.append([x for x, y in zip(documents, Kmodel.labels_) if  y == i])
        paragraphs2.append([x for x, y in zip(new_docs, Kmodel.labels_) if y == i])

    for i in range(len(paragraphs2)):
        temp,temp2 = '', ''
        for j in paragraphs[i]:
            temp += j
        for j in paragraphs2[i]:
            temp2 += j
        paragraphs3.append(temp)
        paragraphs4.append(temp2.split()[:-1])
    del paragraphs2, paragraphs

    ##################### keyword extraction ############################
    vectorizer = TfidfVectorizer()
    sp_matrix = vectorizer.fit_transform(documents)
    word2id = defaultdict(lambda : 0)
    for idx, feature in enumerate(vectorizer.get_feature_names()):
        word2id[feature] = idx

    li = []

    for i, sentence in enumerate(documents):
        morph = mecab.nouns(sentence)
        a = [(token, sp_matrix[i, word2id[token]]) for token in morph if token not in stop_words]
        sortt = sorted(a, key=lambda k:k[1])
        sortt = rmmult(sortt)

        li += [(token, sp_matrix[i, word2id[token]]) for token in morph]

        sort_li = sorted(li, key=lambda k: k[1])
    a = sort_li[::-1]
    keywords = [word for word, score in a[:10]]

    ###################### subject predict #############################
    topic_idx = []
    for i in range(nums):
        sequences = tokenizer.texts_to_sequences([paragraphs4[i]])
        sequences_matrix = sequence.pad_sequences(sequences, maxlen=max_len)
        topic_idx.append(model.predict_classes(sequences_matrix))

    ################## return ###############################
    # 1. subject별 내용
    result = {'new_str' : '','subject': [], 'paragraph':[], 'keywords' : []}
    result['new_str'] = str_
    result['keywords'] = keywords
    for i in range(nums):
        result['subject'].append(topic[str(int(topic_idx[i]))])
        result['paragraph'].append(paragraphs3[i])
    return result

    

@app.route("/classifier", methods=["POST"])
def classfier():
    data = request.get_json(silent=True)
    
    str_ = data['file_url'] # 나중에 stt url받아서 api로 전송
    nums = data['subject_nums']

    result = keyword_subjectClassifier(str_, int(nums))

    return jsonify(result)
    

if __name__ == '__main__':
    import argparse
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000), debug = True))