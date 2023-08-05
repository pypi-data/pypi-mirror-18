
/***************************************
	Auteur : Pierre Aubert
	Mail : aubertp7@gmail.com
	Licence : CeCILL-C
****************************************/

#ifndef __PLIB_VECTORIZED_H__
#define __PLIB_VECTORIZED_H__

#include "plib_vectorized_def.h"

#ifndef NOVECTORIZATION
#	ifdef PLIB_AVX
		///Size of the vectorial register in bytes
#		define PLIB_VECTOR_SIZE_BYTE 32lu
		///Size of the vectorial register in float
#		define PLIB_VECTOR_SIZE_FLOAT 8lu
		///Size of the vectorial register in double
#		define PLIB_VECTOR_SIZE_DOUBLE 4lu
#		ifdef PLIB_AVX2
			///Size of an SSSE3 vector register in long int
#			define PLIB_VECTOR_SIZE_LONG_INT 4lu
			///Size of an SSSE3 vector register in int
#			define PLIB_VECTOR_SIZE_INT 8lu
			///Size of an SSSE3 vector register in short
#			define PLIB_VECTOR_SIZE_SHORT 16lu
			///Size of an SSSE3 vector register in char
#			define PLIB_VECTOR_SIZE_CHAR 32lu
#		elif defined PLIB_SSSE3
			///Size of an SSSE3 vector register in long int
#			define PLIB_VECTOR_SIZE_LONG_INT 2lu
			///Size of an SSSE3 vector register in int
#			define PLIB_VECTOR_SIZE_INT 4lu
			///Size of an SSSE3 vector register in short
#			define PLIB_VECTOR_SIZE_SHORT 8lu
			///Size of an SSSE3 vector register in char
#			define PLIB_VECTOR_SIZE_CHAR 16lu
#		endif
#	elif defined PLIB_SSE4
		///Size of the vectorial register in bytes
#		define PLIB_VECTOR_SIZE_BYTE 16lu
		///Size of the vectorial register in float
#		define PLIB_VECTOR_SIZE_FLOAT 4lu
		///Size of the vectorial register in double
#		define PLIB_VECTOR_SIZE_DOUBLE 2lu
#		ifdef PLIB_SSSE3
			///Size of an SSSE3 vector register in long int
#			define PLIB_VECTOR_SIZE_LONG_INT 2lu
			///Size of an SSSE3 vector register in int
#			define PLIB_VECTOR_SIZE_INT 4lu
			///Size of an SSSE3 vector register in short
#			define PLIB_VECTOR_SIZE_SHORT 8lu
			///Size of an SSSE3 vector register in char
#			define PLIB_VECTOR_SIZE_CHAR 16lu
#		endif
#	endif
#else
//No vectorization extention, so define scalar macro
#	define PLIB_VECTOR_SIZE_BYTE 4lu
	///Size of the vectorial register in float
#	define PLIB_VECTOR_SIZE_FLOAT 1lu
	///Size of the vectorial register in double
#	define PLIB_VECTOR_SIZE_DOUBLE 1lu
	///Size of a vector register in long int
#	define PLIB_VECTOR_SIZE_LONG_INT 1lu
	///Size of a vector register in int
#	define PLIB_VECTOR_SIZE_INT 1lu
	///Size of a vector register in short
#	define PLIB_VECTOR_SIZE_SHORT 1lu
	///Size of a vector register in char
#	define PLIB_VECTOR_SIZE_CHAR 1lu
	///To avoid __builtin_assume_aligned gcc function
#	define __builtin_assume_aligned(X,Y) (X)
#endif

#endif

