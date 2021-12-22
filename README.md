# Mastermind
A python script that helps you beat the board game mastermind everytime in a few moves.

It works by concidering all possible guesses and chooses the one that in the worst case eliminates the largest number of 
combinations.  
The code is written in python and the application is currently terminal based.

## How to use 
When in the root of the project, simply run  
```python mastermind.py```  

## The game  
You can read about the game [here.](https://www.wikihow.com/Play-Mastermind)

## Different guessing strategies

I have implemented three different strategies for guessing combinations

1. Select the guess that maximizes the number of discarded guesses in the worst case
2. Select a random combination that has not yet been ruled out
3. Select a totally random guess

Running each strategy once for each of the 6^4 possible solutions resulted in these data:
|Category/Strategy|1: Maximize discarded|2: Random possible|3: Random|
|---|---|---|---|
|Most guesses|  4 | 6  | 14  |
|Average guesses| 3.74  | 4.11  |  5.36 |  

It is worth noting that strategy 2 and 3 are nondeterministic.
