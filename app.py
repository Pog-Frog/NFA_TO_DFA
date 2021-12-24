import pandas as pd

"""
states_no = int(input("Enter the number of states: "))
print("##Note: The empty input 'ε' is represented by '$' and is counted in the number of inputs\n")
input_no = int(input("Enter the number of possible inputs: "))
"""
nfa = {'1': {'a': ['1'], 'b': ['2']}, '2': { 'a': ['2','3'], 'b': ['3']}, '3': {'a': ['1'], 'b': []}}
dfa = {}
nfa_inputs = ['a', 'b']
empty_flag = False

"""
for i in range(input_no):
    tmp = input("\nEnter an input: ")
    if tmp == '$':
        empty_flag = True 
    nfa_inputs.append(tmp)

print("\n")

for i in range(states_no):
    state = input("\n\nEnter a state: ")
    nfa[state] = {}
    for j in range(input_no):
        print(f"Enter the next state(s) when the current state {state} has the input '{nfa_inputs[j]}': ")
        nfa[state][nfa_inputs[j]] = list(x for x in input().strip().split())
"""
##nfa_end_state = list(input("Enter the end state(s): ")).strip().split()
nfa_end_state = ['1']
dfa_end_state = []
nfa_states = list(nfa.keys())
nfa_table = pd.DataFrame(nfa)
nfa_new_states = {}
nfa_new_states_states = []
nfa_new_states_table = {}
print(f"\n\nnfa table:\n{nfa_table.transpose()}")
print(f"nfa_states: {nfa_states}")
print(f"nfa_end_state(s): {nfa_end_state}")


def add_nfa_new_states(lst):
    nfa_new_states[tuple(lst)] = {}
    for k in nfa_inputs:
        nfa_new_states[tuple(lst)][k] = []
        tmp = []
        for l in lst:
            tmp.extend(nfa[l][k])
        tmp = sorted(list(dict.fromkeys(tmp)))
        nfa_new_states[tuple(lst)][k] = tmp
        if tuple(tmp) not in nfa_new_states_states:
            nfa_new_states_states.append(tuple(tmp))
            add_nfa_new_states(tmp)


if '$' in nfa_inputs:
    empty_flag = True

if not empty_flag:
    for i in nfa_states:
        for j in nfa_inputs:
            if len(nfa[i][j]) > 1 and tuple(nfa[i][j]) not in nfa_new_states_states:
                nfa_new_states[tuple(nfa[i][j])] = {}
                nfa_new_states_states.append(tuple(nfa[i][j]))
                for k in nfa_inputs:
                    nfa_new_states[tuple(nfa[i][j])][k] = []
                    tmp = []
                    for l in nfa[i][j]:
                        tmp.extend(nfa[l][k])
                    tmp = sorted(list(dict.fromkeys(tmp)))
                    nfa_new_states[tuple(nfa[i][j])][k] = tmp
                    if tmp not in nfa_new_states_states and len(tmp) > 1:
                        nfa_new_states_states.append(tuple(tmp))
                        add_nfa_new_states(tmp)
    
    for i in nfa_states:
        if i in nfa_end_state:
            dfa_end_state.append(''.join(sorted(i)))

    for i in nfa_new_states.keys():
        nfa_new_states_table[''.join(sorted(i))] = nfa_new_states[i]
        for j in i:
            if j in nfa_end_state and i not in dfa_end_state:
                dfa_end_state.append(''.join(sorted(i)))

    for i in nfa_states:
        if i in nfa_end_state and i not in dfa_end_state:
            dfa_end_state.append(''.join(sorted(i)))
        """
        for i in nfa_new_states_table.keys():
            for j in nfa_inputs:
                nfa_new_states_table[i][j] = ''.join(nfa_new_states_table[i][j])    
        """
    nfa.update(nfa_new_states_table)
    nfa_new_states_table = pd.DataFrame(nfa).transpose()
    print("\n\ndfa table: \n", nfa_new_states_table)
    print(f"\n\ndfa end state(s): {list(dict.fromkeys(dfa_end_state))}")
else:
    closure_nfa_states = {}
    ## getting closure of 1st state
    for i in nfa_states:
        if len(nfa[i]['$']) > 0:
            closure_nfa_states[i] = []
            closure_nfa_states[i].extend(nfa[i]['$'])
            if nfa_states.index(i) == 0:
                closure_nfa_states[i].extend([i])
                closure_nfa_states[i] = sorted(closure_nfa_states[i])
                add_nfa_new_states(closure_nfa_states[i])

    print("\n\nClosures of nfa: ", closure_nfa_states)

    for i in nfa_states:
        if i in nfa_end_state:
            dfa_end_state.append(''.join(sorted(i)))

    for i in nfa_new_states.keys():
        if not ''.join((sorted(i))) == '' and empty_flag:
            nfa_new_states_table[''.join(sorted(i))] = nfa_new_states[i]
            for j in i:
                if j in nfa_end_state and i not in dfa_end_state:
                    dfa_end_state.append(''.join(sorted(i)))
        else:
            nfa_new_states_table['$'] = nfa_new_states[i]
            for j in i:
                if j in nfa_end_state and i not in dfa_end_state:
                    dfa_end_state.append('')

    for i in nfa_states:
        if i in nfa_end_state and i not in dfa_end_state:
            dfa_end_state.append(''.join(sorted(i)))
        """
        for i in nfa_new_states_table.keys():
            for j in nfa_inputs:
                nfa_new_states_table[i][j] = ''.join(nfa_new_states_table[i][j])    
        """
    for i in nfa_new_states_table.keys():
        del nfa_new_states_table[i]['$']
    ##nfa.update(nfa_new_states_table)
    nfa_new_states_table = pd.DataFrame(nfa_new_states_table).transpose()
    print("\n\ndfa table: \n", nfa_new_states_table)
    print(f"\n\ndfa end state(s): {list(dict.fromkeys(dfa_end_state))}")

"""
for i in range(states_no):
    for j in range(input_no):
        for k in range(len(nfa[i][j])):
"""

"""
{
 ('2', '3'): {'a': ['2', '3', '1'], 'b': ['3']},
  ('2', '3', '1'): {'a': ['2', '3', '1'], 'b': ['3', '2']}
}
"""
