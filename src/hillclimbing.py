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
                listTuple = current.serialize()
                neighbour = copy.deepcopy(current.swapSatuMatkul(listTuple))
            else:
                neighbour = copy.deepcopy(current.moveOneSuccessorMethod()) 
            if neighbour.countObjective() < current.countObjective():
                current = neighbour
        return copy.deepcopy(current), current.countObjective()

class SteepestAscentHC:
    def __init__(self, stateAwal : State):
        self.stateAwal = stateAwal 
    
    def solve(self):
        current = self.stateAwal
        iterationCount = 0
        while (True):
            iterationCount += 1
            selectedSuccessor = None
            minObjectiveFunction = 99999999

            #Pilih aksi swap atau move secara random

            if (random.choice([True, False])):
                successors = current.swapMethod()
            else:
                successors = current.moveAllSuccessorMethod()

            # Cari successor dengan nilai obj function terendah
            for successor in successors:
                    if successor.countObjective() < minObjectiveFunction:
                        selectedSuccessor = successor
                        minObjectiveFunction = successor.countObjective()

            neighbour = copy.deepcopy(selectedSuccessor)

            if (neighbour.countObjective() >= current.countObjective()):
                break
            else:
                current = neighbour
        return copy.deepcopy(current), current.countObjective()

class SidewaysMoveHC:
    def __init__(self, stateAwal : State, maxSidewaysMove : int):
        self.stateAwal = stateAwal 
        self.maxSidewaysMove = maxSidewaysMove
    
    def solve(self):
        current = self.stateAwal
        iterationCount = 0
        sidewaysMove = 0
        while (True):
            iterationCount += 1
            selectedSuccessor = None
            minObjectiveFunction = 99999999

            #Pilih aksi swap atau move secara random

            if (random.choice([True, False])):
                successors = current.swapMethod()
            else:
                successors = current.moveAllSuccessorMethod()

            # Cari successor dengan nilai obj function terendah
            for successor in successors:
                    if successor.countObjective() < minObjectiveFunction:
                        selectedSuccessor = successor
                        minObjectiveFunction = successor.countObjective()

            neighbour = copy.deepcopy(selectedSuccessor) 

            if (neighbour.countObjective() > current.countObjective()):
                break
            else:
                # jumlah sideways move bertambah jika sama 
                if (neighbour.countObjective() == current.countObjective()):
                    sidewaysMove += 1
                current = neighbour
                if (sidewaysMove == self.maxSidewaysMove):
                    break
        return copy.deepcopy(current), current.countObjective()



