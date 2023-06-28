import numpy as np
# Para imprimir las matrices por pantalla


def arrayprint(array):  # Función creada para visualizar mejor las matrices por pantalla
    a = np.array(array)
    print('\n'.join([''.join(['{:14}'.format(item) for item in row]) for row in a]))


def fill_array(array):
    # Función creada para rellenar las listas internas de una matriz con -1 hasta que tengan todas el mismo tamaño
    tamano_mayor = 0
    for i in range(len(array)):  # Averiguo cuantos elementos tiene la lista interna de mayor tamaño
        if len(array[i]) > tamano_mayor:
            tamano_mayor = len(array[i])
    for i in range(len(array)):
        if len(array[i]) < tamano_mayor:
            n_anadir = tamano_mayor - len(array[i])
            for j in range(n_anadir):
                array[i].append(-1)
    return array


class Ivpsol:
    def __init__(self, atol, rtol, max_step_size, max_num_steps, max_error_test_fails):
        # Constructor de la clase ivpsol. Se utilizará para las simulaciones en simulate_logic_based_ode_obs.py
        self.atol = atol
        self.rtol = rtol
        self.max_step_size = max_step_size
        self.max_num_steps = max_num_steps
        self. max_error_test_fails = max_error_test_fails


