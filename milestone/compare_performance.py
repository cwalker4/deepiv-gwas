import numpy as np
from matplotlib import pyplot as plt

import one_stage_nn
import deepiv_simulation
import time

n_simulations = 1 # number of draws from the DGP per sample size and rho
rhos = [0.1, 0.25, 0.5, 0.75, 0.9]
sample_sz = [1000, 5000, 10000, 20000] # if we want to test against diff sample sizes

deep_perf = np.zeros((n_simulations, len(rhos)))
ffn_perf = np.zeros_like(deep_perf)

n = 10000
for i, rho in enumerate(rhos):
    avg_deep = 0
    avg_ffn = 0
    for j in range(n_simulations):
        tic = time.time()
        print(i, j)
        
        print("Fitting deepiv")
        dp = deepiv_simulation.deepiv(n, rho)
        print("Fitting FFN")
        fp = one_stage_nn.one_stage(n, rho)
        deep_perf[j, i] = dp
        ffn_perf[j, i] = fp
        avg_deep += dp
        avg_ffn += fp
        print(dp, fp)
        print(fp)
        toc = time.time()

        print("Time for iteration: %.4f" % (toc - tic))

    avg_deep = avg_deep / n_simulations
    avg_ffn = avg_ffn/ n_simulations
    print("For rho = %f" % rho)
    print("Avg ffn: %.5f" % avg_ffn)
    print("Avg deep: %.5f" % avg_deep)

np.savetxt('simulation_results/ffn.csv', ffn_perf, delimiter=',')
np.savetxt('simulation_results/deep.csv', deep_perf, delimiter=',')
        
                

