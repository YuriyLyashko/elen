import pymysql

class AdminDB:
    _NAME_DB = 'elen_db'
    _NAME_TABLE_USERS = 'users'
    _NAME_TABLE_LOG = 'log'
    _NAME_TABLE_HISTORY = 'history'
    _NAME_TABLE_TARIFFS = 'tariffs'
    _HOST_DB = 'localhost'
    _USER_DB = 'root'
    _PASSWORD_DB = '123456'

    STARTING_TARIFFS = 'starting tariffs', '01.09.2015', 100, 300, 0.5, 1.0, 2.0

    def __init__(self):
        try:
            self.connect_db()
        except pymysql.err.InternalError:
            try:
                self.create_db()
                self.use_db()
                self.create_table(self._NAME_TABLE_USERS)
                self.create_table('{}'.format(self._NAME_TABLE_TARIFFS),
                                  'date_now',
                                  'limit_tariff_1', 'limit_tariff_2', 'tariff_1', 'tariff_2', 'tariff_3'
                                  )
                self.write_into('{}'.format(self._NAME_TABLE_TARIFFS),
                                self.STARTING_TARIFFS)
            except:
                raise ConnectionError

    def create_db(self):
        print('create_db', self._NAME_DB)
        self.conn = pymysql.connect(host=self._HOST_DB,
                                    user=self._USER_DB,
                                    password=self._PASSWORD_DB)
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE DATABASE {}'.format(self._NAME_DB))

    def use_db(self):
        print('use_db', self._NAME_DB)
        self.cur.execute('USE {}'.format(self._NAME_DB))

    def connect_db(self):
        print('connect_db', self._NAME_DB)
        self.conn = pymysql.connect(host=self._HOST_DB,
                                    user=self._USER_DB,
                                    password=self._PASSWORD_DB,
                                    db=self._NAME_DB,
                                    use_unicode=True,
                                    charset="utf8"
                                    )
        self.cur = self.conn.cursor()

    def create_table(self, name_table, *args, **kwargs):
        print('create_table', name_table)
        if name_table == self._NAME_TABLE_USERS:
            self.cur.execute('CREATE TABLE {}('
                             'id integer AUTO_INCREMENT PRIMARY KEY, '
                             'user varchar(20) NOT NULL, '
                             'password varchar(40) NOT NULL)'
                             .format(name_table)
                             )
        elif name_table == self._NAME_TABLE_TARIFFS:
            self.cur.execute('CREATE TABLE {}('
                             'user varchar(20) NOT NULL PRIMARY KEY, '
                             .format(name_table)
                             +
                             str([arg + ' varchar(20) NOT NULL' for arg in args])[1:-1].replace("'", "")
                             +
                             ')'
                             )
        elif self._NAME_TABLE_HISTORY or self._NAME_TABLE_LOG in name_table:
            self.cur.execute('CREATE TABLE {}('
                             .format(name_table)
                             +
                             str([arg + ' varchar(20) NOT NULL' for arg in args])[1:-1].replace("'", "")
                             +
                             ')'
                             )

    def create_user(self, user_name, user_password):
        print('create_user', user_name)
        self.cur.execute('INSERT INTO users(user, password) VALUES(%s, %s)', (user_name, user_password))
        self.conn.commit()

    def check_user(self, user_name):
        print('check_user', user_name)
        self.cur.execute('SELECT user FROM users WHERE user="{}"'.format(user_name))
        return self.cur.fetchall()

    def write_into(self, table, info):
        print('write_into', table, info)
        self.cur.execute('INSERT INTO {} VALUES{}'.format(table, info))
        self.conn.commit()

    def update(self, table, info):
        print('update', table, info)
        self.cur.execute('REPLACE INTO {} '
                         'VALUES {}'
                         .format(table, info)
                         )
        self.conn.commit()

    def check_password(self, user_name, user_password):
        print('check_password', user_name)
        self.cur.execute('SELECT password '
                         'FROM users '
                         'WHERE user="{}"'
                         .format(user_name)
                         )
        password_from_db = self.cur.fetchone()[0]
        return user_password == password_from_db

    def read_saved_tariffs(self, user_name):
        print('read_saved_tariffs', user_name)
        self.cur.execute('SELECT * '
                         'FROM tariffs '
                         'WHERE user="{}"'
                         .format(user_name)
                         )
        tariffs_from_db = self.cur.fetchone()[1:]
        return tariffs_from_db

    def close_connection(self):
        print('close_connection')
        self.conn.close()
