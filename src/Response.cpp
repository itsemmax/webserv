# include "../inc/Response.hpp"

Mime Response::_mime;

Response::Response()
{
    _target_file = "";
    _body.clear();
    _body_length = 0;
    _response_content = "";
    _response_body = "";
    _location = "";
    _code = 0;
    _cgi = 0;
    _cgi_response_length = 0;
    _auto_index = 0;
}

Response::~Response() {}

Response::Response(HttpRequest &req) : request(req)
{
    _target_file = "";
    _body.clear();
    _body_length = 0;
    _response_content = "";
    _response_body = "";
    _location = "";
    _code = 0;
    _cgi = 0;
    _cgi_response_length = 0;
    _auto_index = 0;
}
void   Response::contentType()
{
    _response_content.append("Content-Type: ");
    if(_target_file.rfind(".", std::string::npos) != std::string::npos && _code == 200)
        _response_content.append(_mime.getMimeType(_target_file.substr(_target_file.rfind(".", std::string::npos))) );
    else
        _response_content.append(_mime.getMimeType("default"));
    _response_content.append("\r\n");
}

void   Response::contentLength()
{
    std::stringstream ss;
    ss << _response_body.length();
    _response_content.append("Content-Length: ");
    _response_content.append(ss.str());
    _response_content.append("\r\n");
}

void   Response::connection()
{
    if(request.getHeader("connection") == "keep-alive")
        _response_content.append("Connection: keep-alive\r\n");
}

void   Response::server()
{
    _response_content.append("Server: AMAnix\r\n");
}

void    Response::location()
{
    if (_location.length())
        _response_content.append("Location: "+ _location +"\r\n");
}

void    Response::date()
{
    char date[1000];
    time_t now = time(0);
    struct tm tm = *gmtime(&now);
    strftime(date, sizeof(date), "%a, %d %b %Y %H:%M:%S %Z", &tm);
    _response_content.append("Date: ");
    _response_content.append(date);
    _response_content.append("\r\n");

}
// uri ecnoding
void    Response::setHeaders()
{
    contentType();
    contentLength();
    connection();
    server();
    location();
    date();

    _response_content.append("\r\n");
}

static bool fileExists (const std::string& f) {
    struct stat buffer;
    return (stat(f.c_str(), &buffer) == 0);
}

static bool isDirectory(std::string path)
{
    struct stat file_stat;
    if (stat(path.c_str(), &file_stat) != 0)
        return (false);

    return (S_ISDIR(file_stat.st_mode));
}

static bool isAllowedMethod(HttpMethod &method, Location &location, short &code)
{
    std::vector<short> methods = location.getMethods();
    
    // Check if the method is implemented
    if (method == NONE)
    {
        code = 501; // Not Implemented
        return (1);
    }
    
    // Check if the method is allowed in this location
    bool allowed = false;
    switch(method)
    {
        case GET:
            allowed = methods[0];
            break;
        case POST:
            allowed = methods[1];
            break;
        case DELETE:
            allowed = methods[2];
            break;
        case PUT:
            allowed = methods[3];
            break;
        case HEAD:
            allowed = methods[4];
            break;
        default:
            code = 501; // Not Implemented
            return (1);
    }
    
    if (!allowed)
    {
        code = 405; // Method Not Allowed
        return (1);
    }
    return (0);
}

static bool    checkReturn(Location &loc, short &code, std::string &location)
{
    if (!loc.getReturn().empty())
    {
        code = 301;
        location = loc.getReturn();
        if (location[0] != '/')
            location.insert(location.begin(), '/');
        return (1);
    }
    return (0);
}

static std::string combinePaths(std::string p1, std::string p2, std::string p3)
{
    std::cout << "DEBUG: combinePaths input: p1='" << p1 << "', p2='" << p2 << "', p3='" << p3 << "'" << std::endl;
    
    std::string res;
    int         len1;
    int         len2;

    // Remove leading slash from p1 if it exists
    if (!p1.empty() && p1[0] == '/')
        p1.erase(0, 1);
        
    len1 = p1.length();
    len2 = p2.length();
    
    // Handle slashes between p1 and p2
    if (p1[len1 - 1] == '/' && (!p2.empty() && p2[0] == '/'))
        p2.erase(0, 1);
    if (p1[len1 - 1] != '/' && (!p2.empty() && p2[0] != '/'))
        p1.insert(p1.end(), '/');
        
    // Handle slashes between p2 and p3
    if (p2[len2 - 1] == '/' && (!p3.empty() && p3[0] == '/'))
        p3.erase(0, 1);
    if (p2[len2 - 1] != '/' && (!p3.empty() && p3[0] != '/'))
        p2.insert(p2.end(), '/');
        
    res = p1 + p2 + p3;
    std::cout << "DEBUG: combinePaths result: '" << res << "'" << std::endl;
    return (res);
}

static void replaceAlias(Location &location, HttpRequest &request, std::string &target_file)
{
    target_file = combinePaths(location.getAlias(), request.getPath().substr(location.getPath().length()), "");
}

static void appendRoot(Location &location, HttpRequest &request, std::string &target_file)
{
    // Get the root path from location or use www as default
    std::string rootPath = location.getRootLocation();
    if (rootPath.empty()) {
        rootPath = "./www";  // Default root path with ./ prefix
    }
    
    // Ensure root path starts with ./
    if (rootPath.substr(0, 2) != "./") {
        rootPath = "./" + rootPath;
    }
    
    // Remove trailing slash if present
    if (rootPath[rootPath.length() - 1] == '/') {
        rootPath = rootPath.substr(0, rootPath.length() - 1);
    }
    
    // For root path ("/"), append index file
    if (request.getPath() == "/" || request.getPath().empty()) {
        target_file = rootPath;
        if (target_file[target_file.length() - 1] != '/') {
            target_file += "/";
        }
        
        // Try location's index first, then server's default index
        std::string idx = location.getIndexLocation();
        if (idx.empty()) {
            idx = "index.html";
        }
        target_file += idx;
    } else {
        // For other paths, combine root with request path
        std::string path = request.getPath();
        if (path[0] == '/') {
            path = path.substr(1); // Remove leading slash
        }
        target_file = rootPath + "/" + path;
    }
    
    std::cout << "DEBUG: Final target file path: " << target_file << std::endl;
}

int Response::handleCgiTemp(std::string &location_key)
{
    std::string path;
    path = _target_file;
    _cgi_obj.clear();
    _cgi_obj.setCgiPath(path);
    _cgi = 1;
    if (pipe(_cgi_fd) < 0)
    {
        _code = 500;
        return (1);
    }
    _cgi_obj.initEnvCgi(request, _server.getLocationKey(location_key)); // + URI
    _cgi_obj.execute(this->_code);
    return (0);
}

/* check a file for CGI (the extension is supported, the file exists and is executable) and run the CGI */
int Response::handleCgi(std::string &location_key)
{
    std::string path;
    std::string exten;
    size_t      pos;

    // Use the target file that was set in handleTarget
    path = _target_file;
    std::cout << "DEBUG: CGI processing path: " << path << std::endl;

    // Handle default index for /cgi-bin/
    if (path == "cgi-bin" || path == "cgi-bin/")
    {
        path = "cgi-bin/" + _server.getLocationKey(location_key)->getIndexLocation();
        std::cout << "DEBUG: Using default CGI index: " << path << std::endl;
    }

    // Check file extension
    pos = path.find(".");
    if (pos == std::string::npos)
    {
        std::cout << "DEBUG: No file extension found in CGI path" << std::endl;
        _code = 501;
        return (1);
    }

    exten = path.substr(pos);
    std::cout << "DEBUG: CGI file extension: " << exten << std::endl;

    // Verify extension is supported
    if (exten != ".py" && exten != ".sh")
    {
        std::cout << "DEBUG: Unsupported CGI extension: " << exten << std::endl;
        _code = 501;
        return (1);
    }

    // Check if file exists and is accessible
    struct stat st;
    if (stat(path.c_str(), &st) != 0)
    {
        std::cout << "DEBUG: CGI file not found: " << path << std::endl;
        _code = 404;
        return (1);
    }

    // Check if file is executable
    if (!(st.st_mode & S_IXUSR))
    {
        std::cout << "DEBUG: CGI file not executable: " << path << std::endl;
        _code = 403;
        return (1);
    }

    // Check if method is allowed
    if (isAllowedMethod(request.getMethod(), *_server.getLocationKey(location_key), _code))
    {
        std::cout << "DEBUG: Method not allowed for CGI" << std::endl;
        return (1);
    }

    // Setup CGI execution
    _cgi_obj.clear();
    _cgi_obj.setCgiPath(path);
    _cgi = 1;

    // Create pipe for CGI communication
    if (pipe(_cgi_fd) < 0)
    {
        std::cout << "DEBUG: Failed to create pipe for CGI" << std::endl;
        _code = 500;
        return (1);
    }
    _cgi_obj.initEnv(request, _server.getLocationKey(location_key)); // + URI
    _cgi_obj.execute(this->_code);
    return (0);
}

/*
    Compares URI with locations from config file and tries to find the best match.
    If match found, then location_key is set to that location, otherwise location_key will be an empty string.
*/

static void    getLocationMatch(std::string &path, std::vector<Location> locations, std::string &location_key)
{
    size_t biggest_match = 0;

    for(std::vector<Location>::const_iterator it = locations.begin(); it != locations.end(); ++it)
    {
        if(path.find(it->getPath()) == 0)
        {
               if( it->getPath() == "/" || path.length() == it->getPath().length() || path[it->getPath().length()] == '/')
               {
                    if(it->getPath().length() > biggest_match)
                    {
                        biggest_match = it->getPath().length();
                        location_key = it->getPath();
                    }
               }
        }
    }
}
int    Response::handleTarget()
{
    std::string location_key;
    std::cout << "DEBUG: Incoming request path: " << request.getPath() << std::endl;
    std::cout << "DEBUG: Request method: " << request.getMethodStr() << std::endl;
    getLocationMatch(request.getPath(), _server.getLocations(), location_key);
    std::cout << "DEBUG: Matched location key: " << location_key << std::endl;
    if (location_key.length() > 0)
    {
        Location target_location = *_server.getLocationKey(location_key);
        std::cout << "DEBUG: Location root: " << target_location.getRootLocation() << std::endl;

        if (isAllowedMethod(request.getMethod(), target_location, _code))
        {
            std::cout << "METHOD NOT ALLOWED \n";
            return (1);
        }
        if (request.getBody().length() > target_location.getMaxBodySize())
        {
            _code = 413;
            return (1);
        }
        if (checkReturn(target_location, _code, _location))
            return (1);

        if (target_location.getPath().find("cgi-bin") != std::string::npos)
        {
            std::cout << "DEBUG: Handling CGI request for path: " << request.getPath() << std::endl;
            _target_file = request.getPath();
            if (_target_file[0] == '/') {
                _target_file = _target_file.substr(1);  // Remove leading slash
            }
            std::cout << "DEBUG: CGI target file: " << _target_file << std::endl;
            return (handleCgi(location_key));
        }

        if (!target_location.getAlias().empty())
        {
            replaceAlias(target_location, request, _target_file);
        }
        else
            appendRoot(target_location, request, _target_file);

        if (!target_location.getCgiExtension().empty())
        {

            if (_target_file.rfind(target_location.getCgiExtension()[0]) != std::string::npos)
            {
                return (handleCgiTemp(location_key));
            }

        }
        if (isDirectory(_target_file))
        {
            if (_target_file[_target_file.length() - 1] != '/')
            {
                _code = 301;
                _location = request.getPath() + "/";
                return (1);
            }
            if (!target_location.getIndexLocation().empty())
                _target_file += target_location.getIndexLocation();
            else
                _target_file += _server.getIndex();
            if (!fileExists(_target_file))
            {
                if (target_location.getAutoindex())
                {
                    _target_file.erase(_target_file.find_last_of('/') + 1);
                    _auto_index = true;
                    return (0);
                }
                else
                {
                    _code = 403;
                    return (1);
                }
            }
            if (isDirectory(_target_file))
            {
                _code = 301;
                if (!target_location.getIndexLocation().empty())
                    _location = combinePaths(request.getPath(), target_location.getIndexLocation(), "");
                else
                    _location = combinePaths(request.getPath(), _server.getIndex(), "");
                if (_location[_location.length() - 1] != '/')
                    _location.insert(_location.end(), '/');

                return (1);
            }
        }
    }
    else
    {
        std::cout << "DEBUG: No location match, using server root: " << _server.getRoot() << std::endl;
        // Handle root path specially
        if (request.getPath() == "/" || request.getPath().empty()) {
            _target_file = combinePaths(_server.getRoot(), "", "");
            if (_target_file[_target_file.length() - 1] != '/') {
                _target_file += "/";
            }
            _target_file += _server.getIndex();
            std::cout << "DEBUG: Using index file: " << _target_file << std::endl;
            
            if (!fileExists(_target_file)) {
                std::cout << "DEBUG: Index file not found: " << _target_file << std::endl;
                _code = 404;
                return (1);
            }
            return (0);
        }
        
        _target_file = combinePaths(_server.getRoot(), request.getPath(), "");
        std::cout << "DEBUG: Final target file path: " << _target_file << std::endl;
        
        if (isDirectory(_target_file))
        {
            if (_target_file[_target_file.length() - 1] != '/')
            {
                _code = 301;
                _location = request.getPath() + "/";
                return (1);
            }
            _target_file += _server.getIndex();
            if (!fileExists(_target_file))
            {
                _code = 404;  // Changed from 403 to 404 for consistency
                return (1);
            }
            if (isDirectory(_target_file))
            {
                _code = 301;
                _location = combinePaths(request.getPath(), _server.getIndex(), "");
                if(_location[_location.length() - 1] != '/')
                    _location.insert(_location.end(), '/');
                return (1);
            }
        }
    }
    return (0);
}

bool Response::reqError()
{
    if(request.errorCode())
    {
        _code = request.errorCode();
        return (1);
    }
    return (0);
}

void Response::setServerDefaultErrorPages()
{
    _response_body = getErrorPage(_code);
}

void Response::buildErrorBody()
{
    if (!_server.getErrorPages().count(_code) || _server.getErrorPages().at(_code).empty() ||
        request.getMethod() == DELETE || request.getMethod() == POST)
    {
        std::cout << "DEBUG: Using default error page for code " << _code << std::endl;
        setServerDefaultErrorPages();
    }
    else
    {
        // Directly serve the error page instead of redirecting
        std::string error_page = _server.getErrorPages().at(_code);
        if (error_page[0] != '/')
            error_page.insert(error_page.begin(), '/');

        _target_file = _server.getRoot() + error_page;

        // If error page doesn't exist, fall back to default
        if (!fileExists(_target_file)) {
            std::cout << "DEBUG: Error page not found, falling back to default for code " << _code << std::endl;
            setServerDefaultErrorPages();
        }
        else
        {
            short old_code = _code;
            if (readFile())
            {
                _code = old_code;
                _response_body = getErrorPage(_code);
            }
        }
    }

}
void    Response::buildResponse()
{
    if (reqError() || buildBody())
    {
        std::cout << "DEBUG: Building error body for code " << _code << std::endl;
        buildErrorBody();
    }
    if (_cgi)
        return;
    else if (_auto_index)
    {
        std::cout << "DEBUG: Generating auto index for target file: " << _target_file << std::endl;
        if (buildHtmlIndex(_target_file, _body, _body_length))
        {
            _code = 500;
            buildErrorBody();
        }
        else
        {
            _code = 200;
            std::cout << "DEBUG: Auto index generated successfully." << std::endl;
        }
        _response_body.insert(_response_body.begin(), _body.begin(), _body.end());
    }
    setStatusLine();
    setHeaders();
    if (request.getMethod() != HEAD && (request.getMethod() == GET || _code != 200))
    {
        std::cout << "DEBUG: Appending response body to response content." << std::endl;
        _response_content.append(_response_body);
    }
}

void Response::setErrorResponse(short code)
{
    _response_content = "";
    _code = code;
    _response_body = "";
    buildErrorBody();
    setStatusLine();
    setHeaders();
    _response_content.append(_response_body);
}

/* Returns the entire reponse ( Headers + Body )*/
std::string Response::getRes()
{
    return (_response_content);
}

/* Returns the length of entire reponse ( Headers + Body) */
size_t Response::getLen() const
{
	return (_response_content.length());
}

/* Constructs Status line based on status code. */
void        Response::setStatusLine()
{
    _response_content.append("HTTP/1.1 " + toString(_code) + " ");
    _response_content.append(statusCodeString(_code));
    _response_content.append("\r\n");
}

int    Response::buildBody()
{
    std::cout << "DEBUG: Building response body..." << std::endl;
    if (request.getBody().length() > _server.getClientMaxBodySize()) {
        std::cout << "DEBUG: Request body too large" << std::endl;
        _code = 413;
        return (1);
    }
    if (handleTarget()) {
        std::cout << "DEBUG: handleTarget failed with code: " << _code << std::endl;
        return (1);
    }
    if (_cgi || _auto_index) {
        std::cout << "DEBUG: CGI or autoindex handling" << std::endl;
        return (0);
    }
    if (_code) {
        std::cout << "DEBUG: Error code set: " << _code << std::endl;
        return (0);
    }

    if (request.getMethod() == GET || request.getMethod() == HEAD) {
        if (readFile())
            return (1);
        _code = 200;
        return (0);
    }
    else if (request.getMethod() == POST || request.getMethod() == PUT) {
        bool existed = fileExists(_target_file);
        std::ofstream file(_target_file.c_str(), std::ios::binary);
        
        if (file.fail()) {
            _code = 500; // Internal Server Error - cannot create/write file
            return (1);
        }
        
        if (request.getMultiformFlag()) {
            std::string body = request.getBody();
            body = removeBoundary(body, request.getBoundary());
            file.write(body.c_str(), body.length());
        } else {
            file.write(request.getBody().c_str(), request.getBody().length());
        }
        
        file.close();
        
        if (request.getMethod() == POST) {
            _code = existed ? 204 : 201;
        } else {
            _code = existed ? 200 : 201;
        }
        return (0);
    }
    else if (request.getMethod() == DELETE) {
        if (!fileExists(_target_file)) {
            _code = 404;
            return (1);
        }
        if (remove(_target_file.c_str()) != 0) {
            _code = 500;
            return (1);
        }
        _code = 204;
        return (0);
    }
    
    // Method not implemented
    _code = 405;
    return (1);
}

int Response::readFile()
{
    std::cout << "DEBUG: Attempting to read file: " << _target_file << std::endl;

    // First check if path exists
    struct stat path_stat;
    if (stat(_target_file.c_str(), &path_stat) != 0)
    {
        std::cout << "DEBUG: File does not exist: " << _target_file << std::endl;
        _code = 404;
        return (1);
    }

    // Check if it's a regular file
    if (!S_ISREG(path_stat.st_mode))
    {
        std::cout << "DEBUG: Path exists but is not a regular file: " << _target_file << std::endl;
        _code = 403;
        return (1);
    }

    // Try to open and read the file
    std::ifstream file(_target_file.c_str(), std::ios::binary);
    if (!file.is_open())
    {
        std::cout << "DEBUG: Failed to open file: " << _target_file << std::endl;
        _code = 403;
        return (1);
    }

    // Read file content
    try {
        std::ostringstream ss;
        ss << file.rdbuf();
        _response_body = ss.str();
        
        if (file.fail())
        {
            std::cout << "DEBUG: Error occurred while reading file: " << _target_file << std::endl;
            _code = 500;
            return (1);
        }
    }
    catch (const std::exception& e)
    {
        std::cout << "DEBUG: Exception while reading file: " << e.what() << std::endl;
        _code = 500;
        return (1);
    }

    file.close();
    std::cout << "DEBUG: Successfully read file: " << _target_file << " (size: " << _response_body.length() << " bytes)" << std::endl;
    return (0);
}

void     Response::setServer(ServerConfig &server)
{
    _server = server;
}

void    Response::setRequest(HttpRequest &req)
{
    request = req;
}

void        Response::cutRes(size_t i)
{
    _response_content = _response_content.substr(i);
}

void   Response::clear()
{
    _target_file.clear();
    _body.clear();
    _body_length = 0;
    _response_content.clear();
    _response_body.clear();
    _location.clear();
    _code = 0;
    _cgi = 0;
    _cgi_response_length = 0;
    _auto_index = 0;
}

int      Response::getCode() const
{
    return (_code);
}

int    Response::getCgiState()
{
    return (_cgi);
}

std::string Response::removeBoundary(std::string &body, std::string &boundary)
{
    std::string buffer;
    std::string new_body;
    std::string filename;
    bool is_boundary = false;
    bool is_content = false;

    if (body.find("--" + boundary) != std::string::npos && body.find("--" + boundary + "--") != std::string::npos)
    {
        for (size_t i = 0; i < body.size(); i++)
        {
            buffer.clear();
            while(body[i] != '\n')
            {
                buffer += body[i];
                i++;
            }
            if (!buffer.compare(("--" + boundary + "--\r")))
            {
                is_content = true;
                is_boundary = false;
            }
            if (!buffer.compare(("--" + boundary + "\r")))
            {
                is_boundary = true;
            }
            if (is_boundary)
            {
                if (!buffer.compare(0, 31, "Content-Disposition: form-data;"))
                {
                    size_t start = buffer.find("filename=\"");
                    if (start != std::string::npos)
                    {
                        size_t end = buffer.find("\"", start + 10);
                        if (end != std::string::npos)
                            filename = buffer.substr(start + 10, end);
                    }
                }
                else if (!buffer.compare(0, 1, "\r") && !filename.empty())
                {
                    is_boundary = false;
                    is_content = true;
                }

            }
            else if (is_content)
            {
                if (!buffer.compare(("--" + boundary + "\r")))
                {
                    is_boundary = true;
                }
                else if (!buffer.compare(("--" + boundary + "--\r")))
                {
                    new_body.erase(new_body.end() - 1);
                    break ;
                }
                else
                    new_body += (buffer + "\n");
            }

        }
    }

    body.clear();
    return (new_body);
}

void      Response::setCgiState(int state)
{
    _cgi = state;
}