#include "utils/vector.h"
#include <fstream>
#include <iostream>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// Boltzman constant
// what's that? cpp shenanigans I see
// constexpr double Kb = 1.380649e-23;
constexpr double Kb = 1;

struct spin
{
  int id;
  // int x, y; // "position of spin" for now idk if neccesary
  //+1 or -1, if isVertical then +1 up and -1 down, if !isVertical +1 right, -1 left
  int value; // potentialy use here vector
  bool isVertical;
  // near neighbour like list
  int neighbourListIndex_J1[4];
  int neighbourListIndex_J2[2];
};

struct lattice
{
  int width;  // cells unit
  int height; // cells unit
  spin* spins;
};

spin* generate_spins(int L)
{
  // one-dimensional table
  spin* spins = (spin*)malloc(sizeof(spin) * (L * 2 * L));

  // int spin_id = 0;

  for (int i = 0; i < L * 2 * L; i++)
  {
    // define spin id
    // spins[i].id = spin_id;
    // spin_id++;
    // vertical-> i%2 = 1
    spins[i].isVertical = (i % 2 == 0) ? false : true;
    // assign spin random orientation (+1 or -1)
    spins[i].value = -1 + 2 * (rand() % 2);
  }

  // generate near neighbour list for each spin
  for (int j = 0; j < L * 2 * L; j++)
  {
    int row = j / (2 * L);      // y
    int column = (j % (2 * L)); // x

    if (spins[j].isVertical)
    {
      // vertical case
      // look for J1 interactions (above and below, periodic)
      spins[j].neighbourListIndex_J2[0] = ((row - 1 + L) % L) * (2 * L) + column;
      spins[j].neighbourListIndex_J2[1] = ((row + 1) % L) * (2 * L) + column;


      // look for J2 interactions (left and right, periodic)
      spins[j].neighbourListIndex_J1[0] = row * (2 * L) + (column - 2 + 2 * L) % (2 * L);
      spins[j].neighbourListIndex_J1[1] = row * (2 * L) + (column + 2) % (2 * L);
      spins[j].neighbourListIndex_J1[2] = ((row - 1 + L) % L) * (2 * L) + (column - 2 + 2 * L) % (2 * L);
      spins[j].neighbourListIndex_J1[3] = ((row + 1) % L) * (2 * L) + (column + 2) % (2 * L);

    }
    else
    {
      // horizontal case
      // look for J1 interactions (left and right, periodic)
      // spins[j].neighbourListIndex_J2[0] = (column <= 1) ? (row * (2 * L)) + (L - (2 - column)) : (j - 2);
      // spins[j].neighbourListIndex_J2[1] = (column >= L - 2) ? (row * L) + (column % 2) : (j + 2);
      spins[j].neighbourListIndex_J2[0] = row * (2 * L) + (column - 2 + 2 * L) % (2 * L);
      spins[j].neighbourListIndex_J2[1] = row * (2 * L) + (column + 2) % (2 * L);


      // look for J2 interactions (above and below, periodic)
      spins[j].neighbourListIndex_J1[0] = ((row - 1 + L) % L) * (2 * L) + (column - 1 + 2 * L) % (2 * L);
      spins[j].neighbourListIndex_J1[1] = ((row - 1 + L) % L) * (2 * L) + (column + 1) % (2 * L);
      spins[j].neighbourListIndex_J1[2] = ((row + 1) % L) * (2 * L) + (column - 1 + 2 * L) % (2 * L);
      spins[j].neighbourListIndex_J1[3] = ((row + 1) % L) * (2 * L) + (column + 1) % (2 * L);
    }

    // std::cout << row << "," << column << "\n"; // debug info
  }

  return spins;
}

lattice* create_lattice(int L)
{
  lattice* lat = (lattice*)malloc(sizeof(lattice));
  // Define board size (NxN)
  lat->width = 2 * L;
  lat->height = L;
  // Generate spins in a structured grid
  // Store spins in data structure
  lat->spins = generate_spins(L);
  return lat;
}

double compute_energy_difference(lattice* lat, int spin_index, double J1, double J2, double T)
{
  spin s = lat->spins[spin_index];
  // int sum_neighbors = 0;
  int sum_J1 = 0;
  int sum_J2 = 0;

  for (int i = 0; i < 4; i++)
    sum_J1 += lat->spins[s.neighbourListIndex_J1[i]].value;
  for (int i = 0; i < 2; i++)
    sum_J2 += lat->spins[s.neighbourListIndex_J2[i]].value;

  return 2 * s.value * (J1 * sum_J1 + J2 * sum_J2);
}

void glauber_step(lattice* lat, double J1, double J2, double T)
{
  int random_spin = rand() % (lat->width * lat->height - 1);

  double dE = compute_energy_difference(lat, random_spin, J1, J2, T);
  if (dE < 0 || exp(-dE / (Kb * T)) > ((double)rand() / RAND_MAX))
    lat->spins[random_spin].value *= -1;
}

physics::vector* compute_magnetization(lattice* lat)
{
  physics::vector* M = physics::create_vector(0.0, 0.0);

  int total_spin = 0;
  int num_spins = lat->width * lat->height;
  for (int i = 0; i < num_spins; i++)
  {
    if (lat->spins[i].isVertical)
      M->y += lat->spins[i].value;
    else
      M->x += lat->spins[i].value;
  }
  return M;
}

void simulate_MT(int L, double J1, double J2, const char* filename) {
  double T_list[] = {0.1, 0.5, 1.0, 1.4, 1.8, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0};
  int T_len = 11; // sizeof(T_list) / sizeof(T_list[0]);

  const int steps = 1'000'000;  // liczba kroków MC na T

  // otwieranie pliku do zapisu
  std::ofstream outfile(filename);
  if (!outfile) {
    std::cerr << "Error opening file: " << filename << std::endl;
    return;
  }

  outfile << "T\tMx\tMy\n";

  for (int t = 0; t < T_len; t++) {
    double T = T_list[t];

    // Twórz nową siątkę dla T
    lattice* board = create_lattice(L);

    double Mx_sum = 0.0;
    double My_sum = 0.0;

    for (int step = 0; step < steps; step++) {
      glauber_step(board, J1, J2, T);
      physics::vector* M = compute_magnetization(board);
      Mx_sum += fabs(M->x);
      My_sum += fabs(M->y);
    }

    double Mx_avg = Mx_sum / steps / ((float(board->width)/2) * board->height);
    double My_avg = My_sum / steps / ((float(board->width)/2) *  board->height);
    printf("%lf",((float(board->width)/2) *  board->height));

    outfile << T << '\t' << Mx_avg << '\t' << My_avg << '\n';

    free(board->spins);
    free(board);
  }

  outfile.close();
  std::cout << "zapisano MT do: " << filename << std::endl;
}



int main(int argc, char* argv[])
{
    const int L = 3;

    // Symulacje tylko dla J1
    simulate_MT(L, 0.3, 0.0, "./wyniki/0.3/J1/SYM_MT_J1_0.3.txt");
    simulate_MT(L, 0.7, 0.0, "./wyniki/0.7/J1/SYM_MT_J1_0.7.txt");
    simulate_MT(L, 1.0, 0.0, "./wyniki/1/J1/SYM_MT_J1_1.txt");
    simulate_MT(L, 1.4, 0.0, "./wyniki/1.4/J1/SYM_MT_J1_1.4.txt");
    simulate_MT(L, 1.8, 0.0, "./wyniki/1.8/J1/SYM_MT_J1_1.8.txt");

    // Symulacje tylko dla J2
    simulate_MT(L, 0.0, 0.3, "./wyniki/0.3/J2/SYM_MT_J2_0.3.txt");
    simulate_MT(L, 0.0, 0.7, "./wyniki/0.7/J2/SYM_MT_J2_0.7.txt");
    simulate_MT(L, 0.0, 1.0, "./wyniki/1/J2/SYM_MT_J2_1.txt");
    simulate_MT(L, 0.0, 1.4, "./wyniki/1.4/J2/SYM_MT_J2_1.4.txt");
    simulate_MT(L, 0.0, 1.8, "./wyniki/1.8/J2/SYM_MT_J2_1.8.txt");

    // simulate_MT(L, 0.5, 1.0, "./wyniki/J1J2/SYM_MT_J1J2_05_1.txt");
    // simulate_MT(L, 1.0, 0.5, "./wyniki/J1J2/SYM_MT_J1J2_1_05.txt");
    // simulate_MT(L, 1.0, 1.0, "./wyniki/J1J2/SYM_MT_J1J2_1_1.txt");
    // simulate_MT(L, 0.7, 1.4, "./wyniki/J1J2/SYM_MT_J1J2_07_14.txt");


  // const int L = 50;
  // const double J1 = 1.0;
  // const double J2 = 1.0;
  // const double T = 1.8;

  // // external field B(x,y)
  // physics::vector* B = physics::create_vector(0.0, 0.0);
  // // physics::vector* M = physics::create_vector(0.0, 0.0);

  // lattice* board = create_lattice(L);

  // std::ofstream outfile("magnetization_data.txt");
  // if (!outfile)
  // {
  //   std::cerr << "Error opening file!" << std::endl;
  //   return 1;
  // }

  // for (int step = 0; step < 10'000; step++)
  // {
  //   glauber_step(board, J1, J2, T);

  //   // Total Magnetization
  //   physics::vector* magnetization = compute_magnetization(board);
  //   outfile << step << '\t' << magnetization->x << '\t' << magnetization->y << '\n';
  // }

  // outfile.close();
  // std::cout << "Magnetization data saved to magnetization_data.txt" << std::endl;
  //

  return 0;
}

// policzyc osobno magnetyzacje spinow na x i y
// wprowadz bx i by/ sprawdz oddzialkywanie
//
// inny program: znajdz przypadek testowy
// dla sieci L = 4
// znajdz wszystkie konfiguracje 2^16 -> 65000
// wyrysuje je z rozkladu boltzmana
//
// //waga z rozkladu boltmzana -> prawdopodobienstwo mikrostanu
// zastanowic sie co robia oddzialywania (samo j1 lub sammo j2) -> jeden z podrozdzialow

// 1. Create simulation board
// a) Define board size (NxN)
// b) Generate spins in a structured grid
// c) Store spins in data structure

// 2. Initialize spins
// a) Assign each spin a random orientation (+1 or -1)
// b) Optionally: Implement different initial states (random, ordered, etc.)
// 2.1. Make neighbor list
// a) Identify nearest neighbors (J1 interactions)
// b) Identify next-nearest neighbors (J2 interactions)
// c) Store neighbor relationships efficiently (e.g., adjacency list, array indices)

// 4. Simulation loop
// a) Pick a random spin
// b) Compute energy difference ΔE using Glauber algorithm
// c) Decide whether to flip the spin (using probability function)
// d) Repeat for a fixed number of Monte Carlo steps

// 5. Data collection & analysis
// a) Measure total system energy at intervals
// b) Track monopole density / correlation functions
// c) Store results in a file for plotting

// 6. Visualization (optional)
// a) Output the spin configurations at different time steps
// b) Generate heatmaps / graphs of magnetization / energy

// 7. Finalize simulation
// a) Save the final state
// b) Close files / free memory
