from flask import *
import time
import json
import databaseq
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
    success = databaseq.signup(username, password, email)
    if not success:
        return render_template("sign.html", error='username exists')

    # create session_id
    session_id = helper.generate_session_id()
    user = databaseq.get_user_by_name(username)
    uid = user[0]
    databaseq.insert_session(session_id, uid)
    # init user data
    helper.user_init(uid)
    resp = redirect(url_for('home'))
    resp.set_cookie('SESSION_ID', session_id)
    return resp


@app.route('/home', methods=['GET'])
def home():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = databaseq.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')
    current_hid = user[4]
    helper = databaseq.get_helper(current_hid)
    model_id = helper[1]
    costume_id = helper[2]
    return render_template("home.html", mode=model_id, cos=costume_id, show_button = "")


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    success = helper.check_login(username, password)
    if not success:
        return render_template("sign.html", error='wrong username and password')

    # create session_id
    session_id = helper.generate_session_id()
    user = databaseq.get_user_by_name(username)
    uid = user[0]
    databaseq.insert_session(session_id, uid)

    resp = redirect(url_for('home'))
    resp.set_cookie('SESSION_ID', session_id)
    return resp


@app.route('/getAllFriends', methods=['POST'])
def get_all_friends():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = databaseq.get_user_by_session_id(session_id)
    if not user:
        return {'code': 'no user'}

    uid = user[0]
    friends_id = databaseq.get_all_friends(uid)
    data = {'code': 'ok'}
    friends_name = {}
    for idx, friend_id in enumerate(friends_id):
        friend = databaseq.get_user_by_uid(friend_id)
        friend_name = friend[1]
        friends_name[idx] = friend_name
    data['data'] = friends_name
    return json.dumps(data)


@app.route('/GoForFriend', methods=['POST'])
def GoForFriend():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = databaseq.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')

    fname = request.form['fname']
    print(fname)
    user = databaseq.get_user_by_name(fname) 
    current_hid = user[4]
    helper = databaseq.get_helper(current_hid)
    model_id = helper[1]
    costume_id = helper[2]
    return render_template("home.html", mode=model_id, cos=costume_id, show_button="display:none;")


@app.route('/friend', methods=['GET'])
def friendlist():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = databaseq.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')

    uid = user[0]
    friends_id = databaseq.get_all_friends(uid)
    friends_name = []
    for friend_id in friends_id:
        friend = databaseq.get_user_by_uid(friend_id)
        friend_name = friend[1]
        friends_name.append(friend_name)
    return render_template("friendlistK.html", uid=uid, Friends=friends_name)


@app.route('/searchUser', methods=['POST'])
def searchUser():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = databaseq.get_user_by_session_id(session_id)
    if not user:
        return {'code': 'no user'}
    current_uid = user[0]; 
    # keyword = request.form['searchContent']
    data_recv = request.get_data(as_text = True)
    data_recv_json = json.loads(data_recv)
    keyword = data_recv_json['Searchkeyword']
    users = databaseq.search_user(keyword)
    databaseq.get_user_by_name("asd")
    data = {'code': 'ok'}
    user_names = {}
    user_isfriend = {}
    frontend_action = {}
    index = 0
    for idx, user in enumerate(users):
        user_name = user[1]
        if user[0] != current_uid:
            user_names[index] = user_name
            isfriend = databaseq.check_friend(current_uid,user[0])
            if isfriend:
                user_isfriend[index] = "已关注"
                frontend_action[index] = "/NoFocusFriend"
            else:
                user_isfriend[index] = "未关注"
                frontend_action[index] = "/FocusFriend"
            index = index + 1;            
    data['data'] = user_names
    data['isfriend'] = user_isfriend
    data['action'] = frontend_action
    return json.dumps(data)

@app.route('/ShowToDoList', methods =['POST'])
def ShowToDoList():
    session_id = request.cookies.get('SESSION_ID', '')
    user = databaseq.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')
    
    current_uid = user[0]
    data = {'code': 'ok'}
    user_todos = databaseq.get_user_todo(current_uid)
    todolist = {}
    for idx, todo in enumerate(user_todos):
        todolist[idx] = todo[0]
    data['data'] = todolist
    return json.dumps(data)

@app.route('/AddToDoList', methods = ['POST'])
def AddToDoList():
    session_id = request.cookies.get('SESSION_ID', '')
    user = databaseq.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')
    
    data = {'code': 'ok'}
    current_uid = user[0]
    data_recv = request.get_data(as_text = True)
    data_recv_json = json.loads(data_recv)
    event = data_recv_json['newevent']
    databaseq.add_todo(current_uid, event)
    return json.dumps(data)
    
@app.route('/RemoveFromToDo', methods = ['POST'])
def RemoveFromToDo():
    session_id = request.cookies.get('SESSION_ID', '')
    user = databaseq.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')
    data = {'code': 'ok'}
    current_uid = user[0]
    data_recv = request.get_data(as_text = True)
    data_recv_json = json.loads(data_recv)
    event = data_recv_json['event']
    databaseq.del_todo(current_uid, event)
    return json.dumps(data)


@app.route('/FocusFriend', methods = ['POST'])
def FocusFriend():
    session_id = request.cookies.get('SESSION_ID', '')
    user = databaseq.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')

    current_uid = user[0]
    fname = request.form['uid']
    friend = databaseq.get_user_by_name(fname)
    fid = friend[0]
    databaseq.add_friend(current_uid,fid)

    resp = redirect(url_for('friendlist'))
    return resp    


@app.route('/NoFocusFriend', methods = ['POST'])
def NoFocusFriend():
    session_id = request.cookies.get('SESSION_ID', '')
    user = databaseq.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')

    current_uid = user[0]
    fname = request.form['uid']
    friend = databaseq.get_user_by_name(fname)
    fid = friend[0]
    databaseq.del_friend(current_uid,fid)
    resp = redirect(url_for('friendlist'))
    return resp    

@app.route('/GoTolearn', methods=['POST'])
def GoTolearn():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = databaseq.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')

    uid = user[0]
    #sid = request.form['subjectID'] 为测试暂时先用1：english代替
    sid = 1
    progress = databaseq.get_progress(uid, sid)
    alert_str = ""
    if progress != 0:
        alert_str = "记录到上次学习至" + progress +"章节, 是否继续学习？"

    return render_template('learn.html', chapter=progress, alertinfo = alert_str)


@app.route('/Totalchapter', methods=['POST'])
def Totalchapter():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = databaseq.get_user_by_session_id(session_id)
    if not user:
        return {'code': 'no user'}
    
    data_recv = request.get_data(as_text = True)
    data_recv_json = json.loads(data_recv)

    sid = data_recv_json['subjectID']
    subject = databaseq.get_subject(sid)
    chapter_no = subject[2]
    data = {'code': 'ok', "data": chapter_no}
    return json.dumps(data)


@app.route('/learn', methods=['POST'])
def learn():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = databaseq.get_user_by_session_id(session_id)
    if not user:
        return {'code': 'no user'}

    #sid = request.form['subjectID'] 为测试暂时用1替代
    sid = 1
    current_uid = user [0]
    data_recv = request.get_data(as_text = True)
    data_recv_json = json.loads(data_recv)

    chapter = data_recv_json['chapter']
    subject = databaseq.get_subject(sid)
    data = {'code': 'ok'}
    if chapter < 0 or chapter > subject[2] - 1:
        return {'code': 'illegal parameter'}

    stored_path = subject[3]
    filename = "table" + str(chapter) + ".csv"
    path = os.path.join(stored_path, filename)
    words = {}
    chineses = {}
    iscollects = {}
    with open(path) as csvfile:
        spamreader = csv.reader(csvfile)
        for idx, row in enumerate(spamreader, 1):
            words[idx] = row[0]
            chineses[idx] = row[1]
            iscollect = databaseq.check_collect(current_uid, row[0])
            if iscollect:
                iscollects[idx] = 1
            else:
                iscollects[idx] = 0

    data['word'] = words
    data['chinese'] = chineses
    data['iscollect'] = iscollects 
    print(data)
    return json.dumps(data)


@app.route('/recordSchedule', methods=['POST'])
def recordSchedule():
    # check login status
    session_id = request.cookies.get('SESSION_ID', '')
    user = databaseq.get_user_by_session_id(session_id)
    if not user:
        return render_template("sign.html", error='please login')

    uid = user[0]
    sid = request.form['subjectID']
    chapter = request.form['chapter']

    databaseq.update_progress(uid, sid, chapter)

    resp = redirect(url_for('home'))
    return resp
