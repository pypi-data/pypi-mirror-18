/*
 * Different data format io routines
 */

#include <Python.h>
#include "byteoffset.h"
#include "agi_bitfield.h"
#include "ccp4.h"
#include "mar345.h"


struct module_state {
    PyObject *error;
};


#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#define CBF_IN_FMT_DEC "Oiy#"
#define CBF_IN_FMT_ENC "Oy#"
#define MAR_IN_FMT_DEC "Oiiiy#y#"
#define CBF_OUT_FMT "y#"
#define CCP4_IN_FMT "y#"
#define CCP4_OUT_FMT "y#y#"
#define CCP4_CONV_IN_FMT "Oy#dd"
#else
#define GETSTATE(m) (&_state)
#define CBF_IN_FMT_DEC "Ois#"
#define CBF_IN_FMT_ENC "Os#"
#define MAR_IN_FMT_DEC "Oiiis#s#"
#define CBF_OUT_FMT "s#"
#define CCP4_OUT_FMT "s#s#"
#define CCP4_IN_FMT "s#"
#define CCP4_CONV_IN_FMT "Os#dd"
static struct module_state _state;
#endif


static PyObject *
destroy_ccp4(PyObject *capsule) {
    geometry *geo;

    geo = (geometry *)PyCapsule_GetPointer(capsule, NULL);

    Py_BEGIN_ALLOW_THREADS
    _destroy_ccp4(geo);
    Py_END_ALLOW_THREADS

    return NULL;
};


static PyObject *
init_ccp4(PyObject *self, PyObject *args) {
    geometry *geo;
    char *c_par;
    int s_par;

    if (!PyArg_ParseTuple(args, CCP4_IN_FMT, &c_par, &s_par))
        return NULL;

    if (s_par != sizeof(parfile)) {
        PyErr_SetString(PyExc_TypeError, "Something wrong with the parfile buffer");
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    geo = _init_ccp4(c_par, s_par);
    Py_END_ALLOW_THREADS

    if (!geo)
        return PyErr_NoMemory();

    Py_BEGIN_ALLOW_THREADS
    calc_cell_matrices(geo);
    sphere_crysalis(geo);
    Py_END_ALLOW_THREADS

    return PyCapsule_New((void *)geo, NULL, (PyCapsule_Destructor)destroy_ccp4);
}


static PyObject *
convert_cbf2ccp4(PyObject *self, PyObject *args) {
    geometry *geo;
    int s_cbf;
    char *c_cbf;
    double angle, osc;
    PyObject *capsule;

    if (!PyArg_ParseTuple(args, CCP4_CONV_IN_FMT, &capsule, &c_cbf, &s_cbf, &angle, &osc))
        return NULL;

    geo = (geometry *)PyCapsule_GetPointer(capsule, NULL);

    Py_BEGIN_ALLOW_THREADS
    decode_byte_offset(c_cbf, geo->cbf);
    cbf2ccp4(geo, angle, osc);
    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}


static PyObject *
get_ccp4_map(PyObject *self, PyObject *args) {
    geometry *geo;
    PyObject *capsule;

    if (!PyArg_ParseTuple(args, "O", &capsule))
        return NULL;

    geo = (geometry *)PyCapsule_GetPointer(capsule, NULL);

    Py_BEGIN_ALLOW_THREADS
    ccp4_map(geo);
    ccp4_header(geo);
    Py_END_ALLOW_THREADS

    return Py_BuildValue(CCP4_OUT_FMT, geo->ccp4_hdr, sizeof(ccp4header),
                         (char *)geo->voxels, geo->s_voxels * sizeof(float));
}


static PyObject *
destroy_cbf(PyObject *capsule) {
    cbfdata *cbf;

    cbf = (cbfdata *)PyCapsule_GetPointer(capsule, NULL);

    Py_BEGIN_ALLOW_THREADS
    _destroy_cbf(cbf);
    Py_END_ALLOW_THREADS

    return NULL;
};


static PyObject *
init_cbf(PyObject *self) {
    cbfdata *cbf;

    Py_BEGIN_ALLOW_THREADS
    cbf = _init_cbf();
    Py_END_ALLOW_THREADS

    if (!cbf)
        return PyErr_NoMemory();
    return PyCapsule_New((void *)cbf, NULL, (PyCapsule_Destructor)destroy_cbf);
}


static PyObject *
decode_cbf(PyObject *self, PyObject *args) {
    char *c_cbf;
    int32_t n_pixels;
    int s_cbf;
    cbfdata *cbf;
    PyObject *capsule;

    if (!PyArg_ParseTuple(args, CBF_IN_FMT_DEC, &capsule, &n_pixels, &c_cbf, &s_cbf))
        return NULL;

    cbf = (cbfdata *)PyCapsule_GetPointer(capsule, NULL);

    Py_BEGIN_ALLOW_THREADS
    cbf = init_cbf_mem(cbf, n_pixels);
    Py_END_ALLOW_THREADS

    if (!cbf)
        return PyErr_NoMemory();

    Py_BEGIN_ALLOW_THREADS
    decode_byte_offset(c_cbf, cbf);
    Py_END_ALLOW_THREADS

    return Py_BuildValue(CBF_OUT_FMT, cbf->mem, cbf->n_pixels * sizeof(int32_t));
}


static PyObject *
encode_cbf(PyObject *self, PyObject *args) {
    int32_t *array;
    int s_array;
    cbfdata *cbf;
    PyObject *capsule;

    if (!PyArg_ParseTuple(args, CBF_IN_FMT_ENC, &capsule, &array, &s_array))
        return NULL;

    cbf = (cbfdata *)PyCapsule_GetPointer(capsule, NULL);

    Py_BEGIN_ALLOW_THREADS
    cbf = init_cbf_mem(cbf, s_array / sizeof(int32_t));
    Py_END_ALLOW_THREADS

    if (!cbf)
        return PyErr_NoMemory();

    Py_BEGIN_ALLOW_THREADS
    s_array = encode_byte_offset(array, cbf);
    Py_END_ALLOW_THREADS

    return Py_BuildValue(CBF_OUT_FMT, cbf->mem, s_array);
}


static PyObject *
destroy_esp(PyObject *capsule) {
    espdata *esp;

    esp = (espdata *)PyCapsule_GetPointer(capsule, NULL);

    Py_BEGIN_ALLOW_THREADS
    _destroy_esp(esp);
    Py_END_ALLOW_THREADS

    return NULL;
};


static PyObject *
init_esp(PyObject *self) {
    espdata *esp;

    Py_BEGIN_ALLOW_THREADS
    esp = _init_esp();
    Py_END_ALLOW_THREADS

    if (!esp)
        return PyErr_NoMemory();
    return PyCapsule_New((void *)esp, NULL, (PyCapsule_Destructor)destroy_esp);
}


static PyObject *
encode_esp(PyObject *self, PyObject *args) {
    int32_t *array;
    int s_array;
    espdata *esp;
    PyObject *capsule;

    if (!PyArg_ParseTuple(args, CBF_IN_FMT_ENC, &capsule, &array, &s_array))
        return NULL;

    esp = (espdata *)PyCapsule_GetPointer(capsule, NULL);

    Py_BEGIN_ALLOW_THREADS
    esp = init_esp_mem(esp, s_array / sizeof(int32_t));
    Py_END_ALLOW_THREADS

    if (!esp)
        return PyErr_NoMemory();

    Py_BEGIN_ALLOW_THREADS
    s_array = encode_agi_bitfield(array, esp);
    Py_END_ALLOW_THREADS

    return Py_BuildValue(CBF_OUT_FMT, esp->mem, s_array);
}


static PyObject *
destroy_mar(PyObject *capsule) {
    mardata *mar;

    mar = (mardata *)PyCapsule_GetPointer(capsule, NULL);

    Py_BEGIN_ALLOW_THREADS
    _destroy_mar(mar);
    Py_END_ALLOW_THREADS

    return NULL;
};


static PyObject *
init_mar(PyObject *self) {
    mardata *mar;

    Py_BEGIN_ALLOW_THREADS
    mar = _init_mar();
    Py_END_ALLOW_THREADS

    if (!mar)
        return PyErr_NoMemory();
    return PyCapsule_New((void *)mar, NULL, (PyCapsule_Destructor)destroy_mar);
}


static PyObject *
decode_mar(PyObject *self, PyObject *args) {
    char *packed, *oft;
    int32_t dim1, dim2, of, s_packed, s_oft;
    mardata *mar;
    PyObject *capsule;

    if (!PyArg_ParseTuple(args, MAR_IN_FMT_DEC, &capsule, &dim1, &dim2, &of, &oft, &s_oft, &packed, &s_packed))
        return NULL;

    mar = (mardata *)PyCapsule_GetPointer(capsule, NULL);

    Py_BEGIN_ALLOW_THREADS
    mar = init_mar_mem(mar, dim1, dim2);
    Py_END_ALLOW_THREADS

    if (!mar)
        return PyErr_NoMemory();

    Py_BEGIN_ALLOW_THREADS
    decode_mar_image(packed, of, oft, mar);
    Py_END_ALLOW_THREADS

    return Py_BuildValue(CBF_OUT_FMT, mar->image, mar->n_pixels * sizeof(uint32_t));
}


static PyMethodDef _cryio_methods[] = {
    {"init_cbf", (PyCFunction)init_cbf, METH_VARARGS, "Initialize memory for cbf compressor"},
    {"decode_cbf", (PyCFunction)decode_cbf, METH_VARARGS, "Decompress a cbf string into a string of numbers"},
    {"encode_cbf", (PyCFunction)encode_cbf, METH_VARARGS, "Compress a string of numbers into a cbf string"},
    {"init_ccp4", (PyCFunction)init_ccp4, METH_VARARGS, "Initialize memory for ccp4 calculations"},
    {"cbf2ccp4", (PyCFunction)convert_cbf2ccp4, METH_VARARGS, "Convert cbf packed string to ccp4"},
    {"get_ccp4_map", (PyCFunction)get_ccp4_map, METH_VARARGS, "Get ccp4 string"},
    {"init_esp", (PyCFunction)init_esp, METH_VARARGS, "Initialize memory for agi_bitfield compressor"},
    {"encode_esp", (PyCFunction)encode_esp, METH_VARARGS, "Compress a string of numbers into a agi_bitfield string"},
    {"init_mar", (PyCFunction)init_mar, METH_VARARGS, "Initialize memory for mar345 compressor"},
    {"decode_mar", (PyCFunction)decode_mar, METH_VARARGS, "Decompress a mar345 string into a string of numbers"},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

static int _cryio_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int _cryio_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_cryio",
    NULL,
    sizeof(struct module_state),
    _cryio_methods,
    NULL,
    _cryio_traverse,
    _cryio_clear,
    NULL
};

#define INITERROR return NULL

PyObject EXPORT(*PyInit__cryio(void))

#else
#define INITERROR return

void EXPORT(init_cryio(void))
#endif
{
    PyObject *module;
    struct module_state *st;

#if PY_MAJOR_VERSION >= 3
    module = PyModule_Create(&moduledef);
#else
    module = Py_InitModule("_cryio", _cryio_methods);
#endif

    if (module == NULL)
        INITERROR;
    st = GETSTATE(module);

    st->error = PyErr_NewException("_cryio.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

#if PY_MAJOR_VERSION >= 3
    return module;
#endif

}

