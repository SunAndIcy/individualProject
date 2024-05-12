
from main.dao.data_base import DatabaseManager

class RentManager:
    db_name = 'car_rental.db'
    table_name = 'rental'

    rental_columns = [
        "user_id INTEGER NOT NULL",
        "user_name VARCHAR(32) NOT NULL",
        "car_id INTEGER NOT NULL",
        "make VARCHAR(32) NOT NULL",
        "model VARCHAR(32) NOT NULL",
        "year VARCHAR(32) NOT NULL",
        "mileage INTEGER NOT NULL",
        "rental_start_day TIMESTAMP NOT NULL",
        "rental_days INTEGER NOT NULL",
        "rate DOUBLE NOT NULL",
        "cost DOUBLE DEFAULT NULL",
        "status INTEGER DEFAULT 1",
        "gmt_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "gmt_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "deleted INTEGER DEFAULT 0"
    ]
    def __init__(self):
        dataManager = DatabaseManager(self.db_name)
        dataManager.create_table(self.table_name, self.rental_columns)

    def insert_rental(self, values):
        dataManager = DatabaseManager(self.db_name)

        dataManager.insert_record(self.table_name, values)

    def select_rental(self, field, value):
        dataManager = DatabaseManager(self.db_name)
        result = dataManager.find_record_by_field(self.table_name, field, value)

        return result

    def select_rental_fields(self, fields):
        dataManager = DatabaseManager(self.db_name)

        result = dataManager.find_allRecord_by_fields(self.table_name, fields);
        return result

    def update_rental_fields(self, updateField, updateValue, conditionField, conditionValue):
        dataManager = DatabaseManager(self.db_name)

        result = dataManager.update_record(self.table_name, updateField, updateValue, conditionField, conditionValue)
        return result