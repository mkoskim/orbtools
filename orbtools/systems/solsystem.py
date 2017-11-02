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

Sun     = Mass("Sun",       GM_Sun,         695000e3,   TasDays(24.6))		

Mercury = Mass("Mercury",   GM_Mercury,	    2440e3,     TasDays(58.6),          Orbit(	"Sun",	57910e6))
Venus   = Mass("Venus",     GM_Venus,	    6052e3,     TasDays(-243),          Orbit(	"Sun",	108200e6))
Earth   = Mass("Earth",     GM_Earth,	    r_Earth,    TasDHMS(0, 23, 56, 0),  Orbit(	"Sun",	AU2m(1)))
Mars    = Mass("Mars",      GM_Mars,	    3397e3,     TasDays(1.03),          Orbit(	"Sun",	227940e6))
Jupiter = Mass("Jupiter",   GM_Jupiter,	    71492e3,    TasDays(0.41),          Orbit(	"Sun",	778330e6))
Saturn  = Mass("Saturn",    GM_Saturnus,    60268e3,    TasDays(0.45),          Orbit(	"Sun",	1429400e6))
Uranus  = Mass("Uranus",    GM_Uranus,	    25559e3,    TasDays(-0.72),         Orbit(	"Sun",	2870990e6))
Neptune = Mass("Neptune",   GM_Neptunus,    24766e3,    TasDays(0.67),          Orbit(	"Sun",	4504300e6))
Pluto   = Mass("Pluto",	    kg2GM(1.3E+22), 1150e3,     TasDays(-6.39),         Orbit(	"Sun",	5913520e6))

#-------------------------------------------------------------------------------
# Earth satellites and orbits
#-------------------------------------------------------------------------------

Moon = Mass("Moon", kg2GM(7.4E+22), 1738e3, "S", Orbit("Earth", 384.399e6))

Mass("LEO",        0, 0, 0, Altitude("Earth", +150e3))
Mass("ISS",        0, 0, 0, Altitude("Earth", +368e3))
Mass("Hubble",     0, 0, 0, Altitude("Earth", +573e3))
Mass("Earth300km", 0, 0, 0, Altitude("Earth", +300e3))
Mass("GEO",        0, 0, 0, Period  ("Earth", Earth.rotate))

#-------------------------------------------------------------------------------
# Mars satellites
#-------------------------------------------------------------------------------

Mass(	"Mars1000km", 0, 0, 0, Altitude("Mars", +1000e3))
Mass(	"Phobos",	kg2GM(1.1E+16),	11e3,	"S",	Orbit(	"Mars",	9e6))
Mass(	"Deimos",	kg2GM(1.8E+15),	6e3,	"S",	Orbit(	"Mars",	23e6))

#-------------------------------------------------------------------------------
# Asteroid belt objects
#-------------------------------------------------------------------------------

Mass("Aten",            kg2GM(0),    0.5e3,     0,  Orbit("Sun",    144514e6))
Mass("Amun",            kg2GM(0),    0.0e3,     0,  Orbit("Sun",    145710e6))
Mass("Icarus",          kg2GM(0),    0.7e3,     0,  Orbit("Sun",    161269e6))
Mass("Gaspra",          kg2GM(0),      8e3,     0,  Orbit("Sun",    205000e6))
Mass("Apollo",          kg2GM(0),    0.7e3,     0,  Orbit("Sun",    220061e6))
Mass("Ida",             kg2GM(0),     35e3,     0,  Orbit("Sun",    270000e6))
Mass("Hephaistos",      kg2GM(0),    4.4e3,     0,  Orbit("Sun",    323884e6))
Mass("Vesta",     kg2GM(3.00e20),    265e3,     0,  Orbit("Sun",    353400e6))
Mass("Juno",            kg2GM(0),    123e3,     0,  Orbit("Sun",    399400e6))
Mass("Eunomia",   kg2GM(8.30e18),    136e3,     0,  Orbit("Sun",    395500e6))
Mass("Ceres",     kg2GM(8.70e20),    466e3,     0,  Orbit("Sun",    413900e6))
Mass("Pallas",    kg2GM(3.18e20),    261e3,     0,  Orbit("Sun",    414500e6))
Mass("Europa(a)",       kg2GM(0),    156e3,     0,  Orbit("Sun",    463300e6))
Mass("Hygiea",    kg2GM(9.30e19),    215e3,     0,  Orbit("Sun",    470300e6))
Mass("Davida",          kg2GM(0),    168e3,     0,  Orbit("Sun",    475400e6))
Mass("Agamemnon",       kg2GM(0),     88e3,     0,  Orbit("Sun",    778100e6))
Mass("Chiron",          kg2GM(0),     85e3,     0,  Orbit("Sun",   2051900e6))

#-------------------------------------------------------------------------------
# Jupiter satellites
#-------------------------------------------------------------------------------

Mass(	"Metis",	kg2GM(9.6E+16),	20e3,	0,	Orbit(	"Jupiter",	128e6))
Mass(	"Adrastea",	kg2GM(1.9E+16),	10e3,	0,	Orbit(	"Jupiter",	129e6))
Mass(	"Amalthea",	kg2GM(3.5E+18),	94e3,	"S",	Orbit(	"Jupiter",	181e6))
Mass(	"Thebe",	kg2GM(7.8E+17),	50e3,	"S",	Orbit(	"Jupiter",	222e6))
Mass(	"Io",	kg2GM(8.9E+22),	1821e3,	"S",	Orbit(	"Jupiter",	422e6))
Mass(	"Europa",	kg2GM(4.8E+22),	1565e3,	"S",	Orbit(	"Jupiter",	671e6))
Mass(	"Ganymede",	kg2GM(1.5E+23),	2634e3,	"S",	Orbit(	"Jupiter",	1070e6))
Mass(	"Callisto",	kg2GM(1.1E+23),	2403e3,	"S",	Orbit(	"Jupiter",	1883e6))
Mass(	"Themisto",	0,	0,	0,	Orbit(	"Jupiter",	7507e6))
Mass(	"Leda",	kg2GM(5.7E+15),	8e3,	0,	Orbit(	"Jupiter",	11094e6))
Mass(	"Himalia",	kg2GM(9.6E+18),	93e3,	TasDays(0.4),	Orbit(	"Jupiter",	11480e6))
Mass(	"Lysithea",	kg2GM(7.8E+16),	18e3,	0,	Orbit(	"Jupiter",	11720e6))
Mass(	"Elara",	kg2GM(7.8E+17),	38e3,	TasDays(0.5),	Orbit(	"Jupiter",	11737e6))
Mass(	"Ananke",	kg2GM(3.8E+16),	15e3,	0,	Orbit(	"Jupiter",	21200e6))
Mass(	"Carme",	kg2GM(9.6E+16),	20e3,	0,	Orbit(	"Jupiter",	22600e6))
Mass(	"Pasiphae",	kg2GM(1.9E+17),	25e3,	0,	Orbit(	"Jupiter",	23500e6))
Mass(	"Sinope",	kg2GM(7.8E+16),	18e3,	0,	Orbit(	"Jupiter",	23700e6))
Mass(	"Iocaste",	0,	0,	0,	Orbit(	"Jupiter",	20216e6))
Mass(	"Harpalyke",	0,	0,	0,	Orbit(	"Jupiter",	21132e6))
Mass(	"Praxidike",	0,	0,	0,	Orbit(	"Jupiter",	20964e6))
Mass(	"Taygete",	0,	0,	0,	Orbit(	"Jupiter",	23312e6))
Mass(	"Chaldene",	0,	0,	0,	Orbit(	"Jupiter",	23387e6))
Mass(	"Kalyke",	0,	0,	0,	Orbit(	"Jupiter",	23745e6))
Mass(	"Callirrhoe",	0,	0,	0,	Orbit(	"Jupiter",	24100e6))
Mass(	"Megaclite",	0,	0,	0,	Orbit(	"Jupiter",	23911e6))
Mass(	"Isonoe",	0,	0,	0,	Orbit(	"Jupiter",	23078e6))
Mass(	"Erinome",	0,	0,	0,	Orbit(	"Jupiter",	23168e6))

#-------------------------------------------------------------------------------
# Saturn satellites
#-------------------------------------------------------------------------------

Mass(	"Pan",	0,	10e3,	0,	Orbit(	"Saturn",	134e6))
Mass(	"Atlas",	0,	15e3,	0,	Orbit(	"Saturn",	138e6))
Mass(	"Prometheus",	kg2GM(2.7E+17),	46e3,	0,	Orbit(	"Saturn",	139e6))
Mass(	"Pandora",	kg2GM(2.2E+17),	42e3,	0,	Orbit(	"Saturn",	142e6))
Mass(	"Epimetheus",	kg2GM(5.6E+17),	57e3,	"S",	Orbit(	"Saturn",	151e6))
Mass(	"Janus",	kg2GM(2.0E+18),	89e3,	"S",	Orbit(	"Saturn",	151e6))
Mass(	"Mimas",	kg2GM(3.8E+19),	199e3,	"S",	Orbit(	"Saturn",	186e6))
Mass(	"Enceladus",	kg2GM(7.3E+19),	249e3,	"S",	Orbit(	"Saturn",	238e6))
Mass(	"Tethys",	kg2GM(6.2E+20),	530e3,	"S",	Orbit(	"Saturn",	295e6))
Mass(	"Telesto",	0,	15e3,	0,	Orbit(	"Saturn",	295e6))
Mass(	"Calypso",	0,	13e3,	0,	Orbit(	"Saturn",	295e6))
Mass(	"Dione",	kg2GM(1.1E+21),	560e3,	"S",	Orbit(	"Saturn",	377e6))
Mass(	"Helene",	0,	16e3,	0,	Orbit(	"Saturn",	377e6))
Mass(	"Rhea",	kg2GM(2.3E+21),	764e3,	"S",	Orbit(	"Saturn",	527e6))
Mass(	"Titan",	kg2GM(1.4E+23),	2575e3,	"S",	Orbit(	"Saturn",	1222e6))
Mass(	"Hyperion",	kg2GM(1.8E+19),	143e3,	0,	Orbit(	"Saturn",	1481e6))
Mass(	"Iapetus",	kg2GM(1.6E+21),	718e3,	"S",	Orbit(	"Saturn",	3561e6))
Mass(	"Phoebe",	kg2GM(0.0E+0),	110e3,	TasDays(0.4),	Orbit(	"Saturn",	12952e6))

#-------------------------------------------------------------------------------
# Uranus satellites
#-------------------------------------------------------------------------------

Mass(	"Cordelia",	0,	13e3,	0,	Orbit(	"Uranus",	50e6))
Mass(	"Ophelia",	0,	16e3,	0,	Orbit(	"Uranus",	54e6))
Mass(	"Bianca",	0,	22e3,	0,	Orbit(	"Uranus",	59e6))
Mass(	"Cressida",	0,	33e3,	0,	Orbit(	"Uranus",	62e6))
Mass(	"Desdemona",	0,	29e3,	0,	Orbit(	"Uranus",	63e6))
Mass(	"Juliet",	0,	42e3,	0,	Orbit(	"Uranus",	64e6))
Mass(	"Portia",	0,	55e3,	0,	Orbit(	"Uranus",	66e6))
Mass(	"Rosalind",	0,	27e3,	0,	Orbit(	"Uranus",	70e6))
Mass(	"Belinda",	0,	34e3,	0,	Orbit(	"Uranus",	75e6))
Mass(	"Puck",	0,	77e3,	0,	Orbit(	"Uranus",	86e6))
Mass(	"Miranda",	kg2GM(6.6E+19),	236e3,	"S",	Orbit(	"Uranus",	130e6))
Mass(	"Ariel",	kg2GM(1.4E+21),	581e3,	"S",	Orbit(	"Uranus",	191e6))
Mass(	"Umbriel",	kg2GM(1.2E+21),	585e3,	"S",	Orbit(	"Uranus",	266e6))
Mass(	"Titania",	kg2GM(3.5E+21),	789e3,	"S",	Orbit(	"Uranus",	436e6))
Mass(	"Oberon",	kg2GM(3.0E+21),	761e3,	"S",	Orbit(	"Uranus",	583e6))
Mass(	"Caliban",	0,	40e3,	0,	Orbit(	"Uranus",	7169e6))
Mass(	"Stephano",	0,	15e3,	0,	Orbit(	"Uranus",	7948e6))
Mass(	"Sycorax",	0,	80e3,	0,	Orbit(	"Uranus",	12213e6))
Mass(	"Prospero",	0,	20e3,	0,	Orbit(	"Uranus",	16568e6))
Mass(	"Setebos",	0,	20e3,	0,	Orbit(	"Uranus",	17681e6))

#-------------------------------------------------------------------------------
# Neptune satellites
#-------------------------------------------------------------------------------

Mass(	"Naiad",	0,	29e3,	0,	Orbit(	"Neptune",	48e6))
Mass(	"Thalassa",	0,	40e3,	0,	Orbit(	"Neptune",	50e6))
Mass(	"Despina",	0,	74e3,	0,	Orbit(	"Neptune",	53e6))
Mass(	"Galatea",	0,	79e3,	0,	Orbit(	"Neptune",	62e6))
Mass(	"Larissa",	0,	96e3,	0,	Orbit(	"Neptune",	74e6))
Mass(	"Proteus",	0,	209e3,	0,	Orbit(	"Neptune",	118e6))
Mass(	"Triton",	kg2GM(2.2E+22),	1353e3,	"S",	Orbit(	"Neptune",	355e6))
Mass(	"Nereid",	0,	170e3,	0,	Orbit(	"Neptune",	5513e6))

#-------------------------------------------------------------------------------
# Pluto satellites
#-------------------------------------------------------------------------------

Mass(	"Charon",	kg2GM(1.5E+21),	603e3,	"S",	Orbit(	"Pluto",	20e6))
Mass(	"Nix",	kg2GM(2.0E+18),	23e3,	0,	Orbit(	"Pluto",	49e6))
Mass(	"Hydra",	kg2GM(2.0E+18),	30e3,	0,	Orbit(	"Pluto",	65e6))
