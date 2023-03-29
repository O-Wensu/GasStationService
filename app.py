from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)

from bson.objectid import ObjectId
from pymongo import MongoClient
import certifi

ca=certifi.where()

client = MongoClient("mongodb+srv://sparta:test@cluster0.kqhn3uz.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
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
	return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/join')
def register():
    return render_template('join.html')

#################################
##  검색 관련 API               ##
#################################

@app.route('/list', methods=['GET'])
def serach_location():
   print("진입")
   keyword_receive = request.args.get('location')
   print(keyword_receive)
   return render_template('list.html', keyword=keyword_receive)

#################################
##  리뷰 관련 API               ##
#################################

@app.route('/review', methods=['GET'])
def station_review() :
    print("진입")
    dic = { 
        'code': request.args.get('code'),
        'name': request.args.get('name'),
        'addr': request.args.get('addr'),        
        'gasoline': request.args.get('gasoline'),
        'diesel': request.args.get('diesel'),
        'lat': request.args.get('lat'),
        'lon': request.args.get('lon')
    }
    print(dic)
    return render_template('review.html', data = dic)

#리뷰 저장
@app.route('/api/review', methods=['POST'])
def web_review_post() :
    comment_receive = request.form['comment_give']
    email_receive = request.form['email_give']
    star_receive = request.form['star_give']
    date_receive = request.form['date_give']
    nickname_receive = request.form['nickname_give']
    code_receive = request.form['code_give']

    doc = {
        'created_at': date_receive,
        'star': star_receive,
        'comment': comment_receive,
        'nickname': nickname_receive,
        'email': email_receive,
        'code' : code_receive
    }
    db.review.insert_one(doc)
    return jsonify({'result' : 'success'})

#리뷰 삭제
@app.route('/api/delete', methods=['POST'])
def web_review_delete():
    id_receive = request.form['id_give']
    obj_id = ObjectId(id_receive)
    db.review.delete_one({'_id':obj_id})
    return jsonify({'result': 'success', 'msg': '삭제 완료'})

#리뷰 수정
@app.route('/api/update', methods=['POST'])
def web_review_update():
    id_receive = request.form['id_give']
    obj_id = ObjectId(id_receive)
    print(obj_id)
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    db.review.update_one({'_id':obj_id}, {"$set":{"comment": comment_receive, "star":star_receive}},upsert=True)
    return jsonify({'result': 'success', 'msg': '수정 완료'})


#리뷰 조회
@app.route('/api/review', methods = ['GET']) 
def web_review_list() : 
    all_data = list(db.review.find({},{'_id': False}))
    all_id = get_reviewId()
    return jsonify({'review': all_data, 'review_id': all_id})

# 모든 리뷰의 오브젝트ID -> string 변환하여 가져오기
def get_reviewId():
    id_reviews = list(db.review.find({},{'_id': True}))
    for data in id_reviews:
        data["_id"] = str(data["_id"])
    return id_reviews
    
#################################
##  로그인 및 회원가입 API      ##
#################################

# [회원가입 API]
# email, pw, nickname을 받아서, mongoDB에 저장
# 저장하기 전에, pw를 sha256 방법으로 암호화해서 저장
@app.route('/api/join', methods=['POST'])
def api_register():
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    
    info = {
        'email': email_receive,
        'password': pw_hash,
        'nickname': nickname_receive
    }

    db.user.insert_one(info)
    return jsonify({'result': 'success'})

# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급
@app.route('/api/login', methods=['POST'])
def api_login():
    email_receive = request.form['email_give']
    pw_receive = request.form['pw_give']

    # pw 암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저 찾기
    result = db.user.find_one({'email': email_receive, 'password': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급
    if result is not None:
        # 만료시간 3시간으로 설정
        payload = {
            'email': email_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token 발급
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '로그인 또는 비밀번호가 일치하지 않습니다.'})

# 로그인한 회원 정보 받기
@app.route('/api/user', methods=['GET'])
def get_user():
    token_receive = request.cookies.get('mytoken')
    try: 
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.user.find_one({'email': payload['email']}, {'_id': 0})
        return jsonify({'result': 'success', 'user': userinfo})

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

if __name__ == '__main__' :
		app.run('0.0.0.0', port = 5001, debug = True)