import numpy as np
import matplotlib.pyplot as plt
from itertools import product

L = 3
Ly = L
Lx = 2*L
total_cells = 2*L*L

print(f"Generating {2 ** (2 * L * L) } configurations")

# UWAGA DLA JAKICH WARTOŚĆ L JEST UZYWANA LINIA
#  to stosować dla L = 4 w innym przypadku będzie problem z pamięcią (program crashuje)
#  dla tego przypadku należy zakomentować kod z rysowaniem matplotlib komentarz ### VISUALIZATION do ### END_VISUALIZATION

# all_configs = np.array(list(product([-1, 1], repeat=total_cells)), dtype=np.int8) # przeczytac powyzszy komentarz

all_configs = list(product([-1, 1], repeat=total_cells)) # to można stosować dla L = 3 i można rysować z kodem

# oblicz magnetyzacje RAZ!
precomputed_magnetization = []


def coord_to_index(x,y):
  return y * Lx + x

# def periodic_x_ByIndex(i):
#   return (i + Lx) % Lx # L=3, i-> 0-2: (-2 + 6) % 6 = 4 % 6 = 4
def periodic_x_ByIndex(i, shift):
    x = i % Lx
    y = i // Lx
    new_x = (x + shift + Lx) % Lx
    return coord_to_index(new_x, y)


def periodic_x(x,n): # by x coordinate
  if n > 0:
    return (x + 2) % Lx
  else:
    return (x - 2 + Lx) % Lx

def periodic_y(y,n): # by coordinate
  if n < 0:
    return (y + 2) % Ly
  else:
    return (y - 2 +Ly) % Ly

def calculate_energy(config, J1, J2):
  E = 0.0

  for spinIndex in range(total_cells):
    x = spinIndex % Lx
    y = spinIndex // Lx

    if spinIndex % 2 == 0:
      spin = config[spinIndex]

      if J2 != 0:
        left = config[periodic_x_ByIndex(spinIndex, -2)]
        right = config[periodic_x_ByIndex(spinIndex, 2)]
        E -= J2 * spin * left
        E -= J2 * spin * right

      # print(x,y)
      if J1 != 0:
        up_left = config[coord_to_index(periodic_x(x,-2), periodic_y(y,2))]
        up_right = config[coord_to_index(periodic_x(x,2), periodic_y(y,2))]
        down_left = config[coord_to_index(periodic_x(x,-2), periodic_y(y,-2))]
        down_right = config[coord_to_index(periodic_x(x,2), periodic_y(y,-2))]

        E -= J1 * spin * up_left
        E -= J1 * spin * up_right
        E -= J1 * spin * down_left
        E -= J1 * spin * down_right

    else:
      spin =  config[spinIndex]
      if J2 != 0:
        up = config[coord_to_index(x, periodic_y(y,2))]
        down = config[coord_to_index(x, periodic_y(y,-2))]

        E -= J2 * spin * up
        E -= J2 * spin * down

      if J1 != 0:
        left_up = config[coord_to_index(periodic_x(x,-2), periodic_y(y,2))]
        right_up = config[coord_to_index(periodic_x(x,2), periodic_y(y,2))]
        left_down = config[coord_to_index(periodic_x(x,-2), periodic_y(y,-2))]
        right_down = config[coord_to_index(periodic_x(x,2), periodic_y(y,-2))]

        E -= J1 * spin * left_up
        E -= J1 * spin * right_up
        E -= J1 * spin * left_down
        E -= J1 * spin * right_down

  return E / 2 # bo oddziaływania spinow np. 1 - 2, 2 - 1 sa liczone dwa razy

def calculate_magnetization(config):
  mx, my = 0, 0

  for i in range(len(config)):
    spin = config[i]
    if i % 2 == 0:
      mx += spin
    else:
      my += spin

  return mx, my

# OBLICZANIE MAGNETYZACJI
for config in all_configs:
    mx, my = calculate_magnetization(config)
    precomputed_magnetization.append((config, abs(mx), abs(my)))


# Zakres temperatur
T_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 3.5, 4, 4.5, 5]

# Funkcja do liczenia M(T)
def compute_MT(J1, J2, filename):
    computation_results = []

    # with open(filename, "w") as f:
    # f.write("T Mx My\n")
    for T in T_list:
        beta = 1.0 / T
        smag_x = 0.0
        smag_y = 0.0
        Z = 0.0

        # for config in all_configs:
        for config, mx_abs, my_abs in precomputed_magnetization:
          E = calculate_energy(config, J1, J2)
          # mx, my = calculate_magnetization(config)
          weight = np.exp(-beta * E)

          # smag_x += weight * abs(mx)
          # smag_y += weight * abs(my)
          smag_x += weight * mx_abs
          smag_y += weight * my_abs
          Z += weight

        mx_avg = smag_x / (Z * (L * L))
        my_avg = smag_y / (Z * (L * L))

        computation_results.append((T, mx_avg, my_avg))

        print(T,smag_x, mx_avg) 
        
    np.savetxt(filename, computation_results, header="T Mx My", comments="")
            # f.write(f"{T} {mx_avg:.6f} {my_avg:.6f}\n")

# Liczenie dla trzech przypadków

#należy się upewnić że podana ścieżka(foldery) filename jest stworzona
# compute_MT(J1=1.0, J2=0.0, filename="./MT_J1.txt")  # tylko J1
# compute_MT(J1=0.0, J2=1.0, filename="./MT_J2.txt")  # tylko J2

compute_MT(J1=1.0, J2=0.0, filename="./wyniki/1/J1/MT_J1.txt")  # tylko J1
compute_MT(J1=0.0, J2=1.0, filename="./wyniki/1/J2/MT_J2.txt")  # tylko J2
# compute_MT(J1=0.3, J2=0.0, filename="./wyniki/0.3/J1/MT_J1.txt")  # tylko J1
# compute_MT(J1=1.7, J2=0.0, filename="./wyniki/0.7/J1/MT_J1.txt")  # tylko J1
# compute_MT(J1=1.4, J2=0.0, filename="./wyniki/1.4/J1/MT_J1.txt")  # tylko J1
# compute_MT(J1=1.8, J2=0.0, filename="./wyniki/1.8/J1/MT_J1.txt")  # tylko J1

# compute_MT(J1=0.0, J2=0.3, filename="./wyniki/0.3/J2/MT_J2.txt")  # tylko J2
# compute_MT(J1=0.0, J2=0.7, filename="./wyniki/0.7/J2/MT_J2.txt")  # tylko J2
# compute_MT(J1=0.0, J2=1.4, filename="./wyniki/1.4/J2/MT_J2.txt")  # tylko J2
# compute_MT(J1=0.0, J2=1.8, filename="./wyniki/1.8/J2/MT_J2.txt")  # tylko J2

# compute_MT(J1=1.0, J2=1.0, filename="MT_J1J2.txt")  # oba razem
# compute_MT(J1=0.5, J2=1.0, filename="./wyniki/J1J2/MT_J1J2_05_1.txt")  # tylko J2
# compute_MT(J1=1.0, J2=0.5, filename="./wyniki/J1J2/MT_J1J2_1_05.txt")  # tylko J2
# compute_MT(J1=0.7, J2=1.4, filename="./wyniki/J1J2/MT_J1J2_07_14.txt")  # tylko J2


# kod zapisujący do pliku nastepujące dane: "config E mx my weight Z"
# data = []
# J1 = 0.0
# J2 = 1.0
# beta = 1.0

# smag_y = 0
# smag_x = 0
# Z = 0

# for config in all_configs:
#   E = calculate_energy(config, J1, J2)
#   mx, my = calculate_magnetization(config)
#   weight = np.exp(-beta * E)

#   smag_x += weight * abs(mx)
#   smag_y += weight * abs(my)
#   Z += weight
#   # M_abs = np.sqrt(mx**2 + my**2) # jako dlugosc wektora
#   data.append((config, E, mx, my, weight))

# mx_abs = smag_x / (2*L*Z)
# my_abs = smag_y / (L*Z)

# Z = sum(weight for _, _, _, _, weight in data)

# # zapisywanie wartosci do pliku
# with open("config_data.txt", "w") as f:
#     f.write("config E mx my weight Z\n")
#     for config, E, mx, my, weight in data:
#         config_str = " ".join(map(str, config))
#         f.write(f"[{config_str}] {E:.3f} {mx} {my} {weight:.6e} {Z:.6e}\n")

# # srednie wartosci
# avg_mx = sum(mx * w for _, _, mx, _, w in data) / Z
# avg_my = sum(my * w for _, _, _, my, w in data) / Z

# print("Funkcja podziału Z:", Z)
# print("Średnia magnetyzacja:", avg_mx, avg_my)

####--------------------------------------------------------------
### VISUALIZATION - rozmieszczenie wektorów na siatce
# print(all_configs[0]) # wektor konfiguracyjny

# cell_w = 100/L;
# cell_h = 200/L;

# target_config = all_configs[0]
# # print(len(target_config))

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