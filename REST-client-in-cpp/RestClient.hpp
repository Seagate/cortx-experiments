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

#pragma once

#ifndef REST_CLIENT_HPP
#define REST_CLIENT_HPP

#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>

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