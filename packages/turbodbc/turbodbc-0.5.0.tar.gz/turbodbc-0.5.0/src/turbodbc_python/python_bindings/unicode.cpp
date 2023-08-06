#include <boost/python.hpp>

namespace turbodbc { namespace bindings {


struct utf8_from_unicode_object {
	static bool is_convertible(PyObject * object)
	{
		return PyUnicode_Check(object);
	}

	static std::string convert(PyObject * object)
	{
		auto utf8 = boost::python::handle<>{PyUnicode_AsUTF8String(object)};
		return PyString_AsString(utf8.get());
	}
};


template<typename Converter>
struct boost_python_converter
{
	using target = decltype(Converter::convert(std::declval<PyObject*>()));

	static void * is_convertible(PyObject* object)
	{
		if(Converter::is_convertible(object)){
			return object;
		} else {
			return nullptr;
		}
	}

	static void convert(PyObject* object, boost::python::converter::rvalue_from_python_stage1_data* data)
	{
		void* storage = (reinterpret_cast<boost::python::converter::rvalue_from_python_storage<target>*>(data))->storage.bytes;
		new (storage) target(Converter::convert(object));
		data->convertible = storage;
	}
};



void for_unicode()
{

	boost::python::converter::registry::push_back(
		& boost_python_converter<utf8_from_unicode_object>::is_convertible,
		& boost_python_converter<utf8_from_unicode_object>::convert,
		boost::python::type_id<typename boost_python_converter<utf8_from_unicode_object>::target>()
	);

}

} }


