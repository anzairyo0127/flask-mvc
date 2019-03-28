'''
controllerが呼び出すview用の関数です。
'''

from flask import render_template
from model_instance.database import db


def index_page():
    return render_template('posts/index.html', db=db)


def argstest_page(post):
    return post + 'hoge'
