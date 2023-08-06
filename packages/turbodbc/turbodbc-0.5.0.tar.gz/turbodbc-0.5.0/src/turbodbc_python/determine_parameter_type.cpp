#include <turbodbc_python/determine_parameter_type.h>

#include <boost/python/extract.hpp>

#include <stdexcept>

#include <datetime.h> // Python header


namespace turbodbc {

namespace {

	struct datetime_initializer {
		datetime_initializer()
		{
			PyDateTime_IMPORT;
		}
	};

	static const datetime_initializer required_for_datetime_interaction;

	std::size_t const size_not_important = 0;

	void set_integer(boost::python::object const & value, cpp_odbc::writable_buffer_element & destination)
	{
		boost::python::extract<long> extractor(value);
		*reinterpret_cast<long *>(destination.data_pointer) = extractor();
		destination.indicator = sizeof(long);
	}

	void set_floating_point(boost::python::object const & value, cpp_odbc::writable_buffer_element & destination)
	{
		boost::python::extract<double> extractor(value);
		*reinterpret_cast<double *>(destination.data_pointer) = extractor();
		destination.indicator = sizeof(double);
	}

	void set_string(boost::python::object const & value, cpp_odbc::writable_buffer_element & destination)
	{
		boost::python::extract<std::string> extractor(value);
		auto const s = extractor();
		auto const length_with_null_termination = s.size() + 1;
		std::memcpy(destination.data_pointer, s.c_str(), length_with_null_termination);
		destination.indicator = s.size();
	}

	void set_date(boost::python::object const & value, cpp_odbc::writable_buffer_element & destination)
	{
		auto ptr = value.ptr();
		auto d = reinterpret_cast<SQL_DATE_STRUCT *>(destination.data_pointer);

		d->year = PyDateTime_GET_YEAR(ptr);
		d->month = PyDateTime_GET_MONTH(ptr);
		d->day = PyDateTime_GET_DAY(ptr);

		destination.indicator = sizeof(SQL_DATE_STRUCT);
	}

	void set_timestamp(boost::python::object const & value, cpp_odbc::writable_buffer_element & destination)
	{
		auto ptr = value.ptr();
		auto d = reinterpret_cast<SQL_TIMESTAMP_STRUCT *>(destination.data_pointer);

		d->year = PyDateTime_GET_YEAR(ptr);
		d->month = PyDateTime_GET_MONTH(ptr);
		d->day = PyDateTime_GET_DAY(ptr);
		d->hour = PyDateTime_DATE_GET_HOUR(ptr);
		d->minute = PyDateTime_DATE_GET_MINUTE(ptr);
		d->second = PyDateTime_DATE_GET_SECOND(ptr);
		// map microsecond precision to SQL nanosecond precision
		d->fraction = PyDateTime_DATE_GET_MICROSECOND(ptr) * 1000;

		destination.indicator = sizeof(SQL_TIMESTAMP_STRUCT);
	}

}
//	class set_field_for : public boost::static_visitor<> {
//	public:
//		set_field_for(cpp_odbc::writable_buffer_element & destination) :
//				destination_(destination)
//		{}
//
//		void operator()(bool const & value)
//		{
//			*destination_.data_pointer = (value ? 1 : 0);
//			destination_.indicator = 1;
//		}
//
//		void operator()(long const & value)
//		{
//			*reinterpret_cast<long *>(destination_.data_pointer) = value;
//			destination_.indicator = sizeof(long);
//		}
//
//		void operator()(double const & value)
//		{
//			*reinterpret_cast<double *>(destination_.data_pointer) = boost::get<double>(value);
//			destination_.indicator = sizeof(double);
//		}
//
//		void operator()(boost::posix_time::ptime const & value)
//		{
//			auto const & date = value.date();
//			auto const & time = value.time_of_day();
//			auto destination = reinterpret_cast<SQL_TIMESTAMP_STRUCT *>(destination_.data_pointer);
//
//			destination->year = date.year();
//			destination->month = date.month();
//			destination->day = date.day();
//			destination->hour = time.hours();
//			destination->minute = time.minutes();
//			destination->second = time.seconds();
//			// map posix_time microsecond precision to SQL nanosecond precision
//			destination->fraction = time.fractional_seconds() * 1000;
//
//			destination_.indicator = sizeof(SQL_TIMESTAMP_STRUCT);
//		}
//
//		void operator()(boost::gregorian::date const & value)
//		{
//			auto destination = reinterpret_cast<SQL_DATE_STRUCT *>(destination_.data_pointer);
//
//			destination->year = value.year();
//			destination->month = value.month();
//			destination->day = value.day();
//
//			destination_.indicator = sizeof(SQL_DATE_STRUCT);
//		}
//
//		void operator()(std::string const & value)
//		{
//			auto const length_with_null_termination = value.size() + 1;
//			std::memcpy(destination_.data_pointer, value.c_str(), length_with_null_termination);
//			destination_.indicator = value.size();
//		}
//
//	private:
//		cpp_odbc::writable_buffer_element & destination_;
//	};
//
//}

python_parameter_info determine_parameter_type(boost::python::object const & value)
{
	{
		boost::python::extract<long> extractor(value);
		if (extractor.check()) {
			return {set_integer, type_code::integer, size_not_important};
		}
	}
	{
		boost::python::extract<double> extractor(value);
		if (extractor.check()) {
			return {set_floating_point, type_code::floating_point, size_not_important};
		}
	}
	{
		boost::python::extract<std::string> extractor(value);
		if (extractor.check()) {
			auto const temp = extractor();
			return {set_string, type_code::string, temp.size()};
		}
	}

	auto ptr = value.ptr();
	if (PyDateTime_Check(ptr)) {
		return {set_timestamp, type_code::timestamp, size_not_important};
	}

	if (PyDate_Check(ptr)) {
		return {set_date, type_code::date, size_not_important};
	}

	throw std::runtime_error("Could not convert python value to C++");
}


}