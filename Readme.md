## Introduction

The program begins with a random string and simulates its evolution to reach the specified target string using Genetic Algorithm.

<p>Genetic algorithm is a search heuristic that is inspired by Charles Darwin’s theory of natural evolution. 
This algorithm reflects the process of natural selection where the fittest individuals are selected for reproduction
in order to produce offspring for the next generation.
It begins with a random initial population consisting of 'n' Chromosomes.
Two pairs of chromosomes (parents) are selected based on their fitness scores. 
The selected parents undergo Cross over and results in a new offspring.
Some of the offspings may undergo mutation (This is to maintain diversity
in the population and to prevent premature convergence). This is repeated untill
a termination criteria is met or the target solution is reached.<p>  

- POPULATION       : A collection of all the possible solutions (In our case, all possible strings).
- CHROMOSOME       : One such solution (In our case, a string).
- GENE             : A gene is one element position of a chromosome (In our case, a charcter in the string).
- FITNESS FUNCTION : Calculates how good (how close) the solution is to the target solution.
- MATING           : Selected parents undergo cross over (iterchange of genes) to generate offspring (new solution).
- MUTATION         : For a small probability of offsprings, some of the genes is altered to maintain diversity in the
                     population


## Usage
Use config.ini to change the parameter values.  

If no string is passed as argument, the string specified in the config.ini file will be assumed as the target string.

```python
python stringEvolution.py --string "target string"
