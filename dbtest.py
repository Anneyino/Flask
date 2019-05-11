import pymysql

conn = pymysql.connect(host = '148.70.247.3',  # 远程主机的ip地址， 
                                            user = 'root',   # MySQL用户名
                                            db = 'moelearn',   # database名
                                            passwd = 'moelearn',   # 数据库密码
                                            port = 3306,  #数据库监听端口，默认3306
                                            charset = "utf8")  #指定utf8编码的连接
cursor = conn.cursor()  # 创建一个光标，然后通过光标执行sql语句

def executeSQL(sql):
    with conn:
        cursor.execute(sql)
        conn.commit()

def fetchAllres(sql):
    with conn:
        cursor.execute(sql)
        return cursor.fetchall()

def fetchOneres(sql):
    with conn:
        cursor.execute(sql)
        return cursor.fetchone()

# values = fetchAllres("select * from user")
# cursor.close() 
# conn.close()  #最后记得关闭光标和连接，防止数据泄露
# print(values)