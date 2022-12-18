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

def deleteUser(cursor, username):
    logMsg = ''
    try:
        cursor.execute("DELETE FROM usertable WHERE username=\'{}\'".format(username))
    except:
        return 'failed to delete user'
    return logMsg

# login
def getLoginStats(cursor):
    cursor.execute("SELECT * FROM loginstats;")
    result = cursor.fetchall()
    return result

def updateLoginStats(loginStats, cursor, conn):
    cursor.execute("UPDATE loginstats SET loggedin=\'{}\', username=\'{}\';".format(loginStats[0], loginStats[1]))
    conn.commit()

# get record by account
def getRecordByAccount(loginStats, cursor):
    cursor.execute("SELECT * FROM myrecord WHERE username=\'{}\';".format(loginStats[1]))
    result = cursor.fetchall()
    return result

# insert new goal
def addNewGoal(loginStats, cursor, conn, goalStats):
    goal = getGoalByAccount(loginStats, cursor)
    goalExist = False
    for i in goal:
        if i[1]==goalStats['action'] and i[2]==int(goalStats['reps']) and i[3]==goalStats['date']:
            goalExist = True
            break
    if goalExist == False:
        cursor.execute("""
                INSERT INTO mygoal (username, action, reps, time, done)
                VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')
                """.format(loginStats[1], goalStats['action'], int(goalStats['reps']), goalStats['date'], False))
        conn.commit()

# get goal by account
def getGoalByAccount(loginStats, cursor):
    cursor.execute("SELECT * FROM mygoal WHERE username=\'{}\' ORDER BY time ASC;".format(loginStats[1]))
    result = cursor.fetchall()
    return result

def changeGoalToDone(cursor, conn, goalItem):
    cursor.execute("""
                UPDATE mygoal SET done=\'{}\'
                WHERE username=\'{}\' AND action=\'{}\' AND reps={} AND time=\'{}\'
                """.format(True, goalItem[0], goalItem[1], goalItem[2], goalItem[3]))
    conn.commit()
