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

    file = getObjectsForLocation(latitude, longitude, altitude, yaw, pitch, roll)
    #pulls the latitude longitude altitude from th database.
    #THIS WORKS ONLY FOR 1 OBJECT. MUST FIX SOON
    object_loc = (file[0][0], file[0][1], file[0][2])


    #read the template file
    f = open(templateFileName)
    templateText = f.read()
    f.close()

    #put the correct data into the template file
    outputText = templateText % ('teapot.dae', object_loc[0], object_loc[1], object_loc[2], longitude, latitude, altitude, pitch, roll, yaw)

    #displays the page
    print 'Content-type: text/html\r\n\r\n',
    print outputText

    #creates a log for debugging
    makeLog(latitude, longitude, altitude, yaw, pitch, roll, object_loc)


def makeLog(latitude, longitude, altitude, yaw, pitch, roll, object_loc):
    log = time.strftime("Month:%m Day:%d Hour:%H Min:%M Sec:%S\n")
    log += "object location: " + str(object_loc)
    log += "\nCamera location: " + latitude + ", " + altitude + ", " + longitude
    log += "\nCamera position: " + yaw + ", " + pitch + ", " + roll + "\n-------------------------------------------------\n"

    f = open('log.txt', 'a')
    f.write(log)
    f.close();


def getObjectsForLocation(latitude, longitude, altitude, yaw, pitch, roll):
    #creates a connection to the database
    db = DataSource()
    return db.getData('Select * from demo;')

def main():
    parameters = getCGIParameters()
    printMainPageAsHTML(parameters['latitude'], parameters['longitude'], parameters['altitude'],  parameters['yaw'], parameters['pitch'], parameters['roll'], 'template.html')

if __name__ == '__main__':
    main()
