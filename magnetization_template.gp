set terminal pngcairo size 1000,800 enhanced

# wielkosc czionki itd
title_font_size = 24
axis_font_size = 18
key_font_size = 16
font_name = "Calibri"

set xlabel 'Temperatura T [ J_1 ]' font sprintf("%s,%d", font_name, axis_font_size)
set ylabel 'Magnetyzacja M' font sprintf("%s,%d", font_name, axis_font_size)
set grid

set xtics font sprintf("%s,%d", font_name, axis_font_size)
set ytics font sprintf("%s,%d", font_name, axis_font_size)
set mxtics 2
set mytics 2

set key at 0.05, 0.03
set key font ",16"
set key box
set key width 2
set key left bottom Left
set yrange[0:1.1]

set output 'wykres MT J2 03 temp.png'
set title 'Wykres M(T) dla J_2 = 0.3' font sprintf("%s,%d", font_name, title_font_size)

plot "./wyniki/0.3/J2/MT_J2.txt" u 1:2 w l lw 6 t "Dokładne wartości Mx",\
    "./wyniki/0.3/J2/SYM_MT_J2_0.3.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
    "./wyniki/0.3/J2/MT_J2.txt" u 1:3 w l lw 4 lc 2 t "Dokładne wartości My",\
    "./wyniki/0.3/J2/SYM_MT_J2_0.3.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";


unset output

set output 'wykres MT J2 1 temp.png'
set title 'Wykres M(T) dla J_2 = 1' font sprintf("%s,%d", font_name, title_font_size)

plot "./wyniki/1/J2/MT_J2.txt" u 1:2 w l lw 6 t "Dokładne wartości Mx",\
    "./wyniki/1/J2/SYM_MT_J2_1.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
    "./wyniki/1/J2/MT_J2.txt" u 1:3 w l lw 4 lc 2 t "Dokładne wartości My",\
    "./wyniki/1/J2/SYM_MT_J2_1.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

unset output

set output 'wykres MT J2 14 temp.png'
set title 'Wykres M(T) dla J_2 = 1.4' font sprintf("%s,%d", font_name, title_font_size)

plot "./wyniki/1.4/J2/MT_J2.txt" u 1:2 w l lw 6 t "Dokładne wartości Mx",\
    "./wyniki/1.4/J2/SYM_MT_J2_1.4.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
    "./wyniki/1.4/J2/MT_J2.txt" u 1:3 w l lw 4 lc 2 t "Dokładne wartości My",\
    "./wyniki/1.4/J2/SYM_MT_J2_1.4.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

unset output

######################
set xlabel 'Temperatura T [ J_2 ]' font sprintf("%s,%d", font_name, axis_font_size)
set output 'wykres MT J1 03 temp.png'
set title 'Wykres M(T) dla J_1 = 0.3' font sprintf("%s,%d", font_name, title_font_size)

plot "./wyniki/0.3/J1/MT_J1.txt" u 1:2 w l lw 6 t "Dokładne wartości Mx",\
    "./wyniki/0.3/J1/SYM_MT_J1_0.3.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
    "./wyniki/0.3/J1/MT_J1.txt" u 1:3 w l lw 4 lc 2 t "Dokładne wartości My",\
    "./wyniki/0.3/J1/SYM_MT_J1_0.3.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

unset output

set output 'wykres MT J1 1 temp.png'
set title 'Wykres M(T) dla J_1 = 1' font sprintf("%s,%d", font_name, title_font_size)

plot "./wyniki/1/J1/MT_J1.txt" u 1:2 w l lw 6 t "Dokładne wartości Mx",\
    "./wyniki/1/J1/SYM_MT_J1_1.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
    "./wyniki/1/J1/MT_J1.txt" u 1:3 w l lw 4 lc 2 t "Dokładne wartości My",\
    "./wyniki/1/J1/SYM_MT_J1_1.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

unset output

set output 'wykres MT J1 14 temp.png'
set title 'Wykres M(T) dla J_1 = 1.4' font sprintf("%s,%d", font_name, title_font_size)

plot "./wyniki/1.4/J1/MT_J1.txt" u 1:2 w l lw 6 t "Dokładne wartości Mx",\
    "./wyniki/1.4/J1/SYM_MT_J1_1.4.txt" u 1:($2) w p ps 3 pt 5 lc 1 t "Symulacyjne wartości Mx",\
    "./wyniki/1.4/J1/MT_J1.txt" u 1:3 w l lw 4 lc 2 t "Dokładne wartości My",\
    "./wyniki/1.4/J1/SYM_MT_J1_1.4.txt" u 1:($3) w p ps 2 pt 7 lc 2 t "Symulacyjne wartości My";

unset output