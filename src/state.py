from kelas import *
import random
import copy
from tabulate import tabulate

class State:
    def __init__(self, listRuangan :list, listMahasiswa :list ,jadwalFlatten = None):
        self.listRuangan = listRuangan
        self.listMahasiswa = listMahasiswa
        if(jadwalFlatten != None):
            self.jadwal = self._from_flat(jadwalFlatten)
        else:

            self.jadwal = {
                "senin":  [[] for _ in range(11)],
                "selasa": [[] for _ in range(11)],
                "rabu":   [[] for _ in range(11)],
                "kamis":  [[] for _ in range(11)],
                "jumat":  [[] for _ in range(11)]
            }
                

    def _from_flat(self, jadwalFlatten: list) -> dict:
        hari_list = ["senin", "selasa", "rabu", "kamis", "jumat"]
        jadwal = {}

        for i, hari in enumerate(hari_list):
            start = i * 11
            end = (i + 1) * 11
            jadwal[hari] = copy.deepcopy(jadwalFlatten[start:end])

        return jadwal

    def makeComplete(self, listMatkul: list):
        hari_list = list(self.jadwal.keys())

        for i, matkul in enumerate(listMatkul):
            if matkul.ruangan is None:
                #proses assign kelas dengan ruangan
                ruangan_terpilih = self.listRuangan[i % len(self.listRuangan)]
                matkul.setRuangan(ruangan_terpilih)

            # pilih hari dan slot acak
            hari = random.choice(hari_list)
            slot = random.randint(0, 10) 

            self.jadwal[hari][slot].append(matkul)


    def countObjective(self) -> float:
        total = 0
        for key in self.jadwal:
            for slots in self.jadwal[key]:
                banyakMatkulNabrak = len(slots)

                #deteksi duplikasi untuk 2 matkul yang kodenya sama dalam 1 slot
                listKodeMk = [mk.kode for mk in slots]
                if len(listKodeMk) != len(set(listKodeMk)):
                    total += 10

                #func objective 1 di spek
                if(banyakMatkulNabrak > 1):
                    for mhs, dfMk in self.listMahasiswa:
                        same = len(set(dfMk) & set(listKodeMk))
                        if same > 1:
                            total += same


                    #func objective 2 di spek
                    for i in range(banyakMatkulNabrak):
                        for j in range(i+1,banyakMatkulNabrak):
                            if slots[i].ruangan == slots[j].ruangan:
                                total = total + slots[i].countBobotPrioritas() +  slots[j].countBobotPrioritas()

                #func objective 3 di spek
                for matkul in slots:
                    if(matkul.ruangan.kuota < matkul.jumlahMahasiswa):
                        total += abs(matkul.ruangan.kuota - matkul.jumlahMahasiswa)

        return total
    
    
    #return state baru hasil swap
    def swapSatuMatkul(self,  listTuple: list, indx1 : int = None, indx2 :int = None):

        if(indx1 is None or indx2 is None):  #jika kosong

            while True:
                indx1, indx2 = random.sample(range(len(listTuple)), 2)
                if listTuple[indx1][2].kode != listTuple[indx2][2].kode:
                    break


        hari1, jamMulai1, matkul1 = listTuple[indx1]
        hari2, jamMulai2, matkul2 = listTuple[indx2]
        
        ruangan1 = matkul1.ruangan
        ruangan2 = matkul2.ruangan

        listTuple[indx1] = (hari2, jamMulai2, matkul2)
        listTuple[indx2] = (hari1, jamMulai1, matkul1)
        
        matkul1.ruangan = ruangan2
        matkul2.ruangan = ruangan1

        newState = State(self.listRuangan, self.listMahasiswa)
        newState.deserialize(listTuple)

        return newState

            

    def swapMethod(self) ->list:
        neighbors = []
        jadwalFlat = [slot for hari in self.jadwal.values() for slot in hari] 
        
        #proses generate neighbors lewat swap
        for i,slots in enumerate(jadwalFlat):
            for idx1,matkul in enumerate(slots):
                for j in range (i+1,len(jadwalFlat)):
                    for idx2,matkul2 in enumerate(jadwalFlat[j]):
                        if(jadwalFlat[i][idx1].kode != jadwalFlat[j][idx2].kode):
                            # shallow copy jadwal baru dan slot-slot untuk index i dan j
                            new_jadwal = jadwalFlat[:]
                            new_jadwal[i] = jadwalFlat[i][:]
                            new_jadwal[j] = jadwalFlat[j][:]

                            # copy matkul yang mau diswap
                            copyMatkul_i = copy.copy(jadwalFlat[i][idx1])
                            copyMatkul_j = copy.copy(jadwalFlat[j][idx2])

                            ruangan_asal1 = copyMatkul_i.ruangan
                            ruangan_asal2 = copyMatkul_j.ruangan

                            #tukar matkul tapi ruangan tetap contoh dibawah ini
                            #before 
                            #slot [i][idx1]: A (Ruang X)
                            #slot [j][idx2]: B (Ruang Y)

                            #after Swap (tukar matkul, ruangan tetap di slot)
                            #slot [i][idx1]: B (Ruang X)
                            #slot [j][idx2]: A (Ruang Y)
                            
                            new_jadwal[i][idx1], new_jadwal[j][idx2] = copyMatkul_j, copyMatkul_i
                            new_jadwal[i][idx1].ruangan = ruangan_asal2
                            new_jadwal[j][idx2].ruangan = ruangan_asal1
 
                            # print("SESUDAH SWAP:", new_jadwal[j][idx2].kode)

                            new_state = State(self.listRuangan, self.listMahasiswa, new_jadwal)

                            neighbors.append(new_state)


        return neighbors
    
    #Method menghasilkan semua successor random dari pemindahan satu pertemuan matkul ke slot yang kosong
    def moveAllSuccessorMethod(self):
        neighbors = []
        jadwalFlat = [slot for hari in self.jadwal.values() for slot in hari] 

        for i in range(len(jadwalFlat)):
            if (jadwalFlat[i] != []):
                # print(f"i = {i}")
                for j in range (len(jadwalFlat)):
                    if (i == j) or (jadwalFlat[j] != []): # slot j sama atau tidak kosong skip
                        continue
                    for x,matkul in enumerate(jadwalFlat[i]):
                        # buat shallow copy jadwal baru, dan shallow copy slot untuk indeks i dan j saja
                        new_jadwal = jadwalFlat[:]
                        new_jadwal[i] = jadwalFlat[i][:]
                        new_jadwal[j] = jadwalFlat[j][:] 

                        # buat copy-an matkul yang dipindah dan isi ruangan random
                        matkulCopy = copy.copy(new_jadwal[i][x])
                        matkulCopy.ruangan = random.choice(self.listRuangan)
                        new_jadwal[j].append(matkulCopy)
                        new_jadwal[i].pop(x)

                        # print(f"j = {j} SESUDAH SWAP: {new_jadwal[j][0].kode}")

                        new_state = State(self.listRuangan, self.listMahasiswa, new_jadwal)
                
                        neighbors.append(new_state)
                          
        return neighbors

    #Method menghasilkan satu successor random dari pemindahan satu pertemuan matkul ke slot yang kosong
    def moveOneSuccessorMethod(self):
        jadwalFlat = [slot for hari in self.jadwal.values() for slot in hari] 

        # cek apakah masih ada slot kosong di jadwal
        emptySlot = [idx for idx, slot in enumerate(jadwalFlat) if len(slot) == 0]
        if (emptySlot):
            new_jadwalFlat = copy.deepcopy(jadwalFlat)
            i, j = 0, 0
            while (True):
                i, j = random.randint(0, len(new_jadwalFlat) - 1), random.randint(0, len(new_jadwalFlat) - 1)
                if (i != j):
                    # cek ada slot kosong tujuan di waktu yang berbeda dari slot awal yang terisi
                    if (new_jadwalFlat[i] != [] and new_jadwalFlat[j] == []):
                        movedMatkulIdx = random.randint(0, len(new_jadwalFlat[i]) - 1)
                        new_jadwalFlat[j].append(new_jadwalFlat[i][movedMatkulIdx])
                        new_jadwalFlat[j][0].ruangan = random.choice(self.listRuangan) # ruangan baru secara random
                        new_jadwalFlat[i].pop(movedMatkulIdx)
                        # print(f"i: {i}, j: {j}, matkul : {new_jadwalFlat[j][0].kode} ")

                        return State(self.listRuangan, self.listMahasiswa, new_jadwalFlat)
        # jika slot jadwal penuh
        return State(self.listRuangan, self.listMahasiswa, jadwalFlat)


    # Method mengembalikan List of tuple {hari, slot, matkul}
    # hari = "senin", "selasa", "rabu", "kamis", "jumat"
    # slot = [0, 10] dimana 0 = jam 7, 10 jam 17
    # matkul = Instansiasi dari Class Matkul
    def serialize(self):
        listTuple = []

        for hari in self.jadwal:
            for i, slot in enumerate(self.jadwal[hari]):
                
                # Tedapat matkul dalam slot
                if slot:
                    for matkul in slot:
                        t = (hari, i, copy.deepcopy(matkul))
                        listTuple.append(t)

        # Sorted by kode matkul ascending
        listTuple.sort(key=lambda x: x[2].kode)

        return listTuple


    # Method mengisi atribut jadwal sesuai dengan listTuple
    # listTuple adalah return dari method serialize()
    def deserialize(self, listTuple):
        # Clear all slots
        for hari in self.jadwal:
            for slot in self.jadwal[hari]:
                slot.clear()

        for t in listTuple:
            self.jadwal[t[0]][t[1]].append(t[2])

    # Fungsi display State dalam bentuk tabel seperti di spek
    def display(self, f=None):
        data = []
        for i in range(11):
            row = [(i + 7)]
            for hari in ["senin", "selasa", "rabu", "kamis", "jumat"]:
                pertemuan_joined = ""
                for matkul in self.jadwal[hari][i]:
                    pertemuan = f"{matkul.kode} @ {matkul.ruangan.kode}"
                    pertemuan_joined += pertemuan + "\n"
                row.append(pertemuan_joined)
            data.append(row)
        
        headers = ["Jam", "Senin", "Selasa", "Rabu", "Kamis", "Jumat"]

        if not f:
            print(tabulate(data, headers=headers, tablefmt="grid"))
        else:
            print(tabulate(data, headers=headers, tablefmt="grid"), file=f)
