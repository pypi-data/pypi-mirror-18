#include <Python.h>
#include <memory.h>
#include <stdint.h>
#include "distortion.h"
#include "bispev.h"


static PyObject *py_destroy_dist(PyObject *capsule) {
    distortion *dist;

    dist = (distortion *)PyCapsule_GetPointer(capsule, NULL);

    Py_BEGIN_ALLOW_THREADS
    destroy_distortion(dist);
    Py_END_ALLOW_THREADS
    return NULL;
};


static PyObject *py_init_dist(PyObject *self) {
    distortion *dist;

    Py_BEGIN_ALLOW_THREADS
    dist = init_distortion();
    Py_END_ALLOW_THREADS

    if (!dist)
        return PyErr_NoMemory();
    return PyCapsule_New((void *)dist, NULL, (PyCapsule_Destructor)py_destroy_dist);
};


static PyObject *py_calc_lut(PyObject *self, PyObject *args) {
    distortion *dist;
    PyObject *capsule;
    char *pos;
    int dim1, dim2, pos_size, delta0, delta1;

    if (!PyArg_ParseTuple(args, "Oiiiiy#", &capsule, &dim1, &dim2, &delta0, &delta1, &pos, &pos_size))
        return NULL;

    dist = (distortion *)PyCapsule_GetPointer(capsule, NULL);

    Py_BEGIN_ALLOW_THREADS
    dist->dim1 = dim1;
    dist->dim2 = dim2;
    dist->delta0 = delta0;
    dist->delta1 = delta1;
    dist->array_size = dist->dim1 * dist->dim2;
    dist->buffer_size = delta0 * delta1 * sizeof(float);
    dist = init_lut(dist);
    Py_END_ALLOW_THREADS

    if (!dist)
        return PyErr_NoMemory();

    Py_BEGIN_ALLOW_THREADS
    memcpy(dist->pos, pos, pos_size);
    calc_lut_size(dist);
    dist = alloc_aux(dist);
    Py_END_ALLOW_THREADS

    if (!dist)
        return PyErr_NoMemory();

    Py_BEGIN_ALLOW_THREADS
    calc_lut_table(dist);
    destroy_aux(dist);
    Py_END_ALLOW_THREADS

    Py_RETURN_NONE;
};


static PyObject *py_correct_lut(PyObject *self, PyObject *args) {
    distortion *dist;
    PyObject *capsule, *res;
    char *image;
    int image_size;
    float *out;

    if (!PyArg_ParseTuple(args, "Oy#", &capsule, &image, &image_size))
        return NULL;

    dist = (distortion *)PyCapsule_GetPointer(capsule, NULL);

    if (image_size != dist->array_size * sizeof(float)) {
        PyErr_SetString(PyExc_ValueError, "The image has wrong dimensions");
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    out = calloc(dist->array_size, sizeof(float));
    Py_END_ALLOW_THREADS

    if (!out)
        return PyErr_NoMemory();

    Py_BEGIN_ALLOW_THREADS
    correct_lut(dist, (float *)image, out);
    Py_END_ALLOW_THREADS

    res = Py_BuildValue("y#", (char *)out, image_size);

    Py_BEGIN_ALLOW_THREADS
    free(out);
    Py_END_ALLOW_THREADS

    return res;
};


static PyObject *py_bispev(PyObject *self, PyObject *args) {
    int kx, ky, tx_s, ty_s, c_s, x_s, y_s;
    char *tx, *ty, *c, *x, *y, *z;
    spline b;
    PyObject *res;

    if (!PyArg_ParseTuple(args, "y#y#y#iiy#y#", &tx, &tx_s, &ty, &ty_s, &c, &c_s, &kx, &ky, &x, &x_s, &y, &y_s))
        return NULL;

    Py_BEGIN_ALLOW_THREADS
    b.tx = (float *)tx;
    b.nx = tx_s / sizeof(float);
    b.ty = (float *)ty;
    b.ny = ty_s / sizeof(float);
    b.kx = kx;
    b.ky = ky;
    b.c = (float *)c;
    b.nc = c_s / sizeof(float);
    b.x = (float *)x;
    b.mx = x_s / sizeof(float);
    b.y = (float *)y;
    b.my = y_s / sizeof(float);
    b.zs = b.mx * b.my;
    b.zss = b.zs * sizeof(float);
    z = bispev(&b);
    Py_END_ALLOW_THREADS

    if (!z)
        return PyErr_NoMemory();
    res = Py_BuildValue("y#", z, b.zss);
    free(z);
    return res;
}


static PyMethodDef _decor_methods[] = {
    {"init_distortion", (PyCFunction)py_init_dist, METH_VARARGS, "Initialize memory for distortion"},
    {"calc_lut", (PyCFunction)py_calc_lut, METH_VARARGS, "Calculate LUT size"},
    {"correct_lut", (PyCFunction)py_correct_lut, METH_VARARGS, "Correct image using LUT"},
    {"bispev", (PyCFunction)py_bispev, METH_VARARGS, "Evaluate a bivariate B-spline and its derivatives"},
    {NULL, NULL, 0, NULL}
};


struct module_state {
    PyObject *error;
};


#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))


static int _decor_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}


static int _decor_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_decor",
    NULL,
    sizeof(struct module_state),
    _decor_methods,
    NULL,
    _decor_traverse,
    _decor_clear,
    NULL
};


PyObject *PyInit__decor(void) {
    PyObject *module;
    struct module_state *st;
    module = PyModule_Create(&moduledef);
    if (module == NULL)
        return NULL;
    st = GETSTATE(module);
    st->error = PyErr_NewException("_decor.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        return NULL;
    }
    return module;
}
