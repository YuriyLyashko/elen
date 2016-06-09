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
                self.use_db()
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

    def create_table(self, name_table):
        self.cur.execute('CREATE TABLE {}('
                         'id integer AUTO_INCREMENT PRIMARY KEY, '
                         'user varchar(20) NOT NULL, '
                         'password varchar(20) NOT NULL)'
                         .format(name_table))