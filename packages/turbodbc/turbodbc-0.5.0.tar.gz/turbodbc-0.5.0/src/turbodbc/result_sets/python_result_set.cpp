#include <turbodbc/result_sets/python_result_set.h>

#include <turbodbc/make_field_translator.h>

#include <boost/python/list.hpp>
#include <boost/python/long.hpp>

#include <sql.h>
#include <Python.h>
#include <datetime.h> // Python header


namespace turbodbc { namespace result_sets {

namespace {

	boost::python::object make_date(SQL_DATE_STRUCT const & date)
	{
		return boost::python::object(boost::python::handle<>(PyDate_FromDate(date.year,
		                                                                     date.month,
		                                                                     date.day)));
	}

	boost::python::object make_timestamp(SQL_TIMESTAMP_STRUCT const & ts)
	{
		// map SQL nanosecond precision to microsecond precision
		long const adjusted_fraction = ts.fraction / 1000;
		return boost::python::object(
				boost::python::handle<>(PyDateTime_FromDateAndTime(ts.year, ts.month, ts.day,
				                                                   ts.hour, ts.minute, ts.second, adjusted_fraction))
			);
	}

	boost::python::object make_object(turbodbc::type_code code, char const * data_pointer)
	{
		switch (code) {
			case type_code::boolean:
				return boost::python::object(*reinterpret_cast<bool const *>(data_pointer));
			case type_code::integer:
				return boost::python::object(*reinterpret_cast<long const *>(data_pointer));
			case type_code::floating_point:
				return boost::python::object(*reinterpret_cast<double const *>(data_pointer));
			case type_code::string:
				return boost::python::object(boost::python::handle<>(PyUnicode_FromString(data_pointer)));
			case type_code::date:
				return make_date(*reinterpret_cast<SQL_DATE_STRUCT const *>(data_pointer));
			case type_code::timestamp:
				return make_timestamp(*reinterpret_cast<SQL_TIMESTAMP_STRUCT const *>(data_pointer));
			default:
				throw std::logic_error("Encountered unsupported type code");
		}
	}

}


python_result_set::python_result_set(result_set & base) :
	row_based_(base)
{
	PyDateTime_IMPORT;
	for (auto const & info : row_based_.get_column_info()) {
		types_.emplace_back(info.type);
	}
}

std::vector<column_info> python_result_set::get_column_info() const
{
	return row_based_.get_column_info();
}


boost::python::object python_result_set::fetch_row()
{
	auto const row = row_based_.fetch_row();
	if (not row.empty()) {
		boost::python::list python_row;
		for (std::size_t column = 0; column != row.size(); ++column) {
			if (row[column].indicator == SQL_NULL_DATA) {
				python_row.append(boost::python::object());
			} else {
				python_row.append(make_object(types_[column], row[column].data_pointer));
			}
		}
		return python_row;
	} else {
		return boost::python::list();
	}
}



} }
