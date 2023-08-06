/*
 * Copied from pyFAI
 */

#include <stdlib.h>
#include <stdint.h>
#include <memory.h>
#include "bispev.h"


static void fpbspl(float *t, int n, int k, float x, int l, float *h, float *hh) {
    int i, j;
    float f;

    h[0] = 1;
    for (j=1; j<=k; ++j) {
        for (i=0; i<j; ++i)
            hh[i] = h[i];
        h[0] = 0;
        for (i=0; i<j; ++i) {
            f = hh[i] / (t[l + i] - t[l + i - j]);
            h[i] = h[i] + f * (t[l + i] - x);
            h[i + 1] = f * (x - t[l + i - j]);
        }
    }
}


static void init_w(float *t, int n, int k, float *x, int m, int32_t *lx, float *w) {
    int i, j, l, l1;
    float arg, tb, te, h[6], hh[5];

    tb = t[k];
    te = t[n - k - 1];
    l = k + 1;
    l1 = l + 1;
    for (i=0; i<m; ++i) {
        arg = x[i];
        if (arg < tb)
            arg = tb;
        if (arg > te)
            arg = te;
        while (!(arg < t[l] || l == (n - k - 1))) {
            l = l1;
            l1 = l + 1;
        }
        fpbspl(t, n, k, arg, l, h, hh);

        lx[i] = l - k - 1;
        for (j=0; j<=k; ++j)
            w[i*(k+1)+j] = h[j];
    }
}


char *bispev(spline *b) {
    int kx1, ky1, nky1, i, j, i1, l2, j1, wxs, wys;
    float *wx, *wy, *z, sp, err, tmp, a;
    int32_t *lx, *ly;
    char *mem;

    kx1 = b->kx + 1;
    ky1 = b->ky + 1;
    nky1 = b->ny - ky1;

    wxs = b->mx * kx1;
    wys = b->my * ky1;
    mem = malloc(b->zss + (wxs + wys) * sizeof(float) + (b->mx + b->my) * sizeof(int32_t));

    if (!mem)
        return NULL;

    z = (float *)mem;
    wx = z + b->zs;
    wy = wx + wxs;
    lx = (int32_t *)(wy + wys);
    ly = lx + b->mx;

    memset(z, 0, b->zss);
    init_w(b->tx, b->nx, b->kx, b->x, b->mx, lx, wx);
    init_w(b->ty, b->ny, b->ky, b->y, b->my, ly, wy);

    for (j=0; j<b->my; ++j) {
        for (i=0; i<b->mx; ++i) {
            sp = 0; err = 0;
            for (i1=0; i1<kx1; ++i1) {
                for (j1=0; j1<ky1; ++j1) {
                    l2 = lx[i] * nky1 + ly[j] + i1 * nky1 + j1;
                    a = b->c[l2] * wx[i*kx1+i1] * wy[j*ky1+j1] - err;
                    tmp = sp + a;
                    err = tmp - sp - a;
                    sp = tmp;
                }
            }
            z[j*b->mx+i] += sp;
        }
    }
    return mem;
}
