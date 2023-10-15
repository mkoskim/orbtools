################################################################################
#
# Solar System Database: Orbital calculation toolbox
#
################################################################################

from orbtools import *

################################################################################
#
# Sun & planets
#
################################################################################

Sun = Star("Sun", 1.0, 1.0, sptype = "G2", L=1, mag = 4.83, T=5773, rotate = TasDays(24.6), dist = 0.00)

Mercury = Planet("Mercury",   GM_Mercury,	    2440e3,     TasDays(58.6),          Orbit("Sun",	  57910e6))
Venus   = Planet("Venus",     GM_Venus,	    6052e3,     TasDays(-243),          Orbit("Sun",	 108200e6))
Earth   = Planet("Earth",     GM_Earth,	    r_Earth,    TasDHMS(0, 23, 56, 0),  Orbit("Sun",	AU2m(1)))
Mars    = Planet("Mars",      GM_Mars,	    3397e3,     TasDays(1.03),          Orbit("Sun",	 227940e6))
Jupiter = Planet("Jupiter",   GM_Jupiter,	    71492e3,    TasDays(0.41),          Orbit("Sun",	 778330e6))
Saturn  = Planet("Saturn",    GM_Saturnus,    60268e3,    TasDays(0.45),          Orbit("Sun",	1433530e6))
Uranus  = Planet("Uranus",    GM_Uranus,	    25559e3,    TasDays(-0.72),         Orbit("Sun",	2870972e6))
Neptune = Planet("Neptune",   GM_Neptune,    24766e3,    TasDays(0.67),          Orbit("Sun",	4504300e6))
Pluto   = Planet("Pluto",	    kg2GM(1.3E+22), 1150e3,     TasDays(-6.39),         Orbit("Sun",	5913520e6))

#-------------------------------------------------------------------------------
# Fictional masses
#-------------------------------------------------------------------------------

#Planet("SuperEarth", GM_Earth*2, Planet.rFromV(GM2kg(GM_Earth*2) / Earth.density), 0)
#Planet("GiantEarth", GM_Earth*4, Planet.rFromV(GM2kg(GM_Earth*4) / Earth.density), 0)

#-------------------------------------------------------------------------------
# Earth satellites and orbits
#-------------------------------------------------------------------------------

Moon = Planet("Moon", kg2GM(7.4E+22), 1738e3, "S", Orbit("Earth", 384.399e6))

Mass("LEO",        0, 0, 0, byAltitude("Earth", +150e3))
Mass("ISS",        0, 0, 0, byAltitude("Earth", +368e3))
Mass("Hubble",     0, 0, 0, byAltitude("Earth", +573e3))
#Mass("Earth300km", 0, 0, 0, Altitude("Earth", +300e3))
Mass("GEO",        0, 0, 0, byPeriod  ("Earth", Earth.rotate))

#-------------------------------------------------------------------------------
# Mars satellites
#-------------------------------------------------------------------------------

#Mass("Mars1000km", 0, 0, 0, Altitude("Mars", +1000e3))
Planet("Phobos",	kg2GM(1.1E+16),	11e3,	"S",	Orbit("Mars",	9e6))
Planet("Deimos",	kg2GM(1.8E+15),	6e3,	"S",	Orbit("Mars",	23e6))

#-------------------------------------------------------------------------------
# Asteroid belt objects
#-------------------------------------------------------------------------------

Planet("Ceres",     kg2GM(8.70e20),    466e3,     0,  Orbit("Sun",     413_900e6))
Planet("Pallas",    kg2GM(3.18e20),    261e3,     0,  Orbit("Sun",     414_500e6))
Planet("Vesta",     kg2GM(3.00e20),    265e3,     0,  Orbit("Sun",     353_400e6))
Planet("Hygiea",    kg2GM(9.30e19),    215e3,     0,  Orbit("Sun",     470_300e6))
Planet("Eunomia",   kg2GM(8.30e18),    136e3,     0,  Orbit("Sun",     395_500e6))

Planet("Aten",            kg2GM(0),    0.5e3,     0,  Orbit("Sun",     144_514e6))
Planet("Amun",            kg2GM(0),    0.0e3,     0,  Orbit("Sun",     145_710e6))
Planet("Icarus",          kg2GM(0),    0.7e3,     0,  Orbit("Sun",     161_269e6))
Planet("Gaspra",          kg2GM(0),      8e3,     0,  Orbit("Sun",     205_000e6))
Planet("Apollo",          kg2GM(0),    0.7e3,     0,  Orbit("Sun",     220_061e6))
Planet("Ida",             kg2GM(0),     35e3,     0,  Orbit("Sun",     270_000e6))
Planet("Hephaistos",      kg2GM(0),    4.4e3,     0,  Orbit("Sun",     323_884e6))
Planet("Juno",            kg2GM(0),    123e3,     0,  Orbit("Sun",     399_400e6))
Planet("Europa(a)",       kg2GM(0),    156e3,     0,  Orbit("Sun",     463_300e6))
Planet("Davida",          kg2GM(0),    168e3,     0,  Orbit("Sun",     475_400e6))
Planet("Agamemnon",       kg2GM(0),     88e3,     0,  Orbit("Sun",     778_100e6))
Planet("Chiron",          kg2GM(0),     85e3,     0,  Orbit("Sun",   2_051_900e6))

#-------------------------------------------------------------------------------
# Jupiter satellites
#-------------------------------------------------------------------------------

Planet("Metis",       kg2GM(9.6E+16),	20e3,	0,	Orbit(	"Jupiter",	128e6))
Planet("Adrastea",	kg2GM(1.9E+16),	10e3,	0,	Orbit(	"Jupiter",	129e6))
Planet("Amalthea",	kg2GM(3.5E+18),	94e3,	"S",	Orbit(	"Jupiter",	181e6))
Planet("Thebe",	    kg2GM(7.8E+17),	50e3,	"S",	Orbit(	"Jupiter",	222e6))
Planet("Io",          kg2GM(8.9E+22),	1821e3,	"S",	Orbit(	"Jupiter",	422e6))
Planet("Europa",      kg2GM(4.8E+22),	1565e3,	"S",	Orbit(	"Jupiter",	671e6))
Planet("Ganymede",	kg2GM(1.5E+23),	2634e3,	"S",	Orbit(	"Jupiter",	1070e6))
Planet("Callisto",	kg2GM(1.1E+23),	2403e3,	"S",	Orbit(	"Jupiter",	1883e6))
Planet("Themisto",	0,	0,	0,	Orbit(	"Jupiter",	7507e6))
Planet("Leda",	    kg2GM(5.7E+15),	8e3,	0,	Orbit(	"Jupiter",	11094e6))
Planet("Himalia",	    kg2GM(9.6E+18),	93e3,	TasDays(0.4),	Orbit(	"Jupiter",	11480e6))
Planet("Lysithea",	kg2GM(7.8E+16),	18e3,	0,	Orbit(	"Jupiter",	11720e6))
Planet("Elara",	    kg2GM(7.8E+17),	38e3,	TasDays(0.5),	Orbit(	"Jupiter",	11737e6))
Planet("Ananke",	    kg2GM(3.8E+16),	15e3,	0,	Orbit(	"Jupiter",	21200e6))
Planet("Carme",	    kg2GM(9.6E+16),	20e3,	0,	Orbit(	"Jupiter",	22600e6))
Planet("Pasiphae",	kg2GM(1.9E+17),	25e3,	0,	Orbit(	"Jupiter",	23500e6))
Planet("Sinope",	    kg2GM(7.8E+16),	18e3,	0,	Orbit(	"Jupiter",	23700e6))
Planet("Iocaste",	    0,	0,	0,	Orbit(	"Jupiter",	20216e6))
Planet("Harpalyke",	0,	0,	0,	Orbit(	"Jupiter",	21132e6))
Planet("Praxidike",	0,	0,	0,	Orbit(	"Jupiter",	20964e6))
Planet("Taygete",	    0,	0,	0,	Orbit(	"Jupiter",	23312e6))
Planet("Chaldene",	0,	0,	0,	Orbit(	"Jupiter",	23387e6))
Planet("Kalyke",	    0,	0,	0,	Orbit(	"Jupiter",	23745e6))
Planet("Callirrhoe",	0,	0,	0,	Orbit(	"Jupiter",	24100e6))
Planet("Megaclite",	0,	0,	0,	Orbit(	"Jupiter",	23911e6))
Planet("Isonoe",	    0,	0,	0,	Orbit(	"Jupiter",	23078e6))
Planet("Erinome",	    0,	0,	0,	Orbit(	"Jupiter",	23168e6))

#-------------------------------------------------------------------------------
# Saturn satellites
#-------------------------------------------------------------------------------

Planet("Pan",	        0,	10e3,	0,	Orbit(	"Saturn",	134e6))
Planet("Atlas",	    0,	15e3,	0,	Orbit(	"Saturn",	138e6))
Planet("Prometheus",	kg2GM(2.7E+17),	46e3,	0,	Orbit(	"Saturn",	139e6))
Planet("Pandora",	    kg2GM(2.2E+17),	42e3,	0,	Orbit(	"Saturn",	142e6))
Planet("Epimetheus",	kg2GM(5.6E+17),	57e3,	"S",	Orbit(	"Saturn",	151e6))
Planet("Janus",	    kg2GM(2.0E+18),	89e3,	"S",	Orbit(	"Saturn",	151e6))
Planet("Mimas",	    kg2GM(3.8E+19),	199e3,	"S",	Orbit(	"Saturn",	186e6))
Planet("Enceladus",	kg2GM(7.3E+19),	249e3,	"S",	Orbit(	"Saturn",	238e6))
Planet("Tethys",	    kg2GM(6.2E+20),	530e3,	"S",	Orbit(	"Saturn",	295e6))
Planet("Telesto",	    0,	15e3,	0,	Orbit(	"Saturn",	295e6))
Planet("Calypso",	    0,	13e3,	0,	Orbit(	"Saturn",	295e6))
Planet("Dione",	    kg2GM(1.1E+21),	560e3,	"S",	Orbit(	"Saturn",	377e6))
Planet("Helene",	    0,	16e3,	0,	Orbit(	"Saturn",	377e6))
Planet("Rhea",	    kg2GM(2.3E+21),	764e3,	"S",	Orbit(	"Saturn",	527e6))
Planet("Titan",	    kg2GM(1.4E+23),	2575e3,	"S",	Orbit(	"Saturn",	1222e6))
Planet("Hyperion",	kg2GM(1.8E+19),	143e3,	0,	Orbit(	"Saturn",	1481e6))
Planet("Iapetus",	    kg2GM(1.6E+21),	718e3,	"S",	Orbit(	"Saturn",	3561e6))
Planet("Phoebe",	    kg2GM(0.0E+0),	110e3,	TasDays(0.4),	Orbit(	"Saturn",	12952e6))

#-------------------------------------------------------------------------------
# Uranus satellites
#-------------------------------------------------------------------------------

Planet("Cordelia",	0,	13e3,	0,	Orbit(	"Uranus",	50e6))
Planet("Ophelia",	    0,	16e3,	0,	Orbit(	"Uranus",	54e6))
Planet("Bianca",	    0,	22e3,	0,	Orbit(	"Uranus",	59e6))
Planet("Cressida",	0,	33e3,	0,	Orbit(	"Uranus",	62e6))
Planet("Desdemona",	0,	29e3,	0,	Orbit(	"Uranus",	63e6))
Planet("Juliet",	    0,	42e3,	0,	Orbit(	"Uranus",	64e6))
Planet("Portia",	    0,	55e3,	0,	Orbit(	"Uranus",	66e6))
Planet("Rosalind",	0,	27e3,	0,	Orbit(	"Uranus",	70e6))
Planet("Belinda",	    0,	34e3,	0,	Orbit(	"Uranus",	75e6))
Planet("Puck",	    0,	77e3,	0,	Orbit(	"Uranus",	86e6))
Planet("Miranda",	    kg2GM(6.6E+19),	236e3,	"S",	Orbit(	"Uranus",	130e6))
Planet("Ariel",	    kg2GM(1.4E+21),	581e3,	"S",	Orbit(	"Uranus",	191e6))
Planet("Umbriel",	    kg2GM(1.2E+21),	585e3,	"S",	Orbit(	"Uranus",	266e6))
Planet("Titania",	    kg2GM(3.5E+21),	789e3,	"S",	Orbit(	"Uranus",	436e6))
Planet("Oberon",	    kg2GM(3.0E+21),	761e3,	"S",	Orbit(	"Uranus",	583e6))
Planet("Caliban",	    0,	40e3,	0,	Orbit(	"Uranus",	7169e6))
Planet("Stephano",	0,	15e3,	0,	Orbit(	"Uranus",	7948e6))
Planet("Sycorax",	    0,	80e3,	0,	Orbit(	"Uranus",	12213e6))
Planet("Prospero",	0,	20e3,	0,	Orbit(	"Uranus",	16568e6))
Planet("Setebos",	    0,	20e3,	0,	Orbit(	"Uranus",	17681e6))

#-------------------------------------------------------------------------------
# Neptune satellites
#-------------------------------------------------------------------------------

Planet("Naiad",	    0,	29e3,	0,	Orbit(	"Neptune",	48e6))
Planet("Thalassa",	0,	40e3,	0,	Orbit(	"Neptune",	50e6))
Planet("Despina",	    0,	74e3,	0,	Orbit(	"Neptune",	53e6))
Planet("Galatea",	    0,	79e3,	0,	Orbit(	"Neptune",	62e6))
Planet("Larissa",	    0,	96e3,	0,	Orbit(	"Neptune",	74e6))
Planet("Proteus",	    0,	209e3,	0,	Orbit(	"Neptune",	118e6))
Planet("Triton",	    kg2GM(2.2E+22),	1353e3,	"S",	Orbit(	"Neptune",	355e6))
Planet("Nereid",	    0,	170e3,	0,	Orbit(	"Neptune",	5513e6))

#-------------------------------------------------------------------------------
# Pluto satellites
#-------------------------------------------------------------------------------

Planet("Charon",	    kg2GM(158.7e19),	603e3,	"S",	Orbit(	"Pluto",	20e6))
Planet("Nix",	        kg2GM(0.005e19),	33e3,	0,	Orbit(	"Pluto",	49e6))
Planet("Hydra",	      kg2GM(0.005e19),	36e3,	0,	Orbit(	"Pluto",	65e6))
