#include <iostream>
#include <sstream>
#include <string>
#include "HTTPRequest.h"
#include "JSONParser.h"
#include "StringUtils.h"

// Author Riccardo Campisano
// riccardo.campisano@gmail.com

//#define DEBUG true

#ifdef DEBUG
#define LOG(WHAT) std::cout << WHAT << std::endl;
#else
#define LOG(WHAT) /*WHAT*/
#endif

// requested libraries:
// libcurl http://curl.haxx.se/libcurl/
// json-c http://oss.metaparadigm.com/json-c/
// debian installation: apt-get install libcurl3 libjson0-dev
// compilation:
// g++ -I/usr/include/json src/main.cpp src/HTTPRequest.cpp src/JSONParser.cpp src/StringUtils.cpp -ljson -lcurl

// from https://developers.google.com/web-search/docs/#fonje
// service format q=Paris%20Hilton&userip=USERS-IP-ADDRESS"
#define GOOGLE_SERVICE_URL "https://ajax.googleapis.com/ajax/services/search/web?v=1.0&"
#define GOOGLE_SERVICE_STATUS "responseStatus"
#define GOOGLE_SERVICE_DATA "responseData"
#define GOOGLE_SERVICE_RESULTS "results"
#define GOOGLE_SERVICE_QUERY "title"

#define FREEGEOIP_SERVICE_URL "http://freegeoip.net/json/"
#define FREEGEOIP_SERVICE_QUERY "ip"

int main(int _num_args, char** _data_args)
{
    if(_num_args != 2)
    {
        std::cerr << "Usage: " << _data_args[0] << " <STRING_TO_SEARCH>" << std::endl;
        std::cerr << " tips: use \" to define a query with spaces, ex \"Paris Hilton\"" << std::endl;

        return -1;
    }

    std::string requested_query = _data_args[1];
    LOG(std::endl << "Requested query: " << requested_query << std::endl);

    std::string query = requested_query;
    size_t find_pos = requested_query.find(" ");

    while (find_pos != std::string::npos)
    {
        query.replace(find_pos, 1, "%20");
        find_pos = query.find(" ", find_pos);
    }

    std::stringstream text_response;
    HTTPRequest http_request;

    std::string ip;
    // IP web search
    {
        LOG("FreeGeoIP request: " << FREEGEOIP_SERVICE_URL);

        if(http_request.getPage(text_response, FREEGEOIP_SERVICE_URL))
        {
            LOG("FreeGeoIP response_________________________________________");
            LOG(text_response.str());
            LOG("___END_____________________________________________________" << std::endl);
            JSONParser json_response(text_response.str());

            if(!json_response.getString(ip, FREEGEOIP_SERVICE_QUERY))
            {
                LOG("FreeGeoIP response unknown");
                ip = "127.0.0.1";
            }
        }
        else
        {
            LOG("FreeGeoIP response error");
            ip = "127.0.0.1";
        }
    }

    LOG("Your ip: " << ip << std::endl);

    text_response.str("");

    //q=Paris%20Hilton&userip=USERS-IP-ADDRESS"
    std::stringstream request_url;
    request_url << GOOGLE_SERVICE_URL << "q=" << query << "&userip=" << ip;
    LOG("GOOGLE requesting url: " << request_url.str() << std::endl);

    if(!http_request.getPage(text_response, request_url.str()))
    {
        std::cerr << "Google query request failed: " << http_request.getError() << std::endl;

        return -2;
    }

    LOG("GOOGLE response____________________________________________");
    LOG(text_response.str());
    LOG("___END_____________________________________________________" << std::endl);

    JSONParser json_response(text_response.str());
    std::string requested_text;

    if(!json_response.getString(requested_text, GOOGLE_SERVICE_STATUS))
    {
        std::cerr << "Google query unknown response: " << http_request.getError() << std::endl;

        return -3;
    }

    if(requested_text != "200")
    {
        std::cerr << "Google query response error code: " << requested_text << std::endl << std::endl;
        std::cerr << "Response data:" << std::endl << text_response.str() << std::endl << std::endl;

        return -4;
    }

    if (! (json_response.navigateTo(GOOGLE_SERVICE_DATA) &&
           json_response.navigateTo(GOOGLE_SERVICE_RESULTS)))
    {
        std::cerr << "Google query unknown response: " << http_request.getError() << std::endl;

        return -5;
    }

    std::list<std::string> list_titles;

    if(!json_response.getListOfElementsWithName(list_titles, GOOGLE_SERVICE_QUERY))
    {
        std::cerr << "Google query unknown response: " << http_request.getError() << std::endl;

        return -6;
    }

    std::list<std::string>::iterator it;
    int total = 0;
    int titles = 0;
    int occurences;

    for(it = list_titles.begin(); it != list_titles.end(); ++it)
    {
        occurences = StringUtils::countLevenshteinOccurrencesWithMaxDistance(*(it), requested_query, 2);
        std::cout << "COUNT: " << occurences << " title: " << *(it) << std::endl;

        total += occurences;

        if(occurences>0)
        {
            ++titles;
        }
    }

    std::cout << "Total occurences: " << total << std::endl;
    std::cout << "Titles containing at least one occurence: " << titles << std::endl;


    return 0;
}
