from mealpy.evolutionary_based import DE
from SELDOMpy.functions.simulate_logic_based_ode import *
# It is imported to do the simulations in the target function trying to minimize the value you get here
import datetime
# Imported to save the date in time within the object of the Res_opt class that is returned
import copy


class Res_opt:
    def __init__(self, f, time, fbest, xbest, neval, numeval):
        # Class constructor "Res_opt".
        self.f = f
        self.time = time
        self.fbest = fbest
        self.xbest = xbest
        self.neval = neval
        self.numeval = numeval


def optimization(model, exps, ivpsol, epoch, pop_size, miu_f, miu_cr):
    f = []
    time = []
    numeval = 0
    neval = []
    model_op = copy.deepcopy(model)

    def opt_fun(X):
        nonlocal numeval
        # It is interesting that numeval is not defined at the most global level of the module so that it
        # resets each time it calls "optimization"
        numeval += 1

        for p in range(len(model_op.index_opt)):
            model_op.x[model_op.index_opt[p]-1] = X[p]

        sol_opt_fun = simulate_logic_based_ode(model_op, exps, ivpsol)
        if not f:  # In the first simulation
            f.append(sol_opt_fun)
            time.append(datetime.datetime.now())
            neval.append(numeval)
        if sol_opt_fun < f[-1]:  # If the simulated value is less than the last best saved in list f
            f.append(sol_opt_fun)  # This new value is saved in list f
            time.append(datetime.datetime.now())  # The time it occurred is saved in the "time" list
            neval.append(numeval)  # The iteration number in which that value was evaluated is saved

        return sol_opt_fun

    LB = []
    UB = []
    for i in range(len(model_op.LB)):
        LB.append(model_op.LB[i])
        UB.append(model_op.UB[i])

    problem = {
        "fit_func": opt_fun,
        "lb": LB,
        "ub": UB,
        "minmax": "min",
        "log_to": None,
        "save_population": False,
    }

    modelo = DE.SHADE(epoch=epoch, pop_size=pop_size, miu_f=miu_f, miu_cr=miu_cr)

    xbest, fbest = modelo.solve(problem)

    xbest = xbest.tolist()

    return Res_opt(f, time, fbest, xbest, neval, numeval)

