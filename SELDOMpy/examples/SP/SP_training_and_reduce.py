from SELDOMpy import *
import os

# This file is generic. In this case it is being used for the SP network, but it is recommended to modify the name
# data of the Excel file, and parameters of simulations and optimization instead of creating another new file since
# the structure of the algorithm is always the same

# ################################################ MODEL TRAINING ############################################################### #


# The initial seed that you want to use for the generation of random numbers is established
initial_seed = 6
rdm.seed(initial_seed)


NBINS = 10  # Number of bins for discretization of measured values for calculation of mutual information
REALK = 4  # Maximum number of entries (max number of 1s in each column of adjMat)

# The object "exps" is generated with data from the experiments and the matrix "conc_data" with the measurements of the nodes
exps, conc_data = gen_exps("SP.xlsx")

for iexp in range(len(exps)):
    exps[iexp].y0 = exps[iexp].exp_data[0]


# The adjacency matrix is calculated from "conc_data". You can also specify the number of bins
# to be performed for the discretization of the measures in the calculation of mutual information
adjMat = buildmim(conc_data, NBINS)


# Generation of model parameters for subsequent simulation
model = getLBODEmodel(adjMat, random=True, is_stimuli=exps[0].is_stimuli, maxInput=REALK, min_tau=0.1, max_tau=12,
                      max_n=5, min_n=1, min_k=0.1, max_k=1)


# The "ivpsol" object is created for simulations
ivpsol = Ivpsol(atol=1e-5, rtol=1e-5, max_step_size=0.1, max_num_steps=int(5000), max_error_test_fails=int(50))

model.nthreads = int(8)

model.namesSpecies = exps[0].namesSpecies


# Optimization to find the values of x in the indices of model.index_opt that minimize the value of the simulation
res = optimization(model=model, exps=exps, ivpsol=ivpsol, epoch=3000, pop_size=50, miu_f=0.5, miu_cr=0.5)

f = res.f
time = res.time
fbest = res.fbest
xbest = res.xbest
neval = res.neval
numeval = res.numeval


# Results are saved in a list
list_save = [f, time, fbest, xbest, neval, numeval, model, conc_data, exps, initial_seed]
file_name = f"results/SP_opt_REALK_{REALK}_NBINS_{NBINS}_SEED_{initial_seed}.pkl"

# Gets the directory path
direct = os.path.dirname(file_name)

# The directory is created if it does not already exist
if not os.path.exists(direct):
    os.makedirs(direct)

# The list is saved to a file in the created directory
with open(file_name, "wb") as file:
    pickle.dump(list_save, file)


for i in range(len(model.index_opt)):
    model.x[model.index_opt[i]-1] = res.xbest[i]


# The graphs obtained before the reduction of the model are simulated and displayed
res_sim = simulate_logic_based_ode_obs(model, exps, ivpsol)
plot_results(exps, res_sim, 1, 10, 1, 4, 1.5)
plot_results(exps, res_sim, 1, 10, 5, 8, 1.5)
plot_results(exps, res_sim, 1, 10, 8, 13, 1.5)

# ################################################### MODEL REDUCTION ########################################################### #

conc_data_train = copy.deepcopy(conc_data)

n_data_train = 0
for i in range(len(conc_data_train)):
    for j in range(len(conc_data_train[i])):
        if conc_data_train[i][j] is not None:
            n_data_train += 1

# The "ivpsol" object is created for simulations
ivpsol = Ivpsol(atol=1e-5, rtol=1e-5, max_step_size=0.1, max_num_steps=int(5000), max_error_test_fails=int(50))

model.nthreads = int(8)

# Application of the Akaike approach
res = akaike(xbest, model, exps, ivpsol, 10, n_data_train)

# The previous model is converted to the "best_model" format
best_model = get_reduced_model(model, exps[0].is_stimuli)

# The number of arrow bows in the model is calculated
edges = rdm.sample(range(1, best_model.count_inputs+1), best_model.count_inputs)


# Checks whether it is possible to remove each arrow bow from the model
for i in range(len(edges)):
    for p in range(len(xbest)):
        best_model.x[best_model.index_opt[p] - 1] = xbest[p]

    reduced = get_reduced_model(best_model, exps[0].is_stimuli, edges[i])

    opt = optimization(model=model, exps=exps, ivpsol=ivpsol, epoch=3000, pop_size=50, miu_f=0.5, miu_cr=0.5)

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


# Results are saved in a list
list_save = [xbest, best_model, exps, conc_data, initial_seed, ivpsol]

# The list is saved to a file
file_name = f"results_reduced_AIC/SP_opt_REALK_{REALK}_NBINS_{NBINS}_SEED_{initial_seed}.pkl"

# Gets the directory path
direct = os.path.dirname(file_name)

# The directory is created if it does not already exist
if not os.path.exists(direct):
    os.makedirs(direct)

# The list is saved to a file in the created directory
with open(file_name, "wb") as file:
    pickle.dump(list_save, file)


# The graphs obtained after the reduction of the model are simulated and displayed
res_sim = simulate_logic_based_ode_obs(best_model, exps, ivpsol)
plot_results(exps, res_sim, 1, 10, 1, 4, 1.5)
plot_results(exps, res_sim, 1, 10, 5, 8, 1.5)
plot_results(exps, res_sim, 1, 10, 8, 13, 1.5)
