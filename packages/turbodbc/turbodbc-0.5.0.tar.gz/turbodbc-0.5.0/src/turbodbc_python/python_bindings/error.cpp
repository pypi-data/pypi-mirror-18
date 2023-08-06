#include <boost/python.hpp>
#include <cpp_odbc/error.h>

namespace turbodbc { namespace bindings {

//this is for translating into python exceptions that follow a specified inheritance hierarchy
PyObject* createExceptionClass(const char* name, PyObject* baseTypeObj = PyExc_StandardError)
{
	// http://stackoverflow.com/questions/9620268/boost-python-custom-exception-class
	using std::string;
	namespace bp = boost::python;

	string scopeName = bp::extract<string>(bp::scope().attr("__name__"));
	string qualifiedName0 = scopeName + "." + name;
	char* qualifiedName1 = const_cast<char *>(qualifiedName0.c_str());

	PyObject* typeObj = PyErr_NewException(qualifiedName1, baseTypeObj, 0);
	if (not typeObj) {
		bp::throw_error_already_set();
	}
	bp::scope().attr(name) = bp::handle<>(bp::borrowed(typeObj));
	return typeObj;
}

static PyObject* ErrorTypeObject = nullptr;

void translate_odbc_exception(cpp_odbc::error const& error)
{
	PyErr_SetString(ErrorTypeObject, error.what());
}

void for_error()
{
    ErrorTypeObject = createExceptionClass("Error");
    boost::python::register_exception_translator<cpp_odbc::error>(translate_odbc_exception);
}

} }
