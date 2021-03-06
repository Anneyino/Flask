import pymysql

conn = pymysql.connect(host='148.70.247.3',  # 远程主机的ip地址，
                       user='root',  # MySQL用户名
                       db='moelearn',  # database名
                       passwd='moelearn',  # 数据库密码
                       port=3306,  # 数据库监听端口，默认3306
                       charset="utf8")  # 指定utf8编码的连接
cursor = conn.cursor()  # 创建一个光标，然后通过光标执行sql语句


def executeSQL(sql, parameters):
    with conn:
        cursor.execute(sql, parameters)
        conn.commit()


def fetchAllres(sql, parameters):
    with conn:
        cursor.execute(sql, parameters)
        return cursor.fetchall()


def fetchOneres(sql, parameters):
    with conn:
        cursor.execute(sql, parameters)
        return cursor.fetchone()


def signup(username, password, email):
    sql_str = "INSERT INTO user(username, passwd, email) values(%s, %s, %s);"
    try:
        executeSQL(sql_str, (username, password, email))
    except:
        return False
    return True

def log(info):
    sql_str = "INSERT INTO loginfo(info) values(%s);"
    try:
        executeSQL(sql_str, (username, password, email))
    except:
        return False
    return True

def get_user_by_name(username):
    sql_str = "SELECT * FROM user WHERE username=%s;"
    user = fetchOneres(sql_str, (username,))
    if not user:
        return None
    return user


def get_user_by_uid(uid):
    sql_str = "SELECT * FROM user WHERE uid=%s;"
    user = fetchOneres(sql_str, (uid,))
    if not user:
        return None
    return user


def get_user_by_session_id(session_id):
    sql_str = "SELECT uid FROM session WHERE session_id=%s;"
    uid = fetchOneres(sql_str, (session_id,))
    if not uid:
        return None
    return get_user_by_uid(uid)


def insert_session(session_id, uid):
    sql_str = "INSERT INTO session(session_id, uid) VALUES(%s, %s);"
    executeSQL(sql_str, (session_id, uid))

def set_user_current_hid(current_hid, uid):
    sql_str = "UPDATE user SET current_hid=%s WHERE uid=%s;"
    executeSQL(sql_str, (current_hid, uid))


def insert_init_user_helper(uid):
    sql_str = "INSERT INTO user_helper VALUES(%s, %s, %s);"
    executeSQL(sql_str, (uid, 1, 0))


def insert_init_user_subject(uid):
    sql_str = "INSERT INTO user_subject VALUES(%s, %s, %s);"
    # 1 is english
    executeSQL(sql_str, (uid, 1, 0))


def get_helper(hid):
    sql_str = "SELECT * FROM helper WHERE hid=%s;"
    helper = fetchOneres(sql_str, (hid,))
    if not helper:
        return None
    return helper


def get_password(username):
    sql_str = "SELECT passwd FROM user WHERE username=%s;"
    passwd = fetchOneres(sql_str, (username,))
    if not passwd:
        return None
    return passwd[0]


def get_all_friends(uid):
    sql_str = "SELECT uid_secondary FROM friend WHERE uid_primary=%s;"
    friends = fetchAllres(sql_str, (uid,))
    return friends

def check_friend(uid_p,uid_s):
    sql_str = "SELECT * FROM friend WHERE uid_primary = %s and uid_secondary= %s;"
    isfriend = fetchOneres(sql_str, (uid_p, uid_s))
    if not isfriend:
        return False
    return True

def add_friend(uid_p,uid_s):
    sql_str = "INSERT INTO friend VALUES(%s, %s);"
    executeSQL(sql_str, (uid_p, uid_s))

def del_friend(uid_p,uid_s):
    sql_str = "DELETE FROM friend WHERE uid_primary = %s and uid_secondary = %s;"
    executeSQL(sql_str,(uid_p, uid_s))

def search_user(keyword):
    sql_str = "SELECT * FROM user WHERE username LIKE %s %s;"
    users = fetchAllres(sql_str, (keyword,"%"))
    return users

def add_collect(uid,word):
    sql_str = "INSERT INTO collect_word(uid,word) VALUES(%s, %s);"
    executeSQL(sql_str, (uid, word))

def check_collect(uid,word):
    sql_str = "SELECT * FROM collect_word WHERE uid = %s and word = %s;"
    iscollect = fetchOneres(sql_str, (uid, word))
    if not iscollect:
        return False
    return True
def del_collect(uid,word):
    sql_str = "DELETE FROM collect_word WHERE uid = %s and word = %s;"
    executeSQL(sql_str,(uid, word)) 

def get_collect(uid):
    sql_str = "SELECT word FROM collect_word WHERE uid = %s;"
    words = fetchAllres(sql_str, (uid,))
    return words

def add_todo(uid,user_plan):
    sql_str = "INSERT INTO user_todo(uid,user_plan) VALUES(%s, %s);"
    executeSQL(sql_str, (uid, user_plan))

def del_todo(uid,user_plan):
    sql_str = "DELETE FROM user_todo WHERE uid = %s and user_plan = %s;"    
    executeSQL(sql_str, (uid, user_plan))

def get_user_todo(uid):
    sql_str = "SELECT user_plan FROM user_todo WHERE uid = %s;"
    todos = fetchAllres(sql_str, (uid,))
    return todos

def get_progress(uid, sid):
    sql_str = "SELECT progress FROM user_subject WHERE uid=%s AND sid=%s;"
    progress = fetchOneres(sql_str, (uid, sid))
    if not progress:
        return None
    return progress[0]


def get_subject(sid):
    sql_str = "SELECT * FROM subject WHERE sid=%s;"
    subject = fetchOneres(sql_str, (sid,))
    if not subject:
        return None
    return subject


def update_progress(uid, sid, progress):
    sql_str = "UPDATE user_subject SET progress=%s WHERE uid=%s AND sid=%s;"
    executeSQL(sql_str, (progress, uid, sid))

# values = fetchAllres("select * from user")
# cursor.close() 
# conn.close()  #最后记得关闭光标和连接，防止数据泄露
# print(values)
