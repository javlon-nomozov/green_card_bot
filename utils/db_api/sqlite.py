import sqlite3

class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    # createe

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255),
            language varchar(5),
            role varchar(15) DEFAULT "user" NOT NULL,
            PRIMARY KEY (id)
            );
        """
        self.execute(sql, commit=True)

    def create_table_chat(self):
        sql = """
            CREATE TABLE chat (
            id_link varchar(250),
            must_subscribe varchar(15),
            description varchar(150) NOT NULL,
            PRIMARY KEY (id_link)
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    # insertt

    def add_user(self, id: int, name: str, email: str = None, language: str = 'uz'):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(id, Name, email, language) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, email, language), commit=True)


    def add_chat(self, id_link: str, must_subscribe: str, description: str):
        sql = """
        INSERT INTO chat(id_link, must_subscribe, description) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id_link, must_subscribe, description), commit=True)


    # readd

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_users_by_role(self, role: str):
        sql = f"""
        SELECT id FROM Users where role='{role}'
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT (*) FROM Users;", fetchone=True)


    def select_all_chat(self):
        sql = """
        SELECT * FROM chat;
        """
        return self.execute(sql, fetchall=True)

    def select_must_sub_chat(self):
        sql = """
                SELECT * FROM chat where must_subscribe='true';
                """
        return self.execute(sql, fetchall=True)

    # updatee

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def update_user_role(self, role, id):
        # admin/ staff/ user

        sql = f"""
        UPDATE Users SET role=? WHERE id=?
        """
        return self.execute(sql, parameters=(role, id), commit=True)


    def update_user_language(self, lang, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET language=? WHERE id=?
        """
        return self.execute(sql, parameters=(lang, id), commit=True)


    # deletee

    def delete_user(self, id):
        self.execute(f"DELETE FROM Users WHERE id = '{id}'", commit=True)

    def delete_chat(self, id_link):
        self.execute(f"DELETE FROM chat WHERE id_link='{id_link}'", commit=True)

DEBUG = True
def logger(statement):
    if DEBUG:
        print(f"""
_______________
Executing:
{statement}
_______________
""".replace('\n', '').replace('    ', ''))
