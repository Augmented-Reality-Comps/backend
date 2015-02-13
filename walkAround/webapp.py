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
    parameters = {'latitude':'', 'longitude':'', 'altitude':'', 'yaw':'', 'pitch':'', 'roll':''}


    #sets default values for each field
    parameters['latitude'] = 0
    parameters['longitude'] = 0
    parameters['altitude'] = 0
    parameters['yaw'] = 0
    parameters['pitch'] = 0
    parameters['roll'] = 0


    #sets parameters as they are passed
    if 'latitude' in form:
        parameters['latitude'] = sanitizeUserInput(form['latitude'].value)

    if 'longitude' in form:
        parameters['longitude'] = sanitizeUserInput(form['longitude'].value)

    if 'altitude' in form:
        parameters['altitude'] = sanitizeUserInput(form['altitude'].value)

    if 'yaw' in form:
        parameters['yaw'] = sanitizeUserInput(form['yaw'].value)

    if 'pitch' in form:
        parameters['pitch'] = sanitizeUserInput(form['pitch'].value)

    if 'roll' in form:
        parameters['roll'] = sanitizeUserInput(form['roll'].value)

    return parameters


def printMainPageAsHTML(latitude, longitude, altitude, yaw, pitch, roll, templateFileName):
    '''
    Prints the page as an htmp based off of template.html. There are 9 fields that must be filled
    in template.html they are in the following order:
    dae file path, object location(lat, lon, alt), camera location(lat, lon, alt), camera rotation(pitch, roll, yaw)
    pitch roll and yaw must be in radians
    '''


    file = getObjectsForLocation(latitude, longitude, altitude, yaw, pitch, roll)
    #pulls the latitude longitude altitude from th database.
    #THIS WORKS ONLY FOR 1 OBJECT. Fix when there is time
    object_loc = (file[0][0], file[0][1], file[0][2])


    #read the template file
    f = open(templateFileName)
    templateText = f.read()
    f.close()

    #put the correct data into the template file
    #angles must be in radians
    outputText = templateText % (file[0][3], object_loc[0], object_loc[1], object_loc[2], latitude, longitude, altitude, pitch, roll, yaw)

    #displays the page
    print 'Content-type: text/html\r\n\r\n',
    print outputText

    #creates a log for debugging
    makeLog(latitude, longitude, altitude, yaw, pitch, roll, object_loc)


def makeLog(latitude, longitude, altitude, yaw, pitch, roll, object_loc):
    '''
    Makes a log in log.txt. Every time a http request is sent, log the current time, object position,
    camera position, and camera orientation
    '''
    log = time.strftime("Month:%m Day:%d Hour:%H Min:%M Sec:%S\n")
    log += "object location: " + str(object_loc)
    log += "\nCamera location: " + latitude + ", " + altitude + ", " + longitude
    log += "\nCamera position: " + yaw + ", " + pitch + ", " + roll + "\n-------------------------------------------------\n"

    f = open('log.txt', 'a')
    f.write(log)
    f.close();


def getObjectsForLocation(latitude, longitude, altitude, yaw, pitch, roll):
    '''
    Gets all the relevant objects for the given location. Currently this returns everything in the database.
    '''
    #creates a connection to the database
    db = DataSource()

    #make the query
    return db.getData('Select * from demo;')

def main():
    parameters = getCGIParameters()
    printMainPageAsHTML(parameters['latitude'], parameters['longitude'], parameters['altitude'],  parameters['yaw'], parameters['pitch'], parameters['roll'], 'template.html')

if __name__ == '__main__':
    main()
