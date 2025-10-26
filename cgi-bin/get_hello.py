#!/usr/bin/python3

import cgi
import sys
import os
# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
first_name = form.getvalue('first_name')
last_name = form.getvalue('last_name')
print(os.environ["QUERY_STRING"], file=sys.stderr)
print("HTTP/1.1 200 OK")
print("Content-type: text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>Hello - Second CGI Program</title>")
print("<style>")
print("body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; background-color: #3f31a3; color: white; }")
print("h1, h2 { color: white; text-align: center; margin-top: 100px; }")
print("a { color: #8be9fd; text-align: center; display: block; margin-top: 50px; }")
print("</style>")
print("</head>")
print("<body>")
print("<h2>Hello %s %s</h2>" % (first_name, last_name))
print("<a href='/index.html'>Return to Home</a>")
print("</body>")
print("</html>")