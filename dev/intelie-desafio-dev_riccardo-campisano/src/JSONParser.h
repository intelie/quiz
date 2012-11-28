#ifndef JSONParser_H_
#define JSONParser_H_

#include <list>
#include <string>

class JSONParser
{
public:
    explicit JSONParser(std::string _json_string);
    virtual ~JSONParser();

    std::string getError();
    void backToRoot();
    bool navigateTo(std::string _node_name);
    bool getString(std::string& _return_string, std::string _node_name);
    bool getListOfElementsWithName(std::list<std::string>& _list_titles, std::string _node_name);

private:
    void* m_response;
    void* m_actual_node;
    std::string m_reponse_error;
};

#endif
