import mysql.connector

class MySQLStorage:
    "This is mysql database storage"

    HOST="localhost"
    USER="root"
    PASSWORD= "root"
    PORT = 3306

    def __init__(self):
        self.connection = mysql.connector.connect(
            host=self.HOST,
            user=self.USER,
            password=self.PASSWORD,
        )
        self.connection._execute_query("CREATE DATABASE IF NOT EXISTS habit_tracker;")
        self.connection._execute_query("USE habit_tracker;")

    def save(self, obj):
        table_name = obj.__table_name__
        columns = []
        for key, value in obj.__dict__.items():
            print(key, value)
            datatype = type(value)
            column_name = key
            column_datatype = ""

            is_primary_key = key == "id"

            if datatype == str:
                column_datatype = f"VARCHAR(255) {'PRIMARY KEY' if is_primary_key else ''}"
            elif datatype == int:
                column_datatype = f"INTEGER(10) {'PRIMARY KEY' if is_primary_key else ''}"

            columns.append(f"`{column_name}` {column_datatype}")
                
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({','.join(columns)})"
        self.connection._execute_query(query)

        row = [f"'{row}'" for row in obj.__dict__.values()]
        columns = list(obj.__dict__.keys())
        print(row)
        print(columns)


        query = f"INSERT INTO {table_name}({', '.join(columns)}) VALUES({', '.join(row)});"
        print(query)
        self.connection._execute_query(query)
        self.connection.commit()
    
    # def create_table(self,obj):