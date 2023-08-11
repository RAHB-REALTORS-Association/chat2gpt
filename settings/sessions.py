import datetime

import datetime

user_sessions = {}

def create_session(user_id):
    current_time = datetime.datetime.now()
    user_sessions[user_id] = current_time

def delete_session(user_id):
    if user_id in user_sessions:
        del user_sessions[user_id]

def get_session(user_id):
    return user_sessions.get(user_id, None)
