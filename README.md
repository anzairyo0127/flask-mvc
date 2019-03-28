# 必要なPythonModule

`requirements.txt`に記載されていますので確認してください。

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
│          test_Databases.py
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
    │      application.cfg
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

こちらはFlaskのインスタンスを作成している場面です。`instance_relative_config=True`は`cfg`ファイルの置き場所を`instance`ディレクトリに設定するというものです。本来は`cfg`ファイルについて同じディレクトリ内のものを読み込むのですが、設定で変更しているわけです。

```
# コンフィグ読込
confmode = dict_confmode[config_mode]
app.config.from_object(confmode)
app.config.from_pyfile('application.cfg', silent=True)
```

コンフィグファイルの読込箇所になります。

`app.config.from_object(confmode)`は辞書`dict_confmode`のValueを使って`setting.py`に書き込まれているクラスを読み込んでいます。

`app.config.from_pyfile('application.cfg', silent=True)`はinstanceディレクトリ内の`application.cfg`を読み込みます。センシティブな内容をこちらに入れるようにしてください。`silent=True`はinstanceディレクトリ内に`application.cfg`がない場合は無視するというものになります。(Errorを吐かないということ)

上記二つの設定は後で呼ばれたほうが上書きするという性質を忘れないでください。

参考[Flask設定ファイルについて]:https://qiita.com/nanakenashi/items/e272ff1aafb3889230bc

```
from controllers.posts import post_ctr
~~~~~~
# コントローラ読込
app.register_blueprint(post_ctr)
```

`from controllers.posts import post_ctr`はMVCに該当するコントローラーに該当するPythonプログラムです。

参考[MVCについて]:https://qiita.com/s_emoto/items/975cc38a3e0de462966a

`app.register_blueprint(post_ctr)`は上記の`post_ctr.py`をコントローラとして読込を行っています。

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

SQL_TABLE = 'hogehoge_table'とするとapp.config[SQL_TABLE]は'hogehoge_table'になります。

また、SECRET_KEYを設定すればapp.secret_keyの値が決まります。その他、色々と設定用の値が決められています。

参考[ビルトインコンフィグバリュー]:http://flask.pocoo.org/docs/1.0/config/#builtin-configuration-values

# controllersディレクトリ
MVCモデルのコントローラープログラムを置いておくディレクトリになります。

## posts.py
TODO

# instanceディレクトリ
factory_app.pyの説明を読んでください。また、`sample_application.cfg`を元に`application.cfg`を作成してください。

# model_instanceディレクトリ
factory_app.pyの説明を読んでください。

# modelsディレクトリ
MVCモデルのモデルプログラムを置いておくディレクトリになります。

## Databases.py
TODO

# templatesディレクトリ
テンプレートエンジンが使用するテンプレートとなるhtmlを置く場所になります。

コントローラ単位で複数ディレクトリを作成しております。

参考[テンプレートエンジンとは]:http://lovee7.blog.fc2.com/blog-entry-95.html

## posts.index.html
TODO

# viewsディレクトリ
MVCモデルのビュープログラムを置いておくディレクトリになります。

## posts.py
TODO



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

これは`pytest`を実行するディレクトリを設定しています。このようにすることで、`www`ディレクトリはテストのことを気にせずにディレクトリ配置、ディレクトリ読込が出来ます。

## flasktest.test_app.py
flaskアプリのテストを行います。`app.test_client()`等を使ったテストが主になります。

参考[app.test_client()について]:http://momijiame.tumblr.com/post/39324429279/python-%E3%81%AE-flask-%E3%81%A7%E4%BD%9C%E3%81%A3%E3%81%9F%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%82%92%E3%83%86%E3%82%B9%E3%83%88%E3%81%99%E3%82%8B

## modeltest.test_Databases.py
Modelのテストを行います。自作のモデルを呼び出すようにします。パスは`www`が起点です。

参考[pytestについて]:https://dev.classmethod.jp/server-side/python/pytest-getting-started/
