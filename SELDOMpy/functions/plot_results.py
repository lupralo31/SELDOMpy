from matplotlib import pyplot


def plot_results(exps, res, n_exps_inic, n_exps_fin, n_nodos_inic, n_nodos_fin, y_lim):
    fig, axs = pyplot.subplots(n_exps_fin-n_exps_inic+1, n_nodos_fin-n_nodos_inic+1)
    for i in range(n_exps_inic-1, n_exps_fin):
        for j in range(n_nodos_inic-1, n_nodos_fin):
            exp_data_values = [val[j] for val in exps[i].exp_data]
            sim_values = [val[j] for val in res[i]]
            axs[i-n_exps_inic+1, j-n_nodos_inic+1].plot(exps[i].t_s, exp_data_values, 'bo')  # Datos de entrada. axs[0,0] significa fila 0 columna 0
            axs[i-n_exps_inic+1, j-n_nodos_inic+1].set_ylim([0, y_lim])
            axs[i-n_exps_inic+1, j-n_nodos_inic+1].plot(exps[i].t_s, sim_values, 'r')  # Resultados de la simulacion
            axs[i-n_exps_inic+1, j-n_nodos_inic+1].set_ylim([0, y_lim])
            axs[i-n_exps_inic+1, j-n_nodos_inic+1].set_xlabel('Time')
            axs[i-n_exps_inic+1, j-n_nodos_inic+1].set_ylim([0, y_lim])
            if j == n_nodos_inic-1:
                axs[i-n_exps_inic+1, j-n_nodos_inic+1].set_ylabel(f'Exp {i+1}')
                axs[i-n_exps_inic+1, j-n_nodos_inic+1].set_ylim([0, y_lim])
            if i == 0:
                axs[i-n_exps_inic+1, j-n_nodos_inic+1].set_title(exps[i].namesSpecies[j])
                axs[i-n_exps_inic+1, j-n_nodos_inic+1].set_ylim([0, y_lim])
    pyplot.show()
    fig.savefig('solution_graph.pdf')

