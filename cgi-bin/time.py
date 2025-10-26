#!/usr/bin/python3

import datetime
import cgi

print("HTTP/1.1 200 OK")
print("Content-type: text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<style>")
print("body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; background-color: #3f31a3; color: white; }")
print("h1 { color: white; font-size: 72px; text-align: center; margin-top: 100px; }")
print("a { color: #8be9fd; text-align: center; display: block; margin-top: 50px; }")
print("</style>")
print("</head>")
print("<body>")
print(datetime.datetime.strftime(datetime.datetime.now(), "<h1>%H:%M:%S</h1>"))
print("<a href='/index.html' style='display: inline-block; padding: 10px 15px; background-color: #5a4cbb; color: white; text-decoration: none; border-radius: 4px;'>Return to Home</a>")
print("</body>")
print("</html>")