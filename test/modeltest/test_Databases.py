import pytest

from models.Databases import HyperDatabase


def test_HyperDatabase():
    db1 = HyperDatabase()
    db2 = HyperDatabase()
    db3 = HyperDatabase()
    db4 = HyperDatabase()
    db1.init_app('127.0.0.1')
    db2.init_app('192.168.1.1')
    db3.init_app('localhost')
    db4.init_app('master_database')
    assert '127.0.0.1' == db1.database
    assert '192.168.1.1' == db2.database
    assert 'localhost' == db3.database
    assert 'master_database' == db4.database
    with pytest.raises(TypeError):
        db1.init_app(1)
        db1.init_app(['127.0.0.1'])
        db1.init_app({'localhost'})
        db1.init_app(('master_database'))
