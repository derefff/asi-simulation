import matplotlib.pyplot as plt
import numpy as np

def draw_spin_config(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    L = int(lines[0].strip())
    spins = [int(line.strip()) for line in lines[1:]]

    if len(spins) != 2 * L * L:
        print(f"Błąd: Oczekiwano {2 * L * L} spinów, ale otrzymano {len(spins)}.")
        return

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 2 * L)
    ax.set_ylim(0, L)
    ax.set_aspect('equal')
    ax.set_xticks(np.arange(0, 2 * L, 1))
    ax.set_yticks(np.arange(0, L, 1))
    ax.grid(which='both', color='gray', linestyle='-', linewidth=0.5)
    ax.set_title('Konfiguracja spinów (wyśrodkowane, pionowe przesunięte w dół)')

    for i in range(L):
        for j in range(L):
            # Spin poziomy (kolumny parzyste: 0, 2, 4, ...)
            spin_h = spins[2 * (i * L + j)]
            x_h = 2 * j
            y = i
            # Wyśrodkowanie poziomej strzałki
            if spin_h == 1:
                ax.arrow(x_h + 0.4, y + 0.8, 0.25, 0, head_width=0.15, head_length=0.1,fc='black', ec='black')# fc='red', ec='red')
            else:
                ax.arrow(x_h + 0.7, y + 0.8, -0.25, 0, head_width=0.15, head_length=0.1, fc='black', ec='black')#fc='blue', ec='blue')

            # Spin pionowy (kolumny nieparzyste: 1, 3, 5, ...)
            spin_v = spins[2 * (i * L + j) + 1]
            x_v = 2 * j + 1
            # Przesunięcie pionowej strzałki w dół (y + 0.4 zamiast y + 0.5)
            if spin_v == 1:
                ax.arrow(x_v + 0.5, y + 0.1, 0, 0.25, head_width=0.15, head_length=0.1, fc='black', ec='black') # fc='green', ec='green')
            else:
                ax.arrow(x_v + 0.5, y + 0.4, 0, -0.25, head_width=0.15, head_length=0.1, fc='black', ec='black')#fc='purple', ec='purple')

    plt.show()

draw_spin_config('test.txt')