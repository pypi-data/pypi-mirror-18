#pragma once

#include <turbodbc_numpy/ndarrayobject.h>

#include <cpp_odbc/multi_value_buffer.h>

#include <boost/python/object.hpp>

namespace turbodbc_numpy {

class masked_column {
public:
	void append(cpp_odbc::multi_value_buffer const & buffer, std::size_t n_values);

	boost::python::object get_data();
	boost::python::object get_mask();

	masked_column(masked_column const &) = delete;
	masked_column & operator=(masked_column const &) = delete;
	virtual ~masked_column();
protected:
	masked_column();
private:
	virtual void do_append(cpp_odbc::multi_value_buffer const & buffer, std::size_t n_values) = 0;

	virtual boost::python::object do_get_data() = 0;
	virtual boost::python::object do_get_mask() = 0;
};

}
