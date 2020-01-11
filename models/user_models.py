import sqlite3

DB_NAME = 'rpi.db'


class Schema:
    """
    Provide methods for db management
    """

    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.curs = self.conn.cursor()
        self.create_user_table()
        self.create_otp_table()

    def __del__(self):
        # body of destructor
        self.conn.close()

    def create_user_table(self):
        """
        Init user table
        :return: void
        """
        query = """
        CREATE TABLE IF NOT EXISTS "user" (
        name TEXT NOT NULL, 
        surname TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        api_key TEXT NOT NULL UNIQUE PRIMARY KEY, 
        created_on DATE DEFAULT CURRENT_DATE
        );
        """

        self.curs.execute(query)
        self.conn.commit()

    def create_otp_table(self):
        """
        Init otp codes table
        :return: void
        """
        query = """
        CREATE TABLE IF NOT EXISTS "otp" (
        api_key TEXT NOT NULL UNIQUE PRIMARY KEY, 
        otp_code TEXT NOT NULL,
        otp_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        """
        self.curs.execute(query)
        self.conn.commit()


class UserModel:
    """
    Provide methods for user management in the db
    """

    USER_TABLE_NAME = "user"
    OTP_TABLE_NAME = "otp"

    def __init__(self, db_url=DB_NAME):
        self.conn = sqlite3.connect(db_url)
        self.conn.row_factory = sqlite3.Row
        self.curs = self.conn.cursor()

    def create(self, name, surname, email, api_key):
        """
        Create new user.

        :param name:
        :param surname:
        :param email:
        :param api_key:
        :return: api_key or False
        """
        query = """
                INSERT INTO user(name, surname, email, api_key)
                VALUES (?, ?, ?, ?)
                """

        try:
            self.curs.execute(query, [name, surname, email, api_key])
            self.conn.commit()
            return api_key
        except Exception as e:
            print(e)
            return False

    def create_otp(self, _api_key, _otp_code):
        """
        Store new otp code.
        :param api_key:
        :param otp_code:
        :return: boolean
        """

        query = """
                INSERT OR REPLACE INTO otp(api_key, otp_code)
                VALUES (?, ?)
                """

        try:
            self.curs.execute(query, [_api_key, _otp_code])
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete_otp(self, api_key, otp_code):
        """
        Store new otp code.
        :param api_key:
        :param otp_code:
        :return: boolean
        """

        query = """
                DELETE FROM otp 
                WHERE api_key=? AND otp_code=?
                """
        try:
            self.curs.execute(query, [api_key, otp_code])
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_user(self, email, api_key):
        """
        Find user by:

        :param email:
        :param api_key:
        :returns tuple(email, api_key)
        """

        query = """
                SELECT email, api_key
                FROM user
                WHERE  email=? AND api_key=?
                """

        try:
            res = self.curs.execute(query, (email, api_key)).fetchone()
            self.conn.commit()
            return res[0], res[1]
        except Exception as e:
            print(e)
            return False

    def get_user_with_otp(self, email, api_key, otp):
        """
        Find user by:

        :param email:
        :param api_key:
        :param otp:
        :return: tuple(email, api_key, otp_code)
        """

        query = """ 
                SELECT user.email, user.api_key, otp.otp_code
                FROM user INNER JOIN otp ON otp.api_key = user.api_key
                WHERE user.email=? AND user.api_key=? AND otp.otp_code=?
                AND otp.otp_timestamp >= datetime('now', '-15 minutes')
                """

        try:
            res = self.curs.execute(query, (email, api_key, otp)).fetchone()
            self.conn.commit()
            return res[0], res[1], res[2]
        except Exception as e:
            print(e)
            return False

    def check_api_key(self, api_key):
        """
        Find user by:

        :param api_key:
        :return True | False
        """

        query = """
                        SELECT name
                        FROM user
                        WHERE  api_key=?
                        """

        try:
            res = self.curs.execute(query, (api_key,)).fetchone()
            self.conn.commit()

            if res is not None:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
