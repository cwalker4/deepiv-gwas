import numpy as np
from matplotlib import pyplot as plt

deep_big = np.loadtxt('simulation_results/deep_big.csv', delimiter=',')
ffn_big = np.loadtxt('simulation_results/ffn_big.csv', delimiter=',')

deep_big_avg = np.mean(deep_big, axis=0)
ffn_big_avg = np.mean(ffn_big, axis=0)

rho = [0.1, 0.25, 0.5, 0.75, 0.9]

plt.boxplot(deep_big, labels=rho, patch_artist=True)
plt.boxplot(ffn_big, labels=rho, patch_artist=True)
plt.patch.set_facecolor('red')
plt.show()

