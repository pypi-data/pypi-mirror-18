#pragma once

#include <turbodbc/result_sets/row_based_result_set.h>
#include <turbodbc/field.h>
#include <turbodbc/field_translator.h>
#include <boost/python/object.hpp>

namespace turbodbc_numpy {

/**
 * @brief This class adapts a result_set to provide access in
 *        terms of numpy python objects
 */
class numpy_result_set {
public:
	/**
	 * @brief Create a new numpy_result_set which presents data contained
	 *        in the base result set in a row-based fashion
	 */
	numpy_result_set(turbodbc::result_sets::result_set & base);

	/**
	 * @brief Retrieve a boost Python object which contains
	 *        values and masks for all data
	 */
	boost::python::object fetch_all();

private:
	turbodbc::result_sets::result_set & base_result_;
};

}
