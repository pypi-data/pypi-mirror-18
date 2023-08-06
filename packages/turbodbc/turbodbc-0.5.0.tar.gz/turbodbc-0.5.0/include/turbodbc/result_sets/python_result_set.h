#pragma once

#include <turbodbc/result_sets/row_based_result_set.h>
#include <turbodbc/field.h>
#include <turbodbc/field_translator.h>
#include <boost/python/object.hpp>

namespace turbodbc { namespace result_sets {

/**
 * @brief This class adapts a result_set to provide row-based access via
 *        the nullable_field data type
 */
class python_result_set {
public:
	/**
	 * @brief Create a new python_result_set which presents data contained
	 *        in the base result set in a row-based fashion
	 */
	python_result_set(result_set & base);

	/**
	 * @brief Retrieve information about each column in the result set
	 */
	std::vector<column_info> get_column_info() const;

	/**
	 * @brief Retrieve a boost Python object which belong to the next row.
	 * @return Returned object is an empty list in case there is no additional row
	 */
	boost::python::object fetch_row();

private:
	row_based_result_set row_based_;
	std::vector<type_code> types_;
};

} }
