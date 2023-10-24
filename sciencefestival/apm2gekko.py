# -*- coding: utf-8 -*-
#
# Source: https://github.com/BYU-PRISM/GEKKO/blob/master/gekko/utilities/apm2gekko.py
# Copyright 2019 Advanced Process Solutions, LLC. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice, this list of
#       conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright notice, this list
#       of conditions and the following disclaimer in the documentation and/or other materials
#       provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY APMONITOR "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL APMONITOR OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those of the
# authors and should not be interpreted as representing official policies, either expressed
# or implied, of Advanced Process Solutions, LLC.

import re
import sys


def convertAPM(modelfile):

    new_filepath = modelfile.split('.')[0]+'_converted.py'

    f = open(modelfile)

    lines = f.readlines()

    state = 0
    # constants = 1
    # parameters = 2
    # variables = 3
    # intermediates = 4
    # equations = 5

    with open(new_filepath, "w") as f_new:
        # Import gekko and setup model
        print('from gekko import GEKKO', file=f_new)
        print('', file=f_new)
        print('m = GEKKO(remote=False)', file=f_new)
        print('m.options.SOLVER=1', file=f_new)
        print(
            'm.solver_options = [\'minlp_maximum_iterations 30000\', \'minlp_max_iter_with_int_sol 30000\']', file=f_new)
        print('m.solver_options = [\'minlp_maximum_iterations 10000\', \'minlp_max_iter_with_int_sol 30000\']', file=f_new)
        print('', file=f_new)

        for line in lines:
            # Remove spaces before and after
            line = line.strip()
            # Check which section of the model we are in
            if 'Model' in line and '!' not in line:
                print('', file=f_new)
                print('#%% ' + line, file=f_new)
                print('', file=f_new)
                state = 0
                continue
            if 'Constants' in line and '!' not in line:
                print('', file=f_new)
                print('#%% ' + line, file=f_new)
                print('', file=f_new)
                state = 1
                continue
            if 'Parameters' in line and '!' not in line:
                print('', file=f_new)
                print('#%% ' + line, file=f_new)
                print('', file=f_new)
                state = 2
                continue
            if 'Variables' in line and '!' not in line:
                print('', file=f_new)
                print('#%% ' + line, file=f_new)
                print('', file=f_new)
                state = 3
                continue
            if 'Intermediates' in line and '!' not in line:
                print('', file=f_new)
                print('#%% ' + line, file=f_new)
                print('', file=f_new)
                state = 4
                continue
            if 'Equations' in line and '!' not in line:
                print('', file=f_new)
                print('#%% ' + line, file=f_new)
                print('', file=f_new)
                state = 5
                continue
        #    print(state)

            # Split line content from comments
            line_content = line.split('!')[0]

            # Replace operators with TS version
            line_content = re.sub('cos\(', 'm.cos(', line_content)
            line_content = re.sub('sin\(', 'm.sin(', line_content)
            line_content = re.sub('tan\(', 'm.tan(', line_content)
            line_content = re.sub('exp\(', 'm.exp(', line_content)
            line_content = re.sub('sqrt\(', 'm.sqrt(', line_content)
            line_content = re.sub('log10\(', 'm.log10(', line_content)
            line_content = re.sub('log\(', 'm.log(', line_content)
            line_content = re.sub('\^', '**', line_content)

            # Split line by spaces
            words = line_content.split()

            # Replace derivative signs with dt()
            for i, word in enumerate(words):
                if ('$' in word):
                    subwords = re.split("[, \-!?:()\*^]+", word)
                    for subword in subwords:
                        if '$' in subword:
                            words[i] = words[i].replace(
                                subword, subword[1:]+str('.dt()'))

            # Check for end of line comments
            comment = ''  # Initialize comment as empty
            if (len(line.split('!')) > 1):
                comment = ' #' + line.split('!')[1]

            # Check for empty line
            if not words and len(line) == 0:
                print('', file=f_new)
            # Check for full line comments
            elif (line[0] == '!'):
                print(line.replace('!', '#'), file=f_new)
            elif (state == 1):
                # Constants
                print(str(words[0]) + ' = m.Const('+''.join(words[2:]) +
                      ',\''+str(words[0])+'\')' + comment, file=f_new)
            elif (state == 2):
                # Parameters
                print(str(words[0]) + ' = m.Param('+''.join(words[2:]) +
                      ',\''+str(words[0])+'\')' + comment, file=f_new)
            elif (state == 3):
                # Variables
                var_params = []
                # Split out just variable value
                value = re.split(',|<|<=|>|>=', ''.join(words[2:]))[0]
                if value != '':
                    value = 'value='+value
                else:
                    value = 'value=1'
                var_params.append(value)
                # Initialize lower and upper bounds
                lb = ''
                ub = ''
                # Parse bounds if any
                has_lb = False
                has_ub = False
                if ('<' in words):
                    ub = 'ub=' + words[words.index('<')+1].split(',')[0]
                    has_ub = True
                if ('<=' in words):
                    ub = 'ub=' + words[words.index('<=')+1].split(',')[0]
                    has_ub = True
                if ('>' in words):
                    lb = 'lb=' + words[words.index('>')+1].split(',')[0]
                    has_lb = True
                if ('>=' in words):
                    lb = 'lb=' + words[words.index('>=')+1].split(',')[0]
                    has_lb = True
                if has_lb:
                    var_params.append(lb)
                if has_ub:
                    var_params.append(ub)
                # Variable name
                if str(words[0]) != '':
                    if str(words[0]).startswith('int'):
                        var_params.append('integer=True')
                    name = 'name=' + '\''+str(words[0])+'\''
                    var_params.append(name)
                print(str(words[0]) + ' = m.Var(' +
                      ' , '.join(var_params)+')' + comment, file=f_new)
            elif (state == 4):
                # Intermediates
                print(str(words[0]).split('=')[0] + ' = m.Intermediate(' +
                      ''.join(words[2:])+',\''+str(words[0])+'\')' + comment, file=f_new)
            elif (state == 5):
                # Equations
                # Check for objective function
                if (words[0] == 'minimize'):
                    print(
                        'm.Obj('+''.join(words[1:])+')' + comment, file=f_new)
                elif (words[0] == 'maximize'):
                    print(
                        'm.Obj(-('+''.join(words[1:])+'))' + comment, file=f_new)
                # Otherwise add new equation
                else:
                    print('m.Equation('+''.join(words).replace('=', '==').replace('<==',
                          '<=').replace('>==', '>=')+')' + comment, file=f_new)
        # print('\nm.solve()',file=f_new)
    f.close()

    return


if __name__ == "__main__":
    filepath = sys.argv[1]
    convertAPM(filepath)
