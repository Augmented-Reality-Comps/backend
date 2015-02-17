#!/usr/bin/python

# http://cmc307-08.mathcs.carleton.edu/~comps/backend/walkAround/labelSelector.py?latitude=44.46247&longitude=-93.1536

import cgi
from datasource import DataSource

def sanitizeUserInput(s):
    ''' does a basic sanitation on input'''
    charsToRemove = ';,\\/:\'"<>@'
    for ch in charsToRemove:
        s = s.replace(ch, '')
    return s

def getCGIParameters():
    ''' This function grabs the HTTP parameters we care about, sanitizes the
        user input. We expect latitude, longitude, altitude, yaw, pitch, roll.
    '''
    form = cgi.FieldStorage()
    parameters = {'latitude':'', 'longitude':''}

    #sets default values for each field
    parameters['latitude'] = 0
    parameters['longitude'] = 0

    #sets parameters as they are passed
    if 'latitude' in form:
        parameters['latitude'] = float(sanitizeUserInput(form['latitude'].value))

    if 'longitude' in form:
        parameters['longitude'] = float(sanitizeUserInput(form['longitude'].value))

    return parameters

def getLabelsForLocation(latitude, longitude):
    db = DataSource()
    allLabels = db.getData('Select * from labels;')
    nearbyLabels = []
    for building in allLabels:
    	if (withinRadius(latitude, longitude, building[0], building[1], building[3])):
    		nearbyLabels.append(building)
    return nearbyLabels

def withinRadius(dLat, dLong, bLat, bLong, radius):
	if (((dLat - bLat)**2 + (dLong - bLong)**2) <= radius**2):
		return True
	else:
		return False

def main():
	parameters = getCGIParameters()
	output = "<!DOCTYPE html><meta content=\"text/html;charset=utf-8\" http-equiv=\"Content-Type\"><meta content=\"utf-8\ http-equiv=\encoding\"><html lang=\"en-US\"><head><title>Building Labels</title></head>"
	output += "<h1>Buildings Nearby: "+str(parameters['latitude']) + ", " + str(parameters['longitude']) + "</h1>"
	buildings = getLabelsForLocation(parameters['latitude'], parameters['longitude'])
	for building in buildings:
		output += "<h2>"+ str(building[2]) + "</h2>"
	output += "</html>"
	print 'Content-type: text/html\r\n\r\n',
	print output

if __name__ == '__main__':
    main()