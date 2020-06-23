import pickle
import matplotlib.pyplot as plt
import numpy as np

tau = pickle.load(open("results/m1_matrix_inf.pkl", 'rb'))
print(tau)
# sigma = pickle.load(open("results/data_sigma.pkl", 'rb'))
# sigmastar = pickle.load(open("results/data_sigmastar.pkl", 'rb'))
#
# # tau plot
# t_tau = np.arange(0,len(tau))
# plt.plot(t_tau,tau)
# plt.title("tau")
# plt.xlabel("timestep")
# plt.ylabel("tau")
# plt.savefig("plots/tau.png")
# plt.show()
#
#
# # sigma plot
# t_sigma = np.arange(0,len(sigma))
# plt.plot(t_sigma,sigma)
# plt.title("sigma")
# plt.xlabel("timestep")
# plt.ylabel("sigma")
# plt.savefig("plots/sigma.png")
# plt.show()
#
#
# # sigmastar plot
# t_sigmastar = np.arange(0,len(sigmastar))
# plt.plot(t_sigmastar,sigmastar)
# plt.title("sigma star")
# plt.xlabel("timestep")
# plt.ylabel("sigma star")
# plt.savefig("plots/sigmastar.png")
# plt.show()
