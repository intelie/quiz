CC=g++
CFLAGS += $(shell pkg-config --cflags json)
LDFLAGS += $(shell pkg-config --libs json)

CFLAGS += $(shell curl-config --cflags)
LDFLAGS += $(shell curl-config --libs )

debug:
	$(CC) -g -Wall $(CFLAGS) src/main.cpp src/HTTPRequest.cpp src/JSONParser.cpp src/StringUtils.cpp $(LDFLAGS) -o test

all:
	$(CC) -Wall $(CFLAGS) src/main.cpp src/HTTPRequest.cpp src/JSONParser.cpp src/StringUtils.cpp $(LDFLAGS) -o test

