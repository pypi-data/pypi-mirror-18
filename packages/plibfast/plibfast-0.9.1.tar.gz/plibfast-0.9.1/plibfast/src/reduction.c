#include "plib_fast_reduction.h"


/// Function that allocates alligned pointer of float
/**	 @param size : number of float to allocate
  *	 @return Aligned pointer of float
  */ 
float c_reduction(const float * tab, size_t size){
	return plib_fast_reduction(tab,size);
}


