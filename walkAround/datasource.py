import psycopg2


class DataSource:
  def __init__(self):
    pass

  def getData(self, query):
    '''
    this is the actual query to the database. every function that wants information
    from the database MUST call this function
    '''
    # Login to the database
    connection = self.login()

    # Query the database
    try:
      cursor = connection.cursor()
      cursor.execute(query)
      return cursor.fetchall()

    except Exception, e:
      print 'Cursor error', e
      connection.close()
      exit()

    connection.close()

  def sendQueries(self, queries):
    '''
    Execute a list of queries
    '''
    connection = self.login()

    # Query the database
    try:
      cursor = connection.cursor()
      for query in queries:
        cursor.execute(query)

    except Exception, e:
      print 'Cursor error', e
      connection.close()
      exit()
    connection.commit()
    connection.close()

  def login(self):
    # Login to the database
    database = 'comps'
    user = 'comps'
    password='jeffcomps#1'
    try:
      connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception, e:
      print 'Connection error: ', e
      exit()
    return connection
