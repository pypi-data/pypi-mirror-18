#ifndef __REDUCTION_H__
#define __REDUCTION_H__
#include <Python.h>

#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif
float c_reduction(const float * tab, size_t size);
#ifdef __cplusplus
}
#endif

#endif


