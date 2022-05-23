f = open("input.txt", 'r')
g = open("output.txt", 'w')

lambda_nfa = {}
alphabet = [letter for letter in f.readline().split()]
initial = int(f.readline())
finals = set(int(x) for x in f.readline().split())

for line in f:
    begin, symbol, end = line.split()
    begin, end = int(begin), int(end)
    if begin in lambda_nfa:
        lambda_nfa[begin].append(tuple([end, symbol]))
    else:
        lambda_nfa[begin] = [tuple([end, symbol])]

# lambda completion

ok = True
while ok:
    ok = False
    for state in lambda_nfa.keys():
        for nxt_state in lambda_nfa[state]:
            if nxt_state[1] == '#' and nxt_state[0] in lambda_nfa.keys():
                for nxt_nxt_state in lambda_nfa[nxt_state[0]]:
                    if nxt_nxt_state[1] == '#':
                        aux = tuple([nxt_nxt_state[0], '#'])
                        if aux not in lambda_nfa[state]:
                            lambda_nfa[state].append(aux)
                            ok = True

# lambda-transition removal

for state in lambda_nfa.keys():
    for nxt_state in lambda_nfa[state]:
        if nxt_state[1] == '#' and nxt_state[0] in lambda_nfa.keys():
            for nxt_nxt_state in lambda_nfa[nxt_state[0]]:
                if nxt_nxt_state[1] != '#':
                    x = tuple([nxt_nxt_state[0], nxt_nxt_state[1]])
                    if x not in lambda_nfa[state]:
                        lambda_nfa[state].append(x)

for state in lambda_nfa.keys():
    aux = [x for x in lambda_nfa[state] if x[1] != '#']
    lambda_nfa[state] = aux.copy()

# nfa to dfa

dfa_tranzitions = []
dfa_finals = []
q = [(initial,)]
nfa_transitions = {}
dfa_transitions = {}

data = []
for state in lambda_nfa:
    for letter in alphabet:
        temp = []
        for t in lambda_nfa[state]:
            if letter == t[1]:
                temp.append(t[0])
        if temp != []:
            data.append([state, letter, temp])

for transition in data:
    nfa_transitions[(transition[0], transition[1])] = transition[2]

for begin in q:
    for symbol in alphabet:
        if len(begin) == 1 and (begin[0], symbol) in nfa_transitions:
            dfa_transitions[(begin, symbol)] = nfa_transitions[(begin[0], symbol)]
            if tuple(dfa_transitions[(begin, symbol)]) not in q:
                q.append(tuple(dfa_transitions[(begin, symbol)]))
        else:
            dest = []
            f_dest = []
            for n_state in begin:
                if (n_state, symbol) in nfa_transitions and nfa_transitions[(n_state, symbol)] not in dest:
                    dest.append(nfa_transitions[(n_state, symbol)])
            if dest:
                for d in dest:
                    for value in d:
                        if value not in f_dest:
                            f_dest.append(value)
                dfa_transitions[(begin, symbol)] = f_dest
                if tuple(f_dest) not in q:
                    q.append(tuple(f_dest))

for key, value in dfa_transitions.items():
    aux = [[key[0], key[1], value]]
    dfa_tranzitions.extend(aux)

for q_state in q:
    for f_state in finals:
        if f_state in q_state:
            dfa_finals.append(q_state)

g.write(f"Stare initiala: {initial}\nStari finale: ")
for fin in set(dfa_finals):
    for x in fin:
        g.write(str(x))
    g.write(" ")

g.write('\nTranzitii:\n')
for transition in dfa_tranzitions:
    begin, symbol, end = transition
    begin = "".join([str(x) for x in begin])
    end = "".join([str(x) for x in end])
    g.write(f"{begin} cu {symbol} in {end}\n")

f.close()
g.close()