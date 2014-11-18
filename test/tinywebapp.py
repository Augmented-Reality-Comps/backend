#!/usr/bin/python
''' tinywebapp.py
    Jeff Ondich, 2012

    This is the server-side script of a very simple web application
    that involves an HTML form with two <input type="text"> elements
    (one named "animal" and the other named "badanimal").
'''

import cgi

# Get the user input from the client's request.
form = cgi.FieldStorage()
animal = form['animal'].value
badAnimal = form['badanimal'].value

# Sanitize the user input. You can't trust users not to mess with
# your scripts. In this case, we allow only letters in our animal
# names. Otherwise, you're stuck with the default animal.
if not animal.isalpha():
    animal = 'DEFAULT ANIMAL'
if not badAnimal.isalpha():
    badAnimal = 'DEFAULT ANIMAL'

# Construct the output page.
output = '''<DOCTYPE HTML>
<html>
<head>
    <title>Tiny web app results</title>
</head>

<body>
    <p>I like %ss, too.</p>
    <p>Also, %ss are gross.</p>
</body>
</html>''' % (animal, badAnimal)

# Send the output page back to the client.
print "Content-type: text/html\r\n\r\n"
print output