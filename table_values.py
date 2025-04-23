import numpy as np
from itertools import product

# NOTES ---------------
# żeby pamiętać
# 1. można zrobić zapis sieci 3x3
# 2. wygenerowany plik z wartościami bedzie użyty do porównania w głównym pliku symulacji (main.c)
#

#poprawki
#2. sprawdz is_horizontal bo chyba jest tam zły warunek

#3. J1 i J2 chyba pomyliłem oddziaływania powinienem zrobić zamiane
# J1 -> J2 i J2 -> J1

#4. Periodic źle działa

#5. zrób pomocniczne wizualizacje sieci żeby mniej wiecej widziec co sie dzieje
# można wylosować losowy spin i wyswietlic jego sąsiadów

#6. źle obliczana jest magnetyzacja, weź popatrz "wyklad1.pdf" tam jest `smag` tak sie oblicza

#7. wyrysowanie temp dla kilku $\beta$ ? (jeszcze sie dopytam)


# 1. są dwie podsieci pion i poziom
# ze względu na zapis spinów w jednej tablicy [ poziom, pion, poziom, pion,... ]
# wymiar LxL naprawdę to (2L)xL żeby wymiar sie zgadzał
L = 4  # rozmiar sieci 4x4 -> 8x4

# tworzenie wszystkich konfiguracji spinów (+1 / -1)
all_configs = list(product([-1, 1], repeat=(2*L) * L))

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

    return E / 2 # bo oddziaływania spinow np. 1 - 2, 2 - 1 sa liczone dwa razy

def calculate_magnetization(config):
    mx, my = 0, 0
    # magnetyzacja nie jest normalizowana
    for y in range(L):
        for x in range(L):
            spin = get_spin(config, x, y)
            if (x + y) % 2 == 0:
                mx += spin
            else:
                my += spin
    return mx, my

data = []
J1 = 1.0
J2 = 1.0
beta = 1.0

for config in all_configs:
    E = calculate_energy(config, J1, J2)
    mx, my = calculate_magnetization(config)
    weight = np.exp(-beta * E)
    data.append((config, E, mx, my, weight))

Z = sum(weight for _, _, _, _, weight in data)

# zapisywanie wartosci do pliku
with open("config_data.txt", "w") as f:
    f.write("config E mx my weight Z\n")  # nagłówek
    for config, E, mx, my, weight in data:
        config_str = " ".join(map(str, config))
        f.write(f"{config_str} {E:.3f} {mx} {my} {weight:.6e} {Z:.6e}\n")

# srednie wartosci
avg_mx = sum(mx * w for _, _, mx, _, w in data) / Z
avg_my = sum(my * w for _, _, _, my, w in data) / Z

# print("Funkcja podziału Z:", Z)
# print("Średnia magnetyzacja:", avg_mx, avg_my)
