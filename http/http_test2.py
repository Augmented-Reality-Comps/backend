#!/usr/bin/python

import cgi
from datasource import DataSource

def sanitizeUserInput(s):
    ''' There are better ways to sanitize input than this, but this is a very
        simple example of the kind of thing you can do to protect your system
        from malicious user input. Unfortunately, this example turns "O'Neill"
        into "ONeill", among other things.
    '''
    charsToRemove = ';,\\/:\'"<>@'
    for ch in charsToRemove:
        s = s.replace(ch, '')
    return s

def getCGIParameters():
    ''' This function grabs the HTTP parameters we care about, sanitizes the
        user input, provides default values for each parameter is no parameter
        is provided by the incoming request, and returns the resulting values
        in a dictionary indexed by the parameter names ('animal' and 'badanimal'
        in this case).
    '''
    form = cgi.FieldStorage()
    parameters = {'lat':'', 'long':'', 'alt':'', 'dis':''}

    if 'lat' in form:
        parameters['lat'] = sanitizeUserInput(form['lat'].value)

    if 'long' in form:
        parameters['long'] = sanitizeUserInput(form['long'].value)

    if 'alt' in form:
        parameters['alt'] = sanitizeUserInput(form['alt'].value)

    if 'dis' in form:
        parameters['dis'] = sanitizeUserInput(form['dis'].value)

    return parameters

def printFileAsPlainText(fileName):
    ''' Prints to standard output the contents of the specified file, preceded
        by a "Content-type: text/plain" HTTP header.
    '''
    text = ''
    try:
        f = open(fileName)
        text = f.read()
        f.close()
    except Exception, e:
        pass

    print 'Content-type: text/plain\r\n\r\n',
    print text

def printMainPageAsHTML(lat, long, alt, dis, templateFileName):
    ''' Prints to standard output the main page for this web application, based on
        the specified template file and parameters. The content of the page is
        preceded by a "Content-type: text/html" HTTP header.
        
        Note that this function is quite awkward, since it assumes knowledge of the contents
        of the template (e.g. that the template contains four %s directives), etc. But
        it gives you a hint of the ways you might separate visual display details (i.e. the
        particulars of the HTML found in the template file) from computational results
        (in this case, the strings built up out of animal and badAnimal). 
    '''
    try:
        db = DataSource()
        file = db.getData(getQuery(lat, long, alt, dis))[0][0]
        report = str(file)

        #show what we pull from database

        outputText = ''
        f = open(templateFileName)
        templateText = f.read()
        f.close()
        outputText = templateText % (report)
    except IndexError, e:
        outputText = 'Cannot read template file or there is no shape at that location "%s".' % (templateFileName)
        
    except Exception, e:
        outputText = 'Cannot read template file or there is no shape at that location "%s".' % (templateFileName)
       

    print 'Content-type: text/html\r\n\r\n',
    print outputText

def getQuery(lat, long, alt, dis):
    lat = int(lat)
    long = int(long)
    alt = int(alt)
    dis = int(dis)
    
    query = 'Select file '
    query += 'from test4 '
    query += 'where lat < %i and lat > %i ' % (lat + dis, lat - dis)
    query += 'and long < %i and long > %i ' % (long + dis, long - dis)
    query += 'and alt < %i and alt > %i;' % (alt + dis, alt - dis)
    return query

def main():
    parameters = getCGIParameters()
    printMainPageAsHTML(parameters['lat'], parameters['long'], parameters['alt'], parameters['dis'], 'teapotPage.html')
    
if __name__ == '__main__':
    main()



