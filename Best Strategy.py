import json
# 0 means Cooperate and 1 means Defect in calculations
# The utility matrix:
#    -------------------
#    |P1\P2|  C  |  D  |
#    -------------------
#    |  C  | 3,3 | 0,5 |
#    -------------------
#    |  D  | 5,0 | 1,1 |
#    -------------------
def genStr(num:int):
    s = ''
    s += str(num % 2)
    while num >= 2:
        num = int(num / 2)
        s += str(num % 2)
    while len(s) < 5:
        s += '0'
    s = s[::-1]
    return s
class DFA:
    state = 0  # current state
    s = []  # transition function
    def __init__(self, num):
        self.state = int(num[0])
        self.s = [[0, 0], [0, 0]]
        self.s[0][0] = int(num[1])
        self.s[0][1] = int(num[2])
        self.s[1][0] = int(num[3])
        self.s[1][1] = int(num[4])
def action(p1:DFA, p2:DFA):
    l = [[p1.state, p2.state]]  # list of each stage strategy
    p1_state = p1.state
    p2_state = p2.state
    for i in range(11):  # repeat the games 6 times
        s1 = p1_state
        s2 = p2_state
        p1_state = p1.s[s1][s2]
        p2_state = p2.s[s2][s1]
        l.append([p1_state, p2_state])
    return l
def utility(l:list):
    u = [0, 0]
    for i in range(12):
        if l[i] == [0, 0]:
            u[0] += 3
            u[1] += 3
        elif l[i] == [0, 1]:
            u[1] += 5
        elif l[i] == [1, 0]:
            u[0] += 5
        elif l[i] == [1, 1]:
            u[0] += 1
            u[1] += 1
    return u
def bestResp(p:DFA):
    maxUtility = -1
    bestResponse = DFA(genStr(0))
    for i in range(32):
        p2 = DFA(genStr(i))
        p1 = p
        u = utility(action(p1, p2))
        #print(i, u, action(p1, p2))
        if u[1] > maxUtility:
            maxUtility = u[1]
            bestResponse = p2
    return bestResponse
def writeOut(p:DFA):
    g = open('output2.txt', 'w')
    g.write('{\n\t"states": {\n\t\t"s1": "c",\n\t\t"s2": "d"\n\t},\n')
    g.write('\t"start": "')
    if p.state == 0:
        g.write('s1')
    else:
        g.write('s2')
    g.write('",\n\t"transitions": {\n')
    g.write('\t\t"s1": ["')
    if p.s[0][0] == 0:
        g.write('s1", "')
    else:
        g.write('s2", "')
    if p.s[0][1] == 0:
        g.write('s1"],\n')
    else:
        g.write('s2"],\n')
    g.write('\t\t"s2": ["')
    if p.s[1][0] == 0:
        g.write('s1", "')
    else:
        g.write('s2", "')
    if p.s[1][1] == 0:
        g.write('s1"]\n\t}\n}')
    else:
        g.write('s2"]\n\t}\n}')
    g.close()
def readIn():
    p = DFA(genStr(0))
    with open('input.txt', 'r') as file:
        f = file.read()
        j = json.loads(f)
        p.state = int(j['states'][j['start']] != 'c')
        i1 = int(j['states']['s1'] != 'c')
        i2 = int(j['states']['s2'] != 'c')
        if j['transitions']['s1'][0] == 's1':
            p.s[i1][i1] = i1
        elif j['transitions']['s1'][0] == 's2':
            p.s[i1][i1] = i2
        if j['transitions']['s1'][1] == 's1':
            p.s[i1][i2] = i1
        elif j['transitions']['s1'][1] == 's2':
            p.s[i1][i2] = i2
        if j['transitions']['s2'][0] == 's1':
            p.s[i2][i1] = i1
        elif j['transitions']['s2'][0] == 's2':
            p.s[i2][i1] = i2
        if j['transitions']['s2'][1] == 's1':
            p.s[i2][i2] = i1
        elif j['transitions']['s2'][1] == 's2':
            p.s[i2][i2] = i2
    return p
# main
p = readIn()
br = bestResp(p)
writeOut(br)
print(br.state, br.s)