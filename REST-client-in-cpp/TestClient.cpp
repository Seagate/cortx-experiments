#include <iostream>
#include <vector>
#include <map>

#include "RestClient.hpp"

bool checkResponse(std::vector<char>& response)
{
    std::string temp = std::string(response.begin(), response.end());

    if ((temp.find("HTTP/1.1 1") != -1) || (temp.find("HTTP/1.1 2") != -1) || (temp.find("HTTP/1.1 3") != -1))
    {
        return true;
    }

    return false;
}

void displayResult(std::map<bool, int>& result)
{
    std::cout << "Number of Requests made: " << 5 << std::endl;
    std::cout << "Number of successful Requests: " << result[true] << std::endl;
    std::cout << "Number of failed Requests: " << result[false] << std::endl;
}

int main()
{
    char choice;
    std::string httpVerb, endpoint, body; 
    std::map<bool, int> result;

    for (int i = 0; i < 5; i++)
    {
        std::cout << "Request Number: " << i + 1 << std::endl;

        std::cout << "Verb: ";
        std::cin >> httpVerb;
        std::cout << "Endpoint: ";
        std::cin >> endpoint;

        std::cout << "Do you want to provide a body?(y/n) ";
        std::cin >> choice;

        if ((choice == 'y') || (choice == 'Y'))
        {
            std::cout << "Body: ";
            std::cin >> body;
        }
        else
        {
            body = "";
        }

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

        cin.clear();
        cin.ignore(100 , '\n');

        while (true)
        {
            std::cout << "Are there any additional headers?(y/n)" << std::endl;
            std::cin >> choice;

            if ((choice == 'n') || (choice == 'N'))
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