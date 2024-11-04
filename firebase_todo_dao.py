# Firebase realtime database의 todos table에 대한 CRUD library

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('D:/Workspace/2024_11_MySQL/bootproject-ce9d4-firebase-adminsdk-ufpty-f80f606466.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://bootproject-ce9d4-default-rtdb.asia-southeast1.firebasedatabase.app/'})

def insert_todo(todo):
    todos_ref = db.reference('todos')
    new_todo_ref = todos_ref.push()
    new_todo_ref.set(todo)

def get_todo_list(uid):
	todos_ref = db.reference('todos')
	todos = todos_ref.get()

	todo_list = []
	for key, todo in todos.items():
		if todo['uid'] == uid:
			todo_list.append(todo)
		
	todo_list.sort(key=lambda x: x['date'])
	return todo_list

def get_todo_list_by_date(uid, date):
	todos_ref = db.reference('todos')
	todos = todos_ref.get()

	todo_list = []
	for key, todo in todos.items():
		if todo['uid'] == uid and todo['date'] == date:
			todo_list.append(todo)
		
	todo_list.sort(key=lambda x: x['date'])
	return todo_list

def update_todo(new_todo):
    todos_ref = db.reference('todos')
    todos = todos_ref.get()
    
    for key, todo in todos.items():
        if todo['uid'] == new_todo['uid'] and todo['date'] == new_todo['date'] and todo['name'] == new_todo['name']:
            update_ref = todos_ref.child(key)
            break
    update_ref.update(new_todo)

def delete_todo(del_todo):
    todos_ref = db.reference('todos')
    todos = todos_ref.get()
    
    for key, todo in todos.items():
        if todo['uid'] == del_todo['uid'] and todo['date'] == del_todo['date'] and todo['name'] == del_todo['name']:
            delete_ref = todos_ref.child(key)
            break
    delete_ref.delete()