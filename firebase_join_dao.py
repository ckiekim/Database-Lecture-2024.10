# Firebase realtime database의 users table과 todos table에 대한 JOIN library

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('D:/Workspace/2024_11_MySQL/bootproject-ce9d4-firebase-adminsdk-ufpty-f80f606466.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://bootproject-ce9d4-default-rtdb.asia-southeast1.firebasedatabase.app/'})

def get_todo_list(uid):
	todos_ref = db.reference('todos')
	todos = todos_ref.get()
 
	users_ref = db.reference('users')
	users = users_ref.get()
	for _, user in users.items():
		if user['uid'] == uid:
			uname = user['uname']

	todo_list = []
	for _, todo in todos.items():
		if todo['uid'] == uid:
			new_todo = todo
			new_todo['uname'] = uname
			todo_list.append(new_todo)
		
	todo_list.sort(key=lambda x: x['date'])
	return todo_list

def get_todo_list_by_date(uid, date):
	todos_ref = db.reference('todos')
	todos = todos_ref.get()

	users_ref = db.reference('users')
	users = users_ref.get()
	for _, user in users.items():
		if user['uid'] == uid:
			uname = user['uname']

	todo_list = []
	for _, todo in todos.items():
		if todo['uid'] == uid and todo['date'] == date:
			new_todo = todo
			new_todo['uname'] = uname
			todo_list.append(new_todo)
		
	todo_list.sort(key=lambda x: x['date'])
	return todo_list

def get_all_todo_list():
	todos_ref = db.reference('todos')
	todos = todos_ref.get()
	users_ref = db.reference('users')
	users = users_ref.get()
	   
	todo_list = []
	for _, todo in todos.items():
		uid = todo['uid']
		for _, user in users.items():
			if user['uid'] == uid:
				uname = user['uname']
		new_todo = todo
		new_todo['uname'] = uname
		todo_list.append(new_todo)

	todo_list.sort(key=lambda x: x['date'])
	return todo_list
