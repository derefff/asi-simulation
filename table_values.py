import numpy as np
import matplotlib.pyplot as plt
from itertools import product

# NOTES ---------------
# żeby pamiętać
# 1. można zrobić zapis sieci 3x3
# 2. wygenerowany plik z wartościami bedzie użyty do porównania w głównym pliku symulacji (main.c)

#poprawki
#2. sprawdz is_horizontal bo chyba jest tam zły warunek -- done

#3. J1 i J2 chyba pomyliłem oddziaływania powinienem zrobić zamiane # J1 -> J2 i J2 -> J1 -- done

#4. Periodic źle działa
    ## czesciowo zle dziala przypadki 12

# 5. wizualizacja: można wylosować losowy spin i wyswietlic jego sąsiadów

#6. źle obliczana jest magnetyzacja, weź popatrz "wyklad1.pdf" tam jest `smag` tak sie oblicza

#7. wyrysowanie temp dla kilku $\beta$ ? (jeszcze sie dopytam)

# 1. są dwie podsieci pion i poziom
# ze względu na zapis spinów w jednej tablicy [ poziom, pion, poziom, pion,... ]
# wymiar LxL naprawdę to (2L)xL żeby wymiar sie zgadzał
L = 3
total_cells = 2*L*L

print(f"Generating {2 ** (2 * L * L) } configurations")

# UWAGA DLA JAKICH WARTOŚĆ L JEST UZYWANA LINIA
#  to stosować dla L = 4 w innym przypadku będzie problem z pamięcią (program crashuje)
#  dla tego przypadku należy zakomentować kod z rysowaniem matplotlib komentarz ### VISUALIZATION do ### END_VISUALIZATION

# all_configs = product([-1, 1], repeat=total_cells) # przeczytac powyzszy komentarz

all_configs = list(product([-1, 1], repeat=total_cells)) # to można stosować dla L = 3 i można rysować z kodem


def get_spin(config, x, y):
    x = x % (2 * L)
    y = y % L
    return config[y * (2 * L) + x]

# jako argument należy wstawiać indeks w postaci: i +- 2 * L
def periodic_y(i):
  return i % (2 * L * L)

# jako argument należy wstawiać indeks w postaci: i +- 2 * L
def periodic_x(i):
  return (i // (2 * L)) * (2 * L) + (i % (2 * L))


def calculate_energy(config, J1, J2):
    E = 0

    for i in range(2*L*L):
      if i % 2 == 0:
        x = i % (2*L)
        y = i // L

        spin = get_spin(config, x, y)
        left = get_spin(config, periodic_x(x - 2*L), y)
        right = get_spin(config, periodic_x(x + 2*L), y)

        E -= J2 * spin * left
        E -= J2 * spin * right
        # print(x,y)
        up_left = get_spin(config, periodic_x(x - 2*L), periodic_y(y - 2 * L))
        up_right = get_spin(config, periodic_x(x + 2*L), periodic_y(y - 2 * L))
        down_left = get_spin(config, periodic_x(x - 2*L), periodic_y(y + 2 * L))
        down_right = get_spin(config, periodic_x(x + 2*L), periodic_y(y + 2 * L))

        E -= J1  * spin * up_left
        E -= J1 * spin * up_right
        E -= J1 * spin * down_left
        E -= J1 * spin * down_right
      else:
        x = i % (2*L)
        y = i // L

        spin = get_spin(config, x, y)
        up = get_spin(config, x, periodic_y(y - 2 * L))
        down = get_spin(config, x, periodic_y(y + 2 * L))
        E -= J2 * spin * up
        E -= J2 * spin * down

        left_up = get_spin(config, periodic_x(x - 2 * L), periodic_y(y - 2 * L))
        right_up = get_spin(config, periodic_x(x + 2 * L), periodic_y(y - 2 * L))
        left_down = get_spin(config, periodic_x(x - 2 * L), periodic_y(y + 2 * L))
        right_down = get_spin(config, periodic_x(x + 2 * L), periodic_y(y + 2 * L))

        E -= J1 * spin * left_up
        E -= J1 * spin * right_up
        E -= J1 * spin * left_down
        E -= J1 * spin * right_down

    return E / 2 # bo oddziaływania spinow np. 1 - 2, 2 - 1 sa liczone dwa razy

# def calculate_energy(config, J1, J2):
#     E = 0
#     for y in range(L):
#         for x in range(L):
#             spin = get_spin(config, x, y)
#             is_horizontal = (x + y) % 2 == 0

#             if is_horizontal:
#                 left = get_spin(config, periodic_x(x - 2), y)
#                 right = get_spin(config, periodic_x(x + 2), y)
#                 E -= J2 * spin * left
#                 E -= J2 * spin * right

#                 up_left = get_spin(config, periodic_x(x - 2), periodic_y(y - 2))
#                 up_right = get_spin(config, periodic_x(x + 2), periodic_y(y - 2))
#                 down_left = get_spin(config, periodic_x(x - 2), periodic_y(y + 2))
#                 down_right = get_spin(config, periodic_x(x + 2), periodic_y(y + 2))

#                 E -= J1  * spin * up_left
#                 E -= J1 * spin * up_right
#                 E -= J1 * spin * down_left
#                 E -= J1 * spin * down_right
#             else:
#                 up = get_spin(config, x, periodic_y(y - 2))
#                 down = get_spin(config, x, periodic_y(y + 2))
#                 E -= J2 * spin * up
#                 E -= J2 * spin * down

#                 left_up = get_spin(config, periodic_x(x - 2), periodic_y(y - 2))
#                 right_up = get_spin(config, periodic_x(x + 2), periodic_y(y - 2))
#                 left_down = get_spin(config, periodic_x(x - 2), periodic_y(y + 2))
#                 right_down = get_spin(config, periodic_x(x + 2), periodic_y(y + 2))

#                 E -= J1 * spin * left_up
#                 E -= J1 * spin * right_up
#                 E -= J1 * spin * left_down
#                 E -= J1 * spin * right_down

#     return E / 2 # bo oddziaływania spinow np. 1 - 2, 2 - 1 sa liczone dwa razy

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
beta = 3.0

smag_y = 0
smag_x = 0
Z = 0

for config in all_configs:
    E = calculate_energy(config, J1, J2)
    mx, my = calculate_magnetization(config)
    weight = np.exp(-beta * E)

    smag_x += weight * abs(mx)
    smag_y += weight * abs(my)
    Z += weight
    # M_abs = np.sqrt(mx**2 + my**2) # jako dlugosc wektora
    data.append((config, E, mx, my, weight))

mx_abs = smag_x / (2*L*Z)
my_abs = smag_y / (L*Z)

Z = sum(weight for _, _, _, _, weight in data)

# zapisywanie wartosci do pliku
with open("config_data.txt", "w") as f:
    f.write("config E mx my weight Z\n")
    for config, E, mx, my, weight in data:
        config_str = " ".join(map(str, config))
        f.write(f"{config_str} {E:.3f} {mx} {my} {weight:.6e} {Z:.6e}\n")

# # srednie wartosci
# avg_mx = sum(mx * w for _, _, mx, _, w in data) / Z
# avg_my = sum(my * w for _, _, _, my, w in data) / Z

# print("Funkcja podziału Z:", Z)
# print("Średnia magnetyzacja:", avg_mx, avg_my)

####--------------------------------------------------------------
### VISUALIZATION
# print(all_configs[190_046]) # wektor konfiguracyjny

# cell_w = 100/L;
# cell_h = 200/L;

# target_config = all_configs[1156]
# print(len(target_config))

# vis_spin_x_start = []
# vis_spin_y_start = []
# vis_spin_x_finish = []
# vis_spin_y_finish = []

# # zapis położenia poszeczgolnych spinow
# for i in range(len(target_config)):
#   x = i % (2 * L)
#   y = i //(2 * L)

#   if i % 2 == 0:
#     if target_config[i] > 0:
#       vis_spin_x_start.append(x*cell_w)
#       vis_spin_x_finish.append(x*cell_w+ cell_w*0.8)
#       # print("prawo")
#     else:
#       vis_spin_x_start.append(x*cell_w+ cell_w*0.8)
#       vis_spin_x_finish.append(x*cell_w)
#       # print("lewo")

#     vis_spin_y_start.append(y* cell_h + cell_h/2)
#     vis_spin_y_finish.append(y* cell_h + cell_h/2)

#   else:
#     vis_spin_x_start.append(x*cell_w + cell_w/2)
#     vis_spin_x_finish.append(x*cell_w + cell_w/2)

#     if target_config[i] > 0:
#       vis_spin_y_start.append(y* cell_h)
#       vis_spin_y_finish.append(y* cell_h+ cell_h*0.5 - 10)
#       # print("gora")
#     else:
#       vis_spin_y_start.append(y* cell_h+ cell_h*0.5 - 10)
#       vis_spin_y_finish.append(y* cell_h)
#       # print("dol")

# plt.figure(figsize=(6, 10))

# for x_start, y_start, x_finish, y_finish in zip(vis_spin_x_start, vis_spin_y_start, vis_spin_x_finish, vis_spin_y_finish):
#     plt.arrow(x_start, y_start, x_finish - x_start, y_finish - y_start, head_width=1.5, head_length=1, fc='black', ec='black')

# # plt.xlim(-1, 4)
# plt.ylim(-20, 200)
# plt.title('Wizualizacja konfiguracji')
# plt.xlabel('X')
# plt.ylabel('Y')

# # Set equal aspect ratio
# # plt.axis('equal')

# plt.grid()
# plt.show()
 ### END_VISUALIZATION