#include "JSONParser.h"

#include <iostream>
#include <json.h>

JSONParser::JSONParser(std::string _json_string) : m_reponse_error("")
{
    MC_SET_DEBUG(1);
    json_object* json_response = json_tokener_parse(_json_string.c_str());
    m_response = (void*) json_response;
    m_actual_node = m_response;
}

JSONParser::~JSONParser()
{
    json_object* json_response = (json_object*) m_response;
    json_object_put(json_response);
    m_actual_node = 0;
    m_response = 0;
}

std::string JSONParser::getError()
{
    return m_reponse_error;
}

void JSONParser::backToRoot()
{
    m_actual_node = m_response;
}

bool JSONParser::navigateTo(std::string _node_name)
{
    json_object* json_actual_node = (json_object*) m_actual_node;

    json_object* json_subnode = json_object_object_get(json_actual_node, _node_name.c_str());

    if(is_error(json_subnode))
    {
        m_reponse_error = json_tokener_errors[-(unsigned long)json_actual_node];
        std::cerr << "json_tokener_parse() failed: " << m_reponse_error << std::endl;

        return false;
    }

    m_actual_node = (void*)json_subnode;

    return true;
}

bool JSONParser::getString(std::string& _return_string, std::string _node_name)
{
    json_object* json_actual_node = (json_object*) m_actual_node;

    if(is_error(json_actual_node))
    {
        m_reponse_error = json_tokener_errors[-(unsigned long)json_actual_node];
        std::cerr << "json_tokener_parse() failed: " << m_reponse_error << std::endl;

        return false;
    }

    json_object* json_ip = json_object_object_get(json_actual_node, _node_name.c_str());

    if(is_error(json_ip))
    {
        m_reponse_error = json_tokener_errors[-(unsigned long)json_ip];
        std::cerr << "json_object_object_get() failed: " << m_reponse_error << std::endl;

        return false;
    }

    _return_string = json_object_get_string(json_ip);
    m_reponse_error = "";

    return true;
}

bool JSONParser::getListOfElementsWithName(std::list<std::string>& _list_titles, std::string _node_name)
{
    json_object* json_actual_node = (json_object*) m_actual_node;

    if(! json_object_is_type(json_actual_node, json_type_array))
    {
        m_reponse_error ="json_type is not json_type_array";
        std::cerr << m_reponse_error << std::endl;

        return false;
    }
    /*
    json_object_object_foreach(json_actual_node, node_name, json_subnode)
    {
        if(_node_name.compare(node_name) == 0 )
        {
            _list_titles.push_back(json_object_get_string(json_subnode));
        }
    }
    */
    int array_len = json_object_array_length(json_actual_node);
    json_object* json_element;
    json_object* json_element_node;
    const char* element_node_value;

    for (int i=0; i<array_len; ++i)
    {
        json_element = json_object_array_get_idx(json_actual_node, i);
        //_list_titles.push_back(json_object_get_string(json_element));
        json_element_node = json_object_object_get(json_element, _node_name.c_str());

        if(!is_error(json_element_node))
        {
            element_node_value = json_object_get_string(json_element_node);

            if(element_node_value != NULL)
            {
                _list_titles.push_back(element_node_value);
            }
        }
    }

    return true;
}
