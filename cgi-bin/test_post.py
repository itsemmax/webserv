#!/usr/bin/env python3

import os
import sys
import urllib.parse

# Print the HTTP headers
print("HTTP/1.1 200 OK")
print("Content-type: text/html\r\n\r\n")

# Initialize variables
form_data = {}

# Read POST data from stdin
try:
    content_length = int(os.environ.get('CONTENT_LENGTH', 0))
    if content_length > 0:
        post_data = sys.stdin.read(content_length)
        # Parse URL-encoded data
        for pair in post_data.split('&'):
            if '=' in pair:
                key, value = pair.split('=', 1)
                form_data[urllib.parse.unquote_plus(key)] = urllib.parse.unquote_plus(value)
except:
    pass

message = ""

# Print HTML content
print("<html>")
print("<head>")
print("<title>POST Method Test</title>")
print("<style>")
print("body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; background-color: #3f31a3; color: white; }")
print("h1, h2 { color: white; }")
print("table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }")
print("th, td { border: 1px solid #5a4cbb; padding: 8px; text-align: left; }")
print("th { background-color: #2c2177; }")
print("code { background-color: #2c2177; padding: 2px 5px; border-radius: 3px; }")
print(".form-data { background-color: #322984; padding: 15px; border-radius: 5px; }")
print("input, textarea { background-color: #2c2177; color: white; border: 1px solid #5a4cbb; }")
print("a { color: #8be9fd; }")
print("</style>")
print("</head>")
print("<body>")
print("<h1>POST Method Test</h1>")
print("<p>This script demonstrates processing data sent via POST method.</p>")

# Check if the form has been submitted
if len(form_data) > 0:
    print("<h2>Form Data Received:</h2>")
    print("<div class='form-data'>")
    print("<table>")
    print("<tr><th>Field Name</th><th>Value</th></tr>")
    
    # Display all form fields
    for field, value in form_data.items():
        print(f"<tr><td>{field}</td><td>{value}</td></tr>")
    print("</table>")
    print("</div>")
else:
    print("<p>No form data was submitted. Submit the form below to test the POST method.</p>")

# Display a test form
print("<h2>Test Form:</h2>")
print("<div class='info'>")
print("<form method='post' action='/cgi-bin/test_post.py'>")
print("<label for='name'>Name:</label>")
print("<input type='text' id='name' name='name' required style='padding: 8px; margin: 5px; width: 300px;'><br><br>")
print("<label for='email'>Email:</label>")
print("<input type='email' id='email' name='email' required style='padding: 8px; margin: 5px; width: 300px;'><br><br>")
print("<label for='message'>Message:</label><br>")
print("<textarea id='message' name='message' rows='4' cols='50' style='padding: 8px; margin: 5px;'></textarea><br><br>")
print("<input type='submit' value='Submit' style='padding: 10px 15px; background-color: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer;'>")
print("</form>")
print("</div>")

print("<p><a href='/index.html' style='display: inline-block; padding: 10px 15px; background-color: #5a4cbb; color: white; text-decoration: none; border-radius: 4px;'>Return to Home</a></p>")
print("</body>")
print("</html>")