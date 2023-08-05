#include "alloc_aligned_type.h"
#ifndef __APPLE__
#include <malloc.h>
#endif
#include "plib_vectorized.h"
#include <stdio.h>

/// Function that allocates alligned pointer of float
/**	 @param size : number of float to allocate
  *	 @return Aligned pointer of float
  */
float* c_alloc_aligned_float(size_t size){
	#ifndef __APPLE__
	float * data = (float*)memalign(PLIB_VECTOR_SIZE_BYTE,size*sizeof(float));
	#else
	float * data = NULL;
	if (posix_memalign((void*)&data, PLIB_VECTOR_SIZE_BYTE,size*sizeof(float))!=0)
		return NULL;
	#endif
	//printf("PLIB_VECTOR_SIZE_BYTE [%lu]\n", PLIB_VECTOR_SIZE_BYTE);
	//printf("data [%p]\n" , data);
	return data;
}
