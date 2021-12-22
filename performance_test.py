import mastermind
for name in mastermind.guessing_strats:
    number_of_guesses = []
    print(f"Benchmarking {name}:")
    for combination in [(x,y,z,w) for x in range(mastermind.COLORS) for y in range(mastermind.COLORS) for z in range(mastermind.COLORS) for w in range(mastermind.COLORS)]:
        number_of_guesses.append(guesses:=mastermind.main(test=True, solution=combination, get_guess=mastermind.guessing_strats[name]))
    print(f"max: {max(number_of_guesses)}, avg: {sum(number_of_guesses)/len(number_of_guesses)}")