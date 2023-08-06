#include <turbodbc/connect.h>

#include <boost/python/def.hpp>

namespace turbodbc { namespace bindings {

void for_connect()
{
    boost::python::def("connect", turbodbc::connect);
}

} }
