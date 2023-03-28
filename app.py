from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.zbsepl2.mongodb.net/test')
db = client.dbsparta

@app.route('/')
def home() :
	return render_template('review.html')

@app.route('/test', methods=['POST'])
def web_review_post() :
    comment_receive = request.form['comment_give']
    #id는 어떻게 받아올 수 있을까?
    #id_receive = request.form['id']
    star_receive = request.form['star_give']
    #id를 받아올 방법을 알 경우 주석 해제
    #doc = {'comment': comment_receive , 'id' : id_receive, 'star': star_receive}
    doc = {'comment': comment_receive, 'star': star_receive}
    db.review.insert_one(doc)
    return jsonify({'result' : 'success'})

@app.route('/test', methods = ['GET']) 
def web_review_get() :
		comment_data = list(db.review.find({},{'_id':False}))
		return jsonify({'result' : comment_data})

if __name__ == '__main__' :
		app.run('0.0.0.0', port = 5000, debug = True)