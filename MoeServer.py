from flask import *
import time
import json
import database, user_auth

app = Flask(__name__)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return render_template('sign.html')

@app.route('/sign', methods=['GET', 'POST'])
def sign():
    username = request.form['username']
    password = request.form['password']
    email = request.form['emailaddr']
    success = user_auth.verify_sign(username,password,email)
    if not success:
        return render_template("sign.html", error = 'username exists')
    time.sleep(3)    
    current_uid = user_auth.get_uid_from_database(username)    
    return render_template("home.html", user_id = current_uid)

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    success = user_auth.check_login(username, password)
    if not success:
        return render_template("sign.html", error = 'wrong username and password')
    time.sleep(3)
    current_uid = user_auth.get_uid_from_database(username)    
    return render_template("home.html", user_id = current_uid)    

@app.route('/Fortest', methods =['GET', 'POST'])
def Fortest():
    testInfo = {}
    for i in range(5):
        testInfo[i] = {}
        testInfo[i]['day'] = '928'
    return json.dumps(testInfo)

@app.route('/ForSendtest', methods = ['POST'])
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

@app.route('/GoForFriend', methods = ['POST'])
def GoForFriend():
    #data = request.get_data(as_text=True)
    #datas = json.loads(data)
    #selected_friendname = datas['friend_name']
    fid = request.form['uid']
    #friend_id = user_auth.get_uid_from_database(selected_friendname)
    #FriendInfo = {}
    #FriendInfo['fid'] = friend_id
    return render_template("home.html")


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/friend', methods=['GET', 'POST'])
def friendlist():
    userid = request.form['uid']
    all_friends_id = user_auth.show_friends(userid)
    all_friends_name = []
    for eachid in all_friends_id:
        all_friends_name.append(user_auth.get_username_from_database(eachid[0]))     
    return render_template("friendlistK.html", uid = userid, Friends = all_friends_name)