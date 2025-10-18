import random
import copy
from state import State
import time
import matplotlib.pyplot as plt
import numpy as np

class genetic_algorithm:
    def __init__(self, listRuangan, listMatkul, listMahasiswa):
        self.listRuangan = listRuangan
        self.listMatkul = listMatkul
        self.listMahasiswa = listMahasiswa

    # Mengembalikan sebuah individual (objek State) secara random dari populasi
    # population: List of State
    @staticmethod
    def random_selection(population):
        fitness = []

		# Rumus: fitness = 1 / (obj + 1)
        for individual in population:
            obj = individual.countObjective()
            fitness.append(1 / (obj + 1))
        
        total_value = 0
        for value in fitness:
            total_value += value

        probability = []

        sum_percentage = 0
        for value in fitness:
            percentage = round((value / total_value) * 100)
            sum_percentage += percentage
            probability.append(sum_percentage)
        
        # batas atasnya probability[-1] karena rounding issue, terkadang cuman sampe 99 bukan 100
        random_num = random.randint(1, probability[-1])

        i = 0
        is_found_chosen_individual = False
        while not is_found_chosen_individual:
            if random_num <= probability[i]:
                is_found_chosen_individual = True
                chosen_individual = population[i]
            i += 1

        return copy.deepcopy(chosen_individual)
    
    # Mengembalikan State (1 child) hasil crossover yang memiliki nilai fitness terbaik
    # parent_1, parent_2: State
    @staticmethod
    def reproduce(parent_1, parent_2):
        serialized_parent_1 = parent_1.serialize()
        serialized_parent_2 = parent_2.serialize()

        crossover_point = random.randint(0, len(serialized_parent_1) - 1)

        child_1 = serialized_parent_1[:crossover_point] + serialized_parent_2[crossover_point:]
        child_2 = serialized_parent_2[:crossover_point] + serialized_parent_1[crossover_point:]

        deserialized_child_1 = copy.deepcopy(parent_1)
        deserialized_child_2 = copy.deepcopy(parent_2)

        deserialized_child_1.deserialize(child_1)
        deserialized_child_2.deserialize(child_2)

        objective_value_1 = deserialized_child_1.countObjective()
        fitness_value_1 = 1 / (objective_value_1 + 1)

        objective_value_2 = deserialized_child_2.countObjective()
        fitness_value_2 = 1 / (objective_value_2 + 1)

        if fitness_value_1 > fitness_value_2:
            return deserialized_child_1
        else:
            return deserialized_child_2

    # Mutasi State/individual dengan pick random sebuah tuple {hari, slot, Matkul} lalu randomize hari, slot, dan ruangan
    # Mengembalikan individual hasil random mutation
    # listRuangan = (Opsional) List of Ruangan
    @staticmethod
    def mutate(individual, listRuangan=None):
        serialized_individual = individual.serialize()

        mutation_point = random.randint(0, len(serialized_individual) - 1)

        hari = ["senin", "selasa", "rabu", "kamis", "jumat"]
        randomized_hari = hari[random.randint(0, 4)]
        randomized_slot = random.randint(0, 10)

        randomized_ruangan = None
        if listRuangan is not None:
            randomized_ruangan = listRuangan[random.randint(0, len(listRuangan) - 1)]

        randomized_tuple = (randomized_hari, randomized_slot, serialized_individual[mutation_point][2])
        serialized_individual.pop(mutation_point)

        serialized_individual.insert(mutation_point, randomized_tuple)

        if randomized_ruangan is not None:
            serialized_individual[mutation_point][2].setRuangan(randomized_ruangan)

        deserialized_individual = copy.deepcopy(individual)
        deserialized_individual.deserialize(serialized_individual)

        return deserialized_individual

    # Function genetic algorithm
    # Akan berhenti ketika ada individu yang memiliki nilai fitness function maximum atau tercapai iterasi maksimal
    # k = banyaknya individu dalam populasi
    # n = banyaknya iterasi maksimal yang dapat dilakukan
    def GA(self, k, n):
        start_time = time.perf_counter()

        start_population = []

        for i in range(k):
            individual = State(self.listRuangan, self.listMahasiswa)
            individual.makeComplete(self.listMatkul)
            start_population.append(individual)

        population = copy.deepcopy(start_population)
        plot = []
        
        max = -1
        sum = 0
        avg = 0

        for individual in population:
		    # Rumus: fitness = 1 / (obj + 1) -> Nilai fitness function = [0, 1], 1 terbaik
            objective_value = individual.countObjective()
            fitness_value = 1 / (objective_value + 1)

            if (fitness_value > max):
                max = fitness_value
            
            sum = sum + fitness_value

        avg = sum / k

        data = [max, avg]
        plot.append(data)

        is_individual_fit = False
        if max == 1:
            is_individual_fit = True
        
        itr = 0
        while itr < n and not is_individual_fit:
            new_population = []
            for i in range(k):
                parent_1 = genetic_algorithm.random_selection(population)
                parent_2 = genetic_algorithm.random_selection(population)
                child = genetic_algorithm.reproduce(parent_1, parent_2)
                child = genetic_algorithm.mutate(child, self.listRuangan)
                new_population.append(child)

            population = new_population

            max = -1
            sum = 0
            avg = 0

            for individual in population:
                # Rumus: fitness = 1 / (obj + 1) -> Nilai fitness function = [0, 1], 1 terbaik
                objective_value = individual.countObjective()
                fitness_value = 1 / (objective_value + 1)

                if (fitness_value > max):
                    max = fitness_value
                
                sum = sum + fitness_value

            avg = sum / k

            data = [max, avg]
            plot.append(data)

            if max == 1:
                is_individual_fit = True

            itr = itr + 1

        max = -1
        fittest_individual = population[0]

        for individual in population:
		    # Rumus: fitness = 1 / (obj + 1) -> Nilai fitness function = [0, 1], 1 terbaik
            objective_value = individual.countObjective()
            fitness_value = 1 / (objective_value + 1)

            if (fitness_value > max):
                max = fitness_value
                fittest_individual = individual
        
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        
        data = (start_population, population, plot, k, n, elapsed_time, fittest_individual)

        return data

    # Fungsi plotting genetic algorithm
    @staticmethod
    def make_chart(data_output, file_path):
        plot = data_output[2]
        k = data_output[3]
        n = data_output[4]
        elapsed_time = str(data_output[5])[:4]

        max = []
        avg = []

        for iteration in plot:
            max.append(iteration[0])
            avg.append(iteration[1])


        title = f"Genetic Algorithm (k={k}, n={n}, iteration={len(plot) - 1}, t={elapsed_time} s)"

        plt.figure(figsize=(6.4, 4.8), layout='constrained')
        plt.title(title)
        plt.xlabel('Iteration')
        plt.ylabel('Fitness Function')
        plt.ylim(0, 1)

        max_array = np.array(max)
        avg_array = np.array(avg)

        max_y = np.array(max_array)
        max_x = np.arange(len(max_array))
        plt.plot(max_x, max_y, label='Max')

        avg_y = np.array(avg_array)
        avg_x = np.arange(len(avg_array))
        plt.plot(avg_x, avg_y, label='Avg')

        for var in (max_y, avg_y):
            plt.annotate('%0.5f' % var.max(), xy=(1, var.max()), xytext=(8, 0),
                        xycoords=('axes fraction', 'data'), textcoords='offset points')

        plt.legend()
        plt.grid(True)
        plt.savefig(file_path)
        plt.close()

    @staticmethod
    def write_data(data_output, file_path):
        with open(file_path, "w") as f:
            f.write(f"Nilai fitness function akhir yang dicapai (max = 1): {data_output[2][-1][0]}\n")
            f.write(f"Durasi pencarian: {data_output[5]} s\n")
            f.write(f"Jumlah individu dalam populasi (k): {data_output[3]}\n")
            f.write(f"Batas maksimum iterasi (n): {data_output[4]}\n")
            f.write(f"Banyak iterasi yang dilakukan: {len(data_output[2]) - 1}\n\n")
            
            f.write(f"Fittest Individual:\n")
            data_output[6].display(f)

            f.write("\n===============================================================\n")

            f.write("Populasi Awal: ")
            for i in range(len(data_output[0])):
                f.write(f"Individu {i + 1}:")
                data_output[0][i].display(f)
                f.write("\n")

            f.write("\n===============================================================\n")

            f.write("Populasi Awal: ")
            for i in range(len(data_output[1])):
                f.write(f"Individu {i + 1}:")
                data_output[1][i].display(f)
                f.write("\n")
        
        print(f"Data Genetic Algorithm sudah tersimpan di {file_path}")
