from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca=certifi.where()

client = MongoClient("mongodb+srv://oilshock:oilshock@cluster0.z5pqg3h.mongodb.net/?retryWrites=true&w=majority")
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
    #     user_info = db.user.find_one({"id": payload['id']})
    #     return render_template('index.html', nickname=user_info["nickname"])
    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
	return render_template('index.html')

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/join')
def register():
    return render_template('join.html')

#################################
##  리뷰 관련 API               ##
#################################
@app.route('/review')
def review_page() :
    # temp = request.args.get('name', '하하하') #주유소이름
    # print(temp)
    return render_template('review.html')

#리뷰 저장
@app.route('/api/review', methods=['POST'])
def web_review_post() :
    comment_receive = request.form['comment_give']
    email_receive = request.form['email_give']
    star_receive = request.form['star_give']
    date_receive = request.form['date_give']
    nickname_receive = request.form['nickname_give']

    doc = {
        'created_at': date_receive,
        'star': star_receive,
        'comment': comment_receive,
        'nickname': nickname_receive,
        'email': email_receive
    }
    db.review.insert_one(doc)
    return jsonify({'result' : 'success'})

@app.route('/api/delete', methods=['POST'])
def web_review_delete():
    comment_delete = request.form['comment_give']
    db.review.delete_one({'comment':comment_delete})
    return jsonify({'result' : 'success'})

@app.route('/api/review', methods = ['GET']) 
def web_review_list() :
    
    all_data = list(db.review.find({},{'_id':False}))
    return jsonify({'review': all_data})
    # token_receive = request.cookies.get('mytoken')
    # all_data = list(db.review.find({},{'_id':False}))

    # #토큰 없으면 전체 회원 조회
    # if token_receive is None:
    #     return jsonify({'all_review': all_data, 'login_review': []})
    # else:
    #     email = get_email()
    #     login_data = list(db.review.find({'email':email},{'_id':False}))
    #     return jsonify({'all_review': all_data, 'login_review': login_data})

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
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        # 만료시간 3시간으로 설정
        payload = {
            'email': email_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '로그인 또는 비밀번호가 일치하지 않습니다.'})

# 로그인한 회원 받기
@app.route('/api/user', methods=['POST'])
def get_user():
    token_receive = request.form['token_give']
    try: 
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.user.find_one({'email': payload['email']}, {'_id': 0})
        return jsonify({'result': 'success', 'user': userinfo})

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

if __name__ == '__main__' :
		app.run('0.0.0.0', port = 5000, debug = True)