NAME = webserv

SRCS = src/main.cpp src/Utils.cpp src/ServerManager.cpp src/Response.cpp src/Client.cpp src/HttpRequest.cpp \
	   src/ConfigFile.cpp src/ConfigParser.cpp src/ServerConfig.cpp src/Location.cpp src/CgiHandler.cpp \
	   src/Mime.cpp src/Logger.cpp

HEADERS	= inc/Webserv.hpp

OBJS = $(SRCS:.cpp=.o)

CXX = c++

CXXFLAGS = -Wall -Wextra -Werror -std=c++98
CXXFLAGS += -g3 

RM = rm -rf
all: $(NAME)
$(NAME) : $(OBJS) $(HEADERS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $(NAME)
	@echo -webserv compiled 🌐

clean:
	$(RM) $(OBJS)

fclean: clean
	$(RM) $(NAME)

re: 	fclean all

.PHONY: all clean fclean re