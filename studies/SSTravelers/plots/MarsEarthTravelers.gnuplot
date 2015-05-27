
set terminal wxt

set yrange [0:3]
set xrange [-400:400]

plot \
	"travel.dat" u 1:2 w points t "Departure", \
	"" u 3:4 w points t "Arrival", \
	"travel_hohmann.dat" u 1:2 w points t "D(hohmann)", \
	"" u 3:4 w points t "A(hohmann)"

