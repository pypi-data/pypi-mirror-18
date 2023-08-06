#include <turbodbc/result_sets/python_result_set.h>

#include <boost/python/class.hpp>
#include <boost/python/def.hpp>

using turbodbc::result_sets::python_result_set;

namespace turbodbc { namespace bindings {


bool has_result_set(std::shared_ptr<turbodbc::result_sets::result_set> result_set_pointer)
{
	return static_cast<bool>(result_set_pointer);
}

python_result_set make_python_result_set(std::shared_ptr<turbodbc::result_sets::result_set> result_set_pointer)
{
	return python_result_set(*result_set_pointer);
}


void for_python_result_set()
{
	boost::python::class_<python_result_set>("ResultSet", boost::python::no_init)
			.def("get_column_info", &python_result_set::get_column_info)
			.def("fetch_row", &python_result_set::fetch_row)
		;

	boost::python::class_<std::shared_ptr<turbodbc::result_sets::result_set>>("RawResultSetPointer", boost::python::no_init);

	boost::python::def("make_row_based_result_set", make_python_result_set);
	boost::python::def("has_result_set", has_result_set);
}

} }
