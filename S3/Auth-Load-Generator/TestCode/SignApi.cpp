/**
 * @file SignApi.cpp
 *
 * This module contains the implementation of the Aws::SignApi class.
 *
 * © 2018 by Richard Walters
 */

#include <algorithm>
#include "SignApi.hpp"
#include "Hmac.hpp"
#include "Sha2.hpp"
#include "Templates.hpp"
#include "Server.hpp"
#include <map>
#include "MessageHeaders.hpp"
#include <sstream>
#include <string>
#include "StringExtensions.hpp"
#include <vector>
#include <stdlib.h>
#include <iostream>
namespace {

    /**
     * This is the identifier defined by Amazon for the hash algorithm
     * used to make message digests in this module.
     */
    static const char* const HASH_ALGORITHM = "AWS4-HMAC-SHA256";

    /**
     * Breaks the given string at each instance of the given delimiter,
     * returning the pieces as a collection of substrings.  The delimiter
     * characters are removed.
     *
     * @param[in] s
     *     This is the string to split.
     *
     * @param[in] d
     *     This is the delimiter character at which to split the string.
     *
     * @return
     *     The collection of substrings that result from breaking the given
     *     string at each delimiter character is returned.
     */
    std::vector< std::string > Split(
        const std::string& s,
        char d
    ) {
        std::vector< std::string > values;
        auto remainder = s;
        while (!remainder.empty()) {
            auto delimiter = remainder.find_first_of(d);
            if (delimiter == std::string::npos) {
                values.push_back(remainder);
                remainder.clear();
            } else {
                values.push_back(remainder.substr(0, delimiter));
                remainder = remainder.substr(delimiter + 1);
            }
        }
        return values;
    }

    /**
     * This function returns the hex digit that corresponds
     * to the given value.
     *
     * @param[in] value
     *     This is the value to convert to a hex digit.
     *
     * @return
     *     The hex digit corresponding to the given value is returned.
     */
    char MakeHexDigit(unsigned int value) {
        if (value < 10) {
            return (char)(value + '0');
        } else {
            return (char)(value - 10 + 'A');
        }
    }

    /**
     * Encode the given string according to Amazon's strange notion of
     * what it means to "URI Encode" something (pretty much the same as
     * the equivalent to the ABNF *(unreserved / pct-encoded) which is
     * definitely NOT what RFC 3986 says a query string can be, which
     * is *(pchar / "/" / "?").  But heck, who reads Internet standards
     * these days, eh?
     *
     * @param[in] s
     *     This is the string to encode.
     *
     * @return
     *     The output of the Amazon brand of "URI Encode" applied
     *     to the given string is returned.
     */
    std::string AmzUriEncode(const std::string& s) {
        std::string output;
        for (uint8_t c: s) {
            if (
                ((c >= 'A') && (c <= 'Z'))
                || ((c >= 'a') && (c <= 'z'))
                || ((c >= '0') && (c <= '9'))
                || (c == '-')
                || (c == '_')
                || (c == '.')
                || (c == '~')
            ) {
                output.push_back(c);
            } else {
                output.push_back('%');
                output.push_back(MakeHexDigit((unsigned int)c >> 4));
                output.push_back(MakeHexDigit((unsigned int)c & 0x0F));
            }
        }
        return output;
    }

    /**
     * This function replaces sequences of two or more spaces with a single
     * space, to meet the requirement of header values in canonical API
     * requests, that multiple spaces should be replaced by a single space.
     *
     * @param[in] s
     *     This is the string for which to replace multiple spaces with a
     *     single space.
     *
     * @return
     *     The given string, with multiple spaces replaced by a single space,
     *     is returned.
     */
    std::string CanonicalizeSpaces(const std::string& s) {
        std::ostringstream output;
        bool lastCharWasSpace = false;
        for (const auto& c: s) {
            if (c == ' ') {
                if (!lastCharWasSpace) {
                    lastCharWasSpace = true;
                    output << ' ';
                }
            } else {
                output << c;
                lastCharWasSpace = false;
            }
        }
        return output.str();
    }

}

namespace Aws {

    std::string SignApi::ConstructCanonicalRequest(const std::string& rawRequest) {
        Http::Server server;
        const auto request = server.ParseRequest(rawRequest);
        if (request == nullptr) {
           return "";
        }
        std::ostringstream canonicalRequest;

        // The following steps should match those shown here:
        // https://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

        // Step 1
        canonicalRequest << request->method << "\n";
//	std::cout<<"canonicalRequest(1)" << canonicalRequest.str();
        // Step 2
        Uri::Uri requestPath;
        requestPath.SetPath(request->target.GetPath());
        requestPath.NormalizePath();
        //canonicalRequest << requestPath.GenerateString() << "\n";
        canonicalRequest << "/1" << "\n";

//	std::cout<<"canonicalRequest(2)" << canonicalRequest.str();
        // Step 3
        if (request->target.HasQuery()) {
            const auto requestQuery = request->target.GetQuery();
            const auto parametersString = Split(requestQuery, '&');
            struct Parameter {
                std::string name;
                std::string value;
            };
            std::vector< Parameter > parametersVector;
            for (const auto& parameter: parametersString) {
                const auto delimiter = parameter.find('=');
                if (delimiter == std::string::npos) {
                    parametersVector.push_back({parameter, ""});
                } else {
                    parametersVector.push_back({
                        parameter.substr(0, delimiter),
                        parameter.substr(delimiter + 1)
                    });
                }
            }
            std::sort(
                parametersVector.begin(),
                parametersVector.end(),
                [](
                    const Parameter& lhs,
                    const Parameter& rhs
                ) {
                    if (lhs.name < rhs.name) {
                        return true;
                    } else if (lhs.name > rhs.name) {
                        return false;
                    } else {
                        return lhs.value < rhs.value;
                    }
                }
            );
            bool first = true;
            for (const auto& parameter: parametersVector) {
                if (first) {
                    first = false;
                } else {
                    canonicalRequest << '&';
                }
                canonicalRequest << AmzUriEncode(parameter.name) << '=' << AmzUriEncode(parameter.value);
            }
        }
        canonicalRequest << "\n";

//	std::cout<<"canonicalRequest(3)" << canonicalRequest.str();
        // Step 4
        std::map<
            std::string,
            std::vector< std::string >
        > headersByName;
        for (const auto& header: request->headers.GetAll()) {
            auto& headerValues = headersByName[StringExtensions::ToLower(header.name)];
            headerValues.push_back(CanonicalizeSpaces(header.value));
        }
        struct Header {
            std::string name;
            std::vector< std::string > values;
        };
        std::vector< Header > headersVector;
        headersVector.reserve(headersByName.size());
        for (auto& header: headersByName) {
            headersVector.push_back({
                header.first,
                header.second
            });
        }
        std::sort(
            headersVector.begin(),
            headersVector.end(),
            [](
                const Header& lhs,
                const Header& rhs
            ) {
                return (lhs.name < rhs.name);
            }
        );
        for (const auto& header: headersVector) {
            canonicalRequest << header.name << ':' << StringExtensions::Join(header.values, ",") << "\n";
        }
        canonicalRequest << "\n";

//	std::cout<<"canonicalRequest(4)" << canonicalRequest.str();

        // Step 5
        bool first = true;
        for (const auto& header: headersVector) {
            if (first) {
                first = false;
            } else {
                canonicalRequest << ';';
            }
            canonicalRequest << header.name;
        }
        canonicalRequest << "\n";
//	std::cout<<"canonicalRequest(5)" << canonicalRequest.str();
	
	request->body = "Action=ListAccounts&ShowAll=False";
        // Step 6
        canonicalRequest << Hash::StringToString< Hash::Sha256 >(request->body);

//	std::cout<<"canonicalRequest(6)" << canonicalRequest.str();
        // Done.  Return constructed request.
        return canonicalRequest.str();
    }

    std::string SignApi::MakeStringToSign(
        const std::string& region,
        const std::string& service,
        const std::string& canonicalRequest
    ) {
        std::ostringstream output;
        std::string dateTime;
        for (const auto& line: StringExtensions::Split(canonicalRequest, '\n')) {
            if (line.substr(0, 11) == "x-amz-date:") {
                dateTime = line.substr(11);
                break;
            }
        }
        output
            << HASH_ALGORITHM << "\n"
            << dateTime << "\n"
            << dateTime.substr(0, 8) << "/" << region << "/" << service << "/aws4_request\n"
            << Hash::StringToString< Hash::Sha256 >(canonicalRequest);
//	std::cout<<"string to sign"<< output.str();
        return output.str();
    }

    std::string SignApi::MakeAuthorization(
        const std::string& stringToSign,
        const std::string& canonicalRequest,
        const std::string& accessKeyId,
        const std::string& accessKeySecret
    ) {
        std::ostringstream output;
        const auto credentialScope = StringExtensions::Split(stringToSign, '\n')[2];
        const auto credentialScopeParts = StringExtensions::Split(credentialScope, '/');
        const auto date = credentialScopeParts[0];
        const auto region = credentialScopeParts[1];
        const auto service = credentialScopeParts[2];
        const auto terminationString = credentialScopeParts[3];
        const auto hmacRawStringToBytes = Hash::MakeHmacStringToBytesFunction(
            Hash::StringToBytes< Hash::Sha256 >,
            Hash::SHA256_BLOCK_SIZE
        );
        const auto hmacBytesToBytes = Hash::MakeHmacBytesToBytesFunction(
            Hash::Sha256,
            Hash::SHA256_BLOCK_SIZE
        );
        const auto hmacBytesToHexString = Hash::MakeHmacBytesToStringFunction(
            Hash::BytesToString< Hash::Sha256 >,
            Hash::SHA256_BLOCK_SIZE
        );

//	std::cout << "MAKE AUTHORIZATION";
	//std::cout << "date"<< date; 
        const auto signingKey = hmacBytesToBytes(
            hmacBytesToBytes(
                hmacBytesToBytes(
                    hmacRawStringToBytes(
                        "AWS4" + accessKeySecret,
                        date
                    ),
                    std::vector< uint8_t >(region.begin(), region.end())
                ),
                std::vector< uint8_t >(service.begin(), service.end())
            ),
            std::vector< uint8_t >(terminationString.begin(), terminationString.end())
        );
        //std::cout << signingKey<<' ';
	//std::cout <<  std::endl;
        const auto signature = hmacBytesToHexString(
            signingKey,
            std::vector< uint8_t >(stringToSign.begin(), stringToSign.end())
        );
        const auto canonicalRequestLines = StringExtensions::Split(canonicalRequest, '\n');
        const auto signedHeaders = canonicalRequestLines[canonicalRequestLines.size() - 2];
        output
            << HASH_ALGORITHM
            << " Credential=" << accessKeyId << "/" << credentialScope
            << ", SignedHeaders=" << signedHeaders
            << ", Signature=" << signature;
//	std::cout<<"Make Auth"<<output.str();
        return output.str();
    }

}
