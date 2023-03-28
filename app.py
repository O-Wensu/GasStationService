from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca=certifi.where()

client = MongoClient('mongodb+srv://oilshock:oilshock@cluster0.z5pqg3h.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# JWT 토큰 생성을 위한 비밀문자열
SECRET_KEY = 'SPARTA'

import jwt 

# 토큰 만료시간을 위한 datetime 모듈 사용
import datetime

# 비밀번호 암호화를 위한 모듈
import hashlib

@app.route('/')
def home() :
    #     token_receive = request.cookies.get('mytoken')
    # try:
    #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    #     user_info = db.users.find_one({"id": payload['id']})
    #     return render_template('index.html', nickname=user_info["nickname"])
    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
	return render_template('review.html')

#################################
##  리뷰 관련 API               ##
#################################

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

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/join')
def register():
    return render_template('join.html')

#################################
##  로그인 및 회원가입 API      ##
#################################

# [회원가입 API]
# email, pw, nickname을 받아서, mongoDB에 저장
# 저장하기 전에, pw를 sha256 방법으로 암호화해서 저장
@app.route('/api/join', methods=['POST'])
def api_register():
    print("진입")
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    
    info = {
        'email': email_receive,
        'password': pw_hash,
        'nickname': nickname_receive
    }

    db.users.insert_one(info)
    return jsonify({'result': 'success'})

if __name__ == '__main__' :
		app.run('0.0.0.0', port = 5000, debug = True)