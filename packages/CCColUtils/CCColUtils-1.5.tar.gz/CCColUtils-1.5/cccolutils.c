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

static PyObject *has_creds(PyObject *self, PyObject *args);

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

static PyObject *
has_creds(PyObject *self, PyObject *args)
{
	krb5_ccache cache;
	krb5_cccol_cursor cursor;
	krb5_cc_cursor cache_cursor;
	krb5_creds creds;
	krb5_error_code code;
	int found = FALSE;

	if (krb5_cccol_cursor_new(kcontext, &cursor))
		Py_RETURN_FALSE;

	while (!(code = krb5_cccol_cursor_next(kcontext, cursor, &cache)) &&
	       cache != NULL)
	{
		code = krb5_cc_start_seq_get(kcontext, cache, &cache_cursor);
		if (code)
			break;

		while (0 == krb5_cc_next_cred(kcontext, cache, &cache_cursor, &creds))
		{
			if (!krb5_is_config_principal(kcontext, creds.server))
			{
				found = TRUE;
				krb5_free_cred_contents(kcontext, &creds);
				break;
			}
		}

		krb5_cc_end_seq_get(kcontext, cache, &cache_cursor);
		krb5_cc_close(kcontext, cache);

		if (found)
			/* If a credential is already found in this current
			 * credential cache, no need to iterate next credential
			 * cache and terminate now. */
			break;
	}

	krb5_cccol_cursor_free(kcontext, &cursor);

	if (found)
		Py_RETURN_TRUE;
	else
		Py_RETURN_FALSE;
}

static PyMethodDef CCColUtilsMethods[] = {
    {"get_user_for_realm", get_username, METH_VARARGS, "Get username for a realm"},
    {"has_creds", has_creds, METH_NOARGS, "Check if there is any credentials."},
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
