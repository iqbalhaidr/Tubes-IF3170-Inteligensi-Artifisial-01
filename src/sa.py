from state import State
import random
import copy
import math
import time
import matplotlib.pyplot as plt


class SimulatedAnnealing:
    def __init__(self, stateAwal : State, jumlahIterasi: int, temperature: int):
        self.stateAwal = stateAwal
        self.jumlahIterasi = jumlahIterasi  
        self.temperature = temperature
        self.coolingRate = 0.95
    
    def solve(self):
        plotObjFunc = []
        plotExp = []
        
        current = self.stateAwal
        currentScore = self.stateAwal.countObjective()
        plotObjFunc.append(currentScore)
        
        start_time = time.perf_counter()

        for i in range(self.jumlahIterasi):
            if currentScore == 0:
                break

            if (random.choice([True, False])):
                listTuple = current.serialize()
                neighbour = current.swapSatuMatkul(listTuple)
            else:
                neighbour = current.moveOneSuccessorMethod()

            neighbourScore = neighbour.countObjective()
            deltaE = neighbourScore - currentScore

            #better
            if  deltaE < 0:
                current = neighbour
                currentScore = neighbourScore             
                prob = 1.0 
            else:
                prob = math.exp(-deltaE / max(self.temperature, 1e-8))
                if random.random() < prob:
                    current = neighbour
                    currentScore = neighbourScore
                   
            plotExp.append((i,prob))
            self.temperature = self.temperature * self.coolingRate
            plotObjFunc.append(currentScore)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        localOptimum = False
        N = min(10, len(plotObjFunc)) 

        if currentScore != 0:
            #kalau 10 trakhir atau n buah obj terakhir nilainya sama local optimum
            if len(set(plotObjFunc[-N:])) == 1:
                localOptimum = True

        return copy.deepcopy(current), currentScore, plotObjFunc, plotExp, elapsed_time, localOptimum
    
    def make_chart(self, data_output, file_path):
        plt.figure(figsize=(8, 5))
        plt.plot(range(len(data_output[2])), data_output[2], color='blue')
        plt.xlabel("Iterasi")
        plt.ylabel("Objective Function")
        plt.title("Perubahan Nilai Objective Function terhadap Iterasi")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{file_path}_objective.png", dpi=300, bbox_inches="tight")
        plt.close()

        iters, probs = zip(*data_output[3])
        plt.figure(figsize=(8, 5))
        plt.plot(iters, probs, color='purple')
        plt.xlabel("Iterasi")
        plt.ylabel("Probabilitas e^(-ΔE/T)")
        plt.title("Perubahan Probabilitas Penerimaan Solusi Buruk terhadap Iterasi")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{file_path}_exp_prob.png", dpi=300, bbox_inches="tight")
        plt.close()





    

