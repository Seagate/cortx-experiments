// Copyright (c) 2021 Seagate Technology LLC and/or its Affiliates
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published
// by the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU Affero General Public License for more details.
// You should have received a copy of the GNU Affero General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.
// For any questions about this software or licensing,
// please email opensource@seagate.com or cortx-questions@seagate.com.

#include <iostream>
#include <cstring>
#include <sstream>
#include <vector>

#include <fcntl.h>

#include "RestClient.hpp"

// Waits for async task to to be completed
std::string restClient::waitForCompletion(bool isReadOp)
{
    timeval timeout;
    timeout.tv_sec = 30;
    timeout.tv_usec = 0;

    fd_set rfds;

    FD_ZERO(&rfds);
    FD_SET(sock, &rfds);

    int ret = select(sock + 1, ((isReadOp) ? &rfds : NULL), ((isReadOp) ? NULL : &rfds), NULL, &timeout);

    if (ret == 0)
    {
        return "Timeout";
    }
    else if (ret == -1)
    {
        return "Error: " + std::to_string(errno);
    }

    return std::string();
}

void restClient::parseEndpoint(std::string& endpoint)
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
}

// Parses the endpoint and set class variables
restClient::restClient(std::string& endpoint)
{
    parseEndpoint(endpoint);

    sock = -1;
    host = NULL;
    bzero(&client, sizeof(client));
}

// Sets sockaddr_in and default headers
std::string restClient::init()
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

// To create and connect to an async socket
// We are making async socket because, read will block the code after 1 Response in case of sync Read
// ie Until socket is diconnected from server
std::string restClient::createAndConnect()
{
    sock = socket(AF_INET, SOCK_STREAM, 0);

    if (sock < 0)
    {
        return "Error at creating socket";
    }

    int flags = fcntl(sock, F_GETFL, 0);

    if (flags == -1)
    {
        return "Error while getting socket flags.";
    }

    flags = flags | O_NONBLOCK;

    int ret = fcntl(sock, F_SETFL, flags);

    if (ret != 0)
    {
        return "Error while setting flag to socket.";
    }

    ret = connect(sock, (struct sockaddr *)&client, sizeof(client));

    if (ret < 0)
    {
        if (errno == EINPROGRESS)
        {
            std::cout << "Waiting for connection to establish ..." << std::endl;
            
            while (true)
            {
                auto error = waitForCompletion(false);

                if (error != "Timeout")
                {
                    break;
                }
            }
        }
        else
        {
            return "Error while establishing connection: " + std::to_string(errno);
        }
    }

    return std::string();
}

// To add additional headers
void restClient::updateHeader(const std::string& key, const std::string& value)
{
    if ((key != "") && (value != ""))
    {
        headers.push_back({key, value});
    }
}

std::string restClient::sendRequest(const std::string& verb, const std::string& body)
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
    ss << body << "\r\n\r\n";

    std::string request = ss.str();

    int ret = send(sock, request.c_str(), request.length(), 0);

    if (ret != (int)request.length()) 
    {
        return "Error sending request: " + std::to_string(errno);
    }

    return std::string();
}

std::string restClient::readResponse(std::vector<char>& data, int& size)
{
    std::cout << "Reading from socket ..." << std::endl;

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
            if (errno == EAGAIN)
            {
                auto ret = waitForCompletion(true);

                // For scenerio when nothing is left to read in socket
                if ((ret == "Timeout") && (data.size() != 0)) 
                {
                    break;
                }
            }
            else
            {
                return "Error while reading response: " + std::to_string(errno);
            }
        }
    }

    return std::string();
}

void restClient::setEndpoint(std::string& endpoint)
{
    parseEndpoint(endpoint);
}

void restClient::setHostName(const std::string& hostName)
{
    this->hostName = hostName;
}

void restClient::setPort(int port)
{
    this->port = port;
}

void restClient::setResource(const std::string& resource)
{
    this->resource = resource;
}

void restClient::setQuery(const std::string& query)
{
    this->query = query;
}

std::string restClient::getHostName()
{
    return hostName;
}

int restClient::getPort()
{
    return port;
}

std::string restClient::getResource()
{
    return resource;
}

std::string restClient::getQuery()
{
    return query;
}

restClient::~restClient()
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