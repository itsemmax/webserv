#!/usr/bin/env python3

import os
import sys
import cgi

# Print the HTTP headers
print("HTTP/1.1 200 OK")
print("Content-type: text/html\r\n\r\n")

# Get environment variables
request_method = os.environ.get('REQUEST_METHOD', '')
path_info = os.environ.get('PATH_INFO', '')
query_string = os.environ.get('QUERY_STRING', '')

# Print HTML content
print("<html>")
print("<head>")
print("<title>DELETE Method Test</title>")
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
print("a { color: #8be9fd; }")
print("button { background-color: #5a4cbb; color: white; border: none; padding: 5px 10px; cursor: pointer; border-radius: 3px; }")
print("</style>")
print("</head>")
print("<body>")
print("<h1>DELETE Method Test</h1>")

# Handle DELETE request
if request_method == 'DELETE':
    print("<div class='info'>")
    print("<h2 class='success'>DELETE Request Received</h2>")
    
    # Parse the resource to delete from query string or path
    resource_to_delete = ""
    
    if query_string:
        params = dict(param.split('=') for param in query_string.split('&') if '=' in param)
        resource_to_delete = params.get('file', '')
    
    if resource_to_delete:
        # For safety, only allow deletion of files in the tmp directory
        tmp_dir = os.path.join(os.getcwd(), 'cgi-bin', 'tmp')
        file_path = os.path.join(tmp_dir, os.path.basename(resource_to_delete))
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"<p>Successfully deleted file: {os.path.basename(resource_to_delete)}</p>")
            except Exception as e:
                print(f"<p class='error'>Error deleting file: {str(e)}</p>")
        else:
            print(f"<p class='error'>File not found: {os.path.basename(resource_to_delete)}</p>")
    else:
        print("<p>No file specified for deletion.</p>")
    
    print("</div>")
else:
    print("<p class='error'>This script should be accessed with a DELETE request method.</p>")
    print("<p>Current request method: " + request_method + "</p>")

# Display files in tmp directory
tmp_dir = os.path.join(os.getcwd(), 'cgi-bin', 'tmp')
print("<h2>Files in tmp directory:</h2>")

if os.path.exists(tmp_dir) and os.path.isdir(tmp_dir):
    files = os.listdir(tmp_dir)
    if files:
        print("<ul>")
        for file in files:
            file_path = os.path.join(tmp_dir, file)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                print(f"<li>{file} ({file_size} bytes)</li>")
        print("</ul>")
    else:
        print("<p>No files found in the tmp directory.</p>")
else:
    print("<p class='error'>The tmp directory does not exist.</p>")

# Display a JavaScript example to trigger DELETE request
print("<h2>Test DELETE Method:</h2>")
print("<p>Click on a file to delete it:</p>")

print("<div id='fileList'></div>")

print("<script>")
print("function loadFiles() {")
print("    const fileList = document.getElementById('fileList');")
print("    fileList.innerHTML = 'Loading files...';")
print("    fetch('/cgi-bin/test_delete.py')")
print("        .then(response => response.text())")
print("        .then(html => {")
print("            const parser = new DOMParser();")
print("            const doc = parser.parseFromString(html, 'text/html');")
print("            const fileListItems = doc.querySelectorAll('ul li');")
print("            if (fileListItems.length === 0) {")
print("                fileList.innerHTML = '<p>No files found in the tmp directory.</p>';")
print("                return;")
print("            }")
print("            let listHTML = '<ul>';")
print("            fileListItems.forEach(item => {")
print("                const fileName = item.textContent.split(' ')[0];")
print("                listHTML += `<li>${item.textContent} <button onclick=\"deleteFile('${fileName}')\">Delete</button></li>`;")
print("            });")
print("            listHTML += '</ul>';")
print("            fileList.innerHTML = listHTML;")
print("        })")
print("        .catch(error => {")
print("            fileList.innerHTML = `<p class=\"error\">Error loading files: ${error}</p>`;")
print("        });")
print("}")
print("")
print("function deleteFile(fileName) {")
print("    if (confirm(`Are you sure you want to delete ${fileName}?`)) {")
print("        fetch(`/cgi-bin/test_delete.py?file=${fileName}`, {")
print("            method: 'DELETE'")
print("        })")
print("        .then(response => response.text())")
print("        .then(() => {")
print("            alert(`File ${fileName} deletion request sent.`);")
print("            loadFiles();")
print("        })")
print("        .catch(error => {")
print("            alert(`Error: ${error}`);")
print("        });")
print("    }")
print("}")
print("")
print("// Load files when page loads")
print("window.onload = loadFiles;")
print("</script>")

print("<p><a href='/index.html' style='display: inline-block; padding: 10px 15px; background-color: #5a4cbb; color: white; text-decoration: none; border-radius: 4px;'>Return to Home</a></p>")
print("</body>")
print("</html>")