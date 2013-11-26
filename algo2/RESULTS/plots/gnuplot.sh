set xlabel "Support"
set ylabel "Time (sec)"

set title "Training Time vs Support"
plot "comparison.csv" index 0 u 1:9 t "CBA (Algo 1)" with lines, \
     "comparison.csv" index 1 u 1:9 t "CBA with 8 Clusters" with lines, \
     "comparison.csv" index 2 u 1:9 t "CBA with 16 Clusters" with lines

pause -1

