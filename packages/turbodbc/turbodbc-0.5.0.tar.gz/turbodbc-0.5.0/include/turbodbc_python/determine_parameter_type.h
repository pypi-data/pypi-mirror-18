#pragma once

#include <turbodbc/parameter.h>
#include <cpp_odbc/multi_value_buffer.h>

#include <boost/python/object.hpp>

namespace turbodbc {

struct python_parameter_info {
	using parameter_converter = void(*)(boost::python::object const &, cpp_odbc::writable_buffer_element &);

	parameter_converter converter;
	type_code type;
	std::size_t size;
};

python_parameter_info determine_parameter_type(boost::python::object const & value);

}