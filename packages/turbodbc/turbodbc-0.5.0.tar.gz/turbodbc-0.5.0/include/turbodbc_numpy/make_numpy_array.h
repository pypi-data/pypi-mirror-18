#pragma once

#include <turbodbc_numpy/numpy_type.h>

#include <boost/python/object.hpp>

namespace turbodbc_numpy {

/**
 * @brief Create new, empty numpy array based on numpy type constants or a
 *        type's string representation
 */
boost::python::object make_empty_numpy_array(numpy_type const & type);
boost::python::object make_empty_numpy_array(std::string const & descriptor);

}
