import psycopg2 as pg2
import psycopg2.extras

# connect to database
def connDB(conInfo):
    conn_string = 'host={} user={} dbname={} password={} sslmode={}'.format(
    conInfo['host'], conInfo['user'], conInfo['dbname'], conInfo['password'], conInfo['sslmode'])

    conn = pg2.connect(conn_string)
    conn.autocommit = True
    
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return cursor, conn

# insert your record
def insertActionCompleted(conn, cursor, value):
    cursor.execute("""
    INSERT INTO myrecord (username, action, reps_l, reps_r, time) VALUES (%s, %s, %s, %s, %s);
    """, (value['username'], value['action'], value['reps_l'], value['reps_r'], value['time']))

    conn.commit()

# return log
def userLogin(cursor, username, password):
    logMsg = ''
    cursor.execute("SELECT * FROM usertable WHERE username=\'{}\'".format(username))
    result = cursor.fetchall()
    if result:
        if result[0][2] == password:
            logMsg = ''
        else:
            logMsg = 'incorrect password of user \'{}\''.format(username)
    else:
        logMsg = 'Username {} not found'.format(username)
    
    return result, logMsg

# register
def userRegister(cursor, username, password, password_r):
    logMsg = ''
    cursor.execute("SELECT * FROM usertable WHERE username=\'{}\'".format(username))
    result = cursor.fetchall()
    if not result:
        if password == password_r:
            cursor.execute("""
            INSERT INTO usertable (username, password) VALUES (\'{}\', \'{}\')
            """.format(username, password))
        else:
            logMsg = 'Password not match'
    else:
        logMsg = 'Username {} already exist'.format(username)
    
    return logMsg

def getLoginStats(cursor):
    cursor.execute("SELECT * FROM loginstats;")
    result = cursor.fetchall()
    return result

def updateLoginStats(loginStats, cursor, conn):
    cursor.execute("UPDATE loginstats SET loggedin=\'{}\', username=\'{}\';".format(loginStats[0], loginStats[1]))
    conn.commit()

