#include <iostream>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>

// Boltzman constant
// what's that? cpp shenanigans I see
constexpr double Kb = 1.380649e-23;

struct spin
{
  int id;
  int x, y; // "position of spin" for now idk if neccesary
  //+1 or -1, if isVertical then +1 up and -1 down, if !isVertical +1 right, -1 left
  int value;
  bool isVertical;
  // near neighbour like list
  int neighbourListIndex_J1[2];
  int neighbourListIndex_J2[4];
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
  spin* spins = (spin*)malloc(sizeof(spin) * (L * L));

  // int spin_id = 0;

  for (int i = 0; i < L * L; i++)
  {
    // define spin id
    // spins[i].id = spin_id;
    // vertical-> i%2 = 1
    spins[i].isVertical = (i % 2 == 0) ? false : true;
    // assign spin random orientation (+1 or -1)
    spins[i].value = -1 + 2 * (rand() % 2);

    // spin_id++;
  }

  // generate near neighbour list for each spin
  for (int j = 0; j < L * L; j++)
  {
    int row = j / L;      // y
    int column = (j % L); // x

    if (spins[j].isVertical)
    {
      // vertical case
      // look for J1 interactions (above and below, periodic)
      spins[j].neighbourListIndex_J1[0] = (row == 0) ? (L * (L - 1) + column) : (j - L);
      spins[j].neighbourListIndex_J1[1] = (row == L - 1) ? column : (j + L);

      // look for J2 interactions (left and right, periodic)
      spins[j].neighbourListIndex_J2[0] = (column == 0) ? (j + (L - 1)) : (j - 1);
      spins[j].neighbourListIndex_J2[1] = (column == L - 1) ? (j - (L - 1)) : (j + 1);
      spins[j].neighbourListIndex_J2[2] = spins[j].neighbourListIndex_J2[0] + L;
      spins[j].neighbourListIndex_J2[3] = spins[j].neighbourListIndex_J2[1] + L;
    }
    else
    {
      // horizontal case
      // look for J1 interactions (left and right, periodic)
      spins[j].neighbourListIndex_J1[0] = (column <= 1) ? (row * L) + (L - (2 - column)) : (j - 2);
      spins[j].neighbourListIndex_J1[1] = (column >= L - 2) ? (row * L) + (column % 2) : (j + 2);

      // look for J2 interactions (above and below, periodic)
      spins[j].neighbourListIndex_J2[0] = (row == 0) ? (L * (L - 1) + column + 1) : (j - L + 1);
      spins[j].neighbourListIndex_J2[1] = (row == 0) ? (L * (L - 1) + column - 1) : (j - L - 1);
      spins[j].neighbourListIndex_J2[2] = (row == L - 1) ? (column + 1) : (j + L + 1);
      spins[j].neighbourListIndex_J2[3] = (row == L - 1) ? (column - 1) : (j + L - 1);
    }

    // std::cout << row << "," << column << "\n"; // debug info
  }

  return spins;
}

lattice* create_lattice(int L)
{
  lattice* lat = (lattice*)malloc(sizeof(lattice));
  // Define board size (NxN)
  lat->width = L;
  lat->height = L;
  // Generate spins in a structured grid
  // Store spins in data structure
  lat->spins = generate_spins(L);
  return lat;
}

double compute_energy_difference(lattice* lat, int spin_index, double J, double T)
{
  spin s = lat->spins[spin_index];
  int sum_neighbors = 0;
  for (int i = 0; i < 2; i++)
    sum_neighbors += lat->spins[s.neighbourListIndex_J1[i]].value;
  for (int i = 0; i < 4; i++)
    sum_neighbors += lat->spins[s.neighbourListIndex_J2[i]].value;

  return 2 * J * s.value * sum_neighbors;
}

void glauber_step(lattice* lat, double J, double T)
{
  int random_spin = rand() % (lat->width * lat->height-1);

  double dE = compute_energy_difference(lat, random_spin, J, T);
  if (dE < 0 || exp(-dE / (Kb * T)) > ((double)rand() / RAND_MAX))
    lat->spins[random_spin].value *= -1;
}

double compute_magnetization(lattice* lat)
{
  int total_spin = 0;
  int num_spins = lat->width * lat->height;
  for (int i = 0; i < num_spins; i++)
    total_spin += lat->spins[i].value;
  return (double)total_spin / num_spins;
}

int main(int argc, char* argv[])
{
  const int L = 70;
  const double J = 1.0;
  const double T = 1.8;
  lattice* board = create_lattice(L);
  
  std::ofstream outfile("magnetization_data.txt");
  if (!outfile) {
    std::cerr << "Error opening file!" << std::endl;
    return 1;
  }
  
  for (int step = 0; step < 10'000; step++) {
    glauber_step(board, J, T);
    double magnetization = compute_magnetization(board);
    outfile << step << " " << magnetization << std::endl;
  }
  
  outfile.close();
  std::cout << "Magnetization data saved to magnetization_data.txt" << std::endl;
  
  return 0;
}

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