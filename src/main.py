import json
import os
import copy
from rich.markdown import Markdown
from rich.console import Console
from state import State, Ruangan, Matkul
from hillclimbing import SteepestAscentHC, StochasticHC, SidewaysMoveHC, RandomRestartHC
from sa import SimulatedAnnealing
from genetic_algorithm import genetic_algorithm
from rich.markdown import Markdown
from rich.console import Console



def load_data(path):
    """Load JSON input berisi data ruangan, mahasiswa, dan kelas."""
    if not os.path.exists(path):
        print(f"[ERROR] File '{path}' tidak ditemukan.")
        exit(1)

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    listRuangan = [Ruangan(r["kode"], r["kuota"]) for r in data["ruangan"]]
    listMahasiswa = [(m["nim"], m["daftar_mk"]) for m in data["mahasiswa"]]

    listMatkul = []
    for value in data["kelas_mata_kuliah"]:
        kode = value["kode"]
        jumlah_mahasiswa = value["jumlah_mahasiswa"]
        sks = value["sks"]

        matkul = Matkul(kode, jumlah_mahasiswa)


        for mhs in data["mahasiswa"]:
            for i, mk in enumerate(mhs["daftar_mk"]):
                if kode == mk:
                    prioritas = mhs["prioritas"][i]
                    matkul.addPriority(str(prioritas))


        for _ in range(sks):
            listMatkul.append(copy.deepcopy(matkul))

    return listRuangan, listMahasiswa, listMatkul


def print_summary(state, label):
    print(f"\n=== {label} ===")
    print(f"Nilai objective: {state.countObjective()}")
    state.display()



def main():
    print()
    console = Console()
    md = Markdown("""
    SISTEM PENJADWALAN OTOMATIS DENGAN BERBAGAI ALGORITMA OPTIMASI
    """)
    console.print(md)

    print()
    print()
    input_path = input("Masukkan path file input JSON (contoh: src/input2.json): ").strip()

    listRuangan, listMahasiswa, listMatkul = load_data(input_path)

    run_count = 1
    while True:
        print(f"\n=================== Percobaan ke-{run_count} ===================")

        # Buat state awal acak
        stateAwal = State(listRuangan, listMahasiswa)
        stateAwal.makeComplete(listMatkul)
        print_summary(stateAwal, f"State Awal {run_count}")

        # Menu algoritma
        print("\nPilih algoritma yang ingin dijalankan:")
        print("1. Steepest Ascent Hill Climbing")
        print("2. Stochastic Hill Climbing")
        print("3. Sideways Move Hill Climbing")
        print("4. Random Restart Hill Climbing")
        print("5. Simulated Annealing")
        print("6. Genetic Algorithm")
        print("7. Keluar")
        choice = input("Masukkan pilihan (1–7): ").strip()

        if choice == "7":
            print("Terima kasih, program selesai.")
            break

        elif choice == "1":
            solver = SteepestAscentHC(stateAwal)
            data = solver.solve()
            final_state, obj_value, *_ = data
            print_summary(final_state, "Steepest Ascent HC")
            print("Banyak iterasi:", data[3])
            print("Waktu:", data[4])
            solver.make_chart(data, f"./plot_steepest_run{run_count}.png")

        elif choice == "2":
            solver = StochasticHC(stateAwal, 20 * len(listMatkul))
            data = solver.solve()
            final_state, obj_value, *_ = data
            print_summary(final_state, "Stochastic HC")
            print("Banyak iterasi:", data[3])
            print("Waktu:", data[4])
            solver.make_chart(data, f"./plot_stochastic_run{run_count}.png")

        elif choice == "3":
            maxSideWaysMove = int(input("Silahkan masukkan berapa max sideways move: "))
            solver = SidewaysMoveHC(stateAwal, maxSideWaysMove)
            data = solver.solve()
            final_state, obj_value, *_ = data
            print_summary(final_state, "Sideways Move HC")
            print("Banyak iterasi:", data[3])
            print("Waktu:", data[4])
            solver.make_chart(data, f"./plot_sideways_run{run_count}.png")

        elif choice == "4":
            maxRestart = int(input("Silahkan masukkan berapa max restart: "))
            solver = RandomRestartHC(listRuangan, listMatkul, listMahasiswa, maxRestart)
            data = solver.solve()
            final_state = data[1]
            print_summary(final_state, "Random Restart HC")
            print("Banyak restart:", data[5])
            for i, value in enumerate(data[4], start=1):
                print(f"Restart {i}: {value}")


            print("Waktu:", data[6])
            solver.make_chart(data, f"./plot_restart_run{run_count}.png")

        elif choice == "5":
            solver = SimulatedAnnealing(stateAwal, 20 * len(listMatkul), 100)
            data = solver.solve()
            final_state, obj_value, *_ = data
            print_summary(final_state, "Simulated Annealing")
            print("Waktu:", data[4])
            print("Jumlah local optimum:", data[6])
            solver.make_chart(data, f"./plot_sa_run{run_count}.png")

        elif choice == "6":
            solver = genetic_algorithm(listRuangan, listMatkul, listMahasiswa)
            data = solver.GA(40, 1000)
            fittest = data[6]
            print_summary(fittest, "Genetic Algorithm")
            genetic_algorithm.make_chart(data, f"./plot_ga_run{run_count}.png")
            print("Waktu:", data[5])

        else:
            print("[ERROR] Pilihan tidak valid. Silakan pilih 1–7.")
        run_count += 1
        print()
        print()

        input("Klik ENTER untuk kembali...")
        os.system('cls')


if __name__ == "__main__":
    main()
