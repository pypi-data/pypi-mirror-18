#include <turbodbc_numpy/numpy_result_set.h>

#include <boost/python/module.hpp>
#include <boost/python/class.hpp>
#include <boost/python/def.hpp>

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
// compare http://docs.scipy.org/doc/numpy/reference/c-api.array.html#importing-the-api
// as to why this define is necessary
#define PY_ARRAY_UNIQUE_SYMBOL turbodbc_numpy_API
#include <numpy/ndarrayobject.h>

using turbodbc_numpy::numpy_result_set;

namespace {

numpy_result_set make_numpy_result_set(std::shared_ptr<turbodbc::result_sets::result_set> result_set_pointer)
{
	return numpy_result_set(*result_set_pointer);
}

}


BOOST_PYTHON_MODULE(turbodbc_numpy_support)
{
	import_array();
	boost::python::class_<numpy_result_set>("NumpyResultSet", boost::python::no_init)
			.def("fetch_all", &numpy_result_set::fetch_all)
		;

	boost::python::def("make_numpy_result_set", make_numpy_result_set);
}
