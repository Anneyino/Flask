from flask import *
import time
import json
import database
import helper
import user_auth
import os
import csv

app = Flask(__name__)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    return render_template('sign.html')


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    email = request.form['emailaddr']

    # try to signup
    success = database.signup(username, password, email)
    if not success:
        return render_template("sign.html", error='username exists')

    # create session_id
    session_id = helper.generate_session_id()
    user = database.get_user_by_name(username)
    uid = user[0]
    database.insert_session(session_id, uid)
    # init user data
    helper.user_init(uid)
    resp = redirect(url_for('home'))
    resp.set_cookie('SESSION_ID', session_id)
    return resp


@app.route('/home', methods=['GET'])
def home():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = database.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')
    current_hid = user[4]
    helper = database.get_helper(current_hid)
    model_id = helper[1]
    costume_id = helper[2]
    return render_template("home.html", mode=model_id, cos=costume_id)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    success = helper.check_login(username, password)
    if not success:
        return render_template("sign.html", error='wrong username and password')

    # create session_id
    session_id = helper.generate_session_id()
    user = database.get_user_by_name(username)
    uid = user[0]
    database.insert_session(session_id, uid)

    resp = redirect(url_for('home'))
    resp.set_cookie('SESSION_ID', session_id)
    return resp


@app.route('/getAllFriends', methods=['POST'])
def get_all_friends():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = database.get_user_by_session_id(session_id)
    if not user:
        return {'code': 'no user'}

    uid = user[0]
    friends_id = database.get_all_friends(uid)
    data = {'code': 'ok'}
    friends_name = {}
    for idx, friend_id in enumerate(friends_id):
        friend = database.get_user_by_uid(friend_id)
        friend_name = friend[1]
        friends_name[idx] = friend_name
    data['data'] = friends_name
    print(data)
    return json.dumps(data)


@app.route('/GoForFriend', methods=['POST'])
def GoForFriend():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = database.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')

    fid = request.form['uid']
    user = database.get_user_by_uid(fid)
    current_hid = user[4]
    helper = database.get_helper(current_hid)
    model_id = helper[1]
    costume_id = helper[2]
    return render_template("home.html", mode=model_id, cos=costume_id)


@app.route('/friend', methods=['GET'])
def friendlist():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = database.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')

    uid = user[0]
    friends_id = database.get_all_friends(uid)
    friends_name = []
    for friend_id in friends_id:
        friend = database.get_user_by_uid(friend_id)
        friend_name = friend[1]
        friends_name.append(friend_name)
    return render_template("friendlistK.html", uid=uid, Friends=friends_name)


@app.route('/searchUser', methods=['POST'])
def searchUser():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = database.get_user_by_session_id(session_id)
    if not user:
        return {'code': 'no user'}

    keyword = request.form['searchContent']
    users = database.search_user(keyword)
    data = {'code': 'ok'}
    user_names = {}
    for idx, user in enumerate(users):
        user_name = user[1]
        user_names[idx] = user_name
    data['data'] = user_names
    return json.dumps(data)


@app.route('/GoTolearn', methods=['POST'])
def GoTolearn():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = database.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')

    uid = user[0]
    sid = request.form['subjectID']
    progress = database.get_progress(uid, sid)
    return render_template('learn.html', chapter=progress)


@app.route('/Totalchapter', methods=['POST'])
def Totalchapter():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = database.get_user_by_session_id(session_id)
    if not user:
        return {'code': 'no user'}

    sid = request.form['subjectID']
    subject = database.get_subject(sid)
    chapter_no = subject[2]
    data = {'code': 'ok', "data": chapter_no}
    return json.dumps(data)


@app.route('/learn', methods=['POST'])
def learn():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = database.get_user_by_session_id(session_id)
    if not user:
        return {'code': 'no user'}

    sid = request.form['subjectID']
    chapter = request.form['chapter']
    subject = database.get_subject(sid)

    if chapter < 0 or chapter > subject[2] - 1:
        return {'code': 'illegal parameter'}

    stored_path = subject[3]
    filename = "table" + str(chapter) + ".csv"
    path = os.path.join(stored_path, filename)

    words = {}
    with open(path) as csvfile:
        spamreader = csv.reader(csvfile)
        for idx, row in enumerate(spamreader, 1):
            words[idx] = {"word": row[0]}
            words[idx] = {"chinese": row[1]}
    ret_data = {"code": "ok", "data": words}
    return json.dumps(ret_data)


@app.route('/recordSchedule', methods=['POST'])
def recordSchedule():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = database.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')

    uid = user[0]
    sid = request.form['subjectID']
    chapter = request.form['chapter']

    database.update_progress(uid, sid, chapter)

    resp = redirect(url_for('home'))
    return resp
