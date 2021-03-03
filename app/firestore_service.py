import firebase_admin
from firebase_admin import credentials, firestore

credentials = credentials.ApplicationDefault()
firebase_admin.initialize_app(credentials)

db = firestore.client()

def get_users():
    return db.collection('users').get()

def get_user(user_id):
    return db.collection('users').document(user_id).get()

def get_to_dos(user_id):
    return db.collection('users').document(user_id).collection('to_dos').get()

def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({ 'password':user_data.password })

def put_to_do(user_id, description):
    to_do_collection_ref = db.collection('users').document(user_id).collection('to_dos')
    to_do_collection_ref.add({'description':description,'done':False})

def delete_to_do(user_id, to_do_id):
    to_do_ref = _get_to_do_ref(user_id, to_do_id)
    #to_do_ref = db.document('users/{}/to_dos/[{}]'.format(user_id, to_do_id))
    to_do_ref.delete()

def update_to_do(user_id, to_do_id, done):
    to_do_done = not bool(done)
    to_do_ref = _get_to_do_ref(user_id, to_do_id)
    to_do_ref.update({ 'done':to_do_done })

def _get_to_do_ref(user_id, to_do_id):
    return db.collection('users').document(user_id).collection('to_dos').document(to_do_id)