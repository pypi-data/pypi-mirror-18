/**
 * Copyright 2016 Patrick Uiterwijk
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
#include <Python.h>
#include <krb5.h>

krb5_context kcontext;

static PyObject *
get_username(PyObject *self, PyObject *args)
{
    const char *realm;
    if (!PyArg_ParseTuple(args, "s", &realm))
	return NULL;

    krb5_error_code code;
    krb5_ccache cache;
    krb5_cccol_cursor cursor;
    char *defname;
    krb5_principal princ;

    if(krb5_cccol_cursor_new(kcontext, &cursor)) {
	PyErr_SetString(PyExc_RuntimeError, "Error getting CCache Collection");
	return NULL;
    }

    while (!(code = krb5_cccol_cursor_next(kcontext, cursor, &cache)) &&
           cache != NULL) {

	if(krb5_cc_get_principal(kcontext, cache, &princ)) {
	    // No valid principal
	    krb5_cc_close(kcontext, cache);
	    continue;
	}

	if(strcmp(princ->realm.data, realm)) {
	    // Not the correct realm
	    krb5_cc_close(kcontext, cache);
	    continue;
	}

	if(krb5_unparse_name_flags(kcontext, princ, KRB5_PRINCIPAL_UNPARSE_NO_REALM, &defname)) {
	    krb5_cc_close(kcontext, cache);
	    continue;
	}

	krb5_cc_close(kcontext, cache);

	return Py_BuildValue("s", defname);
    }

    Py_RETURN_NONE;
}

static PyMethodDef CCColUtilsMethods[] = {
    {"get_user_for_realm", get_username, METH_VARARGS, "Get username for a realm"},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION == 2
PyMODINIT_FUNC
initcccolutils(void)
{
    if(krb5_init_context(&kcontext)) {
	PyErr_SetString(PyExc_RuntimeError, "Error initializing krb5");
    }

    (void) Py_InitModule("cccolutils", CCColUtilsMethods);
}

#elif PY_MAJOR_VERSION == 3
static struct PyModuleDef cccolutilsmodule = {
   PyModuleDef_HEAD_INIT,
   "cccolutils",
   NULL,
   -1,
   CCColUtilsMethods
};

PyMODINIT_FUNC
PyInit_cccolutils(void)
{
    if(krb5_init_context(&kcontext)) {
	PyErr_SetString(PyExc_RuntimeError, "Error initializing krb5");
	return NULL;
    }
    return PyModule_Create(&cccolutilsmodule);
}

#else
#error "Only Py2 and Py3 supported"
#endif
