# set yrange [0:3]
# set xrange [-400:400]
# set parametric

set terminal wxt size 500,500
set yrange [-25:25]
set xrange [-25:25]

plot \
	"MarsEarthOrbits.dat" u 1:2 w lines t "Earth", \
	"MarsEarthOrbits.dat" u 3:4 w lines t "Mars", \
	"MarsEarthOrbits.dat" u 5:6 w lines t "Trajectory", \
	"MarsEarthTrajectory.dat" u 1:2 w points t "Flight"

pause -1 "Press ENTER"

