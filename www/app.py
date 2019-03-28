'''
Flaskを実行するプログラム。
factory_appから設定を引き継いで実行されます。
'''
import os

from factory_app import create_app


app = create_app('test')  # chose test, dev, pro

if __name__ == '__main__':
    app.run()
