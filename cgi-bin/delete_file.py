#!/usr/bin/env python3

import os
import sys
import json
import cgi
from urllib.parse import parse_qs

# Print the HTTP headers
print("HTTP/1.1 200 OK")
print("Content-type: application/json\r\n\r\n")

# Get request method and query string
request_method = os.environ.get('REQUEST_METHOD', '')
query_string = os.environ.get('QUERY_STRING', '')

# Directory for files
directory = os.path.join(os.getcwd(), 'cgi-bin', 'tmp')

# Parse query string
params = {}
if query_string:
    params = parse_qs(query_string)
    params = {k: v[0] for k, v in params.items()}

response = {}

# Process DELETE request
if request_method == 'DELETE':
    if 'file' in params:
        filename = params['file']
        file_type = params.get('type', 'regular')
        
        if file_type == 'test':
            # For test files, they are in the cgi-bin directory
            file_path = os.path.join(os.getcwd(), 'cgi-bin', os.path.basename(filename))
            # Security check: make sure it's a test file in the cgi-bin directory
            if not filename.startswith('test_') or not filename.endswith('.py'):
                response = {"success": False, "message": "Can only delete test files (files starting with test_)"}
                print(json.dumps(response))
                sys.exit(0)
        else:
            # Regular files in the tmp directory
            file_path = os.path.join(directory, os.path.basename(filename))
            
        # Security checks
        real_path = os.path.realpath(file_path)
        if file_type == 'test':
            real_dir = os.path.realpath(os.path.join(os.getcwd(), 'cgi-bin'))
        else:
            real_dir = os.path.realpath(directory)
        
        # Make sure file exists and is in the correct directory
        if (real_path.startswith(real_dir) and 
            os.path.exists(file_path) and 
            os.path.isfile(file_path)):
            try:
                os.remove(file_path)
                response = {
                    "success": True,
                    "message": f"File '{filename}' was successfully deleted."
                }
            except Exception as e:
                response = {
                    "success": False,
                    "message": f"Error deleting file: {str(e)}"
                }
        else:
            response = {
                "success": False,
                "message": f"File '{filename}' not found or access denied."
            }
    else:
        response = {
            "success": False,
            "message": "No file specified for deletion."
        }
else:
    response = {
        "success": False,
        "message": f"Invalid request method. Expected DELETE, got {request_method}."
    }

# Return JSON response
print(json.dumps(response))