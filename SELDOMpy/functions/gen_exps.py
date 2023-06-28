import pandas as pd
# Se importa la libreria pandas necesaria para importar datos de Excel
# Además se añadió al proyecto la libreria openpyxl, necesaria para el uso de pandas (pandas la llama por debajo)


class Experiment:
    def __init__(self, t_s, t_0, t_f, n_controls_t, index_observables, u, exp_data, is_stimuli,
                 y0, t_con, n_observables, namesSpecies):
        # Constructor de la clase Experiment. Se utilizará para crear objetos con los datos de cada experimento
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
    # Se lee el archivo de Excel donde se han definido los datos de los diferentes experimentos
    n_exps = len(excelExps.columns) - 1
    # Se calcula el nº de experimentos que hay en la hoja de excel
    exps = []
    # Se inicializa la lista exps, que contendrá objetos de la clase Experiment con información de los experimentos
    conc_data = []

    for i in range(n_exps):
        # Para cada experimento...
        experiment = pd.read_excel(excel_exps, index_col=i + 1)
        # Objeto con los datos de un Experimento

        t_s = (list(experiment.index)[0]).split(',')
        for j in range(len(t_s)):
            t_s[j] = float(t_s[j])
        # Se guardan los valores de t_s en una lista de floats

        t_0 = float(experiment.index[1])
        # Se guarda el valor de t_0 en un float

        t_f = float(experiment.index[2])
        # Se guarda el valor de t_f en un float

        n_controls_t = int(experiment.index[3])
        # Se guarda el valor de n_controls_t en un int

        index_observables = (list(experiment.index)[4]).split(',')
        for k in range(len(index_observables)):
            index_observables[k] = int(index_observables[k])
        # Se guarda el valor de index_observables en una lista de ints

        u = (list(experiment.index)[5]).split(',')
        for l in range(len(u)):
            u[l] = int(u[l])
        # Se guarda el valor de u en una lista de ints

        exp_data = (list(experiment.index)[6]).split(';')
        for m in range(len(exp_data)):
            exp_data[m] = exp_data[m].split(',')
            for n in range(len(exp_data[m])):
                exp_data[m][n] = float(exp_data[m][n])
            conc_data.append(exp_data[m])  # Voy formando la matriz conc_data cada vez que ejecuto la instrucción
        # Se guarda el valor de exp_data en una matriz con tantas listas (tantas filas) como medidas y en cada una
        # de ellas tantos elementos (tantas columnas) como nodos. Los valores son floats

        is_stimuli = (list(experiment.index)[7]).split(',')
        for o in range(len(is_stimuli)):
            is_stimuli[o] = int(is_stimuli[o])
        # Se guarda el valor de is_stimuli en una lista de ints

        t_con = (list(experiment.index)[8]).split(',')
        for q in range(len(t_con)):
            t_con[q] = float(t_con[q])
        # Se guarda el valor de t_con en una lista de floats

        n_observables = int(experiment.index[9])
        # Se guarda el valor de n_observables en un int

        namesSpecies = (list(experiment.index)[10]).split(',')
        for r in range(len(namesSpecies)):
            namesSpecies[r] = str(namesSpecies[r])
        # Se guarda el valor de namesSpecies en una lista de strings

        y0 = []
        # Le doy el valor a y0 en training_and_reduce.py

        exps.append(Experiment(t_s, t_0, t_f, n_controls_t, index_observables, u, exp_data,
                               is_stimuli, y0, t_con, n_observables, namesSpecies))
        # Se crea un objeto de tipo Experiment con los datos calculados y se añade este objeto a la lista exps

    return exps, conc_data

