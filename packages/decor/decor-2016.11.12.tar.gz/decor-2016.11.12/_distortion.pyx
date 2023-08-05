#!/usr/bin/env python
# -*- coding: utf-8 -*-

# stolen from pyFai, thanks Jerome

import cython
from cython cimport view
from cython.parallel import prange
cimport numpy
import numpy
from libc.math cimport floor, ceil, fabs
from libc.string cimport memset, memcpy


cdef struct lut_point:
    numpy.int32_t idx
    numpy.float32_t coef


dtype_lut = numpy.dtype([("idx", numpy.int32), ("coef", numpy.float32)])


cpdef inline int clip(int value, int min_val, int max_val) nogil:
    if value < min_val:
        return min_val
    elif value > max_val:
        return max_val
    else:
        return value


@cython.wraparound(False)
@cython.boundscheck(False)
def calc_size(float[:, :, :, :] pos not None, shape):
    cdef:
        int i, j, k, l, shape0, shape1, min0, min1, max0, max1
        numpy.ndarray[numpy.int32_t, ndim = 2] lut_size = numpy.zeros(shape, dtype=numpy.int32)
        float a0, a1, b0, b1, c0, c1, d0, d1
    shape0, shape1 = shape
    with nogil:
        for i in range(shape0):
            for j in range(shape1):
                a0 = pos[i, j, 0, 0]
                a1 = pos[i, j, 0, 1]
                b0 = pos[i, j, 1, 0]
                b1 = pos[i, j, 1, 1]
                c0 = pos[i, j, 2, 0]
                c1 = pos[i, j, 2, 1]
                d0 = pos[i, j, 3, 0]
                d1 = pos[i, j, 3, 1]
                min0 = clip(<int> floor(min(a0, b0, c0, d0)), 0, shape0)
                min1 = clip(<int> floor(min(a1, b1, c1, d1)), 0, shape1)
                max0 = clip(<int> ceil(max(a0, b0, c0, d0)) + 1, 0, shape0)
                max1 = clip(<int> ceil(max(a1, b1, c1, d1)) + 1, 0, shape1)
                for k in range(min0, max0):
                    for l in range(min1, max1):
                        lut_size[k, l] += 1
    return lut_size


@cython.wraparound(False)
@cython.boundscheck(False)
@cython.cdivision(True)
def calc_lut(float[:, :, :, :] pos not None, shape, bin_size, max_pixel_size):
    cdef int i, j, ms, ml, ns, nl, shape0, shape1, delta0, delta1, buffer_size, i0, i1
    cdef int offset0, offset1, box_size0, box_size1, size, k
    cdef numpy.int32_t idx = 0
    cdef float a0, a1, b0, b1, c0, c1, d0, d1, pab, pbc, pcd, pda, cab, cbc, ccd, cda, area, value
    cdef lut_point[:, :, :] lut
    size = bin_size.max()
    shape0, shape1 = shape
    delta0, delta1 = max_pixel_size
    cdef int[:, :] out_max = view.array(shape=(shape0, shape1), itemsize=sizeof(int), format="i")
    out_max[:, :] =0
    cdef float[:, :] buffer = view.array(shape=(delta0, delta1), itemsize=sizeof(float), format="f")
    lut = view.array(shape=(shape0, shape1, size), itemsize=sizeof(lut_point), format="if")
    lut_total_size = shape0 * shape1 * size * sizeof(lut_point)
    memset(&lut[0, 0, 0], 0, lut_total_size)
    buffer_size = delta0 * delta1 * sizeof(float)
    with nogil:
        # i,j, idx are indexes of the raw image uncorrected
        for i in range(shape0):
            for j in range(shape1):
                # reinit of buffer
                buffer[:, :] = 0
                a0 = pos[i, j, 0, 0]
                a1 = pos[i, j, 0, 1]
                b0 = pos[i, j, 1, 0]
                b1 = pos[i, j, 1, 1]
                c0 = pos[i, j, 2, 0]
                c1 = pos[i, j, 2, 1]
                d0 = pos[i, j, 3, 0]
                d1 = pos[i, j, 3, 1]
                offset0 = (<int> floor(min(a0, b0, c0, d0)))
                offset1 = (<int> floor(min(a1, b1, c1, d1)))
                box_size0 = (<int> ceil(max(a0, b0, c0, d0))) - offset0
                box_size1 = (<int> ceil(max(a1, b1, c1, d1))) - offset1
                a0 -= <float> offset0
                a1 -= <float> offset1
                b0 -= <float> offset0
                b1 -= <float> offset1
                c0 -= <float> offset0
                c1 -= <float> offset1
                d0 -= <float> offset0
                d1 -= <float> offset1
                if b0 != a0:
                    pab = (b1 - a1) / (b0 - a0)
                    cab = a1 - pab * a0
                else:
                    pab = cab = 0.0
                if c0 != b0:
                    pbc = (c1 - b1) / (c0 - b0)
                    cbc = b1 - pbc * b0
                else:
                    pbc = cbc = 0.0
                if d0 != c0:
                    pcd = (d1 - c1) / (d0 - c0)
                    ccd = c1 - pcd * c0
                else:
                    pcd = ccd = 0.0
                if a0 != d0:
                    pda = (a1 - d1) / (a0 - d0)
                    cda = d1 - pda * d0
                else:
                    pda = cda = 0.0
                integrate(buffer, b0, a0, pab, cab)
                integrate(buffer, a0, d0, pda, cda)
                integrate(buffer, d0, c0, pcd, ccd)
                integrate(buffer, c0, b0, pbc, cbc)
                area = 0.5 * ((c0 - a0) * (d1 - b1) - (c1 - a1) * (d0 - b0))
                for ms in range(box_size0):
                    ml = ms + offset0
                    if ml < 0 or ml >= shape0:
                        continue
                    for ns in range(box_size1):
                        # ms,ns are indexes of the corrected image in short form, ml & nl are the same
                        nl = ns + offset1
                        if nl < 0 or nl >= shape1:
                            continue
                        value = buffer[ms, ns] / area
                        if value <= 0:
                            continue
                        k = out_max[ml, nl]
                        lut[ml, nl, k].idx = idx
                        lut[ml, nl, k].coef = value
                        out_max[ml, nl] = k + 1
                idx += 1

    # Hack to prevent memory leak !!!
    cdef numpy.ndarray[numpy.float64_t, ndim = 2] tmp_ary = numpy.empty(shape=(shape0*shape1, size),
                                                                        dtype=numpy.float64)
    memcpy(&tmp_ary[0, 0], &lut[0, 0, 0], tmp_ary.nbytes)
    return numpy.core.records.array(tmp_ary.view(dtype=dtype_lut), shape=(shape0 * shape1, size),
                                    dtype=dtype_lut, copy=True)


@cython.wraparound(False)
@cython.boundscheck(False)
@cython.cdivision(True)
cdef inline void integrate(float[:, :] box, float start, float stop, float slope, float intercept) nogil:
    cdef:
        int i, h = 0
        float p, dp, a, aa, da, sign
    if start < stop:  # positive contribution
        p = ceil(start)
        dp = p - start
        if p > stop:  # start and stop are in the same unit
            a = calc_area(start, stop, slope, intercept)
            if a != 0:
                aa = fabs(a)
                sign = a / aa
                da = (stop - start)  # always positive
                h = 0
                while aa > 0:
                    if da > aa:
                        da = aa
                        aa = -1
                    box[(<int> floor(start)), h] += sign * da
                    aa -= da
                    h += 1
        else:
            if dp > 0:
                a = calc_area(start, p, slope, intercept)
                if a != 0:
                    aa = fabs(a)
                    sign = a / aa
                    h = 0
                    da = dp
                    while aa > 0:
                        if da > aa:
                            da = aa
                            aa = -1
                        box[(<int> floor(p)) - 1, h] += sign * da
                        aa -= da
                        h += 1
            # subsection p1->pn
            for i in range((<int> floor(p)), (<int> floor(stop))):
                a = calc_area(i, i + 1, slope, intercept)
                if a != 0:
                    aa = fabs(a)
                    sign = a / aa

                    h = 0
                    da = 1.0
                    while aa > 0:
                        if da > aa:
                            da = aa
                            aa = -1
                        box[i , h] += sign * da
                        aa -= da
                        h += 1
            # Section pn->B
            p = floor(stop)
            dp = stop - p
            if dp > 0:
                a = calc_area(p, stop, slope, intercept)
                if a != 0:
                    aa = fabs(a)
                    sign = a / aa
                    h = 0
                    da = fabs(dp)
                    while aa > 0:
                        if da > aa:
                            da = aa
                            aa = -1
                        box[(<int> floor(p)), h] += sign * da
                        aa -= da
                        h += 1
    elif start > stop:  # negative contribution. Nota is start=stop: no contribution
        p = floor(start)
        if stop > p:  # start and stop are in the same unit
            a = calc_area(start, stop, slope, intercept)
            if a != 0:
                aa = fabs(a)
                sign = a / aa
                da = (start - stop)  # always positive
                h = 0
                while aa > 0:
                    if da > aa:
                        da = aa
                        aa = -1
                    box[(<int> floor(start)), h] += sign * da
                    aa -= da
                    h += 1
        else:
            dp = p - start
            if dp < 0:
                a = calc_area(start, p, slope, intercept)
                if a != 0:
                    aa = fabs(a)
                    sign = a / aa
                    h = 0
                    da = fabs(dp)
                    while aa > 0:
                        if da > aa:
                            da = aa
                            aa = -1
                        box[(<int> floor(p)) , h] += sign * da
                        aa -= da
                        h += 1
            # subsection p1->pn
            for i in range((<int> start), (<int> ceil(stop)), -1):
                a = calc_area(i, i - 1, slope, intercept)
                if a != 0:
                    aa = fabs(a)
                    sign = a / aa
                    h = 0
                    da = 1
                    while aa > 0:
                        if da > aa:
                            da = aa
                            aa = -1
                        box[i - 1, h] += sign * da
                        aa -= da
                        h += 1
            # Section pn->B
            p = ceil(stop)
            dp = stop - p
            if dp < 0:
                a = calc_area(p, stop, slope, intercept)
                if a != 0:
                    aa = fabs(a)
                    sign = a / aa
                    h = 0
                    da = fabs(dp)
                    while aa > 0:
                        if da > aa:
                            da = aa
                            aa = -1
                        box[(<int> floor(stop)), h] += sign * da
                        aa -= da
                        h += 1


cpdef inline float calc_area(float i1, float i2, float slope, float intercept) nogil:
    return 0.5 * (i2 - i1) * (slope * (i2 + i1) + 2 * intercept)


@cython.wraparound(False)
@cython.boundscheck(False)
def correct_lut(image, shape, lut_point[:, :] lut not None):
    cdef int i, j, lshape0, lshape1, idx, size, shape0, shape1
    cdef float coef, sum_, error, t ,y
    cdef float[:] lout, lin
    shape0, shape1 = shape
    # noinspection PyUnresolvedReferences
    lshape0 = lut.shape[0]
    # noinspection PyUnresolvedReferences
    lshape1 = lut.shape[1]
    img_shape = image.shape
    if (img_shape[0] < shape0) or (img_shape[1] < shape1):
        new_image = numpy.zeros((shape0, shape1), dtype=numpy.float32)
        new_image[:img_shape[0], :img_shape[1]] = image
        image = new_image

    out = numpy.zeros(shape, dtype=numpy.float32)
    lout = out.ravel()
    lin = numpy.ascontiguousarray(image.ravel(), dtype=numpy.float32)
    size = lin.size
    for i in prange(lshape0, nogil=True, schedule="static"):
        sum_ = 0.0    # Implement kahan summation
        error = 0.0
        for j in range(lshape1):
            idx = lut[i, j].idx
            coef = lut[i, j].coef
            if coef <= 0:
                continue
            if idx >= size:
                with gil:
                    continue
            y = lin[idx] * coef - error
            t = sum_ + y
            error = (t - sum_) - y
            sum_ = t
        lout[i] += sum_  # this += is for Cython's reduction
    return out[:img_shape[0], :img_shape[1]]
