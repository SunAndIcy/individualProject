class User:

    def __init__(self, id, userName, password, gmtCreated, gmtModified, role, deleted):
        self._id = id
        self._userName = userName
        self._password = password
        self._gmtCreated = gmtCreated
        self._gmtModified = gmtModified
        self._role = role
        self._deleted = deleted

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
