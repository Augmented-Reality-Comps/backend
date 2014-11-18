#!/usr/bin/python
''' webapp.py

    By Andrew Elenbogen and Aidan Carroll  4/21/22
    Based on Code by Jeff Ondich, 4/6/12

    A sample showing a couple simple-minded techniques for presenting a web form,
    sanitizing user input, and displaying source code.

    This page takes user input via the search box and diplays results of the search.
'''

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
        in a dictionary indexed by the parameter names (searchTerm in this case).
    '''
    form = cgi.FieldStorage()
    parameters = {'searchTerm':'',  'showsource':''}

    if 'searchTerm' in form:
        parameters['searchTerm'] = sanitizeUserInput(form['searchTerm'].value)

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

def printMainPageAsHTML(searchTerm, templateFileName):
    ''' Prints to standard output the main page for this web application, based on
        the specified template file and parameters. The content of the page is
        preceded by a "Content-type: text/html" HTTP header.
        
        Note that this function is quite awkward, since it assumes knowledge of the contents
        of the template (e.g. that the template contains four %s directives), etc. But
        it gives you a hint of the ways you might separate visual display details (i.e. the
        particulars of the HTML found in the template file) from computational results
        (in this case, the strings built up out of searchTerm). 
    '''
    
    outputText = ''

    try:
        f = open(templateFileName)
        templateText = f.read()
        f.close()
        datas=DataSource()
        print searchTerm,datas.getData()
        outputText = templateText % ("stuff");
    except Exception, e:
        outputText = 'Cannot read template file "%s".' % (templateFileName)

    print 'Content-type: text/html\r\n\r\n',
    print outputText

def main():
    #parameters = getCGIParameters()
    ds = DataSource()
    #print ds.getData()
    print "Content-type: text/html\r\n\r\n<html> <head>"
    print ds.getData()
    print " </head> </html>"
        
if __name__ == '__main__':
    main()


