from django.db import connection, transaction

def search(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    raw = cursor.fetchall()
    return raw

def modify(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    transaction.commit_unless_managed()
