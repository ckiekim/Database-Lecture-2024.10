# Firebase realtime database의 users table에 대한 CRUD library

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('D:/Workspace/2024_11_MySQL/bootproject-ce9d4-firebase-adminsdk-ufpty-f80f606466.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://bootproject-ce9d4-default-rtdb.asia-southeast1.firebasedatabase.app/'})

def insert_user(user):
    users_ref = db.reference('users')
    new_user_ref = users_ref.push()
    new_user_ref.set(user)
    
def find_by_uid(uid):
    users_ref = db.reference('users')
    users = users_ref.get()
    
    for key, user in users.items():		# key, value 쌍을 key, user로 이름만 변경
        if user['uid'] == uid:
            return user
    return {}

def get_user_list():
    users_ref = db.reference('users')
    users = users_ref.get()
    
    user_list = []
    for key, user in users.items():
        user_list.append(user)
    return user_list

def get_user_ordered_list(field='uid', ascending=True):
    users_ref = db.reference('users')
    users = users_ref.get()
    
    ordered_user_list = []
    for key, user in users.items():
        ordered_user_list.append(user)
        
    if ascending == True:
        ordered_user_list.sort(key=lambda x: x[field])
    else:
        ordered_user_list.sort(key=lambda x: x[field], reverse=True)
    return ordered_user_list

def get_user_list_by_uname_length(length=3):
    users_ref = db.reference('users')
    users = users_ref.get()
    
    selected_users = []
    for key, user in users.items():
        if len(user['uname']) == length:
            selected_users.append(user)
    return selected_users

def update_user(new_user):
    users_ref = db.reference('users')
    users = users_ref.get()
    
    for key, user in users.items():
        if user['uid'] == new_user['uid']:
            update_ref = users_ref.child(key)
            break
    update_ref.update(new_user)

def delete_user(uid):
    users_ref = db.reference('users')
    users = users_ref.get()
    
    for key, user in users.items():
        if user['uid'] == uid:
            delete_ref = users_ref.child(key)
            break
    delete_ref.delete()
