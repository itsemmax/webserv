#!/usr/bin/python3

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import cgi, os
import sys

# Print the HTTP headers
print("HTTP/1.1 200 OK")
print("Content-Type: text/html;charset=utf-8\r\n\r\n")

try:
    form = cgi.FieldStorage()
    
    # Create the tmp directory if it doesn't exist
    tmp_dir = os.path.join(os.getcwd(), 'cgi-bin', 'tmp')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    
    # Get filename here
    if 'filename' not in form:
        message = 'Error: No file uploaded (missing "filename" field)'
    else:
        fileitem = form['filename']
        
        # Test if the file was uploaded
        if fileitem.filename:
            safe_filename = os.path.basename(fileitem.filename)
            save_path = os.path.join(tmp_dir, safe_filename)
            
            with open(save_path, 'wb') as f:
                f.write(fileitem.file.read())
            
            message = 'The file "' + safe_filename + '" was successfully uploaded to ' + tmp_dir
        else:
            message = 'Uploading Failed: No file selected'
except Exception as e:
    message = f'Error during file upload: {str(e)}'

# Output HTML content
print("<html>")
print("<head>")
print("<title>File Upload Result</title>")
print("<style>")
print("body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; background-color: #3f31a3; color: white; }")
print("h1 { color: white; }")
print(".success { color: #4dff4d; }")
print(".error { color: #ff6b6b; }")
print("a { color: #8be9fd; text-decoration: none; }")
print("a:hover { text-decoration: underline; }")
print(".container { background-color: #322984; padding: 20px; border-radius: 5px; margin-top: 20px; }")
print("</style>")
print("</head>")
print("<body>")

if "Error" in message:
    print(f'<h1 class="error">{message}</h1>')
else:
    print(f'<h1 class="success">{message}</h1>')

print("<div class='container'>")
print("  <p>What would you like to do next?</p>")
print("  <div style='margin-top: 20px;'>")
print("    <a href='/file_management.html' style='background-color: #5a4cbb; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; margin-right: 10px; display: inline-block;'>Manage Files</a>")
print("    <a href='/index.html' style='background-color: #5a4cbb; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; display: inline-block;'>Return to Home</a>")
print("  </div>")
print("</div>")
print("</body>")
print("</html>")
