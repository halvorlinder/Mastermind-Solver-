# Mastermind
A python script that helps you beat the board game mastermind everytime in a few moves.

The code is written in python and the application is currently terminal based.

## How to use 
When in the root of the project, simply run  
```python mastermind.py```
This will run the program using the strategy **worst_case**. To select a different strategy, simply supply the name of the strategy as a command line argument. The different strategies are listed below.
The program is now running and the first guess is calculated. The guess will be displayed in the terminal and the program will ask for the number of red and white pins supplied for the given guess. This process repeats untill the solution is found.

## The game  
You can read about the game [here.](https://www.wikihow.com/Play-Mastermind)

## Different guessing strategies

I have implemented three different strategies for guessing combinations

- **worst_case**: Select the guess that maximizes the number of discarded guesses in the worst case
- **random_possible**: Select a random combination that has not yet been ruled out
- **random**: Select a totally random guess
- **excpected**: Select the guess that maximizes the excpected value of the number of discarded guesses

Running each strategy once for each of the 6^4 possible solutions resulted in these data:
|Category/Strategy|worst_case|random_possible|random|excpected|
|---|---|---|---|---|
|Most guesses|  4 | 6  | 14  | 5 |
|Average guesses| 3.74  | 4.11  |  5.36 |  3.66 |

As can be seen from this table, the excpected value strategy on average performs better than the worst case strategy. Its worst case, however, is greater.

It is worth noting that strategy 2 and 3 are nondeterministic.
