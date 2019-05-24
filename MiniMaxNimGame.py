import random
from functools import lru_cache as cache

def get_input(message):    #input handler
    input_num = input(message)
    try:
        return int(input_num) 
    except:
        print("Invalid Input".format(input_num))
        return get_input(message)

def init():       #initializng the game
    p1Type = get_input('Choose the type of player 1 (1 for Human, 2 for Random, 3 for AI): ')
    while p1Type not in (1,2,3):
        print("Wrong Input")
        p1Type = get_input('Choose the type of player 1 (1 for Human, 2 for Random, 3 for AI): ')
    p2Type = get_input('Choose the type of player 2 (1 for Human, 2 for Random, 3 for AI): ')
    while p2Type not in (1,2,3):
        print("Wrong Input")
        p2Type = get_input('Choose the type of player 1 (1 for Human, 2 for Random, 3 for AI): ')
    return p1Type, p2Type, [random.randint(2,9),random.randint(2,9),random.randint(2,9)]

def humanMove(state):
    index = get_input("Select the heap Index: ")
    while index not in range(0,len(state[1])):
        print("Wrong Input")
        index = get_input('Select the heap Index: ')
    if(state[1][index] == 2):           #if heap is 2
        get = get_input('press 1 to score and 2 to add to other number: ')
        while get not in (1,2):
            print("Wrong Input")
            get = get_input('press 1 to score and 2 to add to other number: ')
        if(get == 1):           #deleting from heap and adding to score
            state[1] = state[1][:index] + state[1][index+1 :]
            if(state[0]==1):
                state[2]=state[2]+2
            else:
                state[3]=state[3]+2
        else:       #addin to another heap
            index2 = get_input('Select the index to add in: ')
            while(index2 == index or index2 not in range(0,len(state[1]))):
                index2 = get_input('Select the index to add in: ')
            if((state[1][index] + state[1][index2]) < 10):
                state[1][index2] = state[1][index] + state[1][index2]
            else:
                state[1][index2] = 10
            state[1] = state[1][:index] + state[1][index+1 :]
    elif(state[1][index]%2 == 1):          #if heap is odd
        get = get_input('press 1 to apply Collatz-Ulam step and 2 to add to other number: ')
        while get not in (1,2):
            print("Wrong Input")
            get = get_input('press 1 to apply Collatz-Ulam step and 2 to add to other number: ')
        if(get == 1):      #Ulam step
            state[1][index] = (3 * state[1][index]) + 1
        else:               #adding to another heap
            index2 = get_input('Select the index to add in: ')
            while(index2 == index or index2 not in range(0,len(state[1]))):
                index2 = get_input('Select the index to add in: ')
            if((state[1][index] + state[1][index2]) < 10):
                state[1][index2] = state[1][index] + state[1][index2]
            else:
                state[1][index2] = 10
            state[1] = state[1][:index] + state[1][index+1 :]
    else:
        get = get_input('press 1 to divide and 2 to add to other number: ')
        while get not in (1,2):
            print("Wrong Input")
            get = get_input('press 1 to divide and 2 to add to other number: ')
        if(get == 1):               #diving heap into 2 equal size heaps
            state[1][index] = int(state[1][index]/2)
            state[1].insert(index + 1, state[1][index])
        else:             #adding to another heap
            index2 = get_input('Select the index to add in: ')
            while(index2 == index or index2 not in range(0,len(state[1]))):
                index2 = get_input('Select the index to add in: ')
            if((state[1][index] + state[1][index2]) < 10):
                state[1][index2] = state[1][index] + state[1][index2]
            else:
                state[1][index2] = 10
            state[1] = state[1][:index] + state[1][index+1 :]
    state[0] = shift(state[0])          #changing player's turn
    
def PCMove(state):
    check = 1
    #optemizing if heap have '2' 
    for i in range(len(state[1])):
        if(state[1][i] == 2):
            del state[1][i]
            if(state[0] == 1):
                state[2] = state[2] + 2
            else:
                state[3] = state[3] + 2
            check = 0
            state[0] = shift(state[0])
            break
    if(check):
        #generating possible moves
        Pmoves = succ(state[0],tuple(state[1]),(state[2],state[3]),0)
        states = []
        for i in Pmoves:
            states.append(i)
        #getting best move
        bestState = minimax(states)
        state[1] = list(bestState[2])
        state[2] = bestState[3][0]
        state[3] = bestState[3][1]
        state[0] = shift(state[0])

def RandomMove(state):         #random legal moves by PC
    index = random.randint(0,len(state[1])-1)
    add = 0
    if(len(state[1]) > 2):
        add = random.randint(0,1)
    if(add == 0):
        if(state[1][index] == 2):
            state[1] = state[1][:index] + state[1][index+1 :]
            if(state[0]==1):
                state[2]=state[2]+2
            else:
                state[3]=state[3]+2
        elif(state[1][index]%2 == 1):
            state[1][index] = (3 * state[1][index]) + 1
        else:
            state[1][index] = int(state[1][index]/2)
            state[1].insert(index + 1, state[1][index])
    else:
        index2 = random.randint(0,len(state[1])-1)
        while(index2 == index):
            index2 = random.randint(0,len(state[1])-1)
        if((state[1][index] + state[1][index2]) < 10):
            state[1][index2] = state[1][index] + state[1][index2]
        else:
            state[1][index2] = 10
        state[1] = state[1][:index] + state[1][index+1 :]
    state[0] = shift(state[0])
    
def move(state, players):           #controlling moves
    if(state[0] == 1):
        print("Player 1 Move :")
        if(players[0] == 1):
            humanMove(state)
        elif(players[0] == 2):
            RandomMove(state)
        else:
            PCMove(state)
    else:
        print("Player 2 Move :")
        if(players[1] == 1):
            humanMove(state)
        elif(players[1] == 2):
            RandomMove(state)
        else:
            PCMove(state)

def terminal(state):            #after game ends
    if(state[2] == state[3]):
        print("Draw")
    elif(state[2] < state[3]):
        print("Player 2 Wins")
    else:
        print("Player 1 Wins")


def utility(state, players):          #controlling game
    succ.cache_clear()             #clearing cache
    move(state, players)
    print(state)

def shift(p):              #changing player turn
    if(p == 1):
        return 2
    else:
        return 1

def printheap(state):          #printing heap
    print(state[1])

@cache(maxsize=None)        #using cache
def succ(player,heap,score,rec):        #move generator
    s = list(score)
    temp = []
    lev = 0        #defining depth of tree
    lev = (6 - len(heap)) * 3
    if(lev < 2):
        lev = 2
    if(rec < lev):
        for i in range(len(heap)):       #moves to add 2 heaps
            if(heap[i] != 2):
                for j in range(len(heap)):
                    if(heap[j] != 2):
                        temp = []
                        h = list(heap)
                        if(heap[i]!=heap[j]):
                            h[j] = heap[i] + heap[j]
                            if(h[j] > 10):
                                h[j] = 10
                            del h[i]
                            temp.append(rec)
                            temp.append(player)
                            temp.append(tuple(h))
                            temp.append(score)
                            if(len(h)):
                                yield from succ(shift(player),tuple(h),score,rec+1)        #recursion
                            if(len(temp)):
                                yield temp
            if(heap[i] == 2):      #moves to handle 2 in heap
                temp = []
                h = list(heap)
                del h[i]
                if(player == 1):
                    s[0] = score[0] + 2
                elif(player == 2):
                    s[1] = score[1] + 2   
                temp.append(rec)
                temp.append(player)
                temp.append(tuple(h))
                temp.append(tuple(s))
            elif(heap[i] % 2 == 0 and heap[i] != 2):        #move to handle even number heap
                temp = []
                h = list(heap)
                h[i] = int(heap[i] / 2)
                h.append(int(heap[i] / 2))
                temp.append(rec)
                temp.append(player)
                temp.append(tuple(h))
                temp.append(score)
            else:
                temp = []
                h = list(heap)
                h[i] = int((3 * heap[i]) + 1)
                temp.append(rec)
                temp.append(player)
                temp.append(tuple(h))
                temp.append(score)
                
            if(len(h)):
                yield from succ(shift(player),tuple(h),tuple(s),rec+1)     #recursion
                s = list(score)
            if(len(temp)):
                yield temp

def minimax(s):           #AI technique Minimax
    org = []
    #getting orignal form of 1st level children heaps
    for i in range(len(s)):
        temp = []
        if(s[i][0] == 0):
            temp.append(i)
            temp.append(s[i][3])
            org.append(temp)
    #finding the maximum score in chilren heaps
    for i in range(1,len(s)):
        temp = list(s[i][3])
        s[i][3] = temp
        if(s[i][0] == (s[i-1][0]-1)):
            for j in range(i-1):
                if(s[i][3][0] < s[j][3][0]):
                    s[i][3][0] = s[j][3][0]
                if(s[i][3][1] < s[j][3][1]):
                    s[i][3][1] = s[j][3][1]
    #finding 1st 1 level child heap
    ind = -11
    for k in range(len(s)):
        if(s[k][0] == 0):
            ind = k
            break
    #finding best heap by score in 1st level children heaps
    best = 0
    worst = float('Inf')
    for k in range(len(s)):
        if(s[k][0] == 0):
            if(s[k][0] == 1):
                if((s[k][3][0] > best) and (s[k][3][1] < worst)):
                    best = s[k][3][0]
                    worst = s[k][3][1]
                    ind = k
            else:
                if((s[k][3][1] > best) and (s[k][3][0] < worst)):
                    best = s[k][3][1]
                    worst = s[k][3][0]
                    ind = k
    #getting best original heap
    for i in range(len(org)):
        if(org[i][0] == ind):
            s[ind][3] = org[i][1]
    return s[ind]


#staring game
print("Welcome")
succ.cache_clear()       #clearing cache
tup = init()             #initializing Game
players = tup[0:2]       #getting players
heap = tup[2]            #getting heap
state = [1, heap, 0, 0]  #setting state
print(state)
#calling game controller till 100 steps
for i in range(100):
    print("Turn #: " + str(i+1))
    if(len(state[1]) == 0):       #breaking loop if heap is 0
        break
    utility(state, players)       #calling game controller
terminal(state)          #after game results
