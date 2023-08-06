#include <turbodbc/parameter.h>

#include <cstring>

namespace turbodbc {

parameter::parameter(cpp_odbc::statement const & statement, std::size_t one_based_index, std::size_t buffered_rows, std::unique_ptr<description const> description) :
	description_(std::move(description)),
	buffer_(description_->element_size(), buffered_rows)
{
	statement.bind_input_parameter(one_based_index, description_->column_c_type(), description_->column_sql_type(), buffer_);
}

parameter::~parameter() = default;

cpp_odbc::multi_value_buffer & parameter::get_buffer()
{
	return buffer_;
}


bool parameter::is_suitable_for(type_code code, std::size_t value_size) const
{
	bool const has_suitable_type = (code == description_->get_type_code());
	bool const is_large_enough = (value_size <= description_->element_size());
	return has_suitable_type and is_large_enough;
}


void move_to_top(parameter & param, std::size_t row_index)
{
	auto & buffer = param.get_buffer();
	auto destination = buffer[0];
	auto const & source = buffer[row_index];
	std::memcpy(destination.data_pointer, source.data_pointer, buffer.capacity_per_element());
	destination.indicator = source.indicator;
}

}
