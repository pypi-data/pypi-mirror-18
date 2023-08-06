#include "turbodbc/connection.h"
#include <sqlext.h>

namespace turbodbc {

connection::connection(std::shared_ptr<cpp_odbc::connection const> low_level_connection) :
	parameter_sets_to_buffer(1000),
	use_async_io(false),
	buffer_size_(megabytes(20)),
	connection_(low_level_connection)
{
	connection_->set_attribute(SQL_ATTR_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF);
}

void connection::commit() const
{
	connection_->commit();
}

void connection::rollback() const
{
	connection_->rollback();
}

cursor connection::make_cursor() const
{
	return {connection_, buffer_size_, parameter_sets_to_buffer, use_async_io};
}

turbodbc::buffer_size connection::get_buffer_size() const
{
    return buffer_size_;
}

void connection::set_buffer_size(turbodbc::buffer_size buffer_size)
{
    buffer_size_ = buffer_size;
}

}
