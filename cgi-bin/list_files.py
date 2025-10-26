#!/usr/bin/env python3

import os
import json

# Print the HTTP headers
print("HTTP/1.1 200 OK")
print("Content-type: application/json\r\n\r\n")

# Directory to list regular files from
directory = os.path.join(os.getcwd(), 'cgi-bin', 'tmp')

# Directory to list test files from
test_directory = os.path.join(os.getcwd(), 'cgi-bin')

# Check if the directory exists
if not os.path.exists(directory):
    os.makedirs(directory, exist_ok=True)

# Get list of regular files
files = []
try:
    # Get regular files from tmp directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_info = {
                "name": filename,
                "size": os.path.getsize(file_path),
                "path": file_path,
                "type": "regular"
            }
            files.append(file_info)
            
    # Get test files (Python files starting with "test_")
    for filename in os.listdir(test_directory):
        if filename.startswith("test_") and filename.endswith(".py"):
            file_path = os.path.join(test_directory, filename)
            if os.path.isfile(file_path):
                file_info = {
                    "name": filename,
                    "size": os.path.getsize(file_path),
                    "path": file_path,
                    "type": "test"
                }
                files.append(file_info)
except Exception as e:
    print(json.dumps({"error": str(e)}))
    exit(1)

# Return JSON response
response = {
    "files": files,
    "directory": directory
}

print(json.dumps(response))