#ifndef CDECOR_DISTORTION_H_   /* Include guard */
#define CDECOR_DISTORTION_H_ 1

#include <stdint.h>

typedef struct {
    int dim1;
    int dim2;
    int array_size;
    float *pos;
    uint32_t *lut_size;
    uint32_t lut_size_max;
    int delta0;
    int delta1;
    float *lut_coef;
    int32_t *lut_idx;
    int *out_max;
    float *buffer;
    int buffer_size;
} distortion;

void destroy_distortion(distortion *dist);
distortion *init_distortion();
distortion *init_lut(distortion *dist);
void destroy_lut(distortion *dist);
void calc_lut_size(distortion *dist);
void calc_lut_table(distortion *dist);
distortion *alloc_aux(distortion *dist);
void destroy_aux(distortion *dist);
void correct_lut(distortion *dist, float *image, float *out);

#endif  // CDECOR_DISTORTION_H_
