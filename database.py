import mysql.connector # type: ignore

database = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='python_bd'
)

