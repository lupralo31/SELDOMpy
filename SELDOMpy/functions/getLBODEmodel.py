from functions.getRandomLBODEmodel import *
# Importo el archivo getRandomLBODEmodel en el que se realiza la ruleta para la creación de modelos


class Model:
    def __init__(self, n_states, n_stimuli, x, adjMat, index_opt, LB, UB, k_pars, n_pars, w_pars,
                 tau_pars, nthreads, estimated_pars=None, active_pars=None, count_inputs=None, count_active_inputs=None,
                 namesSpecies=None):
        # Constructor de la clase Model. Se utilizará en getLBODEmodel para crear un objeto con los datos de un modelo
        self.n_states = n_states
        self.n_stimuli = n_stimuli
        self.x = x
        self.adjMat = adjMat
        self.index_opt = index_opt
        self.LB = LB
        self.UB = UB
        self.k_pars = k_pars
        self.n_pars = n_pars
        self.w_pars = w_pars
        self.tau_pars = tau_pars
        self.nthreads = nthreads
        self.estimated_pars = estimated_pars
        self.active_pars = active_pars
        self.count_inputs = count_inputs
        self.count_active_inputs = count_active_inputs
        self.namesSpecies = namesSpecies


def getLBODEmodel(adjMat, is_stimuli=None, max_tau=1, min_tau=0.00001, min_k=0.05, max_k=1, min_n=0, max_n=6,
                  max_w=1, min_w=0, random=False, maxInput=6):
    if is_stimuli is None:
        is_stimuli = [0, 0, 0, 0]

    if maxInput > len(adjMat[0]):
        maxInput = len(adjMat[0])

    x = []  # La lista tita donde voy a guardar todos los parametros
    index_opt = []
    LB = []
    UB = []
    index_w = []
    index_n = []
    index_k = []
    index_tau = []

    counter = 0  # Inicializacion del contador
    if random:
        adjMat = getRandomLBODEmodel(adjMat, maxInput)
        # Calculo de la matriz de adyacencia con 1s y 0s y metodo de la ruleta

    for i in range(len(adjMat[0])):  # Recorro columas de adjMat
        counter += 1

        inputs = []  # Lista donde guardaré los indices de las filas que valgan 1 en esa columna
        for ii in range(len(adjMat)):  # Recorro filas de la columna de adjMat
            if adjMat[ii][i] == 1:
                inputs.append(ii)

        x.append(len(inputs))  # Pongo en primera posicion el numero de entradas de esa columna

        if len(inputs) > 0:  # Si hay alguna entrada en el nodo de esa columna

            for j in range(len(inputs)):  # Recorro las entradas de esa columna
                # inputs index
                counter += 1
                x.append(inputs[j])  # Pongo el indice de esa entrada en esa columna

                # k
                counter += 1
                x.append(0.1)

                if is_stimuli[i] == 0:
                    index_k.append(counter)

                # n
                counter += 1
                x.append(1)
                if is_stimuli[i] == 0:
                    index_n.append(counter)

            # w
            for j in range(2**(len(inputs))):
                counter += 1
                x.append(1)
                if is_stimuli[i] == 0:
                    index_w.append(counter)

            # TAU
            counter += 1
            if is_stimuli[i] == 1:
                x.append(0)
            else:
                x.append(1)

            if is_stimuli[i] == 0:
                index_tau.append(counter)

        else:
            counter += 1
            if is_stimuli[i] == 1:
                x.append(0)
            else:
                x.append(1)

            if is_stimuli[i] == 0:
                index_tau.append(counter)

    for i in index_k:
        index_opt.append(i)
    for i in index_n:
        index_opt.append(i)
    for i in index_w:
        index_opt.append(i)
    for i in index_tau:
        index_opt.append(i)

    k_pars = []
    for i in range(len(index_k)):
        k_pars.append(i+1)

    n_pars = []
    for i in range(k_pars[-1]+1, k_pars[-1]+len(index_n)+1):
        n_pars.append(i)

    w_pars = []
    for i in range(n_pars[-1]+1, n_pars[-1]+len(index_w)+1):
        w_pars.append(i)

    tau_pars = []
    for i in range(w_pars[-1]+1, w_pars[-1]+len(index_tau)+1):
        tau_pars.append(i)

    for i in range(len(index_opt)):
        LB.append(0)
        UB.append(0)

    for i in k_pars:
        LB[i-1] = min_k
        UB[i-1] = max_k

    for i in n_pars:
        LB[i-1] = min_n
        UB[i-1] = max_n

    for i in w_pars:
        LB[i-1] = min_w
        UB[i-1] = max_w

    for i in tau_pars:
        LB[i-1] = min_tau
        UB[i-1] = max_tau

    n_states = len(adjMat)
    n_stimuli = len(adjMat)
    nthreads = int(2)
    model = Model(n_states, n_stimuli, x, adjMat, index_opt, LB, UB, k_pars, n_pars, w_pars, tau_pars, nthreads)

    return model
