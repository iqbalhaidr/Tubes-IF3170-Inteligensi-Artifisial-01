from state import State
import random
import copy
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class StochasticHC:
    def __init__(self, stateAwal : State, jumlahIterasi: int):
        self.stateAwal = stateAwal
        self.jumlahIterasi = jumlahIterasi  
    
    def solve(self):
        current = self.stateAwal
        currentScore = self.stateAwal.countObjective()
        plotObjFunc = []

        start_time = time.perf_counter()
        
        for i in range(self.jumlahIterasi):
            listTuple = current.serialize()
            neighbor1 = current.swapSatuMatkul(listTuple)
            neighbor2 = current.moveOneSuccessorMethod()

            # Bandingkan nilai cost / objective
            if neighbor1.countObjective() < neighbor2.countObjective():
                neighbour = neighbor1
            else:
                neighbour = neighbor2

            neighbourScore = neighbour.countObjective()

            # Pindah ke neighbour jika nilai obj func nya lebih rendah
            if neighbourScore < currentScore:
                current = neighbour
                currentScore = neighbourScore
                plotObjFunc.append(currentScore)
            else:
                plotObjFunc.append(currentScore)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        return copy.deepcopy(current), currentScore, plotObjFunc, self.jumlahIterasi, elapsed_time
    
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

    def findBestSuccessor(self, successors : list):
        minSuccessorObjFunction = 99999999
        selectedSuccessor = None
        for successor in successors:
                    if successor.countObjective() < minSuccessorObjFunction:
                        selectedSuccessor = successor
                        minSuccessorObjFunction = successor.countObjective()
        return selectedSuccessor
    
    def solve(self):
        current = self.stateAwal
        currentScore = self.stateAwal.countObjective()
        plotObjFunc = []
        iterationCount = 0

        start_time = time.perf_counter()
        while (True):
            iterationCount += 1

            successors1 = current.swapMethod()
            successors2 = current.moveAllSuccessorMethod()

            neighbor1 = self.findBestSuccessor(successors1)
            neighbor2 = self.findBestSuccessor(successors2)

            # Bandingkan nilai cost / objective
            if neighbor1.countObjective() < neighbor2.countObjective():
                neighbour = neighbor1
            else:
                neighbour = neighbor2
            
            neighbourScore = neighbour.countObjective()
           

            # keluarkan hasil ketika tidak ada neighbour yang lebih rendah dengan nilai obj func
            if (neighbourScore >= currentScore):
                plotObjFunc.append(currentScore)
                break
            else:
                current = neighbour
                currentScore = neighbourScore
                plotObjFunc.append(currentScore)
   
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        return copy.deepcopy(current), currentScore, plotObjFunc, iterationCount, elapsed_time
    
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

    def findBestSuccessor(self, successors : list):
        minSuccessorObjFunction = 99999999
        selectedSuccessor = None
        for successor in successors:
                    if successor.countObjective() < minSuccessorObjFunction:
                        selectedSuccessor = successor
                        minSuccessorObjFunction = successor.countObjective()
        return selectedSuccessor
    
    def solve(self):
        current = self.stateAwal
        currentScore = self.stateAwal.countObjective()
        iterationCount = 0
        sidewaysMove = 0
        plotObjFunc = []

        start_time = time.perf_counter()
        while (True):
            iterationCount += 1

            successors1 = current.swapMethod()
            successors2 = current.moveAllSuccessorMethod()

            neighbor1 = self.findBestSuccessor(successors1)
            neighbor2 = self.findBestSuccessor(successors2)

            # Bandingkan nilai cost / objective
            if neighbor1.countObjective() < neighbor2.countObjective():
                neighbour = neighbor1
            else:
                neighbour = neighbor2
            
            neighbourScore = neighbour.countObjective()

            # keluarkan hasil ketika tidak ada neighbour yang lebih rendah sama dengan nilai obj func
            if (neighbourScore > currentScore):
                plotObjFunc.append(currentScore)
                break
            else:
                # jumlah sideways move bertambah jika nilai obj func sama
                if (neighbourScore == currentScore):
                    sidewaysMove += 1

                current = neighbour
                currentScore = neighbourScore
                plotObjFunc.append(currentScore)
                if (sidewaysMove == self.maxSidewaysMove):
                    break
       
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        return copy.deepcopy(current), currentScore, plotObjFunc, iterationCount, elapsed_time
    
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

class RandomRestartHC:
    def __init__(self, listRuangan : list, listMatkul : list, listMahasiswa : list, maxRestart: int):
        self.listRuangan = listRuangan
        self.listMatkul = listMatkul
        self.listMahasiswa = listMahasiswa
        self.maxRestart = maxRestart

    def findBestSuccessor(self, successors : list):
        minSuccessorObjFunction = 99999999
        selectedSuccessor = None
        for successor in successors:
                    if successor.countObjective() < minSuccessorObjFunction:
                        selectedSuccessor = successor
                        minSuccessorObjFunction = successor.countObjective()
        return selectedSuccessor
    
    def solve(self):
        restartCount = 0
        initialStates = []
        plotObjFunc, iterationCountList = [], [] # Obj func keseluruhan tiap restart

        start_time = time.perf_counter()

        bestState = None
        bestScore = 9999999
        while (restartCount < self.maxRestart and bestScore > 0):
            # initial random state
            current = State(self.listRuangan, self.listMahasiswa)
            current.makeComplete(self.listMatkul)
            currentScore = current.countObjective()
            initialStates.append(current)

            if (restartCount == 0):
                bestState = current

            subPlotObjFunc = []
            iterationCount = 0

            while (True):
                iterationCount += 1

                successors1 = current.swapMethod()
                successors2 = current.moveAllSuccessorMethod()

                neighbor1 = self.findBestSuccessor(successors1)
                neighbor2 = self.findBestSuccessor(successors2)

                # Bandingkan nilai cost / objective
                if neighbor1.countObjective() < neighbor2.countObjective():
                    neighbour = neighbor1
                else:
                    neighbour = neighbor2
                
                neighbourScore = neighbour.countObjective()
                
                # Buat hasil ketika tidak ada neighbour yang lebih rendah nilai obj func
                if (neighbourScore >= currentScore):
                    bestScore = currentScore
                    subPlotObjFunc.append(currentScore)
                    break
                else:
                    current = neighbour
                    currentScore = neighbourScore
                    subPlotObjFunc.append(currentScore)

            # Mengambil state terbaik saat ini dengan membandingkan nilai
            # obj func dari hasil state restart
            if (bestScore > currentScore):
                bestState = current

            # Masukkan obj func per iterasi dalam satu restart ke plot obj
            iterationCountList.append(iterationCount)
            plotObjFunc.append(subPlotObjFunc)
            restartCount += 1
        
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        
        return initialStates, copy.deepcopy(bestState), bestScore, plotObjFunc, iterationCountList, restartCount, elapsed_time
    
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
    


