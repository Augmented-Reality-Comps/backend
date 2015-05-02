#!/usr/bin/python

import cgi
import time
import random
from datasource import DataSource

def sanitizeUserInput(s):
    ''' does a basic sanitation on input
    '''
    charsToRemove = ';,\\/:\'"<>@'
    for ch in charsToRemove:
        s = s.replace(ch, '')
    return s

def getCGIParameters():
    ''' This function grabs the HTTP parameters we care about, sanitizes the
        user input. We expect latitude, longitude, altitude, yaw, pitch, roll.
    '''
    form = cgi.FieldStorage()
    parameters = {'latitude':'', 'longitude':'', 'altitude':''}

    #sets default values for each field
    parameters['latitude'] = 0
    parameters['longitude'] = 0
    parameters['altitude'] = 0

    #sets parameters as they are passed
    if 'latitude' in form:
        parameters['latitude'] = sanitizeUserInput(form['latitude'].value)

    if 'longitude' in form:
        parameters['longitude'] = sanitizeUserInput(form['longitude'].value)

    if 'altitude' in form:
        parameters['altitude'] = sanitizeUserInput(form['altitude'].value)

    return parameters

def printMainPageAsHTML(latitude, longitude, altitude, templateFileName):
    '''
    Prints the page as an htmp based off of template.html. There are 9 fields that must be filled
    in template.html they are in the following order:
    dae file path, object location(lat, lon, alt), camera location(lat, lon, alt), camera rotation(pitch, roll, yaw)
    pitch roll and yaw must be in radians
    '''

    # file = getObjectsForLocation(latitude, longitude, altitude, yaw, pitch, roll)
    objectList = getAllObjects()

    #read the template file
    f = open(templateFileName)
    templateText = f.read()
    f.close()

    #put the correct data into the template file
    #angles must be in radians
    outputText = templateText % (objectList)

    #displays the page
    print 'Content-type: text/html\r\n\r\n',
    print outputText

def getAllObjects():
    '''
    Gets all the relevant objects for the given location. Currently this returns everything in the database.
    '''
    #make the query
    return [{'latitude': objectTuple[0],
            'longitude': objectTuple[1],
            'altitude': objectTuple[2],
            'filename': objectTuple[3],
            'x_rot': objectTuple[4],
            'y_rot': objectTuple[5],
            'z_rot': objectTuple[6]
        } for objectTuple in DataSource().getData('Select * from object_table;')]

def sendTestObjects(number, lat, lon, alt):
    DataSource().sendQueries([("insert into object_table values(%s, %s, %s, 'objects/teapot3.dae', 1,0,0);" % (coord[0], coord[1], coord[2])) for coord in [[lat + random.randint(-50, 50), lon + random.randint(-50, 50), alt + random.randint(-20, 20)] for i in range(number)]])

def removeTestObjects():
    DataSource().sendQueries(['delete from object_table where x_rot = 1;'])

def main():
    parameters = getCGIParameters()
    printMainPageAsHTML(parameters['latitude'], parameters['longitude'], parameters['altitude'], 'template.html')

if __name__ == '__main__':
    main()
