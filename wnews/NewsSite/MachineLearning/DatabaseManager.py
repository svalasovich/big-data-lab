import mysql.connector
from mysql.connector import Error


class DatabaseManager:
    connection = None
    table_names = {}

    _cursor = None

    def create_connection(self, host_name, user_name, user_password, db_name):
        try:
            self.connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name,
                connect_timeout=2000,
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return self.connection

    def create_table(self, tag):
        self.table_names[tag] = "{}_train_data".format(tag.name)
        create_table_query = """
        CREATE TABLE IF NOT EXISTS {} (
          id INT AUTO_INCREMENT, 
          text TEXT NOT NULL, 
          x TEXT, 
          y TEXT, 
          PRIMARY KEY (id)
        ) ENGINE = InnoDB
        """.format(self.table_names[tag])
        self._execute_query(create_table_query)

    def add_new_articles(self, tag, texts, x_matrix, y_matrix):
        values = ["('{}', '{}', '{}')".format(t, x, y) for t, x, y in zip(texts, x_matrix, y_matrix)]
        add_article_query = """
        INSERT INTO
          `{}` (`text`, `x`, `y`)
        VALUES
          {};
        """.format(self.table_names[tag], ','.join(values))
        self._execute_query(add_article_query)

    def _execute_query(self, query):
        if self._cursor is None:
            self._cursor = self.connection.cursor()
        try:
            self._cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")