from main.dataBase.DataBase import DatabaseManager


class UserManager:
    db_name = 'car_rental.db'
    table_name = 'user'

    def create_user_table(self):
        # 创建用户表
        user_columns = [
            "user_name VARCHAR(32) NOT NULL",
            "password VARCHAR(32) NOT NULL",
            "gmt_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "gmt_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "role INTEGER NOT NULL",
            "deleted INTEGER DEFAULT 0"
        ]
        dataManager = DatabaseManager(self.db_name)

        dataManager.create_table(self.table_name, user_columns)

    def insert_user(self, values):
        dataManager = DatabaseManager(self.db_name)

        dataManager.insert_record(self.table_name, values)

    def select_user(self, field, value):
        dataManager = DatabaseManager(self.db_name)

        result = dataManager.find_record_by_field(self.table_name, field, value)
        return result

    def select_user_fields(self, fields):
        dataManager = DatabaseManager(self.db_name)

        result = dataManager.find_record_by_fields(self.table_name, fields);
        return result
