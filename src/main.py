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




stochasticSolver = StochasticHC(stateAwal, 200)
stateAkhir, objectiveFunc = stochasticSolver.solve()
for key in stateAkhir.jadwal:
    for x, list in enumerate(stateAkhir.jadwal[key]):
        if not list:
            print("hari " + key + " jam "+ str(x+7))
            continue
        for i,matkul in enumerate(list):
            print("hari " + key + " jam "+ str(x+7) + " " + matkul.kode)
print("Nilai objective akhir stochastic " + str(objectiveFunc))
print()
print()

steepestAscentSolver = SteepestAscentHC(stateAwal)
stateAkhir, objectiveFunc = steepestAscentSolver.solve()
for key in stateAkhir.jadwal:
    for x, list in enumerate(stateAkhir.jadwal[key]):
        if not list:
            print("hari " + key + " jam "+ str(x+7))
            continue
        for i,matkul in enumerate(list):
            print("hari " + key + " jam "+ str(x+7) + " " + matkul.kode)
print("Nilai objective akhir steepest ascent " + str(objectiveFunc))
print()
print()

sidewaysMoveSolver = SidewaysMoveHC(stateAwal, 20)
stateAkhir, objectiveFunc = sidewaysMoveSolver.solve()
for key in stateAkhir.jadwal:
    for x, list in enumerate(stateAkhir.jadwal[key]):
        if not list:
            print("hari " + key + " jam "+ str(x+7))
            continue
        for i,matkul in enumerate(list):
            print("hari " + key + " jam "+ str(x+7) + " " + matkul.kode)
print("Nilai objective akhir sideways move " + str(objectiveFunc))
print()
print()
print()

# ====================== Contoh Pengggunaan SA ========================
sa = SimulatedAnnealing(stateAwal, 400, 100)
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

sa.make_chart(data,"./plot.png")

print("Nilai objective akhir SA " + str(objFunc))
finalState.display()
print()
print()

# ====================== Contoh Pengggunaan GA ========================
# Instansiasi object dari class genetic_algorithm
obj_GA = genetic_algorithm(listRuangan, listMatkul, listMahasiswa)

# Menjalankan genetic algorithm, GA(k, n)
data_GA = obj_GA.GA(40, 1000)

# Membuat chart plotting
genetic_algorithm.make_chart(data_GA, "./plot.png")
# ====================== Contoh Pengggunaan GA ========================

#berhasil (keknya)
