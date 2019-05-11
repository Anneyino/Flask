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


def get_user_by_name(username):
    sql_str = "SELECT * FROM user WHERE username=%s;"
    user = fetchOneres(sql_str, (username,))
    return user


def get_user_by_uid(uid):
    sql_str = "SELECT * FROM user WHERE uid=%s;"
    user = fetchOneres(sql_str, (uid,))
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

# values = fetchAllres("select * from user")
# cursor.close() 
# conn.close()  #最后记得关闭光标和连接，防止数据泄露
# print(values)
