import psycopg2 as pg2

def connDB(conInfo):
    conn_string = 'host={} user={} dbname={} password={} sslmode={}'.format(
    conInfo['host'], conInfo['user'], conInfo['dbname'], conInfo['password'], conInfo['sslmode'])

    conn = pg2.connect(conn_string)
    conn.autocommit = True
    
    cursor = conn.cursor()
    return cursor, conn