import pymssql


class DBRead(object):
    # Database Read Class
    # __init__:     initializes connection to database using
    #               (host, user, password, database)
    # query:        queries statement and returns results
    # close:        closes MS SQL connection (IMPORTANT)

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = pymssql.connect(host, user, password, database)
        self.cursor = self.connection.cursor()

    def query(self, statement):
        self.cursor.execute(statement)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()


class DBWrite(DBRead):
    # Database Write Class - Inherits from DBRead
    # execute:      executes statement, commits changes,
    #               and returns results of statement

    def execute(self, statement):
        self.cursor.execute(statement)
        self.connection.commit()

    # properly format keys for SQL insert
    def key_list(self, **kwargs):
        key_list = ""

        for key, value in kwargs.items():
            if not key_list:
                key_list = "[%s]" % (key)
            else:
                key_list = "%s, [%s]" % (key_list, key)

        return key_list

    # properly format values for SQL insert
    def value_list(self, **kwargs):
        value_list = None

        for key, value in kwargs.items():
            if value_list is None:
                if value is None:
                    value_list = "NULL"
                else:
                    value_list = "\'%s\'" % (value)
            else:
                if value is None:
                    value_list = "%s, NULL" % (value_list)
                else:
                    value_list = "%s, \'%s\'" % (value_list, value)

        return value_list

    def null_to_false(self, value):
        if value is None:
            return 0
        else:
            return value

    def true_false_to_int(self, value):
        if value:
            return 1
        else:
            return 0

    def insert_results(self, table, **kwargs):
        insert_statement = "INSERT INTO [%s] (%s) VALUES (%s)" % (table, self.key_list(**kwargs), self.value_list(**kwargs))
        self.execute(insert_statement)
        return insert_statement
