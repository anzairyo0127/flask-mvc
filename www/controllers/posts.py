'''
コントローラです。
route('/***')の値を受け取った時、下部の関数を実行します。
returnにviewの関数を実行させています。
'''
from flask import Blueprint, current_app, request, redirect, url_for
from views.posts import index_page, argstest_page

post_ctr = Blueprint('post_ctr', __name__)


@post_ctr.route('/')
def index():
    return index_page()


@post_ctr.route('/a/<post>')
def argstest(post):
    return argstest_page(post)


@post_ctr.route('/redirect')
def redtest():
    return redirect(url_for('post_ctr.index'))
