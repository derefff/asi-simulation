set terminal pngcairo size 1000,800 enhanced font 'Arial,12'
set output 'phase.png'

set xlabel "B_x"
set ylabel "B_y"
set cblabel "Monopole density"
set title "Phase Diagram"

#set cbrange [0:1] # nie działa w takim rangu
set dgrid3d 21,21      # przekształć dane punktowe na siatkę
set pm3d map
# set palette defined ( 0 "white", 1 "blue", 2 "red" )

splot 'phase_diagram.txt' using 1:2:5 with pm3d notitle
