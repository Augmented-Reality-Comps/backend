#!/usr/bin/python
''' index.py

    Jeff Ondich, 4/6/12
    Modified by Emily Shack and Naomi Yamamoto

    The program does one of two things, depending on its CGI parameters.

    1. Display the blank form if there is no input text, followed
       by links to the source files.

    2. Display the blank form plus the input text if something has been input, 
       followed by links to the source files.  
'''

import cgi
import datasource

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
    '''
    This function grabs the HTTP parameters we care about, sanitizes the
        user input, provides default values for each parameter is no parameter
        is provided by the incoming request, and returns the resulting values
        in a dictionary indexed by the parameter name ('searchText' in this case).
    '''
    form = cgi.FieldStorage()
    parameters = {'searchText':'', 'checkbox':0, 'showSource':''}

    if 'searchText' in form:
        parameters['searchText'] = sanitizeUserInput(form['searchText'].value)

    if 'checkbox' in form:
        parameters['checkbox'] = 1
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

def printMainPageAsHTML(searchText, checkbox, templateFileName):
    ''' Prints to standard output the main page for this web application, based on
        the specified template file and parameters. The content of the page is
        preceded by a "Content-type: text/html" HTTP header.
        
        Note that this function is quite awkward, since it assumes knowledge of the contents
        of the template (e.g. that the template contains four %s directives), etc. But
        it gives you a hint of the ways you might separate visual display details (i.e. the
        particulars of the HTML found in the template file) from computational results. 
    '''
    tempReport = ''
    wordList = datasource.performSearch(checkbox, searchText)
    tempReport = wordList
    links = '<p><a href="showsource.py?source=index.py">index.py source</a></p>\n'
    links += '<p><a href="showsource.py?source=%s">%s source</a></p>\n' % (templateFileName, templateFileName)
    links += '<p><a href="showsource.py?source=datasource.py">datasource.py source</a></p>\n'
    links += '<p><a href="showsource.py?source=showsource.py">the script we use for showing source</a></p>\n'
    links += '<p><a href="showsource.py?source=readme.txt">README</a></p>\n'

    outputText = ''
    try:
        f = open(templateFileName)
        templateText = f.read()
        f.close()
        outputText = templateText % (searchText, checkbox, tempReport, links)
    except Exception, e:
        outputText = 'Cannot read template file "%s".' % (templateFileName)

    print 'Content-type: text/html\r\n\r\n',
    print outputText

def main():
    parameters = getCGIParameters()
    printMainPageAsHTML(parameters['searchText'], parameters['checkbox'], 'template.html')
        
if __name__ == '__main__':
    main()



