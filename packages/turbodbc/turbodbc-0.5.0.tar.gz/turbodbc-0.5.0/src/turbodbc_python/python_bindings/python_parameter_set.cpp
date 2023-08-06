#include <turbodbc_python/python_parameter_set.h>
#include <turbodbc/cursor.h>

#include <boost/python/class.hpp>
#include <boost/python/def.hpp>

namespace turbodbc { namespace bindings {


python_parameter_set make_parameter_set(cursor & cursor)
{
	return {cursor.get_command()->get_parameters()};
}


void for_python_parameter_set()
{
	boost::python::class_<python_parameter_set>("ParameterSet", boost::python::no_init)
			.def("add_set", &python_parameter_set::add_parameter_set)
			.def("flush", &python_parameter_set::flush)
		;

	boost::python::def("make_parameter_set", make_parameter_set);
}

} }
