import threading

local_data = threading.local()

def set_current_user(user):
    local_data.user = user

def get_current_user():
    return getattr(local_data, 'user', None)

def on_closing():
    user = get_current_user()
    if user:
        print(f"User {user.userName} logged out.")
        del local_data.user

def set_login_user(user):
    set_current_user(user)
    print(f"User {user.userName} logged in.")