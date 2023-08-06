#include <turbodbc_numpy/make_numpy_array.h>

#include <turbodbc_numpy/ndarrayobject.h>

namespace turbodbc_numpy {


boost::python::object make_empty_numpy_array(numpy_type const & type)
{
	npy_intp no_elements = 0;
	int const flags = 0;
	int const one_dimensional = 1;
	// __extension__ needed because of some C/C++ incompatibility.
	// see issue https://github.com/numpy/numpy/issues/2539
	return boost::python::object{boost::python::handle<>(__extension__ PyArray_New(&PyArray_Type,
																				   one_dimensional,
																				   &no_elements,
																				   type.code,
																				   nullptr,
																				   nullptr,
																				   type.size,
																				   flags,
																				   nullptr))};
}


boost::python::object make_empty_numpy_array(std::string const & descriptor)
{
	npy_intp no_elements = 0;
	int const flags = 0;
	int const one_dimensional = 1;
	// __extension__ needed because of some C/C++ incompatibility.
	// see issue https://github.com/numpy/numpy/issues/2539
	PyArray_Descr * descriptor_ptr = nullptr;
	__extension__ PyArray_DescrConverter(boost::python::object(descriptor).ptr(), &descriptor_ptr);

	// descriptor_ptr reference is stolen
	return boost::python::object{boost::python::handle<>(__extension__ PyArray_NewFromDescr(&PyArray_Type,
																							descriptor_ptr,
																							one_dimensional,
																							&no_elements,
																							nullptr,
																							nullptr,
																							flags,
																							nullptr))};
}

}
