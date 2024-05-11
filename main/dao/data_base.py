import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        # 创建表
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {', '.join(columns)}
            )
        ''')
        self.conn.commit()

    def insert_record(self, table_name, values):
        # 插入记录
        placeholders = ', '.join(['?' for _ in values])
        sql = f"INSERT INTO {table_name} VALUES (NULL, {placeholders})"
        self.cursor.execute(sql, values)
        self.conn.commit()

    def find_record_by_field(self, table_name, field, value):
        # 根据字段值查询记录
        self.cursor.execute(f'SELECT * FROM {table_name} WHERE deleted = 0 and {field}=?', (value,))
        return self.cursor.fetchone()

    def find_record_by_field(self, table_name, field1, value1, field2, value2):
        # 根据字段值查询记录
        self.cursor.execute(f'SELECT * FROM {table_name} WHERE deleted = 0 and {field1}=? and {field2}=?', (value1, value2))
        return self.cursor.fetchone()

    def find_record_by_fields(self, table_name, fields):
        # 根据多个字段值查询记录
        conditions = ' AND '.join([f'{field}=?' for field in fields])
        sql = f'SELECT * FROM {table_name} WHERE {conditions}'
        self.cursor.execute(sql, tuple(fields.values()))
        return self.cursor.fetchone()

    def find_allRecord_by_fields(self, table_name, fields):
        # 根据多个字段值查询记录
        conditions = ' AND '.join([f'{field}=?' for field in fields])
        sql = f'SELECT * FROM {table_name} WHERE {conditions}'
        self.cursor.execute(sql, tuple(fields.values()))
        return self.cursor.fetchall()


    def update_record(self, table_name, update_field, update_value, condition_field, condition_value):
        self.cursor.execute(f'UPDATE {table_name} SET {update_field}=? WHERE {condition_field}=?', (update_value, condition_value))
        self.conn.commit()

    def update_records(self, table_name, updateFields, conditionField, conditionValue):
        set_clause = ", ".join([f"{key}= '{value}'" for key, value in updateFields.items()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {conditionField} = {conditionValue}"
        self.cursor.execute(sql)
        self.conn.commit()

    def __del__(self):
        # 在销毁对象时关闭数据库连接
        self.conn.close()
