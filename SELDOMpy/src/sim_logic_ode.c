#include <stdio.h>
#include <stdlib.h>
#include <Python.h>
#include <AMIGO_model.h>
#include <AMIGO_problem.h>
#include "numpy/ndarraytypes.h"
#include "numpy/ufuncobject.h"
#include "numpy/npy_3kcompat.h"


int amigoRHS(realtype t, N_Vector y, N_Vector ydot, void *data);

void amigoRHS_get_OBS(void* data);

void amigoRHS_get_sens_OBS(void* data);

void amigo_Y_at_tcon(void* amigo_model, realtype t, N_Vector y);

int tamano_real_int (int* matriz, int ncolumnas, int nfila);
// Función para conocer tamaño real de una fila de matriz sin contar los -1 para matrices de tipo int

int tamano_real_double (double* matriz, int ncolumnas, int nfila);
// Función para conocer tamaño real de una fila de matriz sin contar los -1 para matrices de tipo double


AMIGO_model* Py_AMIGOmodelAlloc(PyArrayObject *n_states_obj, PyArrayObject *x_obj, PyArrayObject *n_stimuli_obj,
                       PyArrayObject *n_observables_obj, PyArrayObject *t_s_obj, PyArrayObject *t_con_obj,
                       PyArrayObject *index_observables_obj, PyArrayObject *t_0_obj, PyArrayObject *t_f_obj,
                       PyArrayObject *y0_obj, PyArrayObject *u_obj, PyArrayObject *exp_data_obj,
                       PyArrayObject *rtol_obj, PyArrayObject *atol_obj, PyArrayObject *max_step_size_obj,
                       PyArrayObject *max_num_steps_obj, PyArrayObject *max_error_test_fails_obj, int exp_num);

double simulation_task(AMIGO_problem* amigo_problem);

static PyObject* sim_obs_task(AMIGO_problem* amigo_problem);

static PyObject* hello_numpy_c(PyObject *dummy, PyObject *args) {
    AMIGO_problem* amigo_problem;
    AMIGO_model** amigo_models;
    double res1;
    PyObject *res2;
    int i,n_exp;

    // Creo los objetos para guardar en ellos las variables que me vienen de Python una vez se ha parseado
    PyArrayObject *nthreads_obj = NULL;
    PyArrayObject *n_states_obj = NULL;
    PyArrayObject *x_obj = NULL;
    PyArrayObject *n_stimuli_obj = NULL;
    PyArrayObject *n_observables_obj = NULL;
    PyArrayObject *t_s_obj = NULL;
    PyArrayObject *t_con_obj = NULL;
    PyArrayObject *index_observables_obj = NULL;
    PyArrayObject *t_0_obj = NULL;
    PyArrayObject *t_f_obj = NULL;
    PyArrayObject *y0_obj = NULL;
    PyArrayObject *u_obj = NULL;
    PyArrayObject *exp_data_obj = NULL;
    PyArrayObject *rtol_obj = NULL;
    PyArrayObject *atol_obj = NULL;
    PyArrayObject *max_step_size_obj = NULL;
    PyArrayObject *max_num_steps_obj = NULL;
    PyArrayObject *max_error_test_fails_obj = NULL;
    PyObject *task_obj = NULL;

    // Parseo los argumentos
    if (!PyArg_ParseTuple(args, "O!O!O!O!O!O!O!O!O!O!O!O!O!O!O!O!O!O!U", &PyArray_Type, &nthreads_obj, &PyArray_Type,
        &n_states_obj, &PyArray_Type, &x_obj, &PyArray_Type, &n_stimuli_obj, &PyArray_Type, &n_observables_obj,
        &PyArray_Type, &t_s_obj, &PyArray_Type, &t_con_obj, &PyArray_Type, &index_observables_obj, &PyArray_Type,
        &t_0_obj, &PyArray_Type, &t_f_obj, &PyArray_Type, &y0_obj, &PyArray_Type, &u_obj, &PyArray_Type, &exp_data_obj,
        &PyArray_Type, &rtol_obj, &PyArray_Type, &atol_obj, &PyArray_Type, &max_step_size_obj, &PyArray_Type,
        &max_num_steps_obj, &PyArray_Type, &max_error_test_fails_obj, &task_obj)) {
        return NULL;
    }

    // El nº de experimentos coincidirá con el nº de valores en la matriz t_f ya que hay un t_f por
    // experimento. Por lo que calculando el nº de elementos en t_f_obj saco el nº de experimentos
    int n = PyArray_SIZE(t_f_obj);

    n_exp=n;

    amigo_models=(AMIGO_model**)malloc(sizeof(AMIGO_model*)*n_exp);

    for (i = 0; i < n_exp; i++){
        amigo_models[i]=Py_AMIGOmodelAlloc(n_states_obj, x_obj, n_stimuli_obj, n_observables_obj, t_s_obj, t_con_obj,
                                           index_observables_obj, t_0_obj, t_f_obj, y0_obj, u_obj, exp_data_obj,
                                           rtol_obj, atol_obj, max_step_size_obj, max_num_steps_obj,
                                           max_error_test_fails_obj, i);
	}

	amigo_problem=allocate_AMIGO_problem(n_exp,amigo_models);

	set_AMIGO_problem_rhs(amigo_problem,amigoRHS,amigo_Y_at_tcon);
	set_AMIGO_problem_obs_function(amigo_problem,amigoRHS_get_OBS,amigoRHS_get_sens_OBS);

    amigo_problem->nthreads=*((int*) PyArray_DATA(nthreads_obj));

    char *task_py = (char*) malloc(sizeof(char)*15);
    for (int i = 0; i < 15; i++){
        task_py[i] = ((char*)PyUnicode_AsUTF8(task_obj))[i]; // Guardo los valores de la matriz
    }

    int type_return = 0;
    if(strcmp(task_py,"sim_CVODES_ODE")==0){
        res1=simulation_task(amigo_problem);
        type_return = 1;
        // Para poder indicar luego que el dato que se devuelve a Python es un double
    }else if(strcmp(task_py,"OBS_CVODES_ODE")==0){
        res2=sim_obs_task(amigo_problem);
        type_return = 2;
        // Para poder indicar luego que el dato que se devuelve a Python es una lista de matrices de doubles
    }
    free (task_py);


    free_AMIGO_problem(amigo_problem);
    free(amigo_models);//FALTABA ESTO

    // Libero el espacio de memoria guardado para los objetos
    /*Py_DECREF(n_states_obj);
    Py_DECREF(x_obj);
    Py_DECREF(n_stimuli_obj);
    Py_DECREF(n_observables_obj);
    Py_DECREF(t_s_obj);
    Py_DECREF(t_con_obj);
    Py_DECREF(index_observables_obj);
    Py_DECREF(t_0_obj);
    Py_DECREF(t_f_obj);
    Py_DECREF(y0_obj);
    Py_DECREF(u_obj);
    Py_DECREF(exp_data_obj);
    Py_DECREF(rtol_obj);
    Py_DECREF(atol_obj);
    Py_DECREF(max_step_size_obj);
    Py_DECREF(max_num_steps_obj);
    Py_DECREF(max_error_test_fails_obj);
    Py_DECREF(task_obj);*/

    if (type_return == 1)
        return Py_BuildValue("d", res1);
    else if (type_return == 2)
        Py_DECREF(res2);
        return res2;

}

AMIGO_model* Py_AMIGOmodelAlloc(PyArrayObject *n_states_obj, PyArrayObject *x_obj, PyArrayObject *n_stimuli_obj,
                                PyArrayObject *n_observables_obj, PyArrayObject *t_s_obj, PyArrayObject *t_con_obj,
                                PyArrayObject *index_observables_obj, PyArrayObject *t_0_obj, PyArrayObject *t_f_obj,
                                PyArrayObject *y0_obj, PyArrayObject *u_obj, PyArrayObject *exp_data_obj,
                                PyArrayObject *rtol_obj, PyArrayObject *atol_obj, PyArrayObject *max_step_size_obj,
                                PyArrayObject *max_num_steps_obj, PyArrayObject *max_error_test_fails_obj, int exp_num){
    AMIGO_model* amigo_model;

    int n_states,n_observables,n_pars,n_opt_pars,n_times,n_opt_ics,n_controls,n_controls_t,i,j,counter;

    n_states = *((int*) PyArray_DATA(n_states_obj));

    n_observables = ((int*) PyArray_DATA(n_observables_obj))[exp_num];

    n_pars = PyArray_SIZE(x_obj);

    int t_s_nelementos = PyArray_SIZE(t_s_obj); // Nº de elementos totales en la matriz t_s
    double *t_s_array = (double*) malloc(sizeof(double)*t_s_nelementos); // Guardo memoria para la matriz
    for (int i = 0; i < t_s_nelementos; i++){
        t_s_array[i] = ((double*) PyArray_DATA(t_s_obj))[i]; // Guardo los valores de la matriz
    }
    int t_s_ncolumnas = PyArray_DIMS(t_s_obj)[1]; // Calculo el nº de elementos por fila (incluyendo los -1)
    n_times = tamano_real_double (t_s_array, t_s_ncolumnas, exp_num); // Calculo el nº de elementos de esa fila sin -1

    n_controls = *((int*) PyArray_DATA(n_stimuli_obj));

    int t_con_nelementos = PyArray_SIZE(t_con_obj); // Nº de elementos totales en la matriz t_con
    double *t_con_array = (double*) malloc(sizeof(double)*t_con_nelementos); // Guardo memoria para la matriz
    for (int i = 0; i < t_con_nelementos; i++){
        t_con_array[i] = ((double*) PyArray_DATA(t_con_obj))[i]; // Guardo los valores de la matriz
    }
    int t_con_ncolumnas = PyArray_DIMS(t_con_obj)[1]; // Calculo el nº de elementos por fila (incluyendo los -1)
    n_controls_t = tamano_real_double (t_con_array, t_con_ncolumnas, exp_num);
    // Calculo el nº de elementos de esa fila sin -1

    n_opt_pars=0;
    n_opt_ics=0;

    amigo_model=allocate_AMIGO_model(n_states,n_observables,n_pars,
  	n_opt_pars,n_times,n_opt_ics,n_controls, n_controls_t,exp_num);

  	int index_observables_nelementos = PyArray_SIZE(index_observables_obj); // Nº de elementos totales
    int *index_observables_array = (int*) malloc(sizeof(int)*index_observables_nelementos);
    // Guardo memoria para la matriz
    for (int i = 0; i < index_observables_nelementos; i++){
        index_observables_array[i] = ((int*) PyArray_DATA(index_observables_obj))[i]; // Guardo los valores de la matriz
    }
    int index_observables_ncolumnas = PyArray_DIMS(index_observables_obj)[1];
    // Calculo el nº de elementos por fila (incluyendo los -1)
    int length_ind_obs = tamano_real_int (index_observables_array, index_observables_ncolumnas, exp_num);
    // Calculo el nº de elementos de esa fila sin -1

  	//index_observables
    if(length_ind_obs<n_observables){
        amigo_model->use_obs_func=1;
        amigo_model->use_sens_obs_func=1;
	}else{
        for (i = 0; i < length_ind_obs; i++) {
          amigo_model->index_observables[i]=index_observables_array[i+index_observables_ncolumnas*exp_num]-1;
        }
	}
    free (index_observables_array);


    //Simulation Pars
	for (i = 0; i < n_pars; i++){
		amigo_model->pars[i]=((double *) PyArray_DATA(x_obj))[i];
	}

    //initial simulation times
	amigo_model->t0=((double*) PyArray_DATA(t_0_obj))[exp_num];

	//final simulation times
    amigo_model->tf=((double*) PyArray_DATA(t_f_obj))[exp_num];

    //Sampling times
    for (i = 0; i < n_times; i++){
        amigo_model->t[i]=t_s_array[i+t_s_ncolumnas*exp_num];
	}
	free (t_s_array);

	//Initial conditions
	int y0_nelementos = PyArray_SIZE(y0_obj); // Nº de elementos totales en la matriz y0
    double *y0_array = (double*) malloc(sizeof(double)*y0_nelementos); // Guardo memoria para la matriz
    for (int i = 0; i < y0_nelementos; i++){
        y0_array[i] = ((double*) PyArray_DATA(y0_obj))[i]; // Guardo los valores de la matriz
    }
    int y0_ncolumnas = PyArray_DIMS(y0_obj)[1]; // Calculo el nº de elementos por fila (incluyendo los -1)
    for (i = 0; i < n_states; i++){
      amigo_model->y0[i]=y0_array[i+y0_ncolumnas*exp_num];
	}
	free (y0_array);

	//Control times
    for (i = 0; i < n_controls_t; i++){
      amigo_model->controls_t[i]=t_con_array[i+t_con_ncolumnas*exp_num];
	}
    free (t_con_array);

    //Control values
    counter = 0;
    int u_nelementos = PyArray_SIZE(u_obj); // Nº de elementos totales en la matriz u
    double *u_array = (double*) malloc(sizeof(double)*u_nelementos); // Guardo memoria para la matriz
    for (int i = 0; i < u_nelementos; i++){
        u_array[i] = ((double*) PyArray_DATA(u_obj))[i]; // Guardo los valores de la matriz
    }
    int u_ncolumnas = PyArray_DIMS(u_obj)[1]; // Calculo el nº de elementos por fila (incluyendo los -1)
    for (i = 0; i < n_controls; i++) {
        for (j= 0; j < n_controls_t-1; j++){
            amigo_model->controls_v[i][j]=u_array[counter+u_ncolumnas*exp_num];
            counter++;
        }
    }
    free (u_array);

    //Experimental data
	counter=0;
	int exp_data_nelementos = PyArray_SIZE(exp_data_obj); // Nº de elementos totales en la matriz exp_data
    double *exp_data_array = (double*) malloc(sizeof(double)*exp_data_nelementos); // Guardo memoria para la matriz
    for (int i = 0; i < exp_data_nelementos; i++){
        exp_data_array[i] = ((double*) PyArray_DATA(exp_data_obj))[i]; // Guardo los valores de la matriz
    }
    int exp_data_ncolumnas = PyArray_DIMS(exp_data_obj)[1]; // Calculo el nº de elementos por fila (incluyendo los -1)
    for (i = 0; i < n_observables; i++) {
        for (j= 0; j < n_times; j++){
            amigo_model->exp_data[i][j]=exp_data_array[counter+exp_data_ncolumnas*exp_num];
            counter++;
        }
    }
    free (exp_data_array);

    //Simulation Related Parameter
	//rtol
    amigo_model->reltol = *((double*) PyArray_DATA(rtol_obj));

    //atol
    amigo_model->atol = *((double*) PyArray_DATA(atol_obj));

    //max_step_size
    amigo_model->max_step_size = *((double*) PyArray_DATA(max_step_size_obj));

    //max_num_steps
    amigo_model->max_num_steps = *((int*) PyArray_DATA(max_num_steps_obj));

    //max_error_test_fails
    amigo_model->max_error_test_fails = *((int*) PyArray_DATA(max_error_test_fails_obj));

    return (amigo_model);
}


double simulation_task(AMIGO_problem* amigo_problem){

  double out;
  double cost;

  cost=eval_AMIGO_problem_LSQ(amigo_problem);

  if(isnan(cost)){
    out=1e10;
  }else if(cost>=DBL_MAX){
    out=1e10;
  }else{
    out=cost;
  }

  return(out);
}


static PyObject* sim_obs_task(AMIGO_problem* amigo_problem){

  int i,j,k;

  eval_AMIGO_problem_LSQ(amigo_problem);

  int length_res = amigo_problem->n_models * amigo_problem->amigo_models[0]->n_observables
                   * amigo_problem->amigo_models[0]->n_times;

  double *list_sim=(double*) malloc(sizeof(double*)*length_res);

  for (i = 0; i < amigo_problem->n_models; i++) {
    for (k = 0; k < amigo_problem->amigo_models[i]->n_times; k++) {
        for (j = 0; j < amigo_problem->amigo_models[i]->n_observables; j++) {
        list_sim [j + amigo_problem->amigo_models[i]->n_observables * k + amigo_problem->amigo_models[i]->n_observables *
        amigo_problem->amigo_models[i]->n_times * i] = amigo_problem->amigo_models[i]->obs_results[j][k];
      }
    }
  }

  PyObject *out = PyList_New(0);
  for (j = 0; j<amigo_problem->n_models; j++){
    PyObject *matriz_python = PyList_New(0);
    for (k = 0; k<amigo_problem->amigo_models[j]->n_times; k++){
      PyObject *lista_python = PyList_New(0);
      for (int l = 0; l<amigo_problem->amigo_models[j]->n_observables; l++){
        PyObject *elemento_a_anadir = PyFloat_FromDouble(list_sim[l+k*amigo_problem->amigo_models[j]->n_observables
        +j*amigo_problem->amigo_models[j]->n_times*amigo_problem->amigo_models[j]->n_observables]);
        PyList_Append(lista_python, elemento_a_anadir);
        Py_DECREF(elemento_a_anadir);
      }
      PyList_Append(matriz_python, lista_python);
      Py_DECREF(lista_python);
    }
    PyList_Append(out,matriz_python);
    Py_DECREF(matriz_python);
  }
  free(list_sim);




  return(Py_BuildValue("O", out));
}





int tamano_real_int(int* matriz, int ncolumnas, int nfila) {
    int tamano = ncolumnas;
    for (int i = 0; i < ncolumnas; i++){
        if (matriz[i + ncolumnas*nfila] == -1){
            tamano --;
        }

    }
    return (tamano);
}


int tamano_real_double(double* matriz, int ncolumnas, int nfila) {
    int tamano = ncolumnas;
    for (int i = 0; i < ncolumnas; i++){
        if (matriz[i + ncolumnas*nfila] == -1){
            tamano --;
        }

    }
    return (tamano);
}



static PyMethodDef hello_methods[] = {
        {
                "hello_numpy", hello_numpy_c, METH_VARARGS,
                "numpy function tester",
        },
        {NULL, NULL, 0, NULL}
};


static struct PyModuleDef hello_definition = {
        PyModuleDef_HEAD_INIT,
        "hello",
        "A Python module that prints 'hello world' from C code.",
        -1,
        hello_methods
};


PyMODINIT_FUNC PyInit_hello(void) {
    Py_Initialize();
    import_array();
    return PyModule_Create(&hello_definition);
}
