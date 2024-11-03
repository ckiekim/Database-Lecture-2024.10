# World database에 있는 koreanCity 테이블을 액세스하는 라이브러리

import json, pymysql

with open('./mysql.json') as f:
    config_str = f.read()
config = json.loads(config_str)

# 어떤 도시의 정보
def find_by_name(name):
	conn = pymysql.connect(**config)
	cur = conn.cursor()
	sql = "SELECT * FROM koreancity WHERE name=%s"
	cur.execute(sql, (name, ))
	row = cur.fetchone()
	cur.close()
	conn.close()
	return row

def find_by_id(id):
	conn = pymysql.connect(**config)
	cur = conn.cursor()
	sql = "SELECT * FROM koreancity WHERE id=%s"
	cur.execute(sql, (id, ))
	row = cur.fetchone()
	cur.close()
	conn.close()
	return row

# 어떤 광역시도의 도시 정보
def find_list_by_district(district):
	conn = pymysql.connect(**config)
	cur = conn.cursor()
	sql = "SELECT * FROM koreancity WHERE district=%s"
	cur.execute(sql, (district, ))
	rows = cur.fetchall()
	cur.close()
	conn.close()
	return rows

# 도시정보 추가
def insert_city(params):
	conn = pymysql.connect(**config)
	cur = conn.cursor()
	sql = "INSERT INTO koreancity VALUES(DEFAULT, %s, %s, %s)"
	cur.execute(sql, params)
	conn.commit()
	cur.close()
	conn.close()

# 도시정보 수정
def update_city(params):
	conn = pymysql.connect(**config)
	cur = conn.cursor()
	sql = "UPDATE koreancity SET name=%s, district=%s, population=%s WHERE id = %s"
	cur.execute(sql, params)
	conn.commit()
	cur.close()
	conn.close()
    
# 도시정보 삭제
def delete_city(id):
	conn = pymysql.connect(**config)
	cur = conn.cursor()
	sql = "DELETE FROM koreancity WHERE id = %s"
	cur.execute(sql, (id, ))
	conn.commit()
	cur.close()
	conn.close()
