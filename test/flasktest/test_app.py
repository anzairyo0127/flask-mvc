from factory_app import create_app

app = create_app('test')
client = app.test_client()


def test_config():

    assert app.config['SQL_ADDRESS'] in client.get('/').data.decode('utf8')
