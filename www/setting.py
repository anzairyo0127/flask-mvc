'''
app.config[***]の部分を設定します。
InitConfを継承している点をよく見ていてください。

SQL_TABLE = 'hogehoge_table'とすると
app.config[SQL_TABLE]は'hogehoge_table'になります。

また、SECRET_KEYを設定すればapp.secret_keyの値が決まります。
その他、色々と設定用の値が決められています。
http://flask.pocoo.org/docs/1.0/config/#builtin-configuration-values
'''


class InitConf(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'secretkey'
    SQL_TABLE = 'hogehoge_table'
    SQL_PASSWORD = 'piyopiyo'


class TestMode(InitConf):
    TESTNG = True
    SQL_ADDRESS = ''


class DevMode(InitConf):
    DEBUG = True
    SQL_ADDRESS = 'slave_database'


class ProdMode(InitConf):
    SQL_ADDRESS = 'prod_slave_database'
