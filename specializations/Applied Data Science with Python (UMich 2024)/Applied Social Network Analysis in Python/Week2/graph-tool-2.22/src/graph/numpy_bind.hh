// graph-tool -- a general graph modification and manipulation thingy
//
// Copyright (C) 2006-2017 Tiago de Paula Peixoto <tiago@skewed.de>
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 3
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.

#ifndef NUMPY_BIND_HH
#define NUMPY_BIND_HH

#include <vector>
#include <boost/python.hpp>

// numpy unique symbol weirdness
#define PY_ARRAY_UNIQUE_SYMBOL graph_tool_numpy
#ifndef NUMPY_EXPORT
#define NO_IMPORT_ARRAY
#endif
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include "numpy/arrayobject.h"

#include <boost/array.hpp>
#define BOOST_DISABLE_ASSERTS
#include <boost/multi_array.hpp>

#include <boost/type_traits.hpp>
#include <boost/mpl/int.hpp>
#include <boost/mpl/vector.hpp>
#include <boost/mpl/map.hpp>
#include <boost/mpl/pair.hpp>
#include <boost/mpl/for_each.hpp>

#include "demangle.hh"

typedef boost::mpl::map<
    boost::mpl::pair<bool, boost::mpl::int_<NPY_BOOL> >,
    boost::mpl::pair<char, boost::mpl::int_<NPY_CHAR> >,
    boost::mpl::pair<int8_t, boost::mpl::int_<NPY_INT8> >,
    boost::mpl::pair<uint8_t, boost::mpl::int_<NPY_UINT8> >,
    boost::mpl::pair<int16_t, boost::mpl::int_<NPY_INT16> >,
    boost::mpl::pair<uint16_t, boost::mpl::int_<NPY_UINT16> >,
    boost::mpl::pair<int32_t, boost::mpl::int_<NPY_INT32> >,
    boost::mpl::pair<uint32_t, boost::mpl::int_<NPY_UINT32> >,
    boost::mpl::pair<int64_t, boost::mpl::int_<NPY_INT64> >,
    boost::mpl::pair<uint64_t, boost::mpl::int_<NPY_UINT64> >,
    boost::mpl::pair<unsigned long, boost::mpl::int_<NPY_ULONG> >,
    boost::mpl::pair<float, boost::mpl::int_<NPY_FLOAT> >,
    boost::mpl::pair<double, boost::mpl::int_<NPY_DOUBLE> >,
    boost::mpl::pair<long double, boost::mpl::int_<NPY_LONGDOUBLE> >,
    boost::mpl::pair<std::complex<float>, boost::mpl::int_<NPY_CFLOAT> >,
    boost::mpl::pair<std::complex<double>, boost::mpl::int_<NPY_CDOUBLE> >,
    boost::mpl::pair<std::complex<long double>, boost::mpl::int_<NPY_CLONGDOUBLE> > 
    > numpy_types;

template <class ValueType>
boost::python::object wrap_vector_owned(const std::vector<ValueType>& vec)
{
    size_t val_type = boost::mpl::at<numpy_types,ValueType>::type::value;
    npy_intp size[1];
    size[0] = vec.size();
    PyArrayObject* ndarray;
    if (vec.empty())
    {
        ndarray = (PyArrayObject*) PyArray_SimpleNew(1, size, val_type);
    }
    else
    {
        ValueType* new_data = new ValueType[vec.size()];
        memcpy(new_data, vec.data(), vec.size() * sizeof(ValueType));
        ndarray = (PyArrayObject*) PyArray_SimpleNewFromData(1, size, val_type,
                                                             new_data);
    }
    PyArray_ENABLEFLAGS(ndarray, NPY_ARRAY_ALIGNED | NPY_ARRAY_C_CONTIGUOUS |
                        NPY_ARRAY_OWNDATA | NPY_ARRAY_WRITEABLE);
    boost::python::handle<> x((PyObject*) ndarray);
    boost::python::object o(x);
    return o;
}

template <class ValueType>
boost::python::object wrap_vector_not_owned(std::vector<ValueType>& vec)
{
    PyArrayObject* ndarray;
    size_t val_type = boost::mpl::at<numpy_types,ValueType>::type::value;
    npy_intp size = vec.size();
    if (vec.empty())
        return wrap_vector_owned(vec); // return an _owned_ array of size one.
    ndarray = (PyArrayObject*) PyArray_SimpleNewFromData(1, &size, val_type,
                                                         vec.data());
    PyArray_ENABLEFLAGS(ndarray,NPY_ARRAY_ALIGNED | NPY_ARRAY_C_CONTIGUOUS |
                        NPY_ARRAY_WRITEABLE);
    boost::python::handle<> x((PyObject*) ndarray);
    boost::python::object o(x);
    return o;
}

template <class ValueType, size_t Dim>
boost::python::object wrap_vector_owned(const std::vector<std::array<ValueType, Dim>>& vec)
{
    size_t n = vec.size() * Dim;
    size_t val_type = boost::mpl::at<numpy_types,ValueType>::type::value;
    PyArrayObject* ndarray;
    if (n == 0)
    {
        npy_intp size[1];
        size[0] = vec.size();
        ndarray = (PyArrayObject*) PyArray_SimpleNew(1, size, val_type);
    }
    else
    {
        ValueType* new_data = new ValueType[n];
        memcpy(new_data, vec.data(), n * sizeof(ValueType));
        npy_intp shape[2] = {int(vec.size()), int(Dim)};
        ndarray = (PyArrayObject*) PyArray_SimpleNewFromData(Dim, shape,
                                                             val_type,
                                                             new_data);
    }
    PyArray_ENABLEFLAGS(ndarray, NPY_ARRAY_ALIGNED | NPY_ARRAY_F_CONTIGUOUS |
                        NPY_ARRAY_OWNDATA | NPY_ARRAY_WRITEABLE);
    boost::python::handle<> x((PyObject*) ndarray);
    boost::python::object o(x);
    return o;
}

template <class ValueType, size_t Dim>
boost::python::object wrap_vector_not_owned(const std::vector<std::array<ValueType, Dim>>& vec)
{
    size_t val_type = boost::mpl::at<numpy_types,ValueType>::type::value;
    if (vec.empty())
        return wrap_vector_owned(vec); // return an _owned_ array of size one.
    npy_intp shape[2] = {int(vec.size()), int(Dim)};
    PyArrayObject* ndarray =
        (PyArrayObject*) PyArray_SimpleNewFromData(Dim, shape, val_type,
                                                   vec.data());
    PyArray_ENABLEFLAGS(ndarray, NPY_ARRAY_ALIGNED | NPY_ARRAY_F_CONTIGUOUS |
                        NPY_ARRAY_WRITEABLE);
    boost::python::handle<> x((PyObject*) ndarray);
    boost::python::object o(x);
    return o;
}

template <class ValueType, size_t Dim>
boost::python::object
wrap_multi_array_owned(const boost::multi_array<ValueType,Dim>& array)
{
    ValueType* new_data = new ValueType[array.num_elements()];
    memcpy(new_data, array.data(), array.num_elements() * sizeof(ValueType));
    size_t val_type = boost::mpl::at<numpy_types,ValueType>::type::value;
    npy_intp shape[Dim];
    for (size_t i = 0; i < Dim; ++i)
        shape[i] = array.shape()[i];
    PyArrayObject* ndarray =
        (PyArrayObject*) PyArray_SimpleNewFromData(Dim, shape, val_type,
                                                   new_data);
    PyArray_ENABLEFLAGS(ndarray, NPY_ARRAY_ALIGNED | NPY_ARRAY_C_CONTIGUOUS |
                        NPY_ARRAY_OWNDATA | NPY_ARRAY_WRITEABLE);
    boost::python::handle<> x((PyObject*) ndarray);
    boost::python::object o(x);
    return o;
}

template <class ValueType, size_t Dim>
boost::python::object
wrap_multi_array_not_owned(boost::multi_array<ValueType,Dim>& array)
{
    size_t val_type = boost::mpl::at<numpy_types,ValueType>::type::value;
    PyArrayObject* ndarray =
        (PyArrayObject*) PyArray_SimpleNewFromData(Dim, array.shape(), val_type,
                                                   array.origin());
    PyArray_ENABLEFLAGS(ndarray, NPY_ARRAY_ALIGNED | NPY_ARRAY_C_CONTIGUOUS |
                        NPY_ARRAY_WRITEABLE);
    boost::python::handle<> x((PyObject*) ndarray);
    boost::python::object o(x);
    return o;
}

// get multi_array_ref from numpy ndarrays

template <class ValueType, size_t dim>
class numpy_multi_array:
    public boost::multi_array_ref<ValueType,dim>
{
    typedef boost::multi_array_ref<ValueType,dim> base_t;
public:
    template <class ExtentList, class StrideList>
    explicit numpy_multi_array(typename base_t::element* data,
                               const ExtentList& sizes,
                               const StrideList& strides)
        : base_t(data, sizes)
    {
        for (size_t i = 0; i < dim; ++i)
            base_t::stride_list_[i] = strides[i];
    }
};

struct InvalidNumpyConversion:
    public std::exception
{
    std::string _error;
public:
    InvalidNumpyConversion(const std::string& error) :_error(error) {}
    ~InvalidNumpyConversion() throw () {}
    const char * what () const throw () {return _error.c_str();}
};

template <class ValueType, size_t dim>
boost::multi_array_ref<ValueType,dim> get_array(boost::python::object points)
{
    PyArrayObject* pa = (PyArrayObject*) points.ptr();

    if (PyArray_NDIM(pa) != dim)
        throw InvalidNumpyConversion("invalid array dimension!");

    if (boost::mpl::at<numpy_types,ValueType>::type::value != PyArray_DESCR(pa)->type_num)
    {
        boost::python::handle<> x(boost::python::borrowed((PyObject*) PyArray_DESCR(pa)->typeobj));
        boost::python::object dtype(x);
        std::string type_name = boost::python::extract<std::string>(boost::python::str(dtype));
        std::string error = "invalid array value type: " + type_name;
        error += " (id: " + boost::lexical_cast<std::string>(PyArray_DESCR(pa)->type_num) + ")";
        error += ", wanted: " + name_demangle(typeid(ValueType).name());
        error += " (id: " + boost::lexical_cast<std::string>(boost::mpl::at<numpy_types,ValueType>::type::value) + ")";
        throw InvalidNumpyConversion(error);
    }

    std::vector<size_t> shape(dim);
    for (size_t i = 0; i < dim; ++i)
        shape[i] = PyArray_DIMS(pa)[i];

    std::vector<size_t> stride(dim);
    for (size_t i = 0; i < dim; ++i)
        stride[i] = PyArray_STRIDE(pa, i) / sizeof(ValueType);

    return numpy_multi_array<ValueType,dim>((ValueType *) PyArray_DATA(pa),
                                            shape, stride);

    // boost::storage_order_type store;
    // if ((PyArray_FLAGS(pa) ^ NPY_ARRAY_C_CONTIGUOUS) != 0)
    //     store = boost::c_storage_order();
    // if (PyArray_FLAGS(pa) ^ NPY_ARRAY_F_CONTIGUOUS) != 0)
    //     store = boost::fortran_storage_order();

}

#endif // NUMPY_BIND_HH
