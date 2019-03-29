# 必要なPythonModule

`requirements.txt`に記載されていますので確認してください。

# MVCモデルで開発をするということ
```
Model
View
Controller
```
それぞれの頭文字をとって`MVC`と呼ばれます。

参考[MVCについて]:https://qiita.com/gcyata/items/772b6989f4cdab0bd047

# ディレクトリ構成

```
カレントディレクトリ
│  .gitignore
│  README.md
│  requirements.txt
│
├─test
│  │  conftest.py
│  │
│  ├─flasktest
│  │      test_app.py
│  │
│  └─modeltest
│         test_Databases.py
│
└─www
   │  app.py
   │  factory_app.py
   │  setting.py
   │
   ├─controllers
   │      posts.py
   │      __init__.py
   │
   ├─insance
   │      sample_application.cfg
   │
   ├─models
   │      Databases.py
   │      __init__.py
   │
   ├─model_instance
   │      database.py
   │      __init__.py
   │
   ├─templates
   │  └─posts
   │          index.html
   │
   └─views
           posts.py
           __init__.py
```

# wwwディレクトリ

実行するFlaskWebアプリケーションはこちらに配置します。

## app.py
flaskの実行ファイルになります。

`factory_app.create_app`関数をインポートし、その返り値を変数`app`に代入しています。`create_app`関数はFlaskの実行ファイルに色々な設定を行って返します。その返り値を受け取った`app`が`app.run()`とすることでWebアプリケーションが起動します。

`create_app`関数に環境ステータスである`dev`か`test`か`prod`のいずれかを渡すようにします。

なお、os.getenv()を使って環境変数から取得するようにするのもよいでしょう。

この`app.py`は`create_app`を通して沢山のmoduleにアクセスしています。ルートパスはこの`app.py`を起点としてインポートしてあげてください。

## factory_app.py
Application Factoryの概念は以下のURLに載っています。

http://flask.pocoo.org/docs/1.0/patterns/appfactories/

```
# Flask実行ファイル読込
app = Flask(__name__, instance_relative_config=True)
```

こちらはFlaskのインスタンスを作成している場面です。`instance_relative_config=True`は`cfg`ファイルの置き場所を`instance`ディレクトリに設定するというものです。本来は`cfg`ファイルについて同じディレクトリ内のものを読み込むのですが、この引数を設定することで`instance`ディレクトリ内のものを読み込むように変更することが出来ます。また、`instance_path='/path/to/instance/folder'`という引数に`絶対PATH`を渡してインスタンスディレクトリのパスと名前を変更することも可能です。

参考[インスタンスフォルダ]:http://flask.pocoo.org/docs/1.0/config/#instance-folders

```
# コンフィグ読込
confmode = dict_confmode[config_mode]
app.config.from_object(confmode)
app.config.from_pyfile('application.cfg', silent=True)
```

コンフィグファイルの読込箇所になります。

`app.config.from_object(confmode)`は辞書`dict_confmode`のValueを使って`setting.py`に書き込まれているクラスを読み込んでいます。

`app.config.from_pyfile('application.cfg', silent=True)`はinstanceディレクトリ内の`application.cfg`を読み込みます。センシティブな内容をこちらに入れるようにしてください。なお、`application.cfg`は`.gitignore`に記載しており、GitHub上にはPushされないようにしてあります。

`silent=True`とは、instanceディレクトリ内に`application.cfg`がない場合は、処理を無視するというものになります。

上記二つの設定ファイルにおいて、同じ値が存在する場合は、後で呼ばれたほうが上書きするという性質を忘れないでください。それ以外の値は、そのままapp.configに代入されます。
```
# app.config.from_object(confmode)
A = 1
B = 2
C = 3
# app.config.from_pyfile('application.cfg', silent=True)
C = 4
D = 5
# 最終的な値
app.config['A'] = 1
app.config['B'] = 2
app.config['C'] = 4
app.config['D'] = 5
```

参考[Flask設定ファイルについて]:https://qiita.com/nanakenashi/items/e272ff1aafb3889230bc

```
from controllers.posts import post_ctr
~~~~~~
# コントローラ読込
app.register_blueprint(post_ctr)
```

`from controllers.posts import post_ctr`はMVCのコントローラーに該当するプログラムです。

参考[MVCについて]:https://qiita.com/s_emoto/items/975cc38a3e0de462966a

`app.register_blueprint(post_ctr)`は上記の`post_ctr.py`をコントローラとして読込を行っています。

`app.register_blueprint(post_ctr, url_prefix='/posts')`とように`url_prefix`引数に値を入れると、その文字列がURLのプレフィックスとなります。

参考[prefixとは]:https://wa3.i-3-i.info/word1208.html

```
from model_instance import database
~~~~~~
# モデルインスタンス初期化
database.init_db(app)
```

`from model_instance import database`は初期設定が必要で使いまわしたいクラスがインスタンス化された変数が格納されているPythonプログラムです。

`database.init_db(app)`は`database.py`内のインスタンスに初期設定を行う関数です。（ちょっと難しいかもです。）

`Flask-SQLAlchemy`といったものがこの方式で初期化可能です。

参考[Flask-SQLAlchemy]:https://qiita.com/shirakiya/items/0114d51e9c189658002e

## setting.py
Flaskの設定用プログラムです。

app.config[***]の部分を設定します。InitConfを継承している点をよく見ていてください。

`SQL_TABLE = 'hogehoge_table'`とすると`app.config['SQL_TABLE']`は`'hogehoge_table'`になります。

また、SECRET_KEYを設定すればapp.secret_keyの値が決まります。その他、色々と設定用の値が決められています。

参考[ビルトインコンフィグバリュー]:http://flask.pocoo.org/docs/1.0/config/#builtin-configuration-values

# controllersディレクトリ
MVCモデルのコントローラープログラムを置いておくディレクトリになります。`factory_app.py`の`app.register_blueprint(post_ctr, url_prefix='/posts')`の項目で説明した通り、`URLプレフィックス`単位でコントローラープログラムを変更したいといった場合は、新しいコントローラープログラムを作成し、このディレクトリにおいてください。

## posts.py
これは`posts`コントローラープログラムになります。

```
from flask import Blueprint ...
post_ctr = Blueprint('post_ctr', __name__)
```

これは`port_ctr`変数が`Blueprint`クラスのインスタンスとなっています。以降は`port_ctr`が持つデコレータ`@post_ctr.route`を使ってURLのコントロールを行います。

参考[Blueprintについて]:http://flask.pocoo.org/docs/1.0/blueprints/

```
from views.posts import index_page ...
~~~~~~
@post_ctr.route('/')
def index():
    return index_page()
```
これは`http://IPADDRESS_or_DOMAINNAME/`にアクセスされたときに`index()`関数が実行されるというデコレータになります。`factory_app.py`の項目で`app.register_blueprint(post_ctr, url_prefix='/posts')`としたように`url_prefix='/posts'`と引数を与えていた場合は,`http://IPADDRESS_or_DOMAINNAME/posts/`にアクセスした際に実行されます。

`return index_page()`はimportされている通り、`views`ディレクトリ`posts.py`の`index`関数になります。詳しくは`views`ディレクトリの項目を読んでください。

```
@post_ctr.route('/a/<post>')
def argstest(post):
    return argstest_page(post)
```
これは`http://IPADDRESS_or_DOMAINNAME/a/some_value/`にアクセスされたときに`argstest(post)`関数が実行されるというデコレータになります。`factory_app.py`の項目で`app.register_blueprint(post_ctr, url_prefix='/posts')`としたように`url_prefix='/posts'`と引数を与えていた場合は,`http://IPADDRESS_or_DOMAINNAME/posts/a/some_value/`にアクセスした際に実行されます。

これはurlの個所に`<post>`という値が来ていることをよく見てください。これはURL変数といって、この個所に書き込まれた内容を関数に引き渡すことが出来ます。例では`some_value`という文字列がURL変数`post`に代入されています。

最終的には`argstest('some_value')`として実行されています。

詳しくは参考を見てください。

参考[variable-rules]:http://flask.pocoo.org/docs/1.0/quickstart/#variable-rules

なお、とてもどうでもいい話ですが、`Blueprint`という言葉は`青図`といって元々は建築物の設計図が書かれた用紙が青色だったことが名前の由来のようです。下記URLにも記載の通り`英語のブループリントと言う言葉は今日も多種様な業界で使われている`ということを覚えておくとよいでしょう。(要するにUnrealEngineというゲームを作るフレームワークにもBlueprintっていうモノがあるのでごちゃごちゃにならないように注意してねってことです。)

参考[青図]:https://ja.wikipedia.org/wiki/%E9%9D%92%E5%9B%B3

# instanceディレクトリ
factory_app.pyの説明を読んでください。また、`sample_application.cfg`を元に`application.cfg`を作成してください。

# model_instanceディレクトリ
初期化が必要なインスタンスを宣言しておくプログラムを入れておくディレクトリになります。factory_app.pyにて初期設定を行い、`view`や`model`のプログラムからここを呼び出して使ってあげてください。

## database.py
これは例のためのプログラムであり、実際はなんら動作しません。

```
from models.Databases import HyperDatabase
db = HyperDatabase()
```
これは`models`ディレクトリの`Databases.py`内に宣言された`HyperDatabase`クラスを呼び、そのクラスのインスタンスが`db`となっています。

`app.py`が最初に実行する`factory_app.py`が呼び出されたとき、`factory_app.py`のimport文として`from model_instance import database`と記載があるため、この`db = HyperDatabase()`まで実行されるということを覚えておいてください。

```
def init_db(app):
    db.init_app(sql_address=app.config['SQL_ADDRESS'])
```
これは、`HyperDatabase`のインスタンスである`db`に対し、初期設定をおこなっています。

上記をまとめると、`factory_app.py`が呼び出されただけで`db`インスタンスが作成され、`create_app`関数内で、この`init_db`関数が実行され、`db`に初期設定が反映されるということになります。

そうして、各モデル内で"初期設定が反映された`db`インスタンス"を呼び出すことが可能となっているのです。

あんまり参考にならないかもしれない参考[db.init_appの初期化処理]:https://teratail.com/questions/175199

# modelsディレクトリ
MVCモデルのモデルプログラムを置いておくディレクトリになります。要するにクラスを入れといてください。

## Databases.py
```
class HyperDatabase(object):
    def init_app(self, sql_address):
    ...
```
初期化が必要であれば、初期化用のクラス内関数`init_app`を作っておくとよいでしょう。そうして、`model_instance`で呼び出すようにしてあげてください。

```
def init_app(self, sql_address):
    if type(sql_address) != str:
        raise TypeError(...)
    else:
        self.database = sql_address
```
`init_app`関数の中身は要約するとこうなっています。単純な話、引数が文字列じゃない場合は`TypeError`というエラーを返していて、そうでない場合はインスタンス変数`database`に引数の値を渡しているわけです。

参考[raiseについて]:https://docs.python.org/ja/3/tutorial/errors.html#raising-exceptions

# templatesディレクトリ
テンプレートエンジンが使用するテンプレートとなるhtmlを置く場所になります。

コントローラ単位で複数ディレクトリを作成しております。

参考[テンプレートエンジンとは]:http://lovee7.blog.fc2.com/blog-entry-95.html

## postディレクトリ
コントローラを複数に設定している場合は、コントローラ単位でディレクトリを構築してあげてもよいでしょう。こうしないとプログラムが動かないというわけではないです。もっといい方法があれば変えていきましょう。

## posts.index.html
htmlについては参考を…

参考[htmlについて]:https://udemy.benesse.co.jp/development/web/what-is-html.html

`{{ db.database }}`と記載がある部分に関して、`html`と違った個所になるかと思います。`views`ディレクトリの`posts.py`の以下のコードを見てください。
```
def index_page():
    return render_template('posts/index.html', db=db)
```
`render_template`関数の引数として`db=db`しておりますが、この左側の`db`が`{{ db }}`として,html内で呼び出されます。`hoge=db`とすれば、`{{ hoge }}`としてあげる必要があります。

また、テンプレートエンジン内で`if文`や`for文`も使うことが出来ます。使い方は`{% if %}`と`{% endif %}`といったものなのですが、普段のpythonとはちょっと違うので以下のURLをよく見てください。

参考[Flaskとjinja2]:https://qiita.com/bookun/items/7ae5de21307d101b4759

# viewsディレクトリ
MVCモデルのビュープログラムを置いておくディレクトリになります。主に`controllers`ディレクトリ内の`posts.py`から呼び出されるようにします。

## posts.py
```
from flask import render_template
~~~~~
def index_page():
    return render_template('posts/index.html', ...)
```
`from flask import render_template`は`flask`の`jinja2`というテンプレートエンジンを呼び出しています。

`render_template('posts/index.html')`はテンプレートとなるhtmlファイルのパスを指定しています。

```
from model_instance.database import db
~~~~~
def index_page():
    return render_template(..., db=db)
```
`from model_instance.database import db`は`model_instanceディレクトリ`の項目をよく見てください。要するに初期設定が反映された`db`を使用しています。

`(db=db)`は左辺が、テンプレートエンジン内で使用する変数名となり、右辺がこの`page.py`内にある変数や値になります。左辺は好きな名前を使用できます。`testディレクトリ`項目の`posts.index.html`の項目をよく見てください。

## 細かいけど注意しておいてほしいこと…

`Flask`はテンプレートエンジンである`jinja2`を内蔵してありますが、`jinja2`は`Flask`内蔵のモノと単品のモノがそれぞれ存在するということを覚えておいてください。そのため、`flask`の`jijna2`について何らかの設定を行うときと単品の`jijna2`の設定を行うときと、設定の仕方が若干異なるということを覚えておいてください。

# testディレクトリ

`pytest`を実行するためのディレクトリです。

参考[pytest]:https://qiita.com/everylittle/items/1a2748e443d8282c94b2

`pytest`を実行するには、このディレクトリの最上部か`test`ディレクトで、CLIにて`pytest`と打つか`python -m pytest`と打ちましょう。

## conftest.py

pytestが呼ばれたときに一番最初に読み込まれるファイルです。

```
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(
    os.path.abspath(__file__)) + "/../www/"))
```

これは`pytest`を実行するディレクトリを設定しています。このようにすることで、`www`ディレクトリは、このテストプログラムのことを気にせずにディレクトリを配置出来たり、ディレクトリの読込みが出来ます。

参考[pytestのPATHについて]:https://www.magata.net/memo/index.php?pytest%C6%FE%CC%E7

## flasktest.test_app.py
flaskアプリのテストを行います。`app.test_client()`等を使ったテストが主になります。

参考[app.test_client()について]:http://momijiame.tumblr.com/post/39324429279/python-%E3%81%AE-flask-%E3%81%A7%E4%BD%9C%E3%81%A3%E3%81%9F%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%82%92%E3%83%86%E3%82%B9%E3%83%88%E3%81%99%E3%82%8B

## modeltest.test_Databases.py
Modelのテストを行います。自作のモデルを呼び出すようにします。パスは`www`が起点です。

参考[pytestについて]:https://dev.classmethod.jp/server-side/python/pytest-getting-started/
