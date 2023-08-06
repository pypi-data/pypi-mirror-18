#include <stdlib.h>
#include <math.h>
#include <stdint.h>
#include <memory.h>
#include "distortion.h"


void destroy_distortion(distortion *dist) {
    destroy_lut(dist);
    if (dist) {
        free(dist);
        dist = NULL;
    }
}


distortion *init_distortion() {
    distortion *dist;

    dist = malloc(sizeof(distortion));
    if (!dist)
        return NULL;
    dist->lut_size = NULL;
    dist->pos = NULL;
    dist->lut_coef = NULL;
    dist->lut_idx = NULL;
    dist->out_max = NULL;
    dist->buffer = NULL;
    dist->dim1 = 0;
    dist->dim2 = 0;
    dist->array_size = 0;
    dist->lut_size_max = 0;
    dist->delta0 = 0;
    dist->delta1 = 0;
    dist->buffer_size = 0;
    return dist;
}


void destroy_aux(distortion *dist) {
    if (dist) {
        if (dist->out_max) {
            free(dist->out_max);
            dist->out_max = NULL;
        }
        if (dist->buffer) {
            free(dist->buffer);
            dist->buffer = NULL;
        }
        if (dist->lut_size) {
            free(dist->lut_size);
            dist->lut_size = NULL;
        }
        if (dist->pos) {
            free(dist->pos);
            dist->pos = NULL;
        }
    }
}


void destroy_lut(distortion *dist) {
    if (dist) {
        if (dist->lut_coef) {
            free(dist->lut_coef);
            dist->lut_coef = NULL;
        }
        if (dist->lut_idx) {
            free(dist->lut_idx);
            dist->lut_idx = NULL;
        }
    }
    destroy_aux(dist);
}


distortion *init_lut(distortion* dist) {
    dist->lut_size = calloc(dist->array_size, sizeof(uint32_t));
    dist->pos = malloc(dist->array_size * 4 * 2 * sizeof(float));
    if (!dist->lut_size || !dist->pos) {
        destroy_lut(dist);
        return NULL;
    }
    return dist;
}


static int clip(int value, int min, int max) {
    if (value < min)
        return min;
    else if (value > max)
        return max;
    else
        return value;
}


static float min4(float a, float b, float c, float d) {
    a = a < b ? a : b;
    c = c < d ? c : d;
    return a < c ? a : c;
}


static float max4(float a, float b, float c, float d) {
    a = a > b ? a : b;
    c = c > d ? c : d;
    return a > c ? a : c;
}


void calc_lut_size(distortion *dist) {
    int i, j, k, l, m, min0, min1, max0, max1;
    float a0, a1, b0, b1, c0, c1, d0, d1;

    for (i=0; i<dist->dim1; ++i) {
        for (j=0; j<dist->dim2; ++j) {
            a0 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+0*2+0];
            a1 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+0*2+1];
            b0 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+1*2+0];
            b1 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+1*2+1];
            c0 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+2*2+0];
            c1 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+2*2+1];
            d0 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+3*2+0];
            d1 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+3*2+1];
            min0 = clip((int)floor(min4(a0, b0, c0, d0)), 0, dist->dim1);
            min1 = clip((int)floor(min4(a1, b1, c1, d1)), 0, dist->dim2);
            max0 = clip((int)ceil(max4(a0, b0, c0, d0))+1, 0, dist->dim1);
            max1 = clip((int)ceil(max4(a1, b1, c1, d1))+1, 0, dist->dim2);
            for (k=min0; k<max0; ++k) {
                for (l=min1; l<max1; ++l) {
                    m = k * dist->dim2 + l;
                    dist->lut_size[m]++;
                    if (dist->lut_size[m] > dist->lut_size_max)
                        dist->lut_size_max = dist->lut_size[m];
                }
            }
        }
    }
}


static float calc_area(float i1, float i2, float slope, float intercept) {
    return 0.5 * (i2 - i1) * (slope * (i2 + i1) + 2 * intercept);
}


static void integrate(distortion *dist, float start, float stop, float slope, float intercept) {
    int i, h, idx;
    float p, dp, a, aa, da, sign;

    h = 0;
    if (start < stop) {
        p = ceil(start);
        dp = p - start;
        if (p > stop) {
            a = calc_area(start, stop, slope, intercept);
            if (a != 0) {
                aa = fabs(a);
                sign = a / aa;
                da = stop - start;
                h = 0;
                while (aa > 0) {
                    if (da > aa) {
                        da = aa;
                        aa = -1;
                    }
                    idx = ((int)floor(start)) * dist->delta1 + h;
                    dist->buffer[idx] += sign * da;
                    aa -= da;
                    h++;
                }
            }
        } else {
            if (dp > 0) {
                a = calc_area(start, p, slope, intercept);
                if (a != 0) {
                    aa = fabs(a);
                    sign = a / aa;
                    h = 0;
                    da = dp;
                    while (aa > 0) {
                        if (da > aa) {
                            da = aa;
                            aa = -1;
                        }
                        idx = (((int)floor(p)) - 1) * dist->delta1 + h;
                        dist->buffer[idx] += sign * da;
                        aa -= da;
                        h++;
                    }
                }
            }
            for (i=(int)floor(p); i<(int)floor(stop); ++i) {
                a = calc_area(i, i + 1, slope, intercept);
                if (a != 0) {
                    aa = fabs(a);
                    sign = a / aa;
                    h = 0;
                    da = 1.0;
                    while (aa > 0) {
                        if (da > aa) {
                            da = aa;
                            aa = -1;
                        }
                        idx = i * dist->delta1 + h;
                        dist->buffer[idx] += sign * da;
                        aa -= da;
                        h++;
                    }
                }
            }
            p = floor(stop);
            dp = stop - p;
            if (dp > 0) {
                a = calc_area(p, stop, slope, intercept);
                if (a != 0) {
                    aa = fabs(a);
                    sign = a / aa;
                    h = 0;
                    da = fabs(dp);
                    while (aa > 0) {
                        if (da > aa) {
                            da = aa;
                            aa = -1;
                        }
                        idx = ((int)floor(p)) * dist->delta1 + h;
                        dist->buffer[idx] += sign * da;
                        aa -= da;
                        h++;
                    }
                }
            }
        }
    } else if (start > stop) {
        p = floor(start);
        if (stop > p) {
            a = calc_area(start, stop, slope, intercept);
            if (a != 0) {
                aa = fabs(a);
                sign = a / aa;
                da = start - stop;
                h = 0;
                while (aa > 0) {
                    if (da > aa) {
                        da = aa;
                        aa = -1;
                    }
                    idx = ((int)floor(start)) * dist->delta1 + h;
                    dist->buffer[idx] += sign * da;
                    aa -= da;
                    h++;
                }
            }
        } else {
            dp = p - start;
            if (dp < 0) {
                a = calc_area(start, p, slope, intercept);
                if (a != 0) {
                    aa = fabs(a);
                    sign = a / aa;
                    h = 0;
                    da = fabs(dp);
                    while (aa > 0) {
                        if (da > aa) {
                            da = aa;
                            aa = -1;
                        }
                        idx = ((int)floor(p)) * dist->delta1 + h;
                        dist->buffer[idx] += sign * da;
                        aa -= da;
                        h++;
                    }
                }
            }
            for (i=(int)start; i>(int)ceil(stop); --i) {
                a = calc_area(i, i - 1, slope, intercept);
                if (a != 0) {
                    aa = fabs(a);
                    sign = a / aa;
                    h = 0;
                    da = 1;
                    while (aa > 0) {
                        if (da > aa) {
                            da = aa;
                            aa = -1;
                        }
                        idx = (i - 1) * dist->delta1 + h;
                        dist->buffer[idx] += sign * da;
                        aa -= da;
                        h++;
                    }
                }
            }
            p = ceil(stop);
            dp = stop - p;
            if (dp < 0) {
                a = calc_area(p, stop, slope, intercept);
                if (a != 0) {
                    aa = fabs(a);
                    sign = a / aa;
                    h = 0;
                    da = fabs(dp);
                    while (aa > 0) {
                        if (da > aa) {
                            da = aa;
                            aa = -1;
                        }
                        idx = ((int)floor(stop)) * dist->delta1 + h;
                        dist->buffer[idx] += sign * da;
                        aa -= da;
                        h++;
                    }
                }
            }
        }
    }
}


void calc_lut_table(distortion *dist) {
    int i, j, ms, ml, ns, nl, offset0, offset1, box_size0, box_size1, k, m, n, idx;
    float a0, a1, b0, b1, c0, c1, d0, d1, pab, pbc, pcd, pda, cab, cbc, ccd, cda, area, value, o0, o1;

    idx = 0;
    for (i=0; i<dist->dim1; ++i) {
        for (j=0; j<dist->dim2; ++j) {
            a0 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+0*2+0];
            a1 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+0*2+1];
            b0 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+1*2+0];
            b1 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+1*2+1];
            c0 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+2*2+0];
            c1 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+2*2+1];
            d0 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+3*2+0];
            d1 = dist->pos[i*(dist->dim2*4*2)+j*(4*2)+3*2+1];
            o0 = floor(min4(a0, b0, c0, d0));
            o1 = floor(min4(a1, b1, c1, d1));
            offset0 = (int)o0;
            offset1 = (int)o1;
            box_size0 = ((int)ceil(max4(a0, b0, c0, d0))) - offset0;
            box_size1 = ((int)ceil(max4(a1, b1, c1, d1))) - offset1;
            a0 -= o0;
            a1 -= o1;
            b0 -= o0;
            b1 -= o1;
            c0 -= o0;
            c1 -= o1;
            d0 -= o0;
            d1 -= o1;
            if (b0 != a0) {
                pab = (b1 - a1) / (b0 - a0);
                cab = a1 - pab * a0;
            } else {
                pab = cab = 0.0;
            }
            if (c0 != b0) {
                pbc = (c1 - b1) / (c0 - b0);
                cbc = b1 - pbc * b0;
            } else {
                pbc = cbc = 0.0;
            }
            if (d0 != c0) {
                pcd = (d1 - c1) / (d0 - c0);
                ccd = c1 - pcd * c0;
            } else {
                pcd = ccd = 0.0;
            }
            if (a0 != d0) {
                pda = (a1 - d1) / (a0 - d0);
                cda = d1 - pda * d0;
            } else {
                pda = cda = 0.0;
            }
            memset(dist->buffer, 0, dist->buffer_size);
            integrate(dist, b0, a0, pab, cab);
            integrate(dist, a0, d0, pda, cda);
            integrate(dist, d0, c0, pcd, ccd);
            integrate(dist, c0, b0, pbc, cbc);
            area = 0.5 * ((c0 - a0) * (d1 - b1) - (c1 - a1) * (d0 - b0));
            for (ms=0; ms<box_size0; ++ms) {
                ml = ms + offset0;
                if (ml < 0 || ml >= dist->dim1)
                    continue;
                for (ns=0; ns<box_size1; ++ns) {
                    nl = ns + offset1;
                    if (nl < 0 || nl >= dist->dim2)
                        continue;
                    value = dist->buffer[ms*dist->delta1+ns] / area;
                    if (value <= 0)
                        continue;
                    m = ml * dist->dim2 + nl;
                    k = dist->out_max[m];
                    n = ml * (dist->dim2 * dist->lut_size_max) + nl * dist->lut_size_max + k;
                    dist->lut_idx[n] = idx;
                    dist->lut_coef[n] = value;
                    dist->out_max[m] = k + 1;
                }
            }
            idx++;
        }
    }
}


distortion *alloc_aux(distortion *dist) {
    dist->lut_coef = malloc(dist->array_size * dist->lut_size_max * sizeof(float));
    dist->lut_idx = malloc(dist->array_size * dist->lut_size_max * sizeof(int32_t));
    dist->out_max = calloc(dist->array_size, sizeof(int));
    dist->buffer = malloc(dist->buffer_size);
    if (!dist->lut_coef || !dist->lut_idx || !dist->out_max || !dist->buffer) {
        destroy_lut(dist);
        return NULL;
    }
    return dist;
}


void correct_lut(distortion *dist, float *image, float *out) {
    int i, j, k, m, idx;
    float sum, error, y, t, coef;

    for (i=0; i<dist->dim1; ++i) {
        for (j=0; j<dist->dim2; ++j) {
            sum = 0; error = 0;
            for (k=0; k<dist->lut_size_max; ++k) {
                m = i * dist->dim2 * dist->lut_size_max + j * dist->lut_size_max + k;
                idx = dist->lut_idx[m];
                coef = dist->lut_coef[m];
                if (coef <= 0 || idx >= dist->array_size)
                    continue;
                y = image[idx] * coef - error;
                t = sum + y;
                error = t - sum - y;
                sum = t;
            }
            out[i*dist->dim2+j] += sum;
        }
    }
}
