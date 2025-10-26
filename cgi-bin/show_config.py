#!/usr/bin/env python3

import os
import sys
import json

# Print the HTTP headers
print("HTTP/1.1 200 OK")
print("Content-type: text/html\r\n\r\n")

# Function to read and parse the config file
def read_config():
    try:
        with open(os.path.join(os.getcwd(), 'configs', 'default.conf'), 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading config file: {str(e)}"

# Read the config
config_content = read_config()

# HTML Output
print("""
<html>
<head>
    <title>Server Configuration</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; background-color: #3f31a3; color: white; }
        h1, h2 { color: white; }
        pre { background-color: #2c2177; padding: 15px; border-radius: 5px; overflow-x: auto; white-space: pre-wrap; }
        .info { background-color: #322984; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .config-file { border: 1px solid #5a4cbb; padding: 20px; border-radius: 5px; }
        a { color: #8be9fd; }
        .btn { 
            display: inline-block; 
            padding: 10px 15px; 
            background-color: #5a4cbb; 
            color: white; 
            text-decoration: none; 
            border-radius: 4px;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Server Configuration</h1>
    
    <div class="info">
        <p>Below is the current server configuration from <code>configs/default.conf</code>.</p>
        <p>This configuration defines server parameters, routes, and allowed methods.</p>
    </div>
    
    <div class="config-file">
        <h2>Configuration File</h2>
        <pre>""")
print(config_content)
print("""</pre>
    </div>
    
    <p><a href='/index.html' class="btn">Return to Home</a></p>
</body>
</html>
""")