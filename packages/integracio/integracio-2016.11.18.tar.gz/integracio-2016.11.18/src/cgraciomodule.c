#include <Python.h>
#include <memory.h>
#include "poni.h"
#include "twoth.h"
#include "splitbbox.h"
#include "memmgr.h"


static PyObject *py_destroy(PyObject *capsule) {
    integration *intg;

    intg = (integration *)PyCapsule_GetPointer(capsule, NULL);

    Py_BEGIN_ALLOW_THREADS
    destroy_integration(intg);
    Py_END_ALLOW_THREADS
    return NULL;
};


static PyObject *py_init(PyObject *self) {
    integration *intg;

    Py_BEGIN_ALLOW_THREADS
    intg = init_integration();
    Py_END_ALLOW_THREADS

    if (!intg)
        return PyErr_NoMemory();
    return PyCapsule_New((void *)intg, NULL, (PyCapsule_Destructor)py_destroy);
}


static PyObject *py_calc_pos(PyObject *self, PyObject *args) {
    int s_geo, dim1, dim2, res;
    char *c_geo;
    PyObject *capsule, *result;
    integration *intg;

    if (!PyArg_ParseTuple(args, "Oiiy#", &capsule, &dim1, &dim2, &c_geo, &s_geo))
        return NULL;

    if (s_geo != sizeof(geometry)) {
        PyErr_SetString(PyExc_TypeError, "The PONI geometry struct cannot be interpreted");
        return NULL;
    }

    if(0 >= dim1 || 0 >= dim2) {
        PyErr_SetString(PyExc_ValueError, "The array dimensions cannot be zeros");
        return NULL;
    }

    intg = (integration *)PyCapsule_GetPointer(capsule, NULL);

    Py_BEGIN_ALLOW_THREADS
    memcpy(intg->geo, c_geo, s_geo);
    res = init_positions(intg, dim1, dim2);
    if (res)
        res = init_aux(intg);
    Py_END_ALLOW_THREADS

    if (!res)
        return PyErr_NoMemory();

    Py_BEGIN_ALLOW_THREADS;
    calculate_positions(intg);
    Py_END_ALLOW_THREADS;

    result = Py_BuildValue("y#", intg->pos->pos, intg->pos->s_pos);

    Py_BEGIN_ALLOW_THREADS
    destroy_aux(intg);
    Py_END_ALLOW_THREADS

    return result;
}


static PyObject *py_integrate(PyObject *self, PyObject *args) {
    int s_image;
    float *image, azmin, azmax;
    integration *intg;
    results *res;
    PyObject *capsule, *py_res;

    if (!PyArg_ParseTuple(args, "Oy#ff", &capsule, &image, &s_image, &azmin, &azmax))
        return NULL;

    intg = (integration *)PyCapsule_GetPointer(capsule, NULL);
    if(s_image != intg->pos->s_buf) {
        PyErr_SetString(PyExc_ValueError, "Image has a wrong size");
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    res = init_results(intg);
    Py_END_ALLOW_THREADS

    if (!res)
        return PyErr_NoMemory();

    Py_BEGIN_ALLOW_THREADS
    res->azmax = azmax;
    res->azmin = azmin;
    bbox_integrate(intg, image, res);
    Py_END_ALLOW_THREADS

    py_res = Py_BuildValue("y#y#", res->merge, intg->pos->s_pos, res->sigma, intg->pos->s_pos);

    Py_BEGIN_ALLOW_THREADS
    destroy_results(res);
    Py_END_ALLOW_THREADS

    return py_res;
}


static PyMethodDef _cgracio_methods[] = {
    {"calc_pos", (PyCFunction)py_calc_pos, METH_VARARGS, "Calculate positions"},
    {"integrate", (PyCFunction)py_integrate, METH_VARARGS, "Integrate an image"},
    {"init", (PyCFunction)py_init, METH_VARARGS, "Initialize memory for integration"},
    {NULL, NULL, 0, NULL}
};


struct module_state {
    PyObject *error;
};


#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))


static int _cgracio_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}


static int _cgracio_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_cgracio",
    NULL,
    sizeof(struct module_state),
    _cgracio_methods,
    NULL,
    _cgracio_traverse,
    _cgracio_clear,
    NULL
};


PyObject *PyInit__cgracio(void) {
    PyObject *module;
    struct module_state *st;
    module = PyModule_Create(&moduledef);
    if (module == NULL)
        return NULL;
    st = GETSTATE(module);
    st->error = PyErr_NewException("_cgracio.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        return NULL;
    }
    return module;
}
