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
    database = 'comps'
    user = 'comps'
    password='jeffcomps#1'
    try:
      connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception, e:
      print 'Connection error: ', e
      exit()

    # Query the database
    try:
      cursor = connection.cursor()
      cursor.execute(query)
      return cursor.fetchall()
      

    # An alternative to "for row in cursor.fetchall()" is "for row in cursor". The former
    # brings all the data into memory in your program, while the latter brings data in
    # small pieces (one row at a time, I think, but I haven't verified it yet).

    except Exception, e:
      print 'Cursor error', e
      connection.close()
      exit()

    connection.close()

 
  def sanitizeInput(self, input):
    '''
    Takes an input string and converts it to a usable form by removing extraneous spaces and similiar.
    '''
    return [] #A String type object

def main():
    ds = DataSource()
    print ds.getData()

#main()
        
