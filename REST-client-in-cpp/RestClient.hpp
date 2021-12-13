#pragma once

#ifndef REST_CLIENT_HPP
#define REST_CLIENT_HPP

#include <iostream>
#include <cstring>
#include <sstream>
#include <fstream>
#include <string>
#include <vector>

#include <ctype.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <netinet/in.h>
#include <unistd.h>
#include <fcntl.h>

using namespace std;

class restClient
{
    int sock, port;
    sockaddr_in client;
    std::string hostName, resource, query;
    hostent *host;
    std::vector<std::pair<std::string, std::string>> headers;

    std::string waitForCompletion(bool isReadOp);

    void parseEndpoint(std::string& endpoint);

    public:

    restClient(std::string& endpoint);

    std::string init();

    std::string createAndConnect();

    void updateHeader(const std::string& key, const std::string& value);

    std::string sendRequest(const std::string& verb, const std::string& body);
    
    std::string readResponse(std::vector<char>& data, int& size);

    void setEndpoint(std::string& endpoint);

    void setHostName(const std::string& hostName);

    void setPort(int port);

    void setResource(const std::string& resource);

    void setQuery(const std::string& query);

    std::string getHostName();

    int getPort();

    std::string getResource();

    std::string getQuery();

    ~restClient();
};

#endif