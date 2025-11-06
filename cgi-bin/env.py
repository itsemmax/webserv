#!/usr/bin/python3

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import cgi

print("HTTP/1.1 200 OK")
print("Content-type: text/html\r\n\r\n")

print("<html>")
print("<head>")
print("<title>Environment Variables</title>")
print("<style>")
print("body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; background-color: #3f31a3; color: white; }")
print("h1, h2 { color: white; }")
print("table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }")
print("th, td { border: 1px solid #5a4cbb; padding: 8px; text-align: left; }")
print("th { background-color: #2c2177; }")
print(".info { background-color: #322984; padding: 15px; border-radius: 5px; }")
print(".success { color: #4dff4d; }")
print(".error { color: #ff6b6b; }")
print("a { color: #8be9fd; }")
print("</style>")
print("</head>")
print("<body>")
print("<h1>Environment Information</h1>")
print("<div class='info'>")
print("<p>This page provides information about the server environment.</p>")
print("<p><strong>Server Software:</strong> " + os.environ.get("SERVER_SOFTWARE", "Unknown") + "</p>")
print("<p><strong>Server Name:</strong> " + os.environ.get("SERVER_NAME", "Unknown") + "</p>")
print("<p><strong>Server Port:</strong> " + os.environ.get("SERVER_PORT", "Unknown") + "</p>")
print("<p><strong>Remote Address:</strong> " + os.environ.get("REMOTE_ADDR", "Unknown") + "</p>")
print("<p><strong>Request Method:</strong> " + os.environ.get("REQUEST_METHOD", "Unknown") + "</p>")
print("<p><strong>Gateway Interface:</strong> " + os.environ.get("GATEWAY_INTERFACE", "Unknown") + "</p>")
print("</div>")

print("<p><a href='/index.html' style='display: inline-block; padding: 10px 15px; background-color: #5a4cbb; color: white; text-decoration: none; border-radius: 4px;'>Return to Home</a></p>")
print("</body>")
print("</html>")