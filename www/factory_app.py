'''
Flaskの設定を行います。
'''

from flask import Flask
from controllers.posts import post_ctr
from model_instance import database

dict_confmode = {
    'test': 'setting.TestMode',
    'dev': 'setting.DevMode',
    'pro': 'setting.ProdMode'
}


def create_app(config_mode='test'):
    # Flask実行ファイル読込
    app = Flask(__name__, instance_relative_config=True)
    # コンフィグ読込
    confmode = dict_confmode[config_mode]
    app.config.from_object(confmode)
    app.config.from_pyfile('application.cfg', silent=True)
    # コントローラ読込
    app.register_blueprint(post_ctr)
    # モデルインスタンス初期化
    database.init_db(app)
    return app
