import numpy as np
from itertools import product

L = 4  # rozmiar sieci 4x4

# Tworzymy wszystkie 2^16 możliwe konfiguracje spinów (+1 / -1)
all_configs = list(product([-1, 1], repeat=L * L))

# Funkcje pomocnicze
def get_spin(config, x, y):
    return config[y * L + x]

def periodic(i):
    return i % L

def calculate_energy(config, J1, J2):
    E = 0
    for y in range(L):
        for x in range(L):
            spin = get_spin(config, x, y)
            is_horizontal = (x + y) % 2 == 0

            if is_horizontal:
                left = get_spin(config, periodic(x - 1), y)
                right = get_spin(config, periodic(x + 1), y)
                E -= J1 * spin * left
                E -= J1 * spin * right

                up_left = get_spin(config, periodic(x - 1), periodic(y - 1))
                up_right = get_spin(config, periodic(x + 1), periodic(y - 1))
                down_left = get_spin(config, periodic(x - 1), periodic(y + 1))
                down_right = get_spin(config, periodic(x + 1), periodic(y + 1))

                E -= J2 * spin * up_left
                E -= J2 * spin * up_right
                E -= J2 * spin * down_left
                E -= J2 * spin * down_right
            else:
                up = get_spin(config, x, periodic(y - 1))
                down = get_spin(config, x, periodic(y + 1))
                E -= J1 * spin * up
                E -= J1 * spin * down

                left_up = get_spin(config, periodic(x - 1), periodic(y - 1))
                right_up = get_spin(config, periodic(x + 1), periodic(y - 1))
                left_down = get_spin(config, periodic(x - 1), periodic(y + 1))
                right_down = get_spin(config, periodic(x + 1), periodic(y + 1))

                E -= J2 * spin * left_up
                E -= J2 * spin * right_up
                E -= J2 * spin * left_down
                E -= J2 * spin * right_down

    return E / 2

def calculate_magnetization(config):
    mx, my = 0, 0
    for y in range(L):
        for x in range(L):
            spin = get_spin(config, x, y)
            if (x + y) % 2 == 0:
                mx += spin
            else:
                my += spin
    return mx, my

# Przykładowe obliczenia
data = []
J1 = 1.0
J2 = 0.5
beta = 1.0

for config in all_configs:
    E = calculate_energy(config, J1, J2)
    mx, my = calculate_magnetization(config)
    weight = np.exp(-beta * E)
    data.append((config, E, mx, my, weight))

Z = sum(weight for _, _, _, _, weight in data)

# Zapisz dane do pliku
with open("config_data.txt", "w") as f:
    f.write("config E mx my weight Z\n")  # Nagłówek
    for config, E, mx, my, weight in data:
        config_str = " ".join(map(str, config))
        f.write(f"{config_str} {E:.6f} {mx} {my} {weight:.6e} {Z:.6e}\n")

# Średnie wartości
avg_mx = sum(mx * w for _, _, mx, _, w in data) / Z
avg_my = sum(my * w for _, _, _, my, w in data) / Z

print("Funkcja podziału Z:", Z)
print("Średnia magnetyzacja:", avg_mx, avg_my)
