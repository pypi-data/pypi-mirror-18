#pragma once

#include <turbodbc_numpy/masked_column.h>
#include <turbodbc/type_code.h>

#include <functional>

namespace turbodbc_numpy {

class datetime_column : public masked_column {
public:
	datetime_column(turbodbc::type_code type);
	virtual ~datetime_column();

	typedef std::function<long (char const * data_pointer)> converter;
private:
	void do_append(cpp_odbc::multi_value_buffer const & buffer, std::size_t n_values) final;

	boost::python::object do_get_data() final;
	boost::python::object do_get_mask() final;

	void resize(std::size_t new_size);

	turbodbc::type_code type_;
	boost::python::object data_;
	boost::python::object mask_;
	std::size_t size_;
	converter converter_;
};

}
