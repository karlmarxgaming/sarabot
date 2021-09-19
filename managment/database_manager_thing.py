import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

database = sqlite3.connect("real_database.db3")
"""
real
""" 
database.row_factory = dict_factory

