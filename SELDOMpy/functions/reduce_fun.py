from SELDOMpy.functions.simulate_logic_based_ode import *
from math import log
import copy


# Function used to obtain the resulting model by reducing an arrow arc from the network
def get_reduced_model(model, is_stimuli=None, delete_edge=-1):
    adjMat = copy.deepcopy(model.adjMat)
    model_copy = copy.deepcopy(model)

    if is_stimuli is None:
        is_stimuli = []
        for iii in range(len(adjMat[0])):
            is_stimuli.append(0)

    counter = 0

    active_inputs = []

    count_inputs = 0

    x = copy.deepcopy(model.x)

    for iii in range(len(adjMat[0])):
        counter = counter + 1

        active_inputs.append([])

        n_inputs = x[counter - 1]

        if n_inputs > 0:
            for jj in range(n_inputs):
                count_inputs = count_inputs + 1

                # inputs index
                counter += 1
                if delete_edge == count_inputs:
                    x[counter - 1] = -1

                is_active = x[counter - 1]

                if is_active >= 0:
                    active_inputs[iii].append(is_active)

                # k
                counter += 1

                # n
                counter += 1

            # w
            for jj in range(2 ** n_inputs):
                counter += 1

            # TAU
            counter += 1

        else:
            counter += 1

    model_copy.estimated_pars = len(model_copy.LB)
    model_copy.x = x
    count_active_inputs = 0

    active_pars = 0
    for iii in range(len(active_inputs)):
        n_inputs = len(active_inputs[iii])
        if n_inputs > 0:
            count_active_inputs += n_inputs

            active_pars = active_pars + 2 * n_inputs + (2 ** n_inputs) + 1

        elif n_inputs == 0 and is_stimuli[iii] == 0:
            active_pars += 1

    model_copy.active_pars = active_pars
    model_copy.count_inputs = count_inputs
    model_copy.count_active_inputs = count_active_inputs

    return model_copy


# Function used to apply akaike criteria to check whether an axis can be removed
def akaike(x, model, exps, ivpsol, k, n_data):
    model_copy = copy.deepcopy(model)

    for p in range(len(model_copy.index_opt)):
        model_copy.x[model_copy.index_opt[p] - 1] = x[p]

    res = simulate_logic_based_ode(model_copy, exps, ivpsol)

    return 2*k+n_data*log(res)


# Function used to reduce the value of the target function
def optim_fun(X, model, exps, ivpsol):
    model_copy = copy.deepcopy(model)

    for p in range(len(model_copy.index_opt)):
        model_copy.x[model_copy.index_opt[p] - 1] = X[p]

    res = simulate_logic_based_ode(model_copy, exps, ivpsol)

    return res
