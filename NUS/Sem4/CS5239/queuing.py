import numpy as np
from scipy.special import factorial

l=3
mu=5
m=1

rho=l/(m*mu)
p0=1/(1+(m*rho)**m/(factorial(m)*(1-rho))+np.sum([(m*rho)**n/factorial(n) for n in range(1, m)]))
rho_=p0*(m*rho)**m/(factorial(m)*(1-rho))
Ew=rho_/(m*mu*(1-rho))
En=m*rho+rho*rho_/(1-rho)

Er=Ew+1/mu
throughput=En/Er
E90=Ew/rho_*np.log(10*rho_)

print('rho={}'.format(rho))
print('p0={}'.format(p0))
print('rho_={}'.format(rho_))
print('Ew={}'.format(Ew))
print('En={}'.format(En))
print('Er={}'.format(Er))
print('E90={}'.format(E90))
print('throughput={}'.format(throughput))
