# World database에 있는 song, girl_group 테이블을 액세스하는 라이브러리
# Connection Pool 사용
# 설치: pip install mysql-connector-python

import json
from mysql.connector import pooling

with open('./mysql.json') as f:
    config_str = f.read()
config = json.loads(config_str)
pool = pooling.MySQLConnectionPool(pool_size=3, pool_name='mypool', **config)

def get_song_list_by_debut(year):
    sql = """SELECT g.name, g.debut, s.title
				FROM song s
				JOIN girl_group g ON s.sid = g.hit_song_id
				WHERE g.debut LIKE CONCAT(%s, '%%')"""
    conn = pool.get_connection()	# pool에서 이미 만들어 놓은 커넥션을 가지고 옴
    cur = conn.cursor()
    cur.execute(sql, (year, ))
    rows = cur.fetchall()
    cur.close()
    conn.close()					# 사용했던 커넥션을 반납
    return rows

def get_song_list(num=20, offset=0):
    sql = "SELECT * FROM song LIMIT %s OFFSET %s"
    conn = pool.get_connection()	
    cur = conn.cursor()
    cur.execute(sql, (num, offset))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_girl_group_list(num=20, offset=0):
    sql = "SELECT * FROM girl_group LIMIT %s OFFSET %s"
    conn = pool.get_connection()	
    cur = conn.cursor()
    cur.execute(sql, (num, offset))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows  

def get_girl_group_list_with_song(num=20, offset=0):
    sql = """SELECT g.gid, g.name, g.debut, s.title
                FROM girl_group g 
                JOIN song s ON g.hit_song_id = s.sid
                LIMIT %s OFFSET %s"""
    conn = pool.get_connection()	
    cur = conn.cursor()
    cur.execute(sql, (num, offset))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows 

def insert_song(params):
    if len(params) == 3:
        sql = "INSERT INTO song VALUES (%s, %s, %s)"
    else:
        sql = "INSERT INTO song VALUES (default, %s, %s)"
    conn = pool.get_connection()	
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()
 
def insert_girl_group(params):
    sql = "INSERT INTO girl_group VALUES (DEFAULT, %s, %s, %s)"
    conn = pool.get_connection()	
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()

def update_song(params):
    sql = "UPDATE song SET title=%s, lyrics=%s WHERE sid=%s"
    conn = pool.get_connection()	
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()

def update_girl_group(params):
    sql = "UPDATE girl_group SET name=%s, debut=% hit_song_id=%s WHERE gid=%s"
    conn = pool.get_connection()	
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()

def delete_song(sid):
    sql = "DELETE FROM song WHERE sid=%s"
    conn = pool.get_connection()	
    cur = conn.cursor()
    cur.execute(sql, (sid, ))
    conn.commit()
    cur.close()
    conn.close()

def delete_girl_group(gid):
    sql = "DELETE FROM girl_group WHERE gid=%s"
    conn = pool.get_connection()	
    cur = conn.cursor()
    cur.execute(sql, (gid, ))
    conn.commit()
    cur.close()
    conn.close()

def get_song(sid):
    sql = "select * from song where sid=%s"
    conn = pool.get_connection()	
    cur = conn.cursor()
    cur.execute(sql, (sid, ))
    song = cur.fetchone()
    cur.close()
    conn.close()
    return song

def get_girl_group(gid):
    sql = "select * from girl_group where gid=%s"
    conn = pool.get_connection()	
    cur = conn.cursor()
    cur.execute(sql, (gid, ))
    girl_group = cur.fetchone()
    cur.close()
    conn.close()
    return girl_group
