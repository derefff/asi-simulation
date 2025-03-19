#include <iostream>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

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
  spin* neighbourList;
};

struct lattice
{
  int width;  // cells unit
  int height; // cells unit
  spin* spins;
};

spin* generate_spins(int L)
{
  // one dimmensional table
  spin* spins = (spin*)malloc(sizeof(spin) * (L * L));

  int spin_id = 0;

  for (int i = 0; i < L * L; i++)
  {
    // define spin id
    spins[i].id = spin_id;
    // vertical-> i%2 = 1
    spins[i].isVertical = (i % 2 == 0) ? false : true;
    // assign spin random orientation (+1 or -1)
    spins[i].value = -1 + 2 * (rand() % 2);

    spin_id++;
  }

  // generate near neighbour list for each spin
  for (int j = 0; j < L * L; j++)
  {
    int row = j / L;      // y
    int column = (j % L); // x

    // std::cout << row << "," << column << "\n"; //debug info
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

int main(int argc, char* argv[])
{
  const int L = 4;
  // Create simulation board
  lattice* board = create_lattice(L);

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