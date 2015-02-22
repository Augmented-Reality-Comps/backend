#!/usr/bin/python

import cgi
import time
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
    #pulls the latitude longitude altitude from th database.
    #THIS WORKS ONLY FOR 1 OBJECT. Fix when there is time
    # object_loc = (file[0][0], file[0][1], file[0][2])

    #read the template file
    f = open(templateFileName)
    templateText = f.read()
    f.close()

    #put the correct data into the template file
    #angles must be in radians
    outputText = templateText % (objectList)
    # outputText = templateText % (file[0][3], object_loc[0], object_loc[1], object_loc[2], latitude, longitude, altitude, pitch, roll, yaw)

    #displays the page
    print 'Content-type: text/html\r\n\r\n',
    print outputText

# def getObjectsForLocation(latitude, longitude, altitude, yaw, pitch, roll):
def getAllObjects():
    '''
    Gets all the relevant objects for the given location. Currently this returns everything in the database.
    '''
    #creates a connection to the database
    db = DataSource()

    #make the query
    objectListFromDB = db.getData('Select * from demo;')

    objectListToReturn = []
    for objectTuple in objectListFromDB:
        objectItem = {}
        objectItem['latitude'] = objectTuple[0]
        objectItem['longitude'] = objectTuple[1]
        objectItem['altitude'] = objectTuple[2]
        objectItem['filename'] = objectTuple[3]
        objectListToReturn.append(objectItem)

    return objectListToReturn

def main():
    parameters = getCGIParameters()
    printMainPageAsHTML(parameters['latitude'], parameters['longitude'], parameters['altitude'], 'template.html')

if __name__ == '__main__':
    main()
