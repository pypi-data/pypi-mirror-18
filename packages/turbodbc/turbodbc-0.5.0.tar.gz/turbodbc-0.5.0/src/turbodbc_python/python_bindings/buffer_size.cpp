#include <turbodbc/buffer_size.h>

#include <boost/python/class.hpp>
#include <boost/variant.hpp>

namespace turbodbc { namespace bindings {

struct buffer_size_to_object : boost::static_visitor<PyObject *> {
    static PyObject * convert(buffer_size const& b) {
        return apply_visitor(buffer_size_to_object(), b);
    }

    template<typename T>
    PyObject * operator()(T const& t) const {
        return boost::python::incref(boost::python::object(t).ptr());
    }
};

struct buffer_size_from_object{
    static bool is_convertible (PyObject * object)
    {
        return boost::python::extract<turbodbc::rows>(object).check()
            or boost::python::extract<turbodbc::megabytes>(object).check();
    }

    static buffer_size convert(PyObject * object)
    {
        boost::python::object python_value{boost::python::handle<>{boost::python::borrowed(object)}};

        {
            boost::python::extract<turbodbc::rows> extractor(object);
            if (extractor.check()) {
                return turbodbc::rows(extractor());
            }
        }
        {
            boost::python::extract<turbodbc::megabytes> extractor(object);
            return turbodbc::megabytes(extractor());
        }
    }
};

template<typename Converter> struct boost_python_converter
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

void for_buffer_size()
{
    boost::python::class_<turbodbc::rows>("Rows", boost::python::init<std::size_t>())
        .def_readwrite("rows", &turbodbc::rows::value)
    ;

    boost::python::class_<turbodbc::megabytes>("Megabytes", boost::python::init<std::size_t>())
        .def_readwrite("megabytes", &turbodbc::megabytes::value)
    ;

    boost::python::to_python_converter<buffer_size, buffer_size_to_object>();

    boost::python::converter::registry::push_back(
		& boost_python_converter<buffer_size_from_object>::is_convertible,
		& boost_python_converter<buffer_size_from_object>::convert,
		boost::python::type_id<typename boost_python_converter<buffer_size_from_object>::target>()
	);

}

} }