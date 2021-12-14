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
#include <vector>
#include <map>

#include "RestClient.hpp"

// Check if response was successful
bool checkResponse(std::vector<char>& response)
{
    std::string temp = std::string(response.begin(), response.end());

    if ((temp.find("HTTP/1.1 1") != -1) || (temp.find("HTTP/1.1 2") != -1) || (temp.find("HTTP/1.1 3") != -1))
    {
        return true;
    }

    return false;
}

// Display overall results of all the requests
void displayResult(std::map<bool, int>& result)
{
    std::cout << "Number of Requests made: " << 5 << std::endl;
    std::cout << "Number of successful Requests: " << result[true] << std::endl;
    std::cout << "Number of failed Requests: " << result[false] << std::endl;
}

// You can test the class my running this main()
int main(int argc, char* argv[])
{
    if ((argc > 4) || (argc < 3))
    {
        std::cout << "Usage: ./a.out [endpoint] [body(optional)]" << std::endl;
        return -1;
    }
    else
    {
        std::string httpVerb = argv[1], endpoint = argv[2], choice;
        std::string body = ((argc == 4) ? argv[3]: ""); 
        std::map<bool, int> result;

        restClient rc(endpoint);
        std::string ret = rc.init();

        if (ret != "")
        {
            std::cout << "Init failed: " << ret << std::endl;
            return -1;
        }

        ret = rc.createAndConnect();

        if (ret != "")
        {
            std::cout << "createAndConnect() failed: " << ret << std::endl;
            return -1;
        }

        for (int i = 0; i < 5; i++)
        {
            std::cout << "Request Number: " << i + 1 << std::endl;

            // It asks for verb, endpoint and body to make next requests
            // For first request, all info was already provided by command-line
            if (i != 0)
            {
                std::cout << "Verb: ";
                std::cin >> httpVerb;
                std::cout << "Endpoint: ";
                std::cin >> endpoint;
                rc.setEndpoint(endpoint);

                std::cout << "Do you want to provide a body?(y/n) ";
                std::cin >> choice;

                if ((choice == "y") || (choice == "Y"))
                {
                    std::cout << "Body: ";
                    std::cin >> body;
                }
                else
                {
                    body = "";
                }
            }

            // if user wants to specify any explicit headers 
            while (true)
            {
                std::cout << "Are there any additional headers?(y/n)" << std::endl;
                std::cin >> choice;

                if ((choice == "n") || (choice == "N"))
                {
                    break;
                }

                std::string key, value;

                std::cout << "Enter key: ";
                std::cin >> key;
                std::cout << "Enter value: ";
                std::cin >> value;

                rc.updateHeader(key, value);
            }

            ret = rc.sendRequest(httpVerb, body);

            if (ret != "")
            {
                std::cout << "sendRequest() failed: " << ret << std::endl;
                return -1;
            }
            
            std::vector<char> data;
            int size = 0;

            ret = rc.readResponse(data, size);

            if (ret != "")
            {
                std::cout << "readResponse failed: " << ret << std::endl;
            }

            std::cout << "Response:" << std::endl;
            for (int i = 0; i < size; i++)
            {
                std::cout << data[i];
            }
            std::cout << std::endl;

            auto check = checkResponse(data);
            result[check]++;    
        }

        displayResult(result);
        return 0;
    }
}
