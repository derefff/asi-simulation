CC=g++
libs=-lm -g
flags=-std=c++17 -Wall -Wextra
debug_options=-g -DDEBUG
target=main.cpp ./utils/vector.cpp
name=asimulation

CFLAGS = -I$(IPATH) -L$(LPATH)

all:
	$(CC) $(target) -o $(name) $(libs)

clang:
	clang++ $(target) $(CFLAGS) -o $(name) $(libs) $(libs)

# debug compilation
debug:
	$(CC) $(target) -I$(IPATH) -L$(LPATH) -o $(name)_debug $(libs) $(debug_options)

min:
	$(CC) $(target) -o $(name)_min $(flags)

clean:
	rm -f $(name) $(name)_debug $(name)_min