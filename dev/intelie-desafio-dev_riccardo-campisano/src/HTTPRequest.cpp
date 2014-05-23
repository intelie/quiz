#include "HTTPRequest.h"

#include <curl/curl.h>
#include <iostream>

namespace
{
    static size_t write_data(void* _ptr, size_t _size, size_t _nmemb, void* _stringstream)
    {
        if(_stringstream)
        {
            std::stringstream* ss = static_cast<std::stringstream*>(_stringstream);
            std::streamsize len = _size * _nmemb;
            ss->write(static_cast<char*>(_ptr), len);

            return _nmemb;
        }

        return 0;
    }
}

HTTPRequest::HTTPRequest() : m_reponse_error("")
{

}

HTTPRequest::~HTTPRequest()
{

}

std::string HTTPRequest::getError()
{
    return m_reponse_error;
}

bool HTTPRequest::getPage(std::stringstream& _return_content, std::string _page_url, long _timeout)
{
    bool retval;

    curl_global_init(CURL_GLOBAL_DEFAULT);
    CURL* curl_handle = curl_easy_init();

    if(curl_handle)
    {
        curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, &write_data);
        curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA, &_return_content);
        curl_easy_setopt(curl_handle, CURLOPT_NOPROGRESS, 1L);
        curl_easy_setopt(curl_handle, CURLOPT_FOLLOWLOCATION, 1L);
        curl_easy_setopt(curl_handle, CURLOPT_TIMEOUT, _timeout);
        curl_easy_setopt(curl_handle, CURLOPT_URL, _page_url.c_str());

        CURLcode curl_response = curl_easy_perform(curl_handle);

        if(curl_response != CURLE_OK)
        {
            m_reponse_error = curl_easy_strerror(curl_response);
            std::cerr << "curl_easy_perform() failed: " << m_reponse_error << std::endl;
        }
        else
        {
            retval = true;
            m_reponse_error = "";
        }

        curl_easy_cleanup(curl_handle);
    }
    else
    {
        m_reponse_error = "curl_easy_init() failed";
    }

    curl_global_cleanup();

    return retval;
}
