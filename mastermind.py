from math import inf
from random import shuffle
COLORS = 6
colorList = ["Blue", "Green", "Yellow", "Orange", "Purple", "Pink"]
shuffle(colorList)

def is_possible(combination, guess, constraint):
    return (reds:=equal_pins(combination, guess))==constraint[0] and semi_equal_pins(combination, guess)-reds==constraint[1] 

def equal_pins(comb1, comb2):
    return len([x for x in list(zip(comb1, comb2)) if x[0]==x[1]])

def combination_to_string(combination):
    return(f"({', '.join(list(map(lambda x: colorList[x], combination)))})")

def semi_equal_pins(comb1, comb2):
    A = [0]*COLORS
    B = [0]*COLORS
    for pin in comb1:
        A[pin]+=1
    for pin in comb2:
        B[pin]+=1
    return sum(map(lambda a: min(a[0],a[1]), zip(A,B)))
    
def excludes(combination, constraint, possible):
    count = 0
    for comb in possible:
        if not is_possible(comb, combination, constraint):
            count+=1
    return count

def guess(guess, possible):
    old_possibilities = len(possible)
    constraintInput = input(f"The guess is {combination_to_string(guess)}. What is the response? 'red' 'white' ").split()
    constraint = (int(constraintInput[0]), int(constraintInput[1]))
    update(guess, constraint, possible)
    new_possibilities = len(possible)
    print(f"Eliminated {old_possibilities-new_possibilities} combination{'' if new_possibilities==1 else ''}. There {'is' if new_possibilities==1 else 'are'} now {new_possibilities} remaining.")


def update(guess, constraint, possible):
    remove_set = set()
    for comb in possible:
        if not is_possible(comb, guess, constraint):
            remove_set.add(comb)
    possible-=remove_set
        

def main():
    combinations = [(x,y,z,w) for x in range(COLORS) for y in range(COLORS) for z in range(COLORS) for w in range(COLORS)]
    possible = set(combinations)
    constraints = [(x,y) for x in range(5) for y in range(5) if x+y<5]
    guess((0,0,1,1), possible)
    if(len(possible)==1):
        print(f"The correct combination is: {combination_to_string(list(possible)[0])}")
        return
    if(len(possible)==0):
            print("The supplied responses lead to a contradiction!")
            return
    while True:
        global_best = 0
        best_comb = (-1,-1,-1,-1)
        for comb in combinations:
            local_worst = inf
            for const in constraints:
                if (exc:=excludes(comb, const, possible)) < local_worst:
                    local_worst = exc
            if local_worst > global_best:
                global_best = local_worst
                best_comb = comb
        guess(best_comb, possible)
        if(len(possible)==1):
            print(f"The correct combination is: {combination_to_string(list(possible)[0])}")
            return
        if(len(possible)==0):
            print("The supplied responses lead to a contradiction!")
            return

main()