'''
クラスを作成します。
'''


class HyperDatabase(object):
    def init_app(self, sql_address):
        if type(sql_address) != str:
            raise TypeError('SQL_ADDRESS is str. Not Type({variable}) => {type}'.format(
                variable=sql_address,
                type=type(sql_address)
            )
            )
        else:
            self.database = sql_address
