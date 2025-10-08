from state import *
import json
from hillclimbing import *


path = "Tubes_AI_1\src\input.json" 


with open(path, "r", encoding="utf-8") as file:
    data = json.load(file)

listRuangan =[]
listMatkul = []

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

stateAwal = State(listRuangan)
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




stochasticSolver = StochasticHC(stateAwal, 3)
stateAkhir, objectiveFunc = stochasticSolver.solve()
for key in stateAkhir.jadwal:
    for x, list in enumerate(stateAkhir.jadwal[key]):
        if not list:
            print("hari " + key + " jam "+ str(x+7))
            continue
        for i,matkul in enumerate(list):
            print("hari " + key + " jam "+ str(x+7) + " " + matkul.kode)
print("Nilai objective akhir " + str(objectiveFunc))

#berhasil (keknya)
