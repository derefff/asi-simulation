#include <iostream>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// change with spin.value
//  enum spinDirection{
//    UP, DOWN, RIGHT, LEFT
//  };

struct spin
{
  int id;
  int x, y;  // "position of spin" for now idk if neccesary
  int value; //+1 or -1, if isVertical then +1 up and -1 down, if !isVertical +1 right, -1 left
  bool isVertical;
  // near neighbour liek list
  // spinDirection direction;
};

struct lattice
{
  int width;  // cells unit
  int height; // cells unit
  spin** spins;
};

spin** generate_spins(int L)
{
  // two dimmensional table
  spin** spins = (spin**)malloc(sizeof(spin) * L);
  for (int col = 0; col < L; col++)
    spins[col] = (spin*)malloc(sizeof(spin) * L);

  int spin_id = 0;
  for (int i = 0; i < L; i++)
  {
    for (int j = 0; j < L; j++)
    {
      // define spin id
      spins[i][j].id = spin_id;
      // vertical-> i%2 = 1
      spins[i][j].isVertical = (j % 2 == 0) ? false : true;
      // assign spin random orientation (+1 or -1)
      spins[i][j].value = -1 + 2 * (rand() % 2);
    }

    spin_id++;
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

// if(argc>1 && std::string_view(argv[1]) == "--gui")
// {
// std::cout<<"guiversion\n";
// //--------------------------------------------------DRAWING
// const int WindowWidth = 600;
// const int WindowHeight= 600;
// InitWindow(WindowWidth, WindowHeight, "ASImulation Graphical Interface");

// double x_scale = 600.f/board->width;
// double y_scale = 600.f/board->height;

// SetTargetFPS(60);

// while (!WindowShouldClose())
// {
//     BeginDrawing();
//     ClearBackground(RAYWHITE);

//     for(int i = 0; i < board->width;i ++)
//     {
//       DrawLine(0, y_scale*i, WindowWidth, y_scale*i, BLACK);
//       DrawLine(x_scale*i, 0, x_scale*i,WindowHeight, BLACK);
//       for(int j = 0; j < board->height;j ++)
//       {
//         DrawLineEx({5,10}, {x_scale-5,10}, 5.f, BLACK);
//       }
//     }

//     EndDrawing();
// }
// CloseWindow();
// }
// //--------------------------------------------------END-DRAWING
