
/***************************************
	Auteur : Pierre Aubert
	Mail : aubertp7@gmail.com
	Licence : CeCILL-C
****************************************/

#ifndef __PLIB_FAST_REDUCTION_H__
#define __PLIB_FAST_REDUCTION_H__

#include "plib_vectorized.h"

#ifdef __cplusplus
extern "C" {
#endif

float plib_fast_reduction_mult64(const float * tab, size_t size);
float plib_fast_reduction_mult32(const float * tab, size_t size);
float plib_fast_reduction_mult16(const float * tab, size_t size);
float plib_fast_reduction_mult8(const float * tab, size_t size);
float plib_fast_reduction(const float * tab, size_t size);

float plib_fast_reduction_sx_sxy_mult32(float * resXY, const float * tabX, const float * tabY, size_t size);
float plib_fast_reduction_block(const float * tab, size_t size);

#ifdef __cplusplus
} /* closing brace for extern "C" */
#endif

#endif

