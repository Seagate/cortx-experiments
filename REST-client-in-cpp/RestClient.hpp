#ifndef REST_HPP
#define REST_HPP

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

using namespace std;

class restClient
{
    int sock, port;
    sockaddr_in client;
    std::string hostName, resource, query;
    hostent *host;
    std::vector<std::pair<std::string, std::string>> headers;

    public:

    // Parses the endpoint and set class variables
    restClient(std::string& endpoint)
    {
        auto index = endpoint.find("://");
        endpoint = ((index == -1) ? endpoint : endpoint.substr(index + 3));

        index = endpoint.find("?");
        query = ((index == -1) ? "" : endpoint.substr(index));
        endpoint = ((index == -1) ? endpoint : endpoint.substr(0, index));

        index = endpoint.find("/");
        resource = ((index == -1) ? "" : endpoint.substr(index));
        endpoint = endpoint.substr(0, index);

        index = endpoint.find(":");
        port = ((index == -1) ? -1 : std::atoi(endpoint.substr(index + 1).c_str()));
        hostName = ((index == -1) ? endpoint : endpoint.substr(0, index));

        sock = -1;
        host = NULL;
        bzero(&client, sizeof(client));
    }

    // Sets sockaddr_in and default headers
    std::string init()
    {
        if ((hostName != "") || (port == -1))
        {
            host = gethostbyname(hostName.c_str());

            if ((host == NULL) || (host->h_addr == NULL))
            {
                return "Error retrieving DNS information.";
            }

            client.sin_family = AF_INET;
            client.sin_port = htons(port);
            memcpy(&client.sin_addr, host->h_addr, host->h_length);

            headers.push_back({"Host", hostName + ":" + std::to_string(port)});
            headers.push_back({"Accept", "*/*"});
        }
        else
        {
            return "Set a Valid Address or Port Number";
        }

        return std::string();
    }

    // To create and connect to socket
    std::string createAndConnect()
    {
        sock = socket(AF_INET, SOCK_STREAM, 0);

        if (sock < 0)
        {
            return "Error at creating socket";
        }

        int ret = connect(sock, (struct sockaddr *)&client, sizeof(client));

        if (ret < 0)
        {
            return "Error while establishing connection" + std::to_string(errno);
        }

        return std::string();
    }

    // To add additional headers
    void updateHeader(const std::string& key, const std::string& value)
    {
        if ((key != "") && (value != ""))
        {
            headers.push_back({key, value});
        }
    }

    // send request
    std::string sendRequest(const std::string& verb, const std::string& body)
    {
        if (body != "")
        {
            headers.push_back({"Content-Length", std::to_string(body.size())});
        }

        stringstream ss;
        ss << verb << " " << resource << query << " HTTP/1.1\r\n";

        for (auto it : headers)
        {
            ss << it.first << ": " << it.second << "\r\n";
        }
        
        ss << "\r\n";
        ss << body << "\r\n";

        std::string request = ss.str();

        int ret = send(sock, request.c_str(), request.length(), 0);

        if (ret != (int)request.length()) 
        {
            return "Error sending request." + std::to_string(errno);
        }

        return std::string();
    }

    // To recieve response
    std::string readResponse(std::vector<char>& data, int& size) const
    {
        while(true)
        {
            char buf[1024] = {'\0'};
            auto valRead = read(sock, buf, 1024);

            if (valRead > 0)
            {
                data.insert(data.end(), buf, buf + valRead);
                size += valRead;
            }
            else if (valRead == 0)
            {
                break;
            }
            else
            {
                return "Error while reading response: " + std::to_string(errno);
            }
        }

        return std::string();
    }

    void setHostName(const std::string& hostName)
    {
        this->hostName = hostName;
    }

    void setPort(int port)
    {
        this->port = port;
    }

    void setResource(const std::string& resource)
    {
        this->resource = resource;
    }

    void setQuery(const std::string& query)
    {
        this->query = query;
    }

    std::string getHostName()
    {
        return hostName;
    }

    int getPort()
    {
        return port;
    }

    std::string getResource()
    {
        return resource;
    }

    std::string getQuery()
    {
        return query;
    }

    ~restClient()
    {
        if (sock >= 0)
        {
            close(sock);
        }
        if (host != NULL)
        {
            endhostent();
        }
    }
};

#endif
