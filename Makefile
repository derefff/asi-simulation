CC=g++
LPATH=./raylib/lib
IPATH=./raylib/include
libs=-lm -l:libraylib.a -g
target=main.cpp
name=asimulation

CFLAGS = -I$(IPATH) -L$(LPATH)

all:
	$(CC) $(target) -I$(IPATH) -L$(LPATH) -o $(name) $(libs)

clang:
	clang++ $(target) $(CFLAGS) -o $(name) $(libs) $(libs)