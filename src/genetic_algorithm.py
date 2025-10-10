import random
import copy
from state import State
import time
import matplotlib.pyplot as plt
import numpy as np

class genetic_algorithm:
    # listRuangan dan listMatkul diperlukan hanya untuk membuat sebuah object State pada fungsi GA
    # supaya parameter GA hanya k, n (ga listRuangan, listMatkul)
    def __init__(self, listRuangan, listMatkul):
        self.listRuangan = listRuangan
        self.listMatkul = listMatkul

    # static function mengembalikan sebuah individual (objek State) secara random dari populasi
    # population: List of State
    @staticmethod
    def random_selection(population):
        # variable untuk menyimpan nilai fitness function setiap individu
        fitness = []

        # # Debug
        # print(f"Individual count: {len(population)}")

        # Kalkulasi nilai fitness function setiap individu (populasi)
		# Rumus: fitness = 1 / (obj + 1)
        for individual in population:
            obj = individual.countObjective()
            fitness.append(1 / (obj + 1))
        
        # # Debug
        # print(f"Fitness function value: {fitness}")

        # hitung total semua nilai fitness function untuk menjadi penyebut
        total_value = 0
        for value in fitness:
            total_value += value

        # # Debug
        # print(f"Total fitness function value: {total_value}")

        # variable untuk menyimpan probability setiap individu
		# cth: individu 1 = 20%, individu 2 = 30%, individu 3 = 50%
		# maka probability[0] = 20, probability[1] = 50, probability[2] = 100
        probability = []

        # buat probability of random selection
        sum_percentage = 0
        for value in fitness:
            percentage = round((value / total_value) * 100)
            sum_percentage += percentage
            probability.append(sum_percentage)
        
        # # Debug
        # print(f"Probability of random selection: {probability}")
        
        # Lakukan random selection (pilih sebuah individu)
        # batas atasnya probability[-1] karena rounding issue, terkadang cuman sampe 99 bukan 100
        random_num = random.randint(1, probability[-1])

        # # Debug
        # print(f"Random number: {random_num}")

        i = 0
        is_found_chosen_individual = False
        while not is_found_chosen_individual:
            if random_num <= probability[i]:
                is_found_chosen_individual = True
                chosen_individual = population[i]
            i += 1

        # # Debug
        # print(f"Chosen individual index: {i - 1} (Individual ke {i})")

        return copy.deepcopy(chosen_individual)
    
    # static function mengembalikan State (1 child) hasil crossover yang memiliki nilai fitness terbaik
    # parent_1, parent_2: State
    # TODO: diasumsikan menggunakan GA modern (child hanya 1, diambil yang memiliki fitness function terbaik)
    @staticmethod
    def reproduce(parent_1, parent_2):
        # Serialisasi state menjadi List of tuple {hari, slot, Matkul}
        serialized_parent_1 = parent_1.serialize()
        serialized_parent_2 = parent_2.serialize()

        # # Debug
        # print(f"Parent 1: (len: {len(serialized_parent_1)})")
        # for t in serialized_parent_1:
        #     print(f"({t[0]}, {t[1] + 7}, {t[2].displayNgasal2()}),")
        # print(f"Parent 2: (len: {len(serialized_parent_2)})")
        # for t in serialized_parent_2:
        #     print(f"({t[0]}, {t[1] + 7}, {t[2].displayNgasal2()}),")

        # Pilih random crossover point
        crossover_point = random.randint(0, len(serialized_parent_1) - 1)

        # # Debug
        # print(f"Crossover point: {crossover_point}")

        # Lakukan crossover, dilakukan dengan membagi [awal, crossover_point-1] dan [crossover_point, akhir]
        # Cth: crossover_point = 2, parent_1 = [1, 2, 3, 4, 5], parent_2 = [6, 7, 8, 9, 10]
        # Maka child_1 = [1, 2, 8, 9, 10], child_2 = [6, 7, 3, 4, 5]
        child_1 = serialized_parent_1[:crossover_point] + serialized_parent_2[crossover_point:]
        child_2 = serialized_parent_2[:crossover_point] + serialized_parent_1[crossover_point:]

        # # Debug
        # print(f"Child 1: (len: {len(child_1)})")
        # for t in child_1:
        #     print(f"({t[0]}, {t[1] + 7}, {t[2].displayNgasal2()}),")
        # print(f"Child 2: (len: {len(child_2)})")
        # for t in child_2:
        #     print(f"({t[0]}, {t[1] + 7}, {t[2].displayNgasal2()}),")

        # Mengembalikan bentuk child dari serialized ke State
        # Dilakukan deep copy, cari aman aja
        deserialized_child_1 = copy.deepcopy(parent_1)
        deserialized_child_2 = copy.deepcopy(parent_2)

        deserialized_child_1.deserialize(child_1)
        deserialized_child_2.deserialize(child_2)

        # Menghitung fitness value setiap child
        objective_value_1 = deserialized_child_1.countObjective()
        fitness_value_1 = 1 / (objective_value_1 + 1)

        objective_value_2 = deserialized_child_2.countObjective()
        fitness_value_2 = 1 / (objective_value_2 + 1)

        # # Debug
        # print(f"fitness value child 1: {fitness_value_1}")
        # print(f"fitness value child 2: {fitness_value_2}")

        # Mengembalikan child dengan fitness value terbesar
        if fitness_value_1 > fitness_value_2:
            return deserialized_child_1
        else:
            return deserialized_child_2

        # IRRELEVANT
        # listChild = []
        # listChild.append(deserialized_child_1)
        # listChild.append(deserialized_child_2)

        # return listChild

    # static function mutasi State/individual dengan pick random sebuah tuple {hari, slot, Matkul}
    # melakukan randomize hari ["senin", "selasa", "rabu", "kamis", "jumat"]
    # melakukan randomize slot [0, 10]
    # melakukan randomize ruangan dari listRuangan (opsional, jika listRuangan diberikan)
    # mengembalikan individual hasil random mutation
    # listRuangan = (Opsional) List of Ruangan
    @staticmethod
    def mutate(individual, listRuangan=None):
        # Serialisasi state menjadi List of tuple {hari, slot, Matkul} -> sort by kode_matkul
        serialized_individual = individual.serialize()

        # # Debug
        # print(f"Individual before mutation: (len: {len(serialized_individual)})")
        # for t in serialized_individual:
        #     print(f"({t[0]}, {t[1] + 7}, {t[2].displayNgasal2()}),")

        # Pilih random mutation_point
        mutation_point = random.randint(0, len(serialized_individual) - 1)

        # # Debug
        # print(f"Mutation point (start from 0): {mutation_point}")

        # Pilih random hari dan slot
        hari = ["senin", "selasa", "rabu", "kamis", "jumat"]
        randomized_hari = hari[random.randint(0, 4)]
        randomized_slot = random.randint(0, 10)

        # # Debug
        # print(f"Randomized hari: {randomized_hari}")
        # print(f"Randomized slot: {randomized_slot}")

        # Pilih random ruangan (Opsional), jangan deep copy (mengikuti setRuangan())
        randomized_ruangan = None
        if listRuangan is not None:
            randomized_ruangan = listRuangan[random.randint(0, len(listRuangan) - 1)]

            # # Debug
            # print(f"Randomized ruangan: ({randomized_ruangan.kode}, {randomized_ruangan.kuota})")
        
        # Lakukan random mutation (hari, slot)
        # tuple tidak bisa dilakukan assigment, Solusi: delete tuple lama, insert tuple baru
        # serialized_individual[mutation_point][0] = randomized_hari
        # serialized_individual[mutation_point][1] = randomized_slot

        randomized_tuple = (randomized_hari, randomized_slot, serialized_individual[mutation_point][2])
        serialized_individual.pop(mutation_point)

        # # Debug
        # print(f"Individual after pop: (len: {len(serialized_individual)})")
        # for t in serialized_individual:
        #     print(f"({t[0]}, {t[1] + 7}, {t[2].displayNgasal2()}),")

        serialized_individual.insert(mutation_point, randomized_tuple)

        # # Debug
        # print(f"Individual after insert: (len: {len(serialized_individual)})")
        # for t in serialized_individual:
        #     print(f"({t[0]}, {t[1] + 7}, {t[2].displayNgasal2()}),")
        

        # Lakukan random mutation (ruang), Ruangan tidak deep copy
        if randomized_ruangan is not None:
            serialized_individual[mutation_point][2].setRuangan(randomized_ruangan)

        # # Debug
        # print(f"Individual after mutation: (len: {len(serialized_individual)})")
        # for t in serialized_individual:
        #     print(f"({t[0]}, {t[1] + 7}, {t[2].displayNgasal2()}),")
        
        # Mengembalikan bentuk individual dari serialized ke State, deep copy (cari aman)
        deserialized_individual = copy.deepcopy(individual)
        deserialized_individual.deserialize(serialized_individual)

        return deserialized_individual

    # static function genetic algorithm
    # akan berhenti ketika ada individu yang memiliki nilai fitness function maximum atau tercapai iterasi maksimal
    # k = banyaknya individu dalam populasi (HARUS GENAP, GANJIL BLM SUPPORT)
    # n = banyaknya iterasi maksimal yang dapat dilakukan
    # Catatan: referensi algoritma dari PPT IF3170 Intelegensi Buatan Beyond Classical Search
    # TODO: support individu ganjil. Ans: setiap crossover hanya memilih 1 child dengan nilai fitness terbaik
    # TODO: support prevent parent adalah individual yang sama
    # TODO: setiap child hasil crossover pasti di mutate
    def GA(self, k, n):
        # Variable menghitung waktu dimulai
        start_time = time.perf_counter()

        # Variable menyimpan populasi awal
        start_population = []

        for i in range(k):
            # Membuat k individual secara random
            individual = State(self.listRuangan)
            individual.makeComplete(self.listMatkul)
            start_population.append(individual)

        # Variable population ini yang akan digunakan selama menjalankan GA
        population = copy.deepcopy(start_population)

        # Variable untuk menyimpan nilai max dan avg populasi untuk tiap iterasi (untuk plotting)
        # List of List, [[max, avg], [max, avg]]
        # idx = 0 -> awal, idx = 1 -> iterasi 1, dst
        plot = []
        
        # Hitung nilai fitness function pada start_population
        max = -1
        sum = 0
        avg = 0

        for individual in population:
            # Kalkulasi nilai fitness function setiap individu (populasi)
		    # Rumus: fitness = 1 / (obj + 1) -> Nilai fitness function = [0, 1], 1 terbaik
            objective_value = individual.countObjective()
            fitness_value = 1 / (objective_value + 1)

            if (fitness_value > max):
                max = fitness_value
            
            sum = sum + fitness_value

        avg = sum / n

        data = [max, avg]
        plot.append(data)

        # Variable untuk check apakah sudah ada individual dengan fitness function maximum
        is_individual_fit = False
        if max == 1:
            is_individual_fit = True
        
        itr = 0
        while itr < n and not is_individual_fit:
            # Variable untuk menampung individual/child baru
            new_population = []
            for i in range(k):
                parent_1 = genetic_algorithm.random_selection(population)
                parent_2 = genetic_algorithm.random_selection(population)
                child = genetic_algorithm.reproduce(parent_1, parent_2)
                child = genetic_algorithm.mutate(child, self.listRuangan)
                new_population.append(child)

            # assign populasi_baru ke populasi
            population = new_population

            # Hitung nilai fitness function population pada current iteration
            max = -1
            sum = 0
            avg = 0

            for individual in population:
                # Kalkulasi nilai fitness function setiap individu (populasi)
                # Rumus: fitness = 1 / (obj + 1) -> Nilai fitness function = [0, 1], 1 terbaik
                objective_value = individual.countObjective()
                fitness_value = 1 / (objective_value + 1)

                if (fitness_value > max):
                    max = fitness_value
                
                sum = sum + fitness_value

            avg = sum / n

            data = [max, avg]
            plot.append(data)

            # Check apakah sudah ada individual dengan fitness function maximum
            if max == 1:
                is_individual_fit = True


            itr = itr + 1
        
        # Variable menghitung waktu selesai
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        
        # Return berupa tuple (start_population, end_population, plot, k, n, durasi)
        data = (start_population, population, plot, k, n, elapsed_time)

        return data

    # Fungsi plotting ajaib khusus genetic algorithm
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


        title = f"Genetic Algorithm (k={k}, n={n}, t={elapsed_time} ms)"

        plt.figure(figsize=(6.4, 4.8), layout='constrained')
        plt.title(title)
        plt.xlabel('Iterasi')
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
        plt.savefig(file_path)