'''
初期設定が必要なクラスをインスタンスで呼び出します。
MySQLなどはFlask-SQLALCHEMYを使うと良いと思います。
https://qiita.com/shirakiya/items/0114d51e9c189658002e
'''

from models.Databases import HyperDatabase

db = HyperDatabase()


def init_db(app):
    db.init_app(sql_address=app.config['SQL_ADDRESS'])
