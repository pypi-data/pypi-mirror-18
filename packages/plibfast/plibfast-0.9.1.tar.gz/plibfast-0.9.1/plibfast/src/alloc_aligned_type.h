#ifndef __ALLOC_ALIGNED_TYPE_H__
#define __ALLOC_ALIGNED_TYPE_H__
#include <Python.h>

#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif
float* c_alloc_aligned_float(size_t size);
#ifdef __cplusplus
}
#endif

#endif
