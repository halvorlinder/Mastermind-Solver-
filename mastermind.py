from math import inf
from random import shuffle, choice
import sys
COLORS = 6
#assigns a random color to each pin, so that the guesses are a bit less predictable
colorList = ["Blue", "Green", "Yellow", "Orange", "Purple", "Pink"]
shuffle(colorList)

#We only want to print if the program is run explicitly
def inform(message):
    if __name__=="__main__":
        print(message)

#Returns if a combination is still possible given a guess and a constraint
def is_possible(combination, guess, constraint):
    return (reds:=equal_pins(combination, guess))==constraint[0] and semi_equal_pins(combination, guess)-reds==constraint[1] 


def combination_to_string(combination):
    return(f"({', '.join(list(map(lambda x: colorList[x], combination)))})")

#Returns the number of white pins in the response, given a guess and a solution
def equal_pins(comb1, comb2):
    return len([x for x in list(zip(comb1, comb2)) if x[0]==x[1]])

#Returns the number of white + red pins in the respons, given a guess and a solution
def semi_equal_pins(comb1, comb2):
    A = [0]*COLORS
    B = [0]*COLORS
    for pin in comb1:
        A[pin]+=1
    for pin in comb2:
        B[pin]+=1
    return sum(map(lambda a: min(a[0],a[1]), zip(A,B)))

def get_constraint(comb1, comb2):
    return (reds:=equal_pins(comb1, comb2), semi_equal_pins(comb1, comb2)-reds)

#Returns the number of combinations ruled out by a guess and a constraint    
def excludes(combination, constraint, possible):
    count = 0
    for comb in possible:
        if not is_possible(comb, combination, constraint):
            count+=1
    return count

#Guesses a given combination
def guess(guess, possible, symmetry, solution=None):
    old_possibilities = len(possible)
    if solution!=None:
        constraint = (reds:=equal_pins(guess, solution), semi_equal_pins(guess, solution)-reds)
    else:
        constraintInput = input(f"The guess is {combination_to_string(guess)}. What is the response? 'red' 'white' ").split()
        constraint = (int(constraintInput[0]), int(constraintInput[1]))
    update(guess, constraint, possible)
    new_possibilities = len(possible)
    inform(f"Eliminated {old_possibilities-new_possibilities} combination{'' if new_possibilities==1 else ''}. There {'is' if new_possibilities==1 else 'are'} now {new_possibilities} remaining.")
    update_symmetry(symmetry, guess, constraint)

#Removes all combinations that are ruled out by the constraint
def update(guess, constraint, possible):
    remove_set = set()
    for comb in possible:
        if not is_possible(comb, guess, constraint):
            remove_set.add(comb)
    possible-=remove_set

#Updates the symmetry table given a guess and a constraint 
def update_symmetry(symmetry, guess, constraint):
    occurences = [0]*COLORS
    for n in guess:
        if n in symmetry["used_once"]:
            symmetry["used_twice"].add(n)
            for m in range(COLORS):
                if n!=m:
                    symmetry["table"][n][m], symmetry["table"][m][n] = 0, 0
    for n in guess:
        occurences[n] = 1 if sum(constraint)==0 else occurences[n]+1
        symmetry["used_once"].add(n)
    sets = dict()
    for n, m in enumerate(occurences):
        if not (m in sets):
            sets[m] = set()
        sets[m].add(n)
    for n in range(COLORS):
        for _,S in sets.items():
            if not (n in S):
                for m in S:
                    symmetry["table"][n][m], symmetry["table"][m][n] = 0, 0
    included = set()
    sets = []
    for n, row in enumerate(symmetry["table"]):
        if n in included:
            continue
        group = set()
        for m, b in enumerate(row):
            if b==1:
                group.add(m)
                included.add(m)
        sets.append(group)
    for i, S in enumerate(sets):
        for n in S:
            symmetry["map"][n] = COLORS+i

#Returns the hash of a combination. Equal hashes => symmetric  
def get_hash(combination, symmetry):
    structure = dict()
    for n in combination:
        if not n in structure:
            structure[n] = len(structure)
    return tuple(map(lambda x: symmetry["map"][x], combination))+tuple(map(lambda x: structure[x], combination))

#Returns the guess that maximizes the number of discarded solutions in the worst case
def get_guess_maximize_worst_case(combinations, constraints, possible, symmetry):
    #The algorithm will always choose this as its first guess, so there is no point in calculating it 
    if len(combinations)==len(possible):
        return (0,0,1,1)
    global_best = 0
    best_comb = (-1,-1,-1,-1)
    #checked contains the hashed values of the conbinations that have been checked
    checked = set()
    #We want to guess from possible when it contains a tied best guess, this is tracked by this bool
    best_in_possible = False
    #Find the combination that has the best worst case, all combinations need be concidered, as the guess
    #that eliminates the highest number of possibilities could lie outside the set of possible solutions
    #I found this by empirical evidence
    for comb in combinations:
        #If the hash already excists it means that a symmetric combination has already been checked
        if get_hash(comb, symmetry) in checked:
            continue
        checked.add(get_hash(comb, symmetry))
        local_worst = inf
        for const in constraints:
            if (exc:=excludes(comb, const, possible)) < local_worst:
                local_worst = exc
        if local_worst > global_best:
            global_best = local_worst
            best_comb = comb
            best_in_possible = comb in possible
        elif (not best_in_possible) and local_worst==global_best and (comb in possible):
            global_best = local_worst
            best_comb = comb
            best_in_possible = True
    # if not best_in_possible:
    #     inform("\nThe guess is not in possible!\n")
    return best_comb

#Returns the guess that maximizes the number of discarded solutions in the worst case
def get_guess_maximize_expected(combinations, constraints, possible, symmetry):
    #The algorithm will always choose this as its first guess, so there is no point in calculating it 
    if len(combinations)==len(possible):
        return (0,0,1,2)
    best = 0
    best_comb = (-1,-1,-1,-1)
    #checked contains the hashed values of the conbinations that have been checked
    checked = set()
    #We want to guess from possible when it contains a tied best guess, this is tracked by this bool
    best_in_possible = False
    #Find the combination that has the best worst case, all combinations need be concidered, as the guess
    #that eliminates the highest number of possibilities could lie outside the set of possible solutions
    #I found this by empirical evidence
    for comb in combinations:
        #If the hash already excists it means that a symmetric combination has already been checked
        if get_hash(comb, symmetry) in checked:
            continue
        checked.add(get_hash(comb, symmetry))
        score = 0
        #Calculate the number of possible solutions that produce each constraint and use this to calculate the excpected 
        #value of the number of discarded solutions 
        distribution = get_distribution(comb, possible, constraints)
        for const in constraints:
            score+=excludes(comb, const, possible)*distribution[const]
        if score > best:
            best = score
            best_comb = comb
            best_in_possible = comb in possible
        elif (not best_in_possible) and score==best and (comb in possible):
            best = score
            best_comb = comb
            best_in_possible = True
    return best_comb

#Returns the probability distribution of getting the different constraints
def get_distribution(combination, possible, constraints):
    distribution = {const:0 for const in constraints}
    for solution in possible:
        distribution[get_constraint(combination, solution)]+=1
    return distribution

#Returns a random combination from the set of possible combinations    
def get_guess_random_from_possible(combinations, constraints, possible, symmetry):
    return choice(tuple(possible))

#Returns a random combination from the set of all combinations
def get_guess_random_from_combinations(combinations, constraints, possible, symmetry):
    return choice(tuple(combinations)) 

guessing_strats = {
        "worst_case":get_guess_maximize_worst_case,
        "random":get_guess_random_from_combinations,
        "rabdom_possible":get_guess_random_from_possible,
        "excpected":get_guess_maximize_expected
    }

def main(test=False, solution=None, get_guess=get_guess_maximize_worst_case):
    number_of_guesses = 0
    #List of all possible combiinations 
    combinations = [(x,y,z,w) for x in range(COLORS) for y in range(COLORS) for z in range(COLORS) for w in range(COLORS)]
    #List of all combinations not yet ruled out
    possible = set(combinations)
    #List of all possible responses
    constraints = [(x,y) for x in range(5) for y in range(5) if x+y<5]
    #object that keeps track of data related to utilizing pin symmetry to speed up move generation
    symmetry = {
        "table":[[1]*COLORS for _ in range(COLORS)],
        "map":{n:-1 for n in range(COLORS)},
        "used_once":set(),
        "used_twice":set()        
    }
    
    while True:
        #Get the combination to be guessed
        generated_guess = get_guess(combinations, constraints, possible, symmetry)
        #Guess the combination
        if test:
            guess(generated_guess, possible, symmetry, solution=solution)
        else:
            guess(generated_guess, possible, symmetry)
        number_of_guesses+=1
        if(len(possible)==1):
            inform(f"The correct combination is: {combination_to_string(list(possible)[0])}")
            break
        if(len(possible)==0):
            inform("The supplied responses lead to a contradiction!")
            break
    return number_of_guesses
if __name__=="__main__":
    if(len(sys.argv)==1):
        main()
    else:
        main(get_guess=guessing_strats[sys.argv[1]])