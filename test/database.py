'''
    psycopg2-test.py
    Jeff Ondich, 1 Oct 2013
    Modified by Amy Csizmar Dalal, 17 April 2014

    This is a short example of how to access a PostgreSQL database in Python.
'''

import psycopg2
import getpass

# Get the database login info. Obviously you'll replace the database and user values with your own username.
database = 'yamamotn'
user = 'yamamotn'
# This next line will prompt you for your password when you connect to the database.
password = getpass.getpass()

# Login to the database
try:
    connection = psycopg2.connect(database=database, user=user, password=password)
except Exception, e:
    print 'Connection error: ', e
    exit()

# Query the database
try:
    cursor = connection.cursor()
    query = "SELECT id FROM words WHERE id BETWEEN 'zygotes' AND 'zz'"
    cursor.execute(query)
    for row in cursor.fetchall():
        print row

    # An alternative to "for row in cursor.fetchall()" is "for row in cursor". The former
    # brings all the data into memory in your program, while the latter brings data in
    # small pieces (one row at a time, I think, but I haven't verified it yet).

except Exception, e:
    print 'Cursor error', e
    connection.close()
    exit()

connection.close()
