from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello!!'

@app.route('/classifier', methods=["POST"])
def classifier():
    data = request.get_json(silent=True)
    
    str_ = data['file_url'] # 나중에 stt url받아서 api로 전송
    nums = data['subject_nums']

    #result = keyword_subjectClassifier(str_, int(nums))

    return jsonify({'result' : str_})
    

if __name__ == '__main__':
    import argparse
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000), debug = True))