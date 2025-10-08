from state import State
import random
import copy


class StochasticHC:
    def __init__(self, stateAwal : State, jumlahIterasi: int):
        self.stateAwal = stateAwal
        self.jumlahIterasi = jumlahIterasi  
    
    def solve(self):
        current = self.stateAwal
        for i in range(self.jumlahIterasi):
            if (random.choice([True, False])):
                neighbour = copy.deepcopy(random.choice(current.swapMethod()))
            else:
                # neighbour = copy.deepcopy(random.choice(current.swapMethod()))
                if (len(current.moveMethod()) > 0):
                    # print("ada")
                    neighbour = copy.deepcopy(random.choice(current.moveMethod()))
                else:
                    neighbour = current
                # print("yo")
                # neighbour = copy.deepcopy(current.moveMethod())
            if neighbour.countObjective() < current.countObjective():
                current = neighbour
        return copy.deepcopy(current), current.countObjective()
