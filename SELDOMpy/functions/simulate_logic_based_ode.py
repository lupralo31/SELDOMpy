import hello
# This is how the "hello" library is imported with the sim_logic_ode.c file and the compiled includes to be able to run
from SELDOMpy.functions.extras import *
# Required to use the "fill_array" function
import decimal


# To avoid "overflow" problems when obtaining simulation results


def simulate_logic_based_ode(model, exps, ivpsol):
    task = "OBS_CVODES_ODE"

    # Now the variables to be sent are converted to the appropriate format starting with those of the "model" model
    nthreads = np.array(model.nthreads, dtype=np.int32)
    n_states = np.array(model.n_states, dtype=np.int32)
    x = np.array(model.x, dtype=np.double)
    n_stimuli = np.array(model.n_stimuli, dtype=np.int32)

    # The variables that come from experiments will be repeated as many times as there are experiments,
    # so those of the same type of all experiments are joined in the same list that will then be covered in sim_logic_ode.c
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
    # This for example is a list in np.array format with the "n_observables" of all experiments in order
    # So for everyone else. In those that are going to be lists of lists you have to execute the function
    # "fill_array" since np.array gives error if all the internal lists are not of the same size
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
    # The transpose is done to put it as the file sim_logic_ode.c wants.
    for j in range(len(exp_data)):
        exp_data[j] = [[row[i] for row in exp_data[j]] for i in range(len(exp_data[j][0]))]
    exp_data = np.array(exp_data, dtype=np.double)

    # "ipvsol" variables are converted
    rtol = np.array(ivpsol.rtol, dtype=np.double)
    atol = np.array(ivpsol.atol, dtype=np.double)
    max_step_size = np.array(ivpsol.max_step_size, dtype=np.double)
    max_num_steps = np.array(ivpsol.max_num_steps, dtype=np.int32)
    max_error_test_fails = np.array(ivpsol.max_error_test_fails, dtype=np.int32)

    # Finally, the "task" string is converted
    task_c = np.array(task, dtype='object')

    # Variables are sent to the sim_logic_ode.c file
    res = hello.hello_numpy(nthreads, n_states, x, n_stimuli, n_observables, t_s, t_con, index_observables, t_0, t_f,
                            y0, u, exp_data, rtol, atol, max_step_size, max_num_steps, max_error_test_fails,
                            task_c.item())

    solution = decimal.Decimal(0)

    for i in range(len(res)):
        for j in range(len(res[i])):
            for k in range(len(res[i][j])):
                solution += (decimal.Decimal(res[i][j][k]) - decimal.Decimal(exps[i].exp_data[j][k])) ** 2

    # The solution is rounded to 8 decimal places
    solution = float(solution)

    return solution
