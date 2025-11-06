#!/usr/bin/env python3

import os
import sys

# Print the HTTP headers
print("HTTP/1.1 200 OK")
print("Content-type: text/html\r\n\r\n")

# Print HTML content
print("<html>")
print("<head>")
print("<title>CGI Test Script</title>")
print("<style>")
print("body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; background-color: #3f31a3; color: white; }")
print("h1, h2 { color: white; }")
print("table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }")
print("th, td { border: 1px solid #5a4cbb; padding: 8px; text-align: left; }")
print("th { background-color: #2c2177; }")
print("code { background-color: #2c2177; padding: 2px 5px; border-radius: 3px; }")
print(".success { color: #4dff4d; }")
print(".error { color: #ff6b6b; }")
print(".info { background-color: #322984; padding: 15px; border-radius: 5px; }")
print("ul { background-color: #322984; padding: 15px; border-radius: 5px; }")
print("li { margin-bottom: 5px; }")
print("a { color: #8be9fd; }")
print("</style>")
print("</head>")
print("<body>")
print("<h1>CGI Test Script - GET Method</h1>")
print("<div class='info'>")
print("<p>This is a test CGI script for handling GET requests.</p>")
print("</div>")

# Display query string if available
query_string = os.environ.get("QUERY_STRING", "")
if query_string:
    print("<h2>Query String Parameters:</h2>")
    print("<div class='info'>")
    print("<table>")
    print("<tr><th>Parameter</th><th>Value</th></tr>")
    params = query_string.split("&")
    for param in params:
        if "=" in param:
            key, value = param.split("=", 1)
            print(f"<tr><td><strong>{key}</strong></td><td>{value}</td></tr>")
    print("</table>")
    print("</div>")

print("<p><a href='/index.html' style='display: inline-block; padding: 10px 15px; background-color: #5a4cbb; color: white; text-decoration: none; border-radius: 4px;'>Return to Home</a></p>")
print("</body>")
print("</html>")