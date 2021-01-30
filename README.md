# STT_Deeplearning

## **구현 목록**
### **AI (박주영)**
----
#### **데이터 셋 구축**
1. web crawling을 통해 네이버 지식백과사전 데이터 셋 구축
2. 각 카테고리 별로 데이터 셋 구축하기
3. 시간 단축을 위해 병렬 코드 작성

#### **게시글 요약 기능**

1. DB에 업로드 하는 event catch하여 유저가 올린 녹음파일을 가져온다.
    - 게시글 작성 event인지 수정 event인지 체크하는 기능 필요
    - 확인 사항: event catch할 때 이미 게시글 작성에서 DB에 넘길 값들은 저장 되었는가 →저장 되었으면 2,3,4번 결과를 DB Update / 안되있으면 이 값들 + 3번, 4번, 5번 결과 DB Insert
2. API를 통해 STT(speech to text)하여 텍스트 얻는다.
3. 얻은 텍스트에서 TF-IDF기반으로 키워드 추출(예정임 → 다른 알고리즘도 고려중)
4. 얻은 텍스트를 주제분류 딥러닝 모델(LSTM)에 input으로 넣어 주제기반으로 분류된 output을 얻는다.
5. 2,3,4번에서 얻은 원본 텍스트, 키워드와 주제 분류된 텍스트 DB에 저장한다.