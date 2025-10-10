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
                # menunggu kode terbaru
                neighbour = copy.deepcopy(random.choice(current.swapMethod()))
            else:
                neighbour = copy.deepcopy(current.moveMethod()) 
            if neighbour.countObjective() < current.countObjective():
                current = neighbour
        return copy.deepcopy(current), current.countObjective()
    

