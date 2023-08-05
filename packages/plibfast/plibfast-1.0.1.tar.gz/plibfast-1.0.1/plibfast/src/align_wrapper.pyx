""" Small Cython file to demonstrate the use of PyArray_SimpleNewFromData
in Cython to create an array from already allocated memory.

Cython enables mixing C-level calls and Python-level calls in the same
file with a Python-like syntax and easy type cohersion. See 
http://cython.org for more information
"""

# Declare the prototype of the C function we are interested in calling
cdef extern from "alloc_aligned_type.c":
	float* c_alloc_aligned_float(size_t size);

cdef extern from "reduction.c":
	float c_reduction(const float * tab, size_t size);

from libc.stdlib cimport free
from cpython cimport PyObject

# We need to build an array-wrapper class to deallocate our array when
# the Python object is deleted.


cdef class PlibArray:
	
	def __cinit__(self,size):
		cdef float *array
		# Call the C function
		array =c_alloc_aligned_float(size)
		self.set_data(size, <float*> array) 
		
	def __dealloc__(self):
		""" Frees the array. This is called by Python when all the
		references to the object are gone. """
		free(<void*>self.data_ptr)
		
	cdef float* data_ptr
	cdef int size
	
	cdef set_data(self, int size, float* data_ptr):
		""" Set the data of the array
		This cannot be done in the constructor as it must recieve C-level
		arguments.
		Parameters:
		-----------
		size: int
			Length of the array.
		data_ptr: float*
			Pointer to the data            
		"""
		self.data_ptr = data_ptr
		self.size = size
		
	def sum(self):
		return c_reduction(self.data_ptr,self.size);
	
	def set_value(self,index,value):
		self.data_ptr[index] = value

