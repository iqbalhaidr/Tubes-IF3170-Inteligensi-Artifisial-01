from state import State
import random
import copy
import math


class SimulatedAnnealing:
    def __init__(self, stateAwal : State, jumlahIterasi: int, temperature: int):
        self.stateAwal = stateAwal
        self.jumlahIterasi = jumlahIterasi  
        self.temperature = temperature
        self.coolingRate = 0.95
    
    def solve(self):
        current = self.stateAwal
        currentScore = self.stateAwal.countObjective()
        
        for i in range(self.jumlahIterasi):
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
            else:
                if (self.temperature != 0 and random.random() < math.exp(-deltaE / self.temperature)) :
                    current = neighbour
                    currentScore = neighbourScore  

            self.temperature = self.temperature * self.coolingRate

        return copy.deepcopy(current), currentScore
    

