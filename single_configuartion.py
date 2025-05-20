import numpy as np
# import matplotlib.pyplot as plt

# włączenie print() informacji o węzłach
J1_DEBUG = False
J2_DEBUG = False

# wymiar siatki
Ly = 3
Lx = Ly*2

configuration = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

# rysowanie configuracji
def draw_configuartion(config):
  for spin_index in range(len(config)):
    x = spin_index % Lx
    y = spin_index // Lx
    print(f"{config[spin_index]}({x},{y})[{spin_index}] ",end="")
    if x == Lx-1: print('\n')

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


def calculate_magnetization(config):
    mx, my = 0, 0

    for i in range(len(config)):
      spin = config[i]

      if i % 2 == 0:
        mx += spin
      else:
        my += spin

    return mx, my

def calculateEnergy(config, J2=0.0, J1 = 0.0):
  E = 0

  for spinIndex in range(len(config)):
    # sprawdzam czy spin jest poziomy czy pionowy
    if not spinIndex % 2 == 0:
      # pionowy
      spin = config[spinIndex]
      x = spinIndex % Lx
      y = spinIndex // Lx
      upperSpinIndex = coord_to_index(x, periodic_y(y,2))
      upperSpin = config[upperSpinIndex]
      bottomSpinIndex = coord_to_index(x, periodic_y(y,-2))
      bottomSpin = config[bottomSpinIndex]

      E -= J2 * spin * upperSpin
      E -= J2 * spin * bottomSpin

      if J2_DEBUG:
        ##pojedynczy przypadek dla oddziaływania J2
        print("------")
        print(f" J2 spin pionowy {spinIndex}({x},{y}), sąsiedzi góra {upperSpinIndex}, dół {bottomSpinIndex} --> {coord_to_index(x,y)}")
        #Energia tutaj będzie razy 2  przez powtarzalne odziaływania
        print(f" E = {E} ---->> {J2 * spin * upperSpin} i {spin * bottomSpin}")


      upperLeftSpinIndex = coord_to_index(periodic_x(x,-2), periodic_y(y,2))
      upperLeftSpin = config[upperLeftSpinIndex]
      bottomLeftSpinIndex = coord_to_index(periodic_x(x,-2), periodic_y(y,-2))
      bottomLeftSpin = config[bottomLeftSpinIndex]
      upperRightSpinIndex = coord_to_index(periodic_x(x,2), periodic_y(y,2))
      upperRightSpin = config[upperRightSpinIndex]
      bottomRightSpinIndex = coord_to_index(periodic_x(x,2), periodic_y(y,-2))
      bottomRightSpin = config[bottomRightSpinIndex]

      E -= J1  * spin * upperLeftSpin
      E -= J1 * spin * bottomLeftSpin
      E -= J1 * spin * upperRightSpin
      E -= J1 * spin * bottomRightSpin

      if J1_DEBUG:
        ##pojedynczy przypadek dla oddziaływania J1
        print("------")
        print(f" J1 spin pionowy {spinIndex}({x},{y}), sąsiedzi góra-lewo {upperLeftSpinIndex}, dół-lewo {bottomLeftSpinIndex}, góra-prawo {upperRightSpinIndex}, dół-prawo {bottomRightSpinIndex}")
        #Energia tutaj będzie razy 2  przez powtarzalne odziaływania
        print(f" E = {E} ---->> {J1  * spin * upperLeftSpin} ; {J1 * spin * bottomLeftSpin} ; {J1 * spin * upperRightSpin}; {J1 * spin * bottomRightSpin}")


    else:
      # poziomy
      spin = config[spinIndex]
      x = spinIndex % Lx
      y = spinIndex // Lx
      rightSpinIndex = periodic_x_ByIndex(spinIndex, + 2)
      rightSpin = config[rightSpinIndex]
      leftSpinIndex = periodic_x_ByIndex(spinIndex, - 2)
      leftSpin = config[leftSpinIndex]

      E -= J2 * spin * rightSpin
      E -= J2 * spin * leftSpin

      if J2_DEBUG:
        ##pojedynczy przypadek dla oddziaływania J2
        print("------")
        print(f" J2 spin poziomy {spinIndex}({x},{y}), sąsiedzi prawo {rightSpinIndex}, lewo {leftSpinIndex}  --> {coord_to_index(x,y)}")
        #Energia tutaj będzie *2 przez powtarzalne odziaływania
        print(f" E = {E} ---->> {J2 * spin * rightSpin} i {spin * leftSpin}")


      upperLeftSpinIndex = coord_to_index(periodic_x(x,-2), periodic_y(y,2))
      upperLeftSpin = config[upperLeftSpinIndex]
      bottomLeftSpinIndex = coord_to_index(periodic_x(x,-2), periodic_y(y,-2))
      bottomLeftSpin = config[bottomLeftSpinIndex]
      upperRightSpinIndex = coord_to_index(periodic_x(x,2), periodic_y(y,2))
      upperRightSpin = config[upperRightSpinIndex]
      bottomRightSpinIndex = coord_to_index(periodic_x(x,2), periodic_y(y,-2))
      bottomRightSpin = config[bottomRightSpinIndex]

      E -= J1  * spin * upperLeftSpin
      E -= J1 * spin * bottomLeftSpin
      E -= J1 * spin * upperRightSpin
      E -= J1 * spin * bottomRightSpin

      if J1_DEBUG:
        ##pojedynczy przypadek dla oddziaływania J1
        print("------")
        print(f" J1 spin pionowy {spinIndex}({x},{y}), sąsiedzi góra-lewo {upperLeftSpinIndex}, dół-lewo {bottomLeftSpinIndex}, góra-prawo {upperRightSpinIndex}, dół-prawo {bottomRightSpinIndex}")
        #Energia tutaj będzie razy 2  przez powtarzalne odziaływania
        print(f" E = {E} ---->> {J1  * spin * upperLeftSpin} ; {J1 * spin * bottomLeftSpin} ; {J1 * spin * upperRightSpin}; {J1 * spin * bottomRightSpin}")


  return E/2


draw_configuartion(configuration)

# pierwsze to pozycja x lub y (w zaleznosci od funkci),
# potem to liczba kierunku sąsiada czyli jeśli i = 0 i chce sprawdzić i-2, to podaje w tym argumencie -2
# sprawdzam periodycznych sąsiadów
# print(periodic_x(0,-2))
# print(periodic_x(4,2))

# # tutaj potencjalnie trzeba zmienić interpretacja +2 -2
# print("przypadki y")
# print(periodic_y(0,-2)) # -> 13
# print(coord_to_index(1,periodic_y(0,-2)))
# print(coord_to_index(1,periodic_y(2,2))) # -> 1

J2 = 1.0 # krótsze
J1 = 0.0 # dłuższe
T = 0.1
beta = 1.0
E_calkowite = calculateEnergy(configuration, J2, J1)
mx, my = calculate_magnetization(configuration)
weight = np.exp(-beta * E_calkowite)
print(f"E_całkowite = {E_calkowite}")
print(f"M = ({mx},{my})")
print(f"waga = {weight}")
