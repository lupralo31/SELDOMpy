import pandas as pd


# Pandas package required to import Excel data
# Openpyxl library needed for panda use


class Experiment:
    def __init__(self, t_s, t_0, t_f, n_controls_t, index_observables, u, exp_data, is_stimuli,
                 y0, t_con, n_observables, namesSpecies):
        # Constructor of the Experiment class. It will be used to create objects with the data of each experiment
        self.t_s = t_s
        self.t_0 = t_0
        self.t_f = t_f
        self.n_controls_t = n_controls_t
        self.index_observables = index_observables
        self.u = u
        self.exp_data = exp_data
        self.is_stimuli = is_stimuli
        self.y0 = y0
        self.t_con = t_con
        self.n_observables = n_observables
        self.namesSpecies = namesSpecies


def gen_exps(excel_exps):
    excelExps = pd.read_excel(excel_exps)
    # The Excel file where the data of the different experiments have been defined is read
    n_exps = len(excelExps.columns) - 1
    # The number of experiments in the excel sheet is calculated
    exps = []
    # The "exps" list is initialized, which will contain objects of the Experiment class with information from the experiments
    conc_data = []

    for i in range(n_exps):
        # For each experiment...
        experiment = pd.read_excel(excel_exps, index_col=i + 1)
        # Object with the data of an Experiment

        t_s = (list(experiment.index)[0]).split(',')
        for j in range(len(t_s)):
            t_s[j] = float(t_s[j])
        # "t_s" values are saved in a float list

        t_0 = float(experiment.index[1])
        # The value of "t_0" is saved in a float

        t_f = float(experiment.index[2])
        # The value of "t_f" is saved in a float

        n_controls_t = int(experiment.index[3])
        # The value of "n_controls_t" is saved in an int

        index_observables = (list(experiment.index)[4]).split(',')
        for k in range(len(index_observables)):
            index_observables[k] = int(index_observables[k])
        # The value of "index_observables" is saved in an ints list

        u = (list(experiment.index)[5]).split(',')
        for l in range(len(u)):
            u[l] = int(u[l])
        # The value of "u" is saved in a list of ints

        exp_data = (list(experiment.index)[6]).split(';')
        for m in range(len(exp_data)):
            exp_data[m] = exp_data[m].split(',')
            for n in range(len(exp_data[m])):
                exp_data[m][n] = float(exp_data[m][n])
            conc_data.append(exp_data[m])  # The array "conc_data" is formed each time the statement is executed
        # The value of exp_data is stored in an array with as many lists (as many rows) as measures
        # and in each of them as many elements (as many columns) as nodes. Values are floats

        is_stimuli = (list(experiment.index)[7]).split(',')
        for o in range(len(is_stimuli)):
            is_stimuli[o] = int(is_stimuli[o])
        # The value of "is_stimuli" is saved in an ints list

        t_con = (list(experiment.index)[8]).split(',')
        for q in range(len(t_con)):
            t_con[q] = float(t_con[q])
        # The value of "t_con" is saved in a list of floats

        n_observables = int(experiment.index[9])
        # The value of "n_observables" is saved in an int

        namesSpecies = (list(experiment.index)[10]).split(',')
        for r in range(len(namesSpecies)):
            namesSpecies[r] = str(namesSpecies[r])
        # The value of "namesSpecies" is saved in a list of strings

        y0 = []
        # "y0" is valued at MAPK_training_and_reduce.py

        exps.append(Experiment(t_s, t_0, t_f, n_controls_t, index_observables, u, exp_data,
                               is_stimuli, y0, t_con, n_observables, namesSpecies))
        # An object of type "Experiment" is created with the calculated data and this object is added to the "exps" list

    return exps, conc_data
