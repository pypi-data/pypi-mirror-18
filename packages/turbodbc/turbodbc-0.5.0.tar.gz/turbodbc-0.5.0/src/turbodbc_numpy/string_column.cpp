#include <turbodbc_numpy/string_column.h>

#include <boost/python/str.hpp>

#include <sql.h>
#include <cstring>

namespace turbodbc_numpy {


string_column::string_column()
{
}


string_column::~string_column() = default;

void string_column::do_append(cpp_odbc::multi_value_buffer const & buffer, std::size_t n_values)
{
	for (std::size_t i = 0; i != n_values; ++i) {
		auto const element = buffer[i];
		if (element.indicator == SQL_NULL_DATA) {
			data_.append(boost::python::object());
		} else {
			data_.append(boost::python::object(boost::python::handle<>(PyUnicode_FromString(element.data_pointer))));
		}
	}
}

boost::python::object string_column::do_get_data()
{
	return data_;
}

boost::python::object string_column::do_get_mask()
{
	return boost::python::object(false);
}


}

