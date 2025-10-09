class Ruangan:
    def __init__(self, kode: str, kuota: int):
        self.kode = kode
        self.kuota = kuota  


class Matkul:
    def __init__(self, kode: str, jumlahMahasiswa: int):
        self.kode = kode
        self.jumlahMahasiswa = jumlahMahasiswa
        self.prioritas = {} 
        self.ruangan = None   

    def addPriority(self, key: str):
        if key in self.prioritas:
            self.prioritas[key] += 1
        else:
            self.prioritas[key] = 1

    def setRuangan(self, ruangan: Ruangan):
        self.ruangan = ruangan

    def countBobotPrioritas(self) -> float:
        total = 0
        for key in self.prioritas:
            total += int(key)*0.25*self.prioritas[key]

        return total
    
    # Method display yang penting muncul
    def displayNgasal(self):
        print(f"Kode: {self.kode}")
        print(f"Jumlah Mhs: {self.jumlahMahasiswa}")
        print(f"Ruangan: {self.ruangan.kode} | Kuota: {self.ruangan.kuota}")
        print(f"Prioritas: {self.prioritas}")