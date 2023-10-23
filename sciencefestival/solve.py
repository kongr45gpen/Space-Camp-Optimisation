# Install APMonitor
# from APMonitor.apm import *

# Solve optimization problem
# sol = apm_solve('system', 3)

# print(sol)

#%% Prepare the name

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("filename", default="output")

args = parser.parse_args()

#%% Solve equation

import apm2gekko

apm2gekko.convertAPM("system.apm")

from gekko.apm import get_file
import system_converted as s
print(s.m._server)
print(s.m._model_name)

s.m.solve()


#%% Display Results

results = {
    "variables": {},
    "intermediates": {}
}

for variable, value in s.__dict__.items():
    # print(type(value).__name__)
    if type(value).__name__ == "GKVariable":
        print("{} -> {}".format(variable, value.VALUE))
        results["variables"][variable] = value.VALUE[0]
    elif type(value).__name__ == "GK_Intermediate":
        print("{} -> {}".format(variable, value.VALUE))
        results["intermediates"][variable] = value.VALUE[0]

import json

with open(args.filename + ".json", 'w') as f:
    json_str = json.dumps(results, indent=4)
    f.write(json_str)

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

print(highlight(json.dumps(results, indent=4), JsonLexer(), TerminalFormatter()))


# f = get_file(m._server,m._model_name,'infeasibilities.txt')
# f = f.decode().replace('\r','')
# with open('infeasibilities.txt', 'w') as fl:
#     fl.write(str(f))
# %%
