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
                            # print(new_jadwal[i][idx1].kode +" "+ new_jadwal[j][idx2].kode)

                            #tukar posisi matkul
                            temp = new_jadwal[i][idx1] 
                            new_jadwal[i][idx1] = new_jadwal[j][idx2]
                            new_jadwal[j][idx2] = temp
 
                            # print("SESUDAH SWAP:", new_jadwal[j][idx2].kode)

                            new_state = State(self.listRuangan, new_jadwal)

                            neighbors.append(new_state)


        return neighbors
    
    def moveMethod(self):
        neighbors = []
        jadwalFlat = [slot for hari in self.jadwal.values() for slot in hari] 

        for i in range(len(jadwalFlat)):
            if (jadwalFlat[i] != []):
                # print(f"i = {i}")
                for j in range (len(jadwalFlat)):
                    if (i == j) or (jadwalFlat[j] != []): # slot j sama atau tidak kosong skip
                        continue
                    for x,matkul in enumerate(jadwalFlat[i]):
                        new_jadwal = copy.deepcopy(jadwalFlat)

                        # pindahin matkul ke slot kosong, matkul di slot lama dihapus referensinya
                        new_jadwal[j].append(new_jadwal[i][x])
                        new_jadwal[i].pop(x)
                        # print(f"j = {j} SESUDAH SWAP: {new_jadwal[j][0].kode}")

                        new_state = State(self.listRuangan, new_jadwal)
                
                        neighbors.append(new_state)
                          
        # print("keluar")
        return neighbors

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
                        t = (hari, i, matkul)
                        listTuple.append(t)

        # Sorted by kode matkul ascending
        listTuple.sort(key=lambda x: x[2].kode)

        return listTuple


    # Method mengisi atribut jadwal sesuai dengan listTuple
    # listTuple adalah return dari method serialize()
    # TODO: apakah lebih baik return deep copy state?
    def deserialize(self, listTuple):
        # Clear all slots
        for hari in self.jadwal:
            for slot in self.jadwal[hari]:
                slot.clear()

        for t in listTuple:
            self.jadwal[t[0]][t[1]].append(t[2])

    # Method display yang penting muncul
    def displayNgasal(self):
        for hari in self.jadwal:
            print("=================================")
            print(f"HARI {hari}")
            for i, slot in enumerate(self.jadwal[hari]):
                if slot:
                    print(f"JAM {i + 7}:")
                    for matkul in slot:
                        print("++++++++")
                        matkul.displayNgasal()