set terminal pngcairo size 800,600 enhanced
set output 'wykres MT J1 1.png'
set title 'Wykres M(T) dla J1 = 1'
set xlabel 'Temperatura T'
set ylabel 'Magnetyzacja M'
set grid

#plot "./wyniki/0.3/J1/MT_J1.txt" u 1:2 w l lw 3 t "Dokładne wartości Mx",\
#    "./wyniki/0.3/J1/SYM_MT_J1_0.3.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
#    "./wyniki/0.3/J1/MT_J1.txt" u 1:3 w l lw 2 lc 2 t "Dokładne wartości My",\
#    "./wyniki/0.3/J1/SYM_MT_J1_0.3.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

#plot "./wyniki/0.7/J1/MT_J1.txt" u 1:2 w l lw 3 t "Dokładne wartości Mx",\
#    "./wyniki/0.7/J1/SYM_MT_J1_0.7.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
#    "./wyniki/0.7/J1/MT_J1.txt" u 1:3 w l lw 2 lc 2 t "Dokładne wartości My",\
#    "./wyniki/0.7/J1/SYM_MT_J1_0.7.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

plot "./wyniki/1/J1/MT_J1.txt" u 1:2 w l lw 3 t "Dokładne wartości Mx",\
    "./wyniki/1/J1/SYM_MT_J1_1.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
    "./wyniki/1/J1/MT_J1.txt" u 1:3 w l lw 2 lc 2 t "Dokładne wartości My",\
    "./wyniki/1/J1/SYM_MT_J1_1.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

#plot "./wyniki/1.4/J1/MT_J1.txt" u 1:2 w l lw 3 t "Dokładne wartości Mx",\
#    "./wyniki/1.4/J1/SYM_MT_J1_1.4.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
#    "./wyniki/1.4/J1/MT_J1.txt" u 1:3 w l lw 2 lc 2 t "Dokładne wartości My",\
#    "./wyniki/1.4/J1/SYM_MT_J1_1.4.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

#plot "./wyniki/1.8/J1/MT_J1.txt" u 1:2 w l lw 3 t "Dokładne wartości Mx",\
#    "./wyniki/1.8/J1/SYM_MT_J1_1.8.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
#    "./wyniki/1.8/J1/MT_J1.txt" u 1:3 w l lw 2 lc 2 t "Dokładne wartości My",\
#    "./wyniki/1.8/J1/SYM_MT_J1_1.8.txt" u 1:($2) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

###############################################
#plot "./wyniki/0.3/J2/MT_J2.txt" u 1:2 w l lw 3 t "Dokładne wartości Mx",\
#    "./wyniki/0.3/J2/SYM_MT_J2_0.3.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
#    "./wyniki/0.3/J2/MT_J2.txt" u 1:3 w l lw 2 lc 2 t "Dokładne wartości My",\
#    "./wyniki/0.3/J2/SYM_MT_J2_0.3.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

#plot "./wyniki/0.7/J2/MT_J2.txt" u 1:2 w l lw 3 t "Dokładne wartości Mx",\
#    "./wyniki/0.7/J2/SYM_MT_J2_0.7.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
#    "./wyniki/0.7/J2/MT_J2.txt" u 1:3 w l lw 2 lc 2 t "Dokładne wartości My",\
#    "./wyniki/0.7/J2/SYM_MT_J2_0.7.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

#plot "./wyniki/1/J2/MT_J2.txt" u 1:2 w l lw 3 t "Dokładne wartości Mx",\
#    "./wyniki/1/J2/SYM_MT_J2_1.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
#    "./wyniki/1/J2/MT_J2.txt" u 1:3 w l lw 2 lc 2 t "Dokładne wartości My",\
#    "./wyniki/1/J2/SYM_MT_J2_1.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

#plot "./wyniki/1.4/J2/MT_J2.txt" u 1:2 w l lw 3 t "Dokładne wartości Mx",\
#    "./wyniki/1.4/J2/SYM_MT_J2_1.4.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
#    "./wyniki/1.4/J2/MT_J2.txt" u 1:3 w l lw 2 lc 2 t "Dokładne wartości My",\
#    "./wyniki/1.4/J2/SYM_MT_J2_1.4.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

#plot "./wyniki/1.8/J2/MT_J2.txt" u 1:2 w l lw 3 t "Dokładne wartości Mx",\
#    "./wyniki/1.8/J2/SYM_MT_J2_1.8.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
#    "./wyniki/1.8/J2/MT_J2.txt" u 1:3 w l lw 2 lc 2 t "Dokładne wartości My",\
#    "./wyniki/1.8/J2/SYM_MT_J2_1.8.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

###############################################
#plot "./wyniki/J1J2/MT_J1J2_05_1.txt" u 1:2 w l lw 3 t "Dokładne wartości Mx",\
#    "./wyniki/J1J2/SYM_MT_J1J2_05_1.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
#    "./wyniki/J1J2/MT_J1J2_05_1.txt" u 1:3 w l lw 2 lc 2 t "Dokładne wartości My",\
#    "./wyniki/J1J2/SYM_MT_J1J2_05_1.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

#plot "./wyniki/J1J2/MT_J1J2_1_05.txt" u 1:2 w l lw 3 t "Dokładne wartości Mx",\
#    "./wyniki/J1J2/SYM_MT_J1J2_1_05.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
#    "./wyniki/J1J2/MT_J1J2_1_05.txt" u 1:3 w l lw 2 lc 2 t "Dokładne wartości My",\
#    "./wyniki/J1J2/SYM_MT_J1J2_1_05.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

#plot "./wyniki/J1J2/MT_J1J2_1.txt" u 1:2 w l lw 3 t "Dokładne wartości Mx",\
#    "./wyniki/J1J2/SYM_MT_J1J2_1_1.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
#    "./wyniki/J1J2/MT_J1J2_1.txt" u 1:3 w l lw 2 lc 2 t "Dokładne wartości My",\
#    "./wyniki/J1J2/SYM_MT_J1J2_1_1.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

#plot "./wyniki/J1J2/MT_J1J2_07_14.txt" u 1:2 w l lw 3 t "Dokładne wartości Mx",\
#    "./wyniki/J1J2/SYM_MT_J1J2_07_14.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
#    "./wyniki/J1J2/MT_J1J2_07_14.txt" u 1:3 w l lw 2 lc 2 t "Dokładne wartości My",\
#    "./wyniki/J1J2/SYM_MT_J1J2_07_14.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

unset output