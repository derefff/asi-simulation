CC=g++
LPATH=./raylib/lib
IPATH=./raylib/include
libs=-lm -l:libraylib.a -g
flags=-std=c++17 -Wall -Wextra
debug_options=-g -DDEBUG
target=main.cpp
name=asimulation

CFLAGS = -I$(IPATH) -L$(LPATH)

all:
	$(CC) $(target) -I$(IPATH) -L$(LPATH) -o $(name) $(libs)

clang:
	clang++ $(target) $(CFLAGS) -o $(name) $(libs) $(libs)

# debug compilation
debug:
	$(CC) $(target) -I$(IPATH) -L$(LPATH) -o $(name)_debug $(libs) $(debug_options)

# compile version without visualization (raylib)
min:
	$(CC) $(target) -o $(name)_min $(flags)

clean:
	rm -f $(name) $(name)_debug $(name)_min