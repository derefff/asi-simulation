import numpy as np
# import matplotlib.pyplot as plt

# włączenie print() informacji o węzłach
J1_DEBUG = True
J2_DEBUG = True

J1_SUM_DEBUG = False
J2_SUM_DEBUG = False
# wymiar siatki (L=2 to 2 * 2 * 2)
Ly = 3
Lx = Ly*2

# configuration = [-1, -1, -1, -1, -1, -1, -1, -1]


configuration = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
# configuration = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

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
#
def periodic_x(x, n):
    return (x + n + Lx) % Lx

def periodic_y(y, n):
    return (y + n + Ly) % Ly


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
      upperSpinIndex = coord_to_index(x, periodic_y(y,1))
      upperSpin = config[upperSpinIndex]
      bottomSpinIndex = coord_to_index(x, periodic_y(y,-1))
      bottomSpin = config[bottomSpinIndex]

      E -= J2 * spin * upperSpin
      E -= J2 * spin * bottomSpin

      if J2_DEBUG:
        ##pojedynczy przypadek dla oddziaływania J2
        print("------")
        print(f" J2 spin pionowy {spinIndex}({x},{y}), sąsiedzi góra {upperSpinIndex}, dół {bottomSpinIndex} --> {coord_to_index(x,y)}")
        #Energia tutaj będzie razy 2  przez powtarzalne odziaływania
        print(f" E = {E} ---->> {J2 * spin * upperSpin} i {spin * bottomSpin}")


      upperLeftSpinIndex = coord_to_index(periodic_x(x,-1), periodic_y(y,0))
      upperLeftSpin = config[upperLeftSpinIndex]
      bottomLeftSpinIndex = coord_to_index(periodic_x(x,-1), periodic_y(y,-1))
      bottomLeftSpin = config[bottomLeftSpinIndex]
      upperRightSpinIndex = coord_to_index(periodic_x(x,1), periodic_y(y, 0))
      upperRightSpin = config[upperRightSpinIndex]
      bottomRightSpinIndex = coord_to_index(periodic_x(x,1), periodic_y(y,-1))
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

      upperLeftSpinIndex = coord_to_index(periodic_x(x, -1), periodic_y(y,0))
      upperLeftSpin = config[upperLeftSpinIndex]
      bottomLeftSpinIndex = coord_to_index(periodic_x(x,-1), periodic_y(y,-1))
      bottomLeftSpin = config[bottomLeftSpinIndex]
      upperRightSpinIndex = coord_to_index(periodic_x(x,1), periodic_y(y,0))
      upperRightSpin = config[upperRightSpinIndex]
      bottomRightSpinIndex = coord_to_index(periodic_x(x,1), periodic_y(y,-1))
      bottomRightSpin = config[bottomRightSpinIndex]

      E -= J1  * spin * upperLeftSpin
      E -= J1 * spin * bottomLeftSpin
      E -= J1 * spin * upperRightSpin
      E -= J1 * spin * bottomRightSpin

      if J1_DEBUG:
        ##pojedynczy przypadek dla oddziaływania J1
        print("------")
        print(f" J1 spin poziomy {spinIndex}({x},{y}), sąsiedzi góra-lewo {upperLeftSpinIndex}, dół-lewo {bottomLeftSpinIndex}, góra-prawo {upperRightSpinIndex}, dół-prawo {bottomRightSpinIndex}")
        #Energia tutaj będzie razy 2  przez powtarzalne odziaływania
        print(f" E = {E} ---->> {J1  * spin * upperLeftSpin} ; {J1 * spin * bottomLeftSpin} ; {J1 * spin * upperRightSpin}; {J1 * spin * bottomRightSpin}")
        print(coord_to_index(periodic_x(x,-2), periodic_y(y,2)),periodic_x(x,-2), periodic_y(y,2) )



  return E/2

def count_interactions_J1_J2(config):
    J1_sum = 0
    J2_sum = 0
    J1_pos = 0
    J1_neg = 0
    J2_pos = 0
    J2_neg = 0

    for spinIndex in range(len(config)):
        spin = config[spinIndex]
        x = spinIndex % Lx
        y = spinIndex // Lx

        if spinIndex % 2 == 0:
            # poziomy
            left = config[periodic_x_ByIndex(spinIndex, -2)]
            right = config[periodic_x_ByIndex(spinIndex, 2)]
            for neighbor in [left, right]:
                interaction = spin * neighbor
                J2_sum += interaction
                if interaction > 0:
                    J2_pos += 1
                else:
                    J2_neg += 1

            # J1 – sąsiedzi
            neighbors = [
                config[coord_to_index(periodic_x(x, -1), periodic_y(y, 0))],
                config[coord_to_index(periodic_x(x, -1), periodic_y(y, -1))],
                config[coord_to_index(periodic_x(x, 1), periodic_y(y, 0))],
                config[coord_to_index(periodic_x(x, 1), periodic_y(y, -1))]
            ]
        else:
            # pionowy
            up = config[coord_to_index(x, periodic_y(y, 1))]
            down = config[coord_to_index(x, periodic_y(y, -1))]
            for neighbor in [up, down]:
                interaction = spin * neighbor
                J2_sum += interaction
                if interaction > 0:
                    J2_pos += 1
                else:
                    J2_neg += 1

            # J1 – sąsiedzi
            neighbors = [
                config[coord_to_index(periodic_x(x, -1), periodic_y(y, 0))],
                config[coord_to_index(periodic_x(x, -1), periodic_y(y, -1))],
                config[coord_to_index(periodic_x(x, 1), periodic_y(y, 0))],
                config[coord_to_index(periodic_x(x, 1), periodic_y(y, -1))]
            ]

        for neighbor in neighbors:
            interaction = spin * neighbor
            J1_sum += interaction
            if interaction > 0:
                J1_pos += 1
            else:
                J1_neg += 1

    # dzieloine przez 2,każda para była liczona dwukrotnie
    J1_sum //= 2
    J2_sum //= 2
    J1_pos //= 2
    J1_neg //= 2
    J2_pos //= 2
    J2_neg //= 2

    return {
        'J1_sum': J1_sum, 'J2_sum': J2_sum,
        'J1_positive': J1_pos, 'J1_negative': J1_neg,
        'J2_positive': J2_pos, 'J2_negative': J2_neg,
    }

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

      if spin == upperSpin:
        J2_sum -= 1

      if not spin == upperSpin:
        J2_sum += 1

      if J2_SUM_DEBUG:
        ##pojedynczy przypadek dla oddziaływania J2
        print("no tak")


      upperLeftSpinIndex = coord_to_index(periodic_x(x,-1), periodic_y(y,0))
      upperLeftSpin = config[upperLeftSpinIndex]
      upperRightSpinIndex = coord_to_index(periodic_x(x,1), periodic_y(y, 0))
      upperRightSpin = config[upperRightSpinIndex]

      if spin == upperLeftSpin:
        J1_sum -= 1

      if not spin == upperLeftSpin:
        J1_sum += 1

      if spin == upperRightSpin:
        J1_sum -= 1

      if not spin == upperRightSpin:
        J1_sum += 1

      if J1_SUM_DEBUG:
        ##pojedynczy przypadek dla oddziaływania J1
        print("------")

    else:
      # poziomy
      spin = config[spinIndex]
      x = spinIndex % Lx
      y = spinIndex // Lx
      rightSpinIndex = periodic_x_ByIndex(spinIndex, + 2)
      rightSpin = config[rightSpinIndex]

      if spin == rightSpin:
        J2_sum -= 1

      if not spin == rightSpin:
        J2_sum += 1


      if J2_SUM_DEBUG:
        ##pojedynczy przypadek dla oddziaływania J2
        print("------")

      upperLeftSpinIndex = coord_to_index(periodic_x(x, -1), periodic_y(y,0))
      upperLeftSpin = config[upperLeftSpinIndex]

      upperRightSpinIndex = coord_to_index(periodic_x(x,1), periodic_y(y,0))
      upperRightSpin = config[upperRightSpinIndex]


      if spin == upperLeftSpin:
        J1_sum -= 1

      if not spin == upperLeftSpin:
        J1_sum += 1

      if spin == upperRightSpin:
        J1_sum -= 1

      if not spin == upperRightSpin:
        J1_sum += 1


      if J1_DEBUG:
        ##pojedynczy przypadek dla oddziaływania J1
        print("------")

  print(f" J2 -> {J2_sum}, J1 -> {J1_sum}")



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

count_interactions(configuration)

# interaction_data = count_interactions_J1_J2(configuration)
# print("\n=== Interakcje spinów ===")
# print(f"Suma J1: {interaction_data['J1_sum']}, (+): {interaction_data['J1_positive']}, (−): {interaction_data['J1_negative']}")
# print(f"Suma J2: {interaction_data['J2_sum']}, (+): {interaction_data['J2_positive']}, (−): {interaction_data['J2_negative']}")
