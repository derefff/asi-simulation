import numpy as np
import matplotlib.pyplot as plt
from itertools import product

L = 2
Ly = L
Lx = 2*L
total_cells = 2*L*L

print(f"Generating {2 ** (2 * L * L) } configurations")

# UWAGA DLA JAKICH WARTOŚĆ L JEST UZYWANA LINIA
#  to stosować dla L = 4 w innym przypadku będzie problem z pamięcią (program crashuje)
#  dla tego przypadku należy zakomentować kod z rysowaniem matplotlib komentarz ### VISUALIZATION do ### END_VISUALIZATION

# all_configs = np.array(list(product([-1, 1], repeat=total_cells)), dtype=np.int8) # przeczytac powyzszy komentarz

all_configs = list(product([-1, 1], repeat=total_cells)) # to można stosować dla L = 3 i można rysować z kodem
len_configs = len(all_configs)

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


# def periodic_x(x,n): # by x coordinate
#   if n > 0:
#     return (x + 2) % Lx
#   else:
#     return (x - 2 + Lx) % Lx

# def periodic_y(y,n): # by coordinate
#   if n < 0:
#     return (y + 2) % Ly
#   else:
#     return (y - 2 +Ly) % Ly

def periodic_x(x, n):
    return (x + n + Lx) % Lx

def periodic_y(y, n):
    return (y + n + Ly) % Ly

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
        up_left = config[coord_to_index(periodic_x(x,-1), periodic_y(y,0))]
        up_right = config[coord_to_index(periodic_x(x,1), periodic_y(y,0))]
        down_left = config[coord_to_index(periodic_x(x,-1), periodic_y(y,-1))]
        down_right = config[coord_to_index(periodic_x(x,1), periodic_y(y,-1))]

        E -= J1 * spin * up_left
        E -= J1 * spin * up_right
        E -= J1 * spin * down_left
        E -= J1 * spin * down_right

    else:
      spin =  config[spinIndex]
      if J2 != 0:
        up = config[coord_to_index(x, periodic_y(y,1))]
        down = config[coord_to_index(x, periodic_y(y,-1))]

        E -= J2 * spin * up
        E -= J2 * spin * down

      if J1 != 0:
        left_up = config[coord_to_index(periodic_x(x,-1), periodic_y(y,0))]
        right_up = config[coord_to_index(periodic_x(x,1), periodic_y(y,0))]
        left_down = config[coord_to_index(periodic_x(x,-1), periodic_y(y,-1))]
        right_down = config[coord_to_index(periodic_x(x,1), periodic_y(y,-1))]

        E -= J1 * spin * left_up
        E -= J1 * spin * right_up
        E -= J1 * spin * left_down
        E -= J1 * spin * right_down

  return E / 2 # bo oddziaływania spinow np. 1 - 2, 2 - 1 sa liczone dwa razy

def count_interactions(config):
  J2_sum  = 0
  J1_sum  = 0

  for spinIndex in range(len(config)):
    # sprawdzam czy spin jest poziomy czy pionowy
    if not spinIndex % 2 == 0:
      # pionowy
      spin = config[spinIndex]
      x = spinIndex % Lx
      y = spinIndex // Lx
      upperSpinIndex = coord_to_index(x, periodic_y(y,1))
      upperSpin = config[upperSpinIndex]

      # if spin == upperSpin:
      J2_sum += spin * upperSpin

      # if not spin == upperSpin:
      #   J2_sum += spin * upperSpin


      upperLeftSpinIndex = coord_to_index(periodic_x(x,-1), periodic_y(y,0))
      upperLeftSpin = config[upperLeftSpinIndex]
      upperRightSpinIndex = coord_to_index(periodic_x(x,1), periodic_y(y, 0))
      upperRightSpin = config[upperRightSpinIndex]

      bottomLeftSpinIndex = coord_to_index(periodic_x(x,-1), periodic_y(y,-1))
      bottomLeftSpin = config[bottomLeftSpinIndex]
      bottomRightSpinIndex = coord_to_index(periodic_x(x,1), periodic_y(y,-1))
      bottomRightSpin = config[bottomRightSpinIndex]

      J1_sum += spin * upperLeftSpin * -1
      J1_sum += spin * upperRightSpin
      J1_sum += spin * bottomLeftSpin
      J1_sum += spin * bottomRightSpin * -1

    else:
      # poziomy
      spin = config[spinIndex]
      x = spinIndex % Lx
      y = spinIndex // Lx
      rightSpinIndex = periodic_x_ByIndex(spinIndex, + 2)
      rightSpin = config[rightSpinIndex]

      J2_sum += spin*rightSpin

  return J1_sum, J2_sum


def count_all_interactions():
  J1_sum_avg = 0
  J2_sum_avg = 0
  for config in all_configs:
    J1_sum, J2_sum = count_interactions(config)
    print(f" J1_sum -> {J1_sum}  J2_sum -> {J2_sum}")
    J1_sum_avg += J1_sum
    J2_sum_avg += J2_sum
    print(f" J1_sum_AVG -> {J1_sum_avg}  J2_sum_AVG -> {J2_sum_avg}")

  print("----------------")
  return (J1_sum_avg / len_configs ), (J2_sum_avg / len_configs)

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

        print(f" T:{T} smag_x: {smag_x}, mx_avg:{mx_avg}, my_avg: {my_avg}")

    np.savetxt(filename, computation_results, header="T Mx My", comments="")
            # f.write(f"{T} {mx_avg:.6f} {my_avg:.6f}\n")

# Liczenie dla trzech przypadków

#należy się upewnić że podana ścieżka(foldery) filename jest stworzona
print("\n J1 = 1")
compute_MT(J1=1.0, J2=0.0, filename="./MT_J1.txt")  # tylko J1

J1_sum_avg , J2_sum_avg = count_all_interactions()
print(f" J1 -> {J1_sum_avg},\t J2 -> {J2_sum_avg}")
# compute_MT(J1=1.0, J2=0.0, filename="./wyniki/1/J1/MT_J1.txt")  # tylko J1
print("\n J2 = 1")
# compute_MT(J1=0.0, J2=1.0, filename="./wyniki/1/J2/MT_J2.txt")  # tylko J2
compute_MT(J1=0.0, J2=1.0, filename="./MT_J2.txt")  # tylko J2
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