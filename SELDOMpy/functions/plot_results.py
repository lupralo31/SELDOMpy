from matplotlib import pyplot


def plot_results(exps, res, n_exps_start, n_exps_end, n_nodos_start, n_nodos_end, y_lim):
    fig, axs = pyplot.subplots(n_exps_end - n_exps_start + 1, n_nodos_end - n_nodos_start + 1)
    for i in range(n_exps_start - 1, n_exps_end):
        for j in range(n_nodos_start - 1, n_nodos_end):
            exp_data_values = [val[j] for val in exps[i].exp_data]
            sim_values = [val[j] for val in res[i]]
            # Input data. axs[0,0] means row 0 column 0
            axs[i - n_exps_start + 1, j - n_nodos_start + 1].plot(exps[i].t_s, exp_data_values, 'bo')
            axs[i - n_exps_start + 1, j - n_nodos_start + 1].set_ylim([0, y_lim])
            axs[i - n_exps_start + 1, j - n_nodos_start + 1].plot(exps[i].t_s, sim_values, 'r')  # Simulation results
            axs[i - n_exps_start + 1, j - n_nodos_start + 1].set_ylim([0, y_lim])
            axs[i - n_exps_start + 1, j - n_nodos_start + 1].set_xlabel('Time')
            axs[i - n_exps_start + 1, j - n_nodos_start + 1].set_ylim([0, y_lim])
            if j == n_nodos_start-1:
                axs[i - n_exps_start + 1, j - n_nodos_start + 1].set_ylabel(f'Exp {i + 1}')
                axs[i - n_exps_start + 1, j - n_nodos_start + 1].set_ylim([0, y_lim])
            if i == 0:
                axs[i - n_exps_start + 1, j - n_nodos_start + 1].set_title(exps[i].namesSpecies[j])
                axs[i - n_exps_start + 1, j - n_nodos_start + 1].set_ylim([0, y_lim])
    pyplot.show()
