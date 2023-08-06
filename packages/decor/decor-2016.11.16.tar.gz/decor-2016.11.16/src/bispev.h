#ifndef CDECOR_BISPEV_H_   /* Include guard */
#define CDECOR_BISPEV_H_ 1

typedef struct {
    float *tx;
    int nx;
    float *ty;
    int ny;
    float *c;
    int nc;
    int kx;
    int ky;
    float *x;
    int mx;
    float *y;
    int my;
    int zs;
    int zss;
} spline;

char *bispev(spline *b);

#endif  // CDECOR_BISPEV_H_
