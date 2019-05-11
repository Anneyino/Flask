from flask import *
import time
import json
import database
import helper
import user_auth

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


@app.route('/getAllFriends', methods=['GET'])
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
    return json.dumps(data)


@app.route('/GoForFriend', methods=['POST'])
def GoForFriend():
    fid = request.form['uid']
    user = database.get_user_by_uid(fid)
    current_hid = user[4]
    helper = database.get_helper(current_hid)
    model_id = helper[1]
    costume_id = helper[2]
    return render_template("home.html", mode=model_id, cos=costume_id)


# unrefactored

@app.route('/Fortest', methods=['GET', 'POST'])
def Fortest():
    testInfo = {}
    for i in range(5):
        testInfo[i] = {}
        testInfo[i]['day'] = '928'
    return json.dumps(testInfo)


@app.route('/ForSendtest', methods=['POST'])
def Forsendtest():
    data = request.get_data(as_text=True)
    datas = json.loads(data)
    current_userid = datas['current_uid']
    intid = int(current_userid)
    all_friends_id = user_auth.show_friends(intid)
    all_friends_name = []
    for eachid in all_friends_id:
        all_friends_name.append(user_auth.get_username_from_database(eachid[0]))
    friends_list_json = {}
    count = 0
    for fn in all_friends_name:
        friends_list_json[count] = {}
        friends_list_json[count]['name'] = fn
        count = count + 1
    return json.dumps(friends_list_json)


@app.route('/friend', methods=['GET', 'POST'])
def friendlist():
    userid = request.form['uid']
    all_friends_id = user_auth.show_friends(userid)
    all_friends_name = []
    for eachid in all_friends_id:
        all_friends_name.append(user_auth.get_username_from_database(eachid[0]))
    return render_template("friendlistK.html", uid=userid, Friends=all_friends_name)
