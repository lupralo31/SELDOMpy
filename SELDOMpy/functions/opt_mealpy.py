from mealpy.evolutionary_based import DE
from functions.simulate_logic_based_ode import *
# Se importa para hacer las simulaciones en la función objetivo tratando de minimizar el valor que obtenga aquí
import datetime
# Se importa para guardar la fecha en time dentro del objeto de la clase Res_opt que se devuelve
import copy


class Res_opt:
    def __init__(self, f, time, fbest, xbest, neval, numeval):
        # Constructor de la clase Res_opt. Se utilizará en MEIGO para devolver los valores obtenidos de la optimización
        self.f = f
        self.time = time
        self.fbest = fbest
        self.xbest = xbest
        self.neval = neval
        self.numeval = numeval


def optimization(model, exps, ivpsol):
    f = []
    time = []
    numeval = 0
    neval = []
    model_op = copy.deepcopy(model)

    def opt_fun(X):
        nonlocal numeval
        # Me interesa que numeval no esté definida al nivel más global del módulo para que resetee cada vez que llame
        # a optimization
        numeval += 1

        for p in range(len(model_op.index_opt)):
            model_op.x[model_op.index_opt[p]-1] = X[p]

        sol_opt_fun = simulate_logic_based_ode(model_op, exps, ivpsol)
        if not f:  # En la primera simulación
            f.append(sol_opt_fun)
            time.append(datetime.datetime.now())
            neval.append(numeval)
        if sol_opt_fun < f[-1]:  # Si el valor simulado es menor al ultimo mejor guardado en la lista f
            f.append(sol_opt_fun)  # Guardo este nuevo valor en la lista f
            time.append(datetime.datetime.now())  # Guardo el momento en que se produjo en la lista time
            neval.append(numeval)  # Guardo el nº de iteración en que se evalúo ese valor

        print(f"Iteración número: {numeval}")
        print(f"Valor función objetivo: {sol_opt_fun}")

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

    modelo = DE.SHADE(epoch=4000, pop_size=50, miu_f=0.3, miu_cr=0.6)

    xbest, fbest = modelo.solve(problem)

    xbest = xbest.tolist()

    return Res_opt(f, time, fbest, xbest, neval, numeval)

