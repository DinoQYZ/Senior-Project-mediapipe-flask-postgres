import logging

def setupTables(cursor, conn):
    L = [createUserTable, createRecordTable, createLoginStats]
    for func in L:
        try:
            func(cursor, conn)
        except Exception as e:
            logging.info(e)

def createUserTable(cursor, conn):
    sql = """
    CREATE TABLE usertable(
        id SERIAL PRIMARY KEY,
        username VARCHAR(20) UNIQUE NOT NULL,
        password VARCHAR(20) NOT NULL
    )
    """
    cursor.execute(sql)
    conn.commit()

def createRecordTable(cursor, conn):
    sql = """
    CREATE TABLE myrecord(
        username VARCHAR(20),
        action VARCHAR(40),
        reps_l INT,
        reps_r INT,
        time VARCHAR(70)
    );
    """
    cursor.execute(sql)
    conn.commit()

def createLoginStats(cursor, conn):
    sql = """
    CREATE TABLE loginStats(
        loggedin BOOLEAN,
        username VARCHAR(20)
    );
    """
    cursor.execute(sql)
    conn.commit()