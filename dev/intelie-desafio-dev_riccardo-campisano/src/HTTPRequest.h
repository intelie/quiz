#ifndef HTTPRequest_H_
#define HTTPRequest_H_

#include <string>
#include <sstream>

class HTTPRequest
{
public:
    explicit HTTPRequest();
    virtual ~HTTPRequest();

    std::string getError();
    bool getPage(std::stringstream& _return_content, std::string _page_url, long _timeout = 0);

private:
    std::string m_reponse_error;
};

#endif
