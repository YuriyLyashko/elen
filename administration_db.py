import pymysql

class AdminDB:
    _NAME_DB = 'elen_db'
    _NAME_TABLE_USERS = 'users'
    _NAME_TABLE_LOG = 'log'
    _NAME_TABLE_HISTORY = 'history'
    _HOST_DB = 'localhost'
    _USER_DB = 'root'
    _PASSWORD_DB = '123456'

    def __init__(self):
        try:
            self.connect_db()
            print('connected')
        except pymysql.err.InternalError:
            try:
                self.create_db()
                print('1')
                self.use_db()
                print(self._NAME_TABLE_USERS)
                self.create_table(self._NAME_TABLE_USERS)
                print('created')
            except:
                raise ConnectionError

    def create_db(self):
        self.conn = pymysql.connect(host=self._HOST_DB,
                                    user=self._USER_DB,
                                    password=self._PASSWORD_DB)
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE DATABASE {}'.format(self._NAME_DB))

    def use_db(self):
        self.cur.execute('USE {}'.format(self._NAME_DB))

    def connect_db(self):
        self.conn = pymysql.connect(host=self._HOST_DB,
                                    user=self._USER_DB,
                                    password=self._PASSWORD_DB,
                                    db=self._NAME_DB)
        self.cur = self.conn.cursor()

    def create_table(self, name_table):
        self.cur.execute('CREATE TABLE {}('
                         'id integer AUTO_INCREMENT PRIMARY KEY, '
                         'user varchar(20) NOT NULL, '
                         'password varchar(40) NOT NULL)'.format(name_table)
                         )

    def create_user(self, user_name, user_password):
        self.cur.execute('INSERT INTO users(user, password) VALUES(%s, %s)', (user_name, user_password))
        self.conn.commit()

    def check_user(self, user_name):
        self.cur.execute('SELECT user FROM users WHERE user="{}"'.format(user_name))
        return self.cur.fetchall()

    def check_password(self, user_name, user_password):
        self.cur.execute('SELECT password FROM users WHERE user="{}"'.format(user_name))
        password_from_db = self.cur.fetchall()
        return user_password == password_from_db

    def close_connection(self):
        self.conn.close()
