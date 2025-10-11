from state import State
import random
import copy
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class StochasticHC:
    def __init__(self, stateAwal : State, jumlahIterasi: int):
        self.stateAwal = stateAwal
        self.jumlahIterasi = jumlahIterasi  
    
    def solve(self):
        current = self.stateAwal
        plotObjFunc = []
        for i in range(self.jumlahIterasi):
            # pilihan aksi swap atau move secara random, satu successor
            if (random.choice([True, False])):
                listTuple = current.serialize()
                neighbour = copy.deepcopy(current.swapSatuMatkul(listTuple))
            else:
                neighbour = copy.deepcopy(current.moveOneSuccessorMethod()) 

            # Pindah ke neighbour jika nilai obj func nya lebih rendah
            if neighbour.countObjective() < current.countObjective():
                current = neighbour
                plotObjFunc.append(current.countObjective())
            else:
                plotObjFunc.append(current.countObjective())
        # for i in range(len(plotObjFunc)):
        #     print(f"value{i}= {plotObjFunc[i]}")
        return copy.deepcopy(current), current.countObjective(), plotObjFunc
    
    def make_chart(self, data_output, file_path):
        plt.figure(figsize=(8, 5))
        plt.plot(range(len(data_output[2])), data_output[2], color='blue')
        plt.xlabel("Iterasi")
        plt.ylabel("Objective Function")
        plt.title("Perubahan Nilai Objective Function terhadap Iterasi (Stochastic HC)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{file_path}_objective.png", dpi=300, bbox_inches="tight")
        plt.close()

class SteepestAscentHC:
    def __init__(self, stateAwal : State):
        self.stateAwal = stateAwal 
    
    def solve(self):
        current = self.stateAwal
        plotObjFunc = []
        iterationCount = 0
        while (True):
            iterationCount += 1

            #Pilih aksi swap atau move secara random, ambil semua successor
            selectedSuccessor = None
            minSuccessorObjFunction = 99999999

            if (random.choice([True, False])):
                successors = current.swapMethod()
            else:
                successors = current.moveAllSuccessorMethod()

            # Cari successor dengan nilai obj function terendah
            for successor in successors:
                    if successor.countObjective() < minSuccessorObjFunction:
                        selectedSuccessor = successor
                        minSuccessorObjFunction = successor.countObjective()

            neighbour = copy.deepcopy(selectedSuccessor)

            # keluarkan hasil ketika tidak ada neighbour yang lebih rendah dengan nilai obj func
            if (neighbour.countObjective() >= current.countObjective()):
                plotObjFunc.append(current.countObjective())
                break
            else:
                current = neighbour
                plotObjFunc.append(current.countObjective())
        # for i in range(len(plotObjFunc)):
        #     print(f"value{i} = {plotObjFunc[i]}")
        # print(f"iter count = {iterationCount}")
        return copy.deepcopy(current), current.countObjective(), plotObjFunc, iterationCount
    
    def make_chart(self, data_output, file_path):
        plt.figure(figsize=(8, 5))
        plt.plot(range(len(data_output[2])), data_output[2], color='blue')
        plt.xlabel("Iterasi")
        plt.ylabel("Objective Function")
        plt.title("Perubahan Nilai Objective Function terhadap Iterasi (Steepest Ascent HC)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{file_path}_objective.png", dpi=300, bbox_inches="tight")
        plt.close()

class SidewaysMoveHC:
    def __init__(self, stateAwal : State, maxSidewaysMove : int):
        self.stateAwal = stateAwal 
        self.maxSidewaysMove = maxSidewaysMove
    
    def solve(self):
        current = self.stateAwal
        iterationCount = 0
        sidewaysMove = 0
        plotObjFunc = []
        while (True):
            iterationCount += 1

            #Pilih aksi swap atau move secara random, ambil semua successor
            selectedSuccessor = None
            minSuccessorObjFunction = 99999999

            if (random.choice([True, False])):
                successors = current.swapMethod()
            else:
                successors = current.moveAllSuccessorMethod()

            # Cari successor dengan nilai obj function terendah
            for successor in successors:
                    if successor.countObjective() < minSuccessorObjFunction:
                        selectedSuccessor = successor
                        minSuccessorObjFunction = successor.countObjective()

            neighbour = copy.deepcopy(selectedSuccessor) 

            # keluarkan hasil ketika tidak ada neighbour yang lebih rendah sama dengan nilai obj func
            if (neighbour.countObjective() > current.countObjective()):
                plotObjFunc.append(current.countObjective())
                break
            else:
                # jumlah sideways move bertambah jika nilai obj func sama
                if (neighbour.countObjective() == current.countObjective()):
                    sidewaysMove += 1
                # print(f"iter count {iterationCount} sideaysmove {sidewaysMove}")
                current = neighbour
                plotObjFunc.append(current.countObjective())
                if (sidewaysMove == self.maxSidewaysMove):
                    # print(f"iter count {iterationCount} break")
                    break
        # for i in range(len(plotObjFunc)):
        #     print(f"value{i} = {plotObjFunc[i]}")
        # print(f"iter count = {iterationCount}")
        return copy.deepcopy(current), current.countObjective(), plotObjFunc, iterationCount
    
    def make_chart(self, data_output, file_path):
        plt.figure(figsize=(8, 5))
        plt.plot(range(len(data_output[2])), data_output[2], color='blue')
        plt.xlabel("Iterasi")
        plt.ylabel("Objective Function")
        plt.title("Perubahan Nilai Objective Function terhadap Iterasi (Sideways Move HC)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{file_path}_objective.png", dpi=300, bbox_inches="tight")
        plt.close()

class RandomRestarttHC:
    def __init__(self, listRuangan : list, listMatkul : list, maxRestart: int):
        self.listRuangan = listRuangan
        self.listMatkul = listMatkul
        self.maxRestart = maxRestart
    
    def solve(self):
        restartCount = 0
        minObjFunctionIteration = 999999
        initialStates = []
        plotObjFunc, iterationCountList = [], [] # Obj func keseluruhan tiap restart

        bestState = None
        while (restartCount < self.maxRestart and minObjFunctionIteration > 0):
            # initial random state
            current = State(self.listRuangan)
            current.makeComplete(self.listMatkul)
            initialStates.append(current)

            if (restartCount == 0):
                bestState = current

            subPlotObjFunc = []
            iterationCount = 0

            while (True):
                iterationCount += 1

                #Pilih aksi swap atau move secara random, ambil semua successor
                selectedSuccessor = None
                minSuccessorObjFunction = 99999999

                if (random.choice([True, False])):
                    successors = current.swapMethod()
                else:
                    successors = current.moveAllSuccessorMethod()

                # Cari successor dengan nilai obj function terendah
                for successor in successors:
                        if successor.countObjective() < minSuccessorObjFunction:
                            selectedSuccessor = successor
                            minSuccessorObjFunction = successor.countObjective()

                neighbour = copy.deepcopy(selectedSuccessor)
                
                # Buat hasil ketika tidak ada neighbour yang lebih rendah nilai obj func
                if (neighbour.countObjective() >= current.countObjective()):
                    minObjFunctionIteration = current.countObjective()
                    subPlotObjFunc.append(current.countObjective())
                    break
                else:
                    current = neighbour
                    subPlotObjFunc.append(current.countObjective())

            # print(f"obj func restart ke {restartCount} : {current.countObjective()}")
            # Mengambil state terbaik saat ini dengan membandingkan nilai
            # obj func dari hasil state restart
            if (bestState.countObjective() > current.countObjective()):
                bestState = current

            # Masukkan obj func per iterasi dalam satu restart ke plot obj
            iterationCountList.append(iterationCount)
            plotObjFunc.append(subPlotObjFunc)
            restartCount += 1
        
            
        return initialStates, copy.deepcopy(bestState), bestState.countObjective(), plotObjFunc, iterationCountList, restartCount
    
    def make_chart(self, data_output, file_path):
        plt.figure(figsize=(8, 5))

        # Membuat fungsi colorMap yang mereturn 1 dari 10 warna berdasarkan indeks warna (< total restart)
        colorMap = cm.get_cmap('tab10',len(data_output[3]))
        #Plot untuk tiap restart
        for i, ObjFuncRestart in enumerate(data_output[3]):
            plt.plot(range(len(ObjFuncRestart)), ObjFuncRestart, label=f"Restart ke - {i}", color=colorMap(i))

        plt.xlabel("Iterasi")
        plt.ylabel("Objective Function")
        plt.title("Perubahan Nilai Objective Function terhadap Iterasi (Random Restart HC)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{file_path}_objective.png", dpi=300, bbox_inches="tight")
        plt.close()
    


