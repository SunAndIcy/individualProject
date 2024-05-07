from main.dataBase.DataBase import DatabaseManager

class CarManager:
    db_name = 'car_rental.db'
    table_name = 'car'
    def create_car_table(self):
        # 创建汽车资料表
        car_columns = [
            "make VARCHAR(32) NOT NULL",
            "model VARCHAR(32) NOT NULL",
            "year VARCHAR(32) NOT NULL",
            "mileage INTEGER NOT NULL",
            "available_now INTEGER DEFAULT 1",
            "minimum_rent_period INTEGER NOT NULL",
            "maximum_rent_period INTEGER NOT NULL",
            "gmt_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "gmt_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "deleted INTEGER DEFAULT 0"
        ]
        dataManager = DatabaseManager(self.db_name)

        dataManager.create_table(self.table_name, car_columns)

    def insert_car(self, values):
        dataManager = DatabaseManager(self.db_name)

        dataManager.insert_record(self.table_name, values)

    def select_car(self, field, value):
        dataManager = DatabaseManager(self.db_name)
        result = dataManager.find_record_by_field(self.table_name, field, value)

        return result

    def select_car_fields(self, fields):
        dataManager = DatabaseManager(self.db_name)

        result = dataManager.find_allRecord_by_fields(self.table_name, fields);
        return result

    def update_car_fields(self, updateField, updateValue, conditionField, conditionValue):
        dataManager = DatabaseManager(self.db_name)

        result = dataManager.update_record(self.table_name, updateField, updateValue, conditionField, conditionValue)
        return result