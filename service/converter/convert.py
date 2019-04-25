import config.constant.my_sql.const as mysqlc


class Converter:
    @classmethod
    def order_to_string(cls, order):
        return "'%s'" % "', '".join([str(field) for field in order.__dict__.values()])

    @classmethod
    def order_string_to_query(cls, order_string):
        return mysqlc.MySQLConstant.INSERT % order_string
