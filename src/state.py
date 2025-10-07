from kelas import *
import random
import copy

class State:
    def __init__(self, listRuangan :list, jadwalFlatten = None):
        self.listRuangan = listRuangan
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

                #func objective 1 di spek
                if(banyakMatkulNabrak > 1):
                    total+= banyakMatkulNabrak

                    #func objective 2 di spek
                    for i in range(banyakMatkulNabrak):
                        for j in range(i+1,banyakMatkulNabrak):
                            if slots[i].ruangan == slots[j].ruangan:
                                total = total + slots[i].countBobotPrioritas() +  slots[j].countBobotPrioritas()

                #func objective 3 di spek
                for matkul in slots:
                    if(matkul.ruangan.kuota < matkul.jumlahMahasiswa):
                        total = abs(matkul.ruangan.kuota - matkul.jumlahMahasiswa)


        return total
                    

    def swapMethod(self) ->list:
        neighbors = []
        jadwalFlat = [slot for hari in self.jadwal.values() for slot in hari] 
        
        #proses generate neighbors lewat swap
        for i,slots in enumerate(jadwalFlat):
            for idx1,matkul in enumerate(slots):
                for j in range (i+1,len(jadwalFlat)):
                    for idx2,matkul2 in enumerate(jadwalFlat[j]):

                        if(jadwalFlat[i][idx1].kode != jadwalFlat[j][idx2].kode):
                            new_jadwal = copy.deepcopy(jadwalFlat)
                            print(new_jadwal[i][idx1].kode +" "+ new_jadwal[j][idx2].kode)

                            #tukar posisi matkul
                            temp = new_jadwal[i][idx1] 
                            new_jadwal[i][idx1] = new_jadwal[j][idx2]
                            new_jadwal[j][idx2] = temp
 
                            print("SESUDAH SWAP:", new_jadwal[i][idx1].kode, "<->", new_jadwal[j][idx2].kode)

                            new_state = State(self.listRuangan, new_jadwal)

                            neighbors.append(new_state)


        return neighbors
    
    # def moveMethod(self):





            