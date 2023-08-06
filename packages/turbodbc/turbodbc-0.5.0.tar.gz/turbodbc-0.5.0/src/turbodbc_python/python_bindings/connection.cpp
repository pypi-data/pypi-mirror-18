#include <turbodbc/connection.h>

#include <boost/python/class.hpp>

namespace turbodbc { namespace bindings {

void for_connection()
{
	boost::python::class_<turbodbc::connection>("Connection", boost::python::no_init)
    		.def("commit", &turbodbc::connection::commit)
    		.def("rollback", &turbodbc::connection::rollback)
    		.def("cursor", &turbodbc::connection::make_cursor)
    		.def("get_buffer_size", &turbodbc::connection::get_buffer_size)
    		.def("set_buffer_size", &turbodbc::connection::set_buffer_size)
    		.def_readwrite("parameter_sets_to_buffer", &turbodbc::connection::parameter_sets_to_buffer)
			.def_readwrite("use_async_io", &turbodbc::connection::use_async_io)
    	;
}

} }
