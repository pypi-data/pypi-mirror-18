# mssql_cli
A way to run queries and execute commands against an MSSQL database.


## Code Example
```python
import datetime  # used for an example below
from mssql_cli import DBRead, DBWrite

read_connection = DBRead(host='some_host', user='some_user', password='some_password', database='some_database')
write_connection = DBWrite(host='some_host', user='some_user', password='some_password', database='some_database')

results = read_connection.query("SELECT * FROM some_table")
more_results = write_connection.query("SELECT * FROM some_table")

write_connection.execute("INSERT INTO [some_table] ([name], [phone_number], [time]) VALUES ('Prince', '111-111-1111', '1999-12-31 23:59:59')")

# insert_results() will create an insert statement based off of a table name and kwargs and execute the resulting statement.
write_connection.insert_results(table='some_table', name='Prince', phone_number='111-111-1111', time=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

read_connection.close()
write_connection.close()
```

## Motivation
This library exists to run queries and execute commands against an MSSQL database.

## Installation
This package requires pymssql, which has a dependency on FreeTDS. Instructions on installing FreeTDS can be found here: http://pymssql.org/en/latest/freetds.html.

pip install mssql_cli

## License
MIT
