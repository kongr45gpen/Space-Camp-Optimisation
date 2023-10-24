#%% Initialisation

import apm2gekko
from importlib import reload

def save_results(filename):
    results = {
        "variables": {},
        "intermediates": {}
    }

    for variable, value in s.__dict__.items():
        try:
        # print(type(value).__name__)
            if type(value).__name__ == "GKVariable":
                print("{} -> {}".format(variable, value.VALUE))
                results["variables"][variable] = value.VALUE[0]
            elif type(value).__name__ == "GK_Intermediate":
                print("{} -> {}".format(variable, value.VALUE))
                results["intermediates"][variable] = value.VALUE[0]
                if variable == "price":
                    results["intermediates"]["Cost"] = value.VALUE[0]
                elif variable == "xperience":
                    results["intermediates"]["Score"] = value.VALUE[0]
        except Exception as e:
            print("Error with {}".format(variable))
            print("{}".format(e))

    import json

    with open("outputs/" + filename + ".json", 'w') as f:
        json_str = json.dumps(results, indent=4)
        f.write(json_str)

    from pygments import highlight
    from pygments.lexers import JsonLexer
    from pygments.formatters import TerminalFormatter

    print(highlight(json.dumps(results, indent=2), JsonLexer(), TerminalFormatter()))

    return s.xperience.VALUE[0], s.price.VALUE[0]

apm2gekko.convertAPM("system.apm")

from gekko.apm import get_file
import system_converted as s
print(s.m._server)
print(s.m._model_name)

#%% Full Solve

s.m.solve()

score, cost = save_results("max_1")

s.m.Equation(s.xperience <= score-1)
s.m.solve()

score, cost = save_results("max_2")

s.m.Equation(s.xperience <= score-1)
s.m.solve()

score, cost = save_results("max_3")

reload(s)

#%% No astronaut solve

# Provide no beds for astronauts
s.m.Equation(s.bed == 0)
#

s.m.solve()

score, cost = save_results("no_astronaut_1")

s.m.Equation(s.xperience <= score-1)
s.m.solve()

score, cost = save_results("no_astronaut_2")

s.m.Equation(s.xperience <= score-1)
s.m.solve()

score, cost = save_results("no_astronaut_3")

reload(s)

# %% No sample return

s.m.Equation(s.bed == 0)
s.m.Equation(s.int_samp_retu == 0)
s.m.solve(disp=True)

score, cost = save_results("no_return_1")

s.m.Equation(s.xperience <= score-1)
s.m.solve(disp=True)

score, cost = save_results("no_return_2")

s.m.Equation(s.xperience <= score-1)
s.m.solve(disp=True)

score, cost = save_results("no_return_3")

reload(s)

#%% Full Solve, cost optim

s.efficiency = s.m.Intermediate(s.price / (s.xperience + 0.01), name="efficiency")
s.m._objectives[0] = 'minimize ((price)/(xperience + 0.01))'
s.m.Equation(s.xperience >= 1)
s.m.solve(disp=True)

save_results("zcheapest_max_1")

s.m.Equation(s.efficiency > s.efficiency.VALUE[0] * 1.01)
s.m.solve(disp=True)

save_results("zcheapest_max_2")

s.m.Equation(s.efficiency > s.efficiency.VALUE[0] * 1.01)
s.m.solve(disp=True)

save_results("zcheapest_max_3")

reload(s)

#%% Full Solve, cost optim, with astronauts

s.efficiency = s.m.Intermediate(s.price / (s.xperience + 0.01), name="efficiency")
s.m._objectives[0] = 'minimize ((price)/(xperience + 0.01))'
s.m.Equation(s.xperience >= 1)
s.m.Equation(s.bed >= 1)
s.m.Equation(s.food >= 1)
s.m.solve(disp=True)

save_results("zcheapest_astronauts_1")

s.m.Equation(s.efficiency > s.efficiency.VALUE[0] * 1.01)
s.m.solve(disp=True)

save_results("zcheapest_astronauts_2")

s.m.Equation(s.efficiency > s.efficiency.VALUE[0] * 1.01)
s.m.solve(disp=True)

save_results("zcheapest_astronauts_3")

reload(s)