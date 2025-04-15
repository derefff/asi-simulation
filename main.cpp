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
  int neighbourListIndex_J1[2];
  int neighbourListIndex_J2[4];
};

struct vertex
{
  int id;
  int spinIndices[4];
  int neighborIndices[4]; // [0]=up, [1]=right, [2]=bottom, [3]=left
  int type;
  int monopoleCharge;
  double energy;
};

struct lattice
{
  int width;  // cells unit
  int height; // cells unit
  spin* spins;
  vertex* vertices;
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
    // spin_id++;
    // vertical-> i%2 = 1
    spins[i].isVertical = (i % 2 == 0) ? false : true;
    // assign spin random orientation (+1 or -1)
    spins[i].value = -1 + 2 * (rand() % 2);
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

vertex* generate_vertex(int L, spin* spins)
{
  int num_vertices = L * L;
  vertex* vertices = (vertex*)malloc(sizeof(vertex) * num_vertices);

  for (int i = 0; i < num_vertices; i++)
  {
    int row = i / L;
    int col = i % L;

    vertex v;
    v.id = i;

    // top, left, bottom, right

    int top_spin_index = ((row == 0) ? (L - 1) : row - 1) * L + col;
    int bottom_spin_index = row * L + col;

    int left_spin_index = row * L + ((col == 0) ? (L - 1) : col - 1);
    int right_spin_index = row * L + col;

    // vertical spins -> (i % 2 == 1), horizontal have odd index

    // vertical neighbors
    while (!spins[top_spin_index].isVertical)
      top_spin_index = (top_spin_index + 1) % (L * L);

    while (!spins[bottom_spin_index].isVertical)
      bottom_spin_index = (bottom_spin_index + 1) % (L * L);

    // horziontal neighbors
    while (spins[left_spin_index].isVertical)
      left_spin_index = (left_spin_index + 1) % (L * L);

    while (spins[right_spin_index].isVertical)
      right_spin_index = (right_spin_index + 1) % (L * L);

    v.spinIndices[0] = top_spin_index;
    v.spinIndices[1] = left_spin_index;
    v.spinIndices[2] = bottom_spin_index;
    v.spinIndices[3] = right_spin_index;

    // neihborVvertex
    for (int d = 0; d < 4; d++)
      v.neighborIndices[d] = -1;

    // placeholders
    v.type = -1;
    v.monopoleCharge = 0;
    v.energy = 0.0;

    vertices[i] = v;
  }

  return vertices;
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
  lat->vertices = generate_vertex(L, lat->spins);
  return lat;
}

void update_vertices(vertex* vertices, spin* spins, int num_vertices, double J1, double J2)
{
  for (int i = 0; i < num_vertices; i++)
  {
    vertex* v = &vertices[i];

    // take those 4 spins
    int s[4];
    for (int k = 0; k < 4; k++)
      s[k] = spins[v->spinIndices[k]].value;

    // spins sum -> monopole charge
    int sum = s[0] + s[1] + s[2] + s[3];
    v->monopoleCharge = sum;

    // vertex type
    switch (abs(sum))
    {
    case 0:
      // type I (2 in, 2 out)
      v->type = 1;
      break;
    case 2:
      // type II (3 in / 1 out)
      v->type = 2;
      break;
    case 4:
      // type III (4 in or 4 out)
      v->type = 3;
      break;
    default:
      // error or unknown
      v->type = -1;
      break;
    }

    // local energy ... not sure if correct
    v->energy = -J1 * (s[0] * s[2] + s[1] * s[3]) - J2 * (s[0] * s[1] + s[0] * s[3] + s[2] * s[1] + s[2] * s[3]);
  }
}

int count_monopoles(vertex* vertices, int num_vertices)
{
  int count = 0;
  for (int i = 0; i < num_vertices; i++)
    if (abs(vertices[i].monopoleCharge) > 0)
      count++;
  return count;
}

// previously there was T in argument
double compute_energy_difference(lattice* lat, int spin_index, double J1, double J2, physics::vector* B)
{
  spin s = lat->spins[spin_index];
  // int sum_neighbors = 0;
  int sum_J1 = 0;
  int sum_J2 = 0;

  for (int i = 0; i < 2; i++)
    sum_J1 += lat->spins[s.neighbourListIndex_J1[i]].value;
  for (int i = 0; i < 4; i++)
    sum_J2 += lat->spins[s.neighbourListIndex_J2[i]].value;

  double field = s.isVertical ? B->y : B->x;

  return 2 * s.value * (J1 * sum_J1 + J2 * sum_J2 + field);
}

void glauber_step(lattice* lat, double J1, double J2, double T, physics::vector* B)
{
  int random_spin = rand() % (lat->width * lat->height - 1);

  double dE = compute_energy_difference(lat, random_spin, J1, J2, B);
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

int main(int argc, char* argv[])
{
  const int L = 40;
  const double J1 = 1.0;
  const double J2 = 1.0;
  const double T = 1.8;
  const int steps = 10'000;
  // const int equil_steps = 5000; // termalizacja?
  // const int samples = steps - equil_steps; // steps -> smples

  // Create output file for phase diagram
  std::ofstream phase_file("phase_diagram.txt");
  if (!phase_file)
  {
    std::cerr << "Error opening phase_diagram.txt!" << std::endl;
    return 1;
  }

  // External field B(x,y)
  physics::vector* B = physics::create_vector(0.0, 0.0);

  int total = 21 * 21;
  int count = 0;

  // Looping over B vector
  for (B->x = -1.0; B->x <= 1.01; B->x += 0.1)
  {
    for (B->y = -1.0; B->y <= 1.01; B->y += 0.1)
    {

      // Create fresh lattice for each B
      lattice* board = create_lattice(L);

      // run simulaation
      for (int step = 0; step < steps; step++)
      {
        glauber_step(board, J1, J2, T, B);
        update_vertices(board->vertices, board->spins, L * L, J1, J2);
      }

      double Mx = 0.0, My = 0.0;
      int monopole_total = 0;

      for (int step = 0; step < steps; step++)
      {
        glauber_step(board, J1, J2, T, B);
        update_vertices(board->vertices, board->spins, L * L, J1, J2);

        physics::vector* M = compute_magnetization(board);
        Mx += M->x;
        My += M->y;

        monopole_total += count_monopoles(board->vertices, L * L);
      }

      // avg variables
      double avg_Mx = Mx / steps;
      double avg_My = My / steps;
      double avg_monopole_density = (double)monopole_total / (steps * L * L);

      // save to phase_diagram.txt file
      phase_file << B->x << '\t' << B->y << '\t' << avg_Mx << '\t' << avg_My << '\t' << avg_monopole_density << '\n';

      count++;
      int progress = (100 * count) / total;
      std::cout << "\rProgress: " << progress << "%     " << std::flush;

      // Free memory for this run
      free(board->spins);
      free(board->vertices);
      free(board);
    }
    phase_file << "\n";
  }

  phase_file.close();
  std::cout << "Phase diagram data saved to phase_diagram.txt" << std::endl;
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

