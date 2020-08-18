import argparse
import configparser
import random


"""

Genetic Algorithm : Genetic algorithm is a search heuristic that is inspired by
                    Charles Darwin’s theory of natural evolution. 
                    This algorithm reflects the process of natural selection where 
                    the fittest individuals are selected for reproduction
                    in order to produce offspring of the next generation.

                    It begins with a random initial population consisting of 'n' Chromosomes.
                    Two pairs of chromosomes (parents) are selected based on their fitness scores. 
                    The selected parents undergo Cross over and results in a new offspring.
                    Some of the offspings may undergo mutation (This is to maintain diversity
                    in the population and to prevent premature convergence). This is repeated untill
                    a termination criteria is met or the target solution is reached.


POPULATION       : It is a subset of all the possible solutions (In our case, all possible strings).
CHROMOSOME       : One such solution (string).
GENE             : A gene is one element position of a chromosome (In our case, a charcter in the string).
FITNESS FUNCTION : Calculates how good (how accurate or how close) the solution is to the target solution.
MUTATION         : For a small probability of offsprings, some of the genes is altered to maintain diversity in the
                   population

"""


class Gene:
    def __init__(self, character = None):
        if character is None:
            self.gene = self.random_gene()
        else:
            self.gene = character


    def random_gene(self):
        return chr(int(random.randint(32, 122))) 
        return chr(int(random.randint(97, 122))) 

    
    def display(self):
        return self.gene


    
class Chromosome:
    GENE_COUNT = 0

    def __init__(self, individual = None):
        if individual is None:
            self.chromosome = self.random_chromosome()
        else:
            self.chromosome = individual
        

    def random_chromosome(self):
        chromosome = [Gene() for _ in range(Chromosome.GENE_COUNT)]
        return chromosome


    def display(self):
        return ''.join([gene.display() for gene in self.chromosome])



class Population:
    CHROMOSOME_COUNT = 0
    TARGET_STRING = ''

    def __init__(self, population = None):
        if population is None:
            self.population = self.random_population()
        else:
            self.population = population


    def random_population(self):
        return [Chromosome() for _ in range(Population.CHROMOSOME_COUNT)]


    def calculate_fitness(self, individual):
        fitness_score = 0

        for index, gene in enumerate(individual.chromosome):
            fitness_score += abs(ord(gene.display()) - ord(Population.TARGET_STRING[index]))
        fitness_score = -fitness_score

        return fitness_score
    
    
    #Selecting the fittest two chromosomes for cross-over
    def selection(self):
        sorted_population = sorted(self.population, key = self.calculate_fitness, reverse = True)
        return sorted_population[:2]

    
    def display(self):
        return '\t'.join([chromosome.display() for chromosome in self.population])



class Evolution:
    def __init__(self, string):
        self.initialise_parameters(string)
        self.generation = list()


    def initialise_parameters(self, string):
        #Reading from the config file
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.POPULATION_COUNT = int(config["PARAMETERS"]["POPULATION COUNT"])
        self.MAX_GENERATION = int(config["PARAMETERS"]["MAX GENERATION"])

        if string is None:
            self.STRING = config["PARAMETERS"]["TARGET STRING"]
        else:
            self.STRING = string

        Chromosome.GENE_COUNT = len(self.STRING)
        Population.CHROMOSOME_COUNT = int(config["PARAMETERS"]["CHROMOSOME COUNT"])
        Population.TARGET_STRING = self.STRING


    def create_initial_generation(self):
        self.generation = [Population() for _ in range(self.POPULATION_COUNT)]


    def cross_over(self, parent1, parent2, point):
        offspring = list()

        for index in range(len(parent1.chromosome)):
            if index < point:
                gene = Gene(parent1.chromosome[index].gene)
            else:
                gene = Gene(parent2.chromosome[index].gene)
            offspring.append(gene)

        return Chromosome(offspring)


    def mutate(self, offspring):
        for _ in range(int(len(self.STRING)*0.09) + 1):
            index = random.randint(0, len(self.STRING)-1)
            offspring.chromosome[index].gene = chr(int(random.randint(32, 122))) 

        return offspring


    def mate(self, parent1, parent2):
        offspring = list()

        for index in range(len(self.STRING)):
            probability = random.random()
            if probability < 0.45:
                offspring.append(Gene(parent1.chromosome[index].display()))
            elif probability < 0.9:
                offspring.append(Gene(parent2.chromosome[index].display()))
            else:
                #Mutation
                offspring.append(Gene())

        return Chromosome(offspring)

        # cross_over_point = random.randint(0, len(parent1.chromosome) - 1)
        # offspring = self.cross_over(parent1, parent2, cross_over_point)
        # if random.random() < 0.25:
        #     offspring = self.mutate(offspring)

        # return offspring



    def display_msg(self, msg, parent1):
        print("#"*100)
        print(f"\n\nEvolution {msg} ! \nEvolved from {self.initial_chromosome.display()} to {parent1.display()}\n")
        print("#"*100)


    def evolve(self):
        self.create_initial_generation()
        self.initial_chromosome = self.generation[0].population[0]

        for generation in range(self.MAX_GENERATION):
            print(f"Generation : {generation + 1}\n", end = "")
            new_generation = list()

            for pop_index, population in enumerate(self.generation):
                new_population = list()
                parent1, parent2 = population.selection()
                print(f"\tPopulation : {pop_index + 1} \t Best String : {parent1.display()} \t Fitness : {population.calculate_fitness(parent1)}")

                if population.calculate_fitness(parent1) == 0:
                    self.display_msg('Successful', parent1)
                    exit(0)

                for _ in range(population.CHROMOSOME_COUNT):
                    new_population.append(self.mate(parent1, parent2))

                new_generation.append(Population(new_population))
                
            self.generation = new_generation

        self.display_msg('Failed', parent1)



def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--string',
                        type = str,
                        help = "--string 'The Target String to which the random string need to be evolved to'",
                        required = False
                        )
    argument = parser.parse_args()

    return argument.string



if __name__ == "__main__":
    string = argument_parser()
    Evolution(string).evolve()