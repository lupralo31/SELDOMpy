import numpy as np
# To print the arrays per screen
import pickle
# To save the results to a binary file


# Function created to better visualize the matrices by screen
def arrayprint(array):
    a = np.array(array)
    print('\n'.join([''.join(['{:14}'.format(item) for item in row]) for row in a]))


# Function created to populate the internal lists of an array with -1 until they are all the same size
def fill_array(array):
    larger_size = 0
    for i in range(len(array)):  # Find out how many items the largest internal list has
        if len(array[i]) > larger_size:
            larger_size = len(array[i])
    for i in range(len(array)):
        if len(array[i]) < larger_size:
            n_append = larger_size - len(array[i])
            for j in range(n_append):
                array[i].append(-1)
    return array


class Ivpsol:
    def __init__(self, atol, rtol, max_step_size, max_num_steps, max_error_test_fails):
        # Constructor of the "ivpsol" class. It will be used for simulations in simulate_logic_based_ode_obs.py
        self.atol = atol
        self.rtol = rtol
        self.max_step_size = max_step_size
        self.max_num_steps = max_num_steps
        self. max_error_test_fails = max_error_test_fails


