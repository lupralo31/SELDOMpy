import hello
# Así importo la librería hello con el archivo sim_logic_ode.c y los includes compilados para poder ejecutarse
from functions.extras import *
# Necesario para usar la función fill_array


def simulate_logic_based_ode_obs(model, exps, ivpsol):

    task = "OBS_CVODES_ODE"

    # Ahora se convierten las variables a enviar al formato adecuado empezando por las del modelo "model"
    nthreads = np.array(model.nthreads, dtype=np.int32)
    n_states = np.array(model.n_states, dtype=np.int32)
    x = np.array(model.x, dtype=np.double)
    n_stimuli = np.array(model.n_stimuli, dtype=np.int32)

    # Las variables que vienen de experimentos estarán repetidas tantas veces como experimentos haya, por lo que se unen
    # las del mismo tipo de todos los experimentos en una misma lista que luego se recorrerá en sim_logic_ode.c
    n_observables = []
    t_s = []
    t_con = []
    index_observables = []
    t_0 = []
    t_f = []
    y0 = []
    u = []
    exp_data = []

    for i in range(len(exps)):
        n_observables.append(exps[i].n_observables)
        t_s.append(exps[i].t_s)
        t_con.append(exps[i].t_con)
        index_observables.append(exps[i].index_observables)
        t_0.append(exps[i].t_0)
        t_f.append(exps[i].t_f)
        y0.append(exps[i].y0)
        u.append(exps[i].u)
        exp_data.append(exps[i].exp_data)

    n_observables = np.array(n_observables, dtype=np.int32)
    # Esto por ejemplo es una lista en formato np.array con los n_observables de todos los experimentos en orden
    # Así para todos los demás. En las que vayan a ser listas de listas hay que ejecutarles la funcion "fill_array"
    # ya que np.array da error si todas las listas internas no son del mismo tamaño
    t_s = fill_array(t_s)
    t_s = np.array(t_s, dtype=np.double)
    t_con = fill_array(t_con)
    t_con = np.array(t_con, dtype=np.double)
    index_observables = fill_array(index_observables)
    index_observables = np.array(index_observables, dtype=np.int32)
    t_0 = np.array(t_0, dtype=np.double)
    t_f = np.array(t_f, dtype=np.double)
    y0 = fill_array(y0)
    y0 = np.array(y0, dtype=np.double)
    u = fill_array(u)
    u = np.array(u, dtype=np.double)
    exp_data = fill_array(exp_data)
    # Hago la traspuesta para ponerla tal y como lo quiere el archivo sim_logic_ode.c
    for j in range(len(exp_data)):
        exp_data[j] = [[row[i] for row in exp_data[j]] for i in range(len(exp_data[j][0]))]
    exp_data = np.array(exp_data, dtype=np.double)

    # Se convierten las variables de ipvsol
    rtol = np.array(ivpsol.rtol, dtype=np.double)
    atol = np.array(ivpsol.atol, dtype=np.double)
    max_step_size = np.array(ivpsol.max_step_size, dtype=np.double)
    max_num_steps = np.array(ivpsol.max_num_steps, dtype=np.int32)
    max_error_test_fails = np.array(ivpsol.max_error_test_fails, dtype=np.int32)

    # Por último se convierte la cadena de caracteres task
    task_c = np.array(task, dtype='object')

    # Se envían las variables al archivo sim_logic_ode.c
    res = hello.hello_numpy(nthreads, n_states, x, n_stimuli, n_observables, t_s, t_con, index_observables, t_0, t_f,
                            y0, u, exp_data, rtol, atol, max_step_size, max_num_steps, max_error_test_fails,
                            task_c.item())

    # Se redondea la solución a 8 decimales
    for i in range(len(res)):
        for j in range(len(res[i])):
            for k in range(len(res[i][j])):
                res[i][j][k] = round(res[i][j][k], 8)

    return res

