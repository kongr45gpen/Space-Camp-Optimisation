# Install APMonitor
from APMonitor.apm import *

# Solve optimization problem
sol = apm_solve('system', 3)

print(sol)

# import apm2gekko

# apm2gekko.convertAPM("system.apm")

# # from gekko.apm import get_file
# # print(m._server)
# # print(m._model_name)
# # f = get_file(m._server,m._model_name,'infeasibilities.txt')
# # f = f.decode().replace('\r','')
# # with open('infeasibilities.txt', 'w') as fl:
# #     fl.write(str(f))