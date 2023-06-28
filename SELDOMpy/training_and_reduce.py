# I import the extra functions file such as "arrayprint"
from functions.gen_exps import *
# I import the file where the "exps" list and "conc_data" is calculated from the Excel "experiments.xlsx"
from functions.buildmim import *
# I import the file where the "buildmin" function for the calculation of the mutual information is defined
from functions.getLBODEmodel import *
# I import the file where the model is calculated for the subsequent simulation
from functions.simulate_logic_based_ode_obs import *
# I import he file where the parameters are passed to "sim_logic_ode" to do the simulation
import pickle
# To be able to save the results in a file
from functions.reduce_fun import *
# Para tener las funciones utilizadas en la parte de reducción del modelo
from functions.plot_results import *
# Para representar las soluciones en gráficas
from functions.opt_mealpy import *
# Para hacer la optimización de la función objetivo

# ########################################## MODEL TRAINING ######################################################### #

save_results = True  # Booleano para indicar si queremos guardar los resultados en una lista y esta en un archivo
# En caso afirmativo habrá un archivo para la parte de entrenamiento y otra para la de reducción del modelo

initial_seed = 11  # Aqui establezco la semilla incial que quiero utilizar para la generación de los números aleatorios
rdm.seed(initial_seed)


NBINS = 10  # Numero de divisiones para discretizacion de valores medidos para cálculo de información mutua
TOPK = 12
REALK = 2  # Numero máximo de entradas (nº max de 1s en cada columna de adjMat)

exps, conc_data = gen_exps("MAPK.xlsx")
# Genero el objeto exps con datos de los experimentos y la matriz conc_data con las mediciones de los nodos

for iexp in range(len(exps)):
    exps[iexp].y0 = exps[iexp].exp_data[0]


inhibitors = []

adjMat = buildmim(conc_data, NBINS)
# Calculo la matriz de adyacencia a partir de conc_data. Se puede especificar también el numero de bins (divisiones)
# a realizar para la discretización de las medidas en el cálculo de la información mutua


model = getLBODEmodel(adjMat, random=True, is_stimuli=exps[0].is_stimuli, maxInput=REALK, min_tau=0, max_tau=1,
                      max_n=5, min_n=1, min_k=0.1, max_k=1)
# Generación de parámetros del modelo para la posterior simulación


ivpsol = Ivpsol(atol=1e-5, rtol=1e-5, max_step_size=1e100, max_num_steps=int(5000), max_error_test_fails=int(50))
# Creo el objeto ivpsol para las simulaciones
model.nthreads = int(4)

model.namesSpecies = exps[0].namesSpecies

print("optimizando...")
res = optimization(model, exps, ivpsol)
# Optimización para hallar los valores de x en los indices de model.index_opt que minimizan el valor de la simulación

f = res.f
time = res.time
fbest = res.fbest
xbest = res.xbest
neval = res.neval
numeval = res.numeval

random_state_training = rdm.getstate()  # Valor del generador de numeros randomicos tras el entrenamiento inicial
# Haciendo rdm.setstate(random_state_training) el generador de aleatorios se pone con los valores que tiene en este punto

if save_results:
    list_save = [f, time, fbest, xbest, neval, numeval, model, conc_data, exps, initial_seed, random_state_training]
    # Guardo los resultados en una lista
    file_name = f"results/opt_TOPK_{TOPK}_REALK_{REALK}_NBINS_{NBINS}_SEED_{initial_seed}.pkl"
    # Guardo la lista en un archivo
    with open(file_name, "wb") as file:
        pickle.dump(list_save, file)


for i in range(len(model.index_opt)):
    model.x[model.index_opt[i]-1] = res.xbest[i]

res_sim = simulate_logic_based_ode_obs(model, exps, ivpsol)
plot_results(exps, res_sim, 1, 10, 1, 4, 1)

# ############################################# MODEL REDUCTION ##################################################### #
RNUM = 0

conc_data_train = copy.deepcopy(conc_data)

n_data_train = 0
for i in range(len(conc_data_train)):
    for j in range(len(conc_data_train[i])):
        if conc_data_train[i][j] is not None:
            n_data_train += 1

ivpsol = Ivpsol(atol=1e-5, rtol=1e-5, max_step_size=0.1, max_num_steps=int(5000), max_error_test_fails=int(50))
# Creo el objeto ivpsol para las simulaciones
model.nthreads = int(1)

res = akaike(xbest, model, exps, ivpsol, 10, n_data_train)

best_model = get_reduced_model(model, exps[0].is_stimuli)

edges = rdm.sample(range(1, best_model.count_inputs+1), best_model.count_inputs)

for i in range(len(edges)):
    for p in range(len(xbest)):
        best_model.x[best_model.index_opt[p] - 1] = xbest[p]

    reduced = get_reduced_model(best_model, exps[0].is_stimuli, edges[i])

    opt = optimization(reduced, exps, ivpsol)

    for p in range(len(opt.xbest)):
        reduced.x[reduced.index_opt[p] - 1] = opt.xbest[p]

    f_reduced = optim_fun(opt.xbest, reduced, exps, ivpsol)
    AIC_reduced = akaike(opt.xbest, reduced, exps, ivpsol, reduced.active_pars, n_data_train)

    f_best = optim_fun(xbest, best_model, exps, ivpsol)
    AIC_best = akaike(xbest, best_model, exps, ivpsol, best_model.active_pars, n_data_train)

    if AIC_reduced <= AIC_best:
        print('\nreduced')
        print('----------------')
        print(f_reduced)
        print(f_best)
        best_model = reduced
        xbest = opt.xbest
        print(edges[i])
        print('----------------')
    else:
        print('\nCould not reduce')
        print('----------------')
        print(f_reduced)
        print(f_best)
        print(edges[i])
        print('----------------')

random_state_reduce = rdm.getstate()  # Valor del generador de numeros randomicos tras la reducción del modelo
# Haciendo rdm.setstate(random_state_reduce) el generador de aleatorios se pone con los valores que tiene en este punto

if save_results:
    list_save = [xbest, best_model, exps, conc_data, initial_seed, ivpsol, random_state_reduce]
    # Guardo los resultados en una lista
    # Guardo la lista en un archivo
    file_name = f"results_reduced_AIC/opt_TOPK_{TOPK}_REALK_{REALK}_NBINS_{NBINS}_SEED_{initial_seed}.pkl"
    with open(file_name, "wb") as file:
        pickle.dump(list_save, file)


res_sim = simulate_logic_based_ode_obs(best_model, exps, ivpsol)
plot_results(exps, res_sim, 1, 10, 1, 4, 1)

print("FIN")