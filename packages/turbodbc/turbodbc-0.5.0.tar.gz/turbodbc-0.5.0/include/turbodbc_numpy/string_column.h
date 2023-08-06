#pragma once

#include <turbodbc_numpy/masked_column.h>
#include <turbodbc/type_code.h>

#include <boost/python/list.hpp>

namespace turbodbc_numpy {

class string_column : public masked_column {
public:
	string_column();
	virtual ~string_column();

private:
	void do_append(cpp_odbc::multi_value_buffer const & buffer, std::size_t n_values) final;

	boost::python::object do_get_data() final;
	boost::python::object do_get_mask() final;

	boost::python::list data_;
};

}
