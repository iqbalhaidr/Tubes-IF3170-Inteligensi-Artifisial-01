from state import *
import json
from hillclimbing import *
from sa import *
from genetic_algorithm import *
import os

path = "src\input2.json" 


with open(path, "r", encoding="utf-8") as file:
    data = json.load(file)

listRuangan =[]
listMatkul = []
listMahasiswa = [] #isinya seperti ini (NIM, dftar mk)

for value in data['mahasiswa']:
    NIM = value['nim']
    daftar_mk = value['daftar_mk']
    listMahasiswa.append((NIM,daftar_mk))

for value in data['ruangan']:
    kode = value['kode']
    kuota = value['kuota']

    ruangan = Ruangan(kode, kuota)
    listRuangan.append(ruangan)


for value in data['kelas_mata_kuliah']:
    kode = value['kode']
    jumlah_mahasiswa = value['jumlah_mahasiswa']
    sks = value['sks']

    matkul = Matkul(kode,jumlah_mahasiswa)

    for mahasewa in data['mahasiswa']:
        for i,mk in enumerate(mahasewa['daftar_mk']):
            if kode == mk:
                prioritas = mahasewa['prioritas'][i]
                matkul.addPriority(str(prioritas))


    for i in range(sks):
        temp = copy.deepcopy(matkul)
        listMatkul.append(temp)

for elem in listRuangan:
    print(elem.kode)

print()

for elem in listMatkul:
    print(elem.kode)

stateAwal = State(listRuangan, listMahasiswa)
stateAwal.makeComplete(listMatkul)

print("berhasil")

for key in stateAwal.jadwal:
    for x, list in enumerate(stateAwal.jadwal[key]):
        if not list:
            print("hari " + key + " jam "+ str(x+7))
            continue
        for i,matkul in enumerate(list):
            print("hari " + key + " jam "+ str(x+7) + " " + matkul.kode)

print("Nilai objective sekarang " + str(stateAwal.countObjective()))

# neighbours = stateAwal.swapMethod()
print("berhasil 2")
print()

#coba salah 1 neighbor
# for key in neighbours[0].jadwal:
#     for list in neighbours[0].jadwal[key]:
#         for i,matkul in enumerate(list):
#             print("hari " + key + " jam "+ str(i+7) + " " + matkul.kode)


print()
print()
# ====================== Contoh Pengggunaan Stochastic ========================
print("====================== Contoh Pengggunaan Stochastic ========================")
stochasticSolver = StochasticHC(stateAwal, 20*len(listMatkul))
data_StochasticHC = stochasticSolver.solve()
stateAwal_StochasticHC = stochasticSolver.stateAwal
stateAkhir_StochasticHC = data_StochasticHC[0]
objFunc_StochasticHC = data_StochasticHC[1]
elapsedTime_StochasticHC = data_StochasticHC[3]

stochasticSolver.make_chart(data_StochasticHC,"./plot0.png")
# for key in stateAkhir.jadwal:
#     for x, list in enumerate(stateAkhir.jadwal[key]):
#         if not list:
#             print("hari " + key + " jam "+ str(x+7))
#             continue
#         for i,matkul in enumerate(list):
#             print("hari " + key + " jam "+ str(x+7) + " " + matkul.kode)
print("Nilai objective akhir stochastic " + str(objFunc_StochasticHC))
print(f"Total waktu : {elapsedTime_StochasticHC} s")
stateAkhir_StochasticHC.display()
print()
print()

# ====================== Contoh Pengggunaan Steepest Ascent ========================
print("====================== Contoh Pengggunaan Steepest Ascent ========================")
steepestAscentSolver = SteepestAscentHC(stateAwal)
data_SteepestAscentHC = steepestAscentSolver.solve()
stateAwal_SteepestAscentHC = steepestAscentSolver.stateAwal
stateAkhir_SteepestAscentHC = data_SteepestAscentHC[0]
objFunc_SteepestAscentHC = data_SteepestAscentHC[1]
iterationCount_SteepestAscentHC = data_SteepestAscentHC[3]
elapsedTime_SteepestAscentHC = data_SteepestAscentHC[4]

steepestAscentSolver.make_chart(data_SteepestAscentHC,"./plot1.png")

# stateAkhir, objectiveFunc = steepestAscentSolver.solve()
# for key in stateAkhir.jadwal:
#     for x, list in enumerate(stateAkhir.jadwal[key]):
#         if not list:
#             print("hari " + key + " jam "+ str(x+7))
#             continue
#         for i,matkul in enumerate(list):
#             print("hari " + key + " jam "+ str(x+7) + " " + matkul.kode)
print("Nilai objective akhir steepest ascent " + str(objFunc_SteepestAscentHC))
print(f"Iteration count = {iterationCount_SteepestAscentHC}")
print(f"Total waktu = {elapsedTime_SteepestAscentHC} s")
stateAkhir_SteepestAscentHC.display()
print()
print()

# ====================== Contoh Pengggunaan Sideways Move ========================
print("====================== Contoh Pengggunaan Sideways Move ========================")
sidewaysMoveSolver = SidewaysMoveHC(stateAwal, 20)
data_SidewaysMoveHC = sidewaysMoveSolver.solve()
stateAwal_SidewaysMoveHC = sidewaysMoveSolver.stateAwal
stateAkhir_SidewaysMoveHC = data_SidewaysMoveHC[0]
objFunc_SidewaysMoveHC = data_SidewaysMoveHC[1]
iterationCount_SidewaysMoveHC = data_SidewaysMoveHC[3]
elapsedTime_SidewaysMoveHC = data_SidewaysMoveHC[4]

sidewaysMoveSolver.make_chart(data_SidewaysMoveHC,"./plot2.png")


# for key in stateAkhir.jadwal:
#     for x, list in enumerate(stateAkhir.jadwal[key]):
#         if not list:
#             print("hari " + key + " jam "+ str(x+7))
#             continue
#         for i,matkul in enumerate(list):
#             print("hari " + key + " jam "+ str(x+7) + " " + matkul.kode)
print("Nilai objective akhir sideways move " + str(objFunc_SidewaysMoveHC))
print(f"Iteration count = {iterationCount_SidewaysMoveHC}")
print(f"Total waktu = {elapsedTime_SidewaysMoveHC} s")
stateAkhir_SidewaysMoveHC.display()
print()
print()

# ====================== Contoh Pengggunaan Random Restart ========================
print("====================== Contoh Pengggunaan Random Restart ========================")
randomRestartSolver = RandomRestartHC(listRuangan, listMatkul, listMahasiswa, 5)
data_RandomRestartHC = randomRestartSolver.solve()
# Kumpulan initial states
statesAwal_RandomRestartHC = data_RandomRestartHC[0] 

stateAkhir_RandomRestartHC = data_RandomRestartHC[1]
objFunc_RandomRestartHC = data_RandomRestartHC[2]
iterationCount_RandomRestartHC = data_RandomRestartHC[4]
restartCount_RandomRestartHC = data_RandomRestartHC[5]
elapsedTime_RandomRestartHC = data_RandomRestartHC[6]

randomRestartSolver.make_chart(data_RandomRestartHC,"./plot3.png")


# for key in stateAkhir.jadwal:
#     for x, list in enumerate(stateAkhir.jadwal[key]):
#         if not list:
#             print("hari " + key + " jam "+ str(x+7))
#             continue
#         for i,matkul in enumerate(list):
#             print("hari " + key + " jam "+ str(x+7) + " " + matkul.kode)
print("Nilai objective akhir Random Restart " + str(objFunc_RandomRestartHC))
# Iteration count per restart
print(f"Banyak restart = {restartCount_RandomRestartHC}")
for i, iterCount in enumerate(iterationCount_RandomRestartHC):
    print(f"Restart {i} - Iteration count = {iterCount}")
print(f"Total waktu = {elapsedTime_RandomRestartHC} s")
print()
stateAkhir_RandomRestartHC.display()
print()
print()

# ====================== Contoh Pengggunaan SA ========================
print("====================== Contoh Pengggunaan SA ========================")
sa = SimulatedAnnealing(stateAwal, 20*len(listMatkul), 100)
data = sa.solve()
stateAwalSA = sa.stateAwal
finalState = data[0]
objFunc = data[1]

if data[5]: 
    print("SA terjebak di local optimum")

# for key in finalState.jadwal:
#     for x, list in enumerate(finalState.jadwal[key]):
#         if not list:
#             print("hari " + key + " jam "+ str(x+7))
#             continue
#         for i,matkul in enumerate(list):
#             print("hari " + key + " jam "+ str(x+7) + " " + matkul.kode)

sa.make_chart(data,"./plot4.png")

print("Nilai objective akhir SA " + str(objFunc))
finalState.display()
print()
print()

# ====================== Contoh Pengggunaan GA ========================
print("====================== Contoh Pengggunaan GA ========================")
# Instansiasi object dari class genetic_algorithm
obj_GA = genetic_algorithm(listRuangan, listMatkul, listMahasiswa)

# Menjalankan genetic algorithm, GA(k, n)
data_GA = obj_GA.GA(40, 1000)

# Membuat chart plotting
genetic_algorithm.make_chart(data_GA, "./plot5.png")
# ====================== Contoh Pengggunaan GA ========================

#berhasil (keknya)
