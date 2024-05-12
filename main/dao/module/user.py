from datetime import datetime

from main.manager.user_manager import UserManager
from main.util.thread_local import set_login_user


class User:
    def __init__(self, userName, password, role, id =None):
        self._id = id
        self._userName = userName
        self._password = password
        self._role = role

    @classmethod
    def from_user_record(cls, record):
        id, username, password, _, _, role, *_ = record
        return cls(username, password, role, id)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def userName(self):
        return self._userName

    @userName.setter
    def userName(self, value):
        self._userName = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    def register(self):
        userManager = UserManager()
        user = userManager.select_user_fields({"user_name": self.userName, "role": self.role});

        if user:
            print("The user is exit, Please login.")
            return False

        userManager.insert_user((self.userName, self.password, datetime.now(), datetime.now(), self.role, 0))
        return True

    def login(self):
        userManager = UserManager()
        result = userManager.select_user_fields({"user_name": self.userName, "role": self.role});

        if not result:
            print("The user is not exit, Please regist!")
            return False

        user = User.from_user_record(result)

        if self.password != user.password:
            print("The password is not correct, Please try again!")
            return False

        set_login_user(user)
        return True