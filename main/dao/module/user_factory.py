from main.dao.module.admin import Admin
from main.dao.module.customer import Customer
from main.enums.role_enum import Role


class UserFactory:
    def create_user(userName, password, role):
        if role == Role.ADMIN.value:
            return Admin(userName, password, role)
        elif role == Role.CUSTOMER.value:
            return Customer(userName, password, role)
        else:
            raise ValueError("not support role")