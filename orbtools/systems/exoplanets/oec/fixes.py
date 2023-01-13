################################################################################
#
# Fixes for OEC catalog. Some of these are real, like fixing HD 80869 surface
# temperature (database: 58.37, real: 5837.0). Some are just adding "best guesses"
# for planet mass/radius, to extend the amount of planets in various plots.
#
# Exoplanets imported from Open Exoplanet Catalog, see:
#
# https://github.com/OpenExoplanetCatalogue/oec_gzip/
#
################################################################################

from orbtools import *

def doFixes(quiet = False):

  def fix(name, param, value):

    def verbose(current):
      if not quiet: print("Fix: %-20s %s = %s --> %s" % (name, param, current, value))
      return value

    mass = masses[name]

    if(param == "GM"):        mass.GM = verbose(mass.GM)
    elif(param == "radius"):  mass.radius = verbose(mass.radius)
    elif(param == "T"):       mass.T = verbose(mass.T)
    elif(param == "L"):       mass.L = verbose(mass.L)
    elif(param == "sptype"):  mass.sptype = verbose(mass.sptype)
    else:
      print("%s[%s]: Invalid param" % (name, param))
      exit()

  fix("HD 80869", "T", 5837)
  fix("HD 110113 b", "GM", MasEarth(4.55))

  fix("Rigel A", "T", 12100)
  fix("Betelgeuse", "T", 3600)

  #stars["16 Cygni C"].radius =
  #stars["16 Cygni C"].T =
  #stars["16 Cygni C"].L =

  fix("51 Eri", "T", 7331)
  fix("51 Eri", "L", 6.7)

  fix("61 Cygni A", "radius", RasSun(0.665))
  fix("61 Cygni A", "T", 4526)
  fix("61 Cygni A", "L", 0.095)

  fix("61 Cygni B", "radius", RasSun(0.595))
  fix("61 Cygni B", "T", 4077)
  fix("61 Cygni B", "L", 0.085)

  fix("EPIC 211089792", "T", 5387.060)
  fix("EPIC 211089792", "L", Star.LasLog10(-0.2953329))

  fix("GJ 163", "radius", RasSun(0.409))
  fix("GJ 163", "T", 3460)
  fix("GJ 163", "L", 0.02163)

  fix("GJ 180", "radius", RasSun(0.4229))
  fix("GJ 180", "T", 3634)
  fix("GJ 180", "L", 0.02427)

  #stars["GJ 2056"].radius = RasSun(0.6715)
  #stars["GJ 2056"].T =
  #stars["GJ 2056"].L =

  fix("GJ 229", "radius", RasSun(0.69))
  fix("GJ 229", "T", 3700)
  fix("GJ 229", "L", 0.0430)

  fix("GJ 27.1", "radius", RasSun(0.5188870))
  fix("GJ 27.1", "T", 3687.0)
  fix("GJ 27.1", "L", Star.LasLog10(-1.34847))

  fix("GJ 3082", "radius", RasSun(0.4652160))
  fix("GJ 3082", "T", 3910.0)
  fix("GJ 3082", "L", Star.LasLog10(-1.46273))

  fix("GJ 3090", "sptype", "M2V")

  fix("GJ 317", "radius", RasSun(0.4170))
  fix("GJ 317", "T", 3510)
  fix("GJ 317", "L", 0.02175)

  fix("GJ 433", "radius", RasSun(0.529))
  fix("GJ 433", "T", 3445)
  fix("GJ 433", "L", 0.034)

  fix("GJ 687", "radius", RasSun(0.492))
  fix("GJ 687", "T", 3095)
  fix("GJ 687", "L", 0.0213)

  fix("GJ 9066", "radius", RasSun(0.164))
  fix("GJ 9066", "T", 3154)
  fix("GJ 9066", "L", Star.LasLog10(-2.60))

  fix("GJ 96", "radius", RasSun(0.5806120))
  fix("GJ 96", "T", 3782.0)
  fix("GJ 96", "L", Star.LasLog10(-1.20665))

  fix("Gliese 1002", "radius", RasSun(0.137))
  fix("Gliese 1002", "T", 3024)
  fix("Gliese 1002", "L", 0.001406)

  Planet("Gliese 1002 a", MasEarth(1.08), orbit = Orbit("Gliese 1002", AU2m(0.0457)))
  Planet("Gliese 1002 b", MasEarth(1.36), orbit = Orbit("Gliese 1002", AU2m(0.0738)))

  fix("Gliese 221", "radius", RasSun(0.613))
  fix("Gliese 221", "T", 4324)
  fix("Gliese 221", "L", 0.001406)

  #fix("Gliese 328", "radius", RasSun(???))
  fix("Gliese 328", "T", 3989)
  fix("Gliese 328", "L", 0.10)

  fix("Gliese 649", "radius", RasSun(0.531))
  fix("Gliese 649", "T", 3621)
  fix("Gliese 649", "L", 0.04373)

  fix("Gliese 674", "radius", RasSun(0.361))
  fix("Gliese 674", "T", 3404)
  fix("Gliese 674", "L", 0.01575)

  fix("Gliese 676 A", "radius", RasSun(0.617))
  fix("Gliese 676 A", "T", 4014)
  fix("Gliese 676 A", "L", 0.08892)

  fix("Gliese 676 A", "radius", RasSun(0.617))
  fix("Gliese 676 A", "T", 4014)
  fix("Gliese 676 A", "L", 0.08892)

  #fix("HD 158259", "radius", RasSun(???))
  fix("HD 158259", "T", 6068)
  fix("HD 158259", "L", 1.6)

  fix("HD 159868", "radius", RasSun(1.97))
  fix("HD 158259", "T", 5558)
  fix("HD 158259", "L", 3.59)

  #fix("HD 163296", "radius", RasSun(???))
  #fix("HD 163296", "T", ???)
  #fix("HD 163296", "L", ???)

  fix("HD 181433", "radius", RasSun(0.8108410))
  fix("HD 181433", "T", 4929.630)
  fix("HD 181433", "L", Star.LasLog10(-0.4561762))

  fix("HD 204313", "radius", RasSun(1.08))
  fix("HD 204313", "T", 5783)
  fix("HD 204313", "L", 1.18)

  fix("HD 20794", "radius", RasSun(0.92))
  fix("HD 20794", "T", 5401)
  fix("HD 20794", "L", 0.74)

  fix("HD 40307", "radius", RasSun(0.716))
  fix("HD 40307", "T", 4977)
  fix("HD 40307", "L", 0.23)

  fix("HD 80653", "T", 5910.000)
  fix("HD 80653", "L", Star.LasLog10(0.24))

  fix("K2-16", "radius", RasSun(0.703181))
  fix("K2-16", "T", 4627.07)
  fix("K2-16", "L", Star.LasLog10(-0.689946))

  fix("K2-165", "radius", RasSun(0.8376060))
  fix("K2-165", "T", 5141.6700)
  fix("K2-165", "L", Star.LasLog10(-0.3548089))

  fix("K2-183", "radius", RasSun(0.87))
  fix("K2-183", "T", 5482)
  fix("K2-183", "L", Star.LasLog10(-0.1317863))

  fix("K2-187", "radius", RasSun(0.894913))
  fix("K2-187", "T", 5477)
  fix("K2-187", "L", Star.LasLog10(-0.1960678))

  fix("K2-219", "radius", RasSun(1.2561700))
  fix("K2-219", "T", 5712.000)
  fix("K2-219", "L", Star.LasLog10(0.17994742))

  fix("K2-32", "radius", RasSun(0.233767))
  fix("K2-32", "T", 3190.0)
  fix("K2-32", "L", Star.LasLog10(-2.2926))

  fix("K2-58", "radius", RasSun(0.8364240))
  fix("K2-58", "T", 5020.000)
  fix("K2-58", "L", Star.LasLog10(-0.3976375))

  fix("K2-80", "radius", RasSun(0.8680660))
  fix("K2-80", "T", 5203.000)
  fix("K2-80", "L", Star.LasLog10(-0.3031848))

  #stars["Kepler-108 B"].radius = RasSun(0.955127)
  #stars["Kepler-108 B"].T = 5309.190
  #stars["Kepler-108 B"].L = Star.LasLog10(-0.1850697)

  fix("Kepler-411", "radius", RasSun(0.76))
  fix("Kepler-411", "T", 4773)
  fix("Kepler-411", "L", 0.27)

  fix("Kepler-42", "radius", RasSun(0.175))
  fix("Kepler-42", "T", 3269)
  fix("Kepler-42", "L", 3.08e-3)

  fix("Kepler-450 A", "radius", RasSun(1.600))
  fix("Kepler-450 A", "T", 6298)
  fix("Kepler-450 A", "L", Star.LasLog10(0.53147524))

  fix("Kepler-595", "radius", RasSun(1.600))
  fix("Kepler-595", "T", 5138.50)
  fix("Kepler-595", "L", Star.LasLog10(-0.3476832))

  fix("Kepler-82", "radius", RasSun(0.955127))
  fix("Kepler-82", "T", 5309.190)
  fix("Kepler-82", "L", Star.LasLog10(-0.1850697))

  fix("KOI-1860", "radius", RasSun(1.08916))
  fix("KOI-1860", "T", 5620.270)
  fix("KOI-1860", "L", Star.LasLog10(0.02790548))

  fix("KOI-1599", "T", 5833.0)
  fix("KOI-1599", "L", Star.LasLog10(0.1619642))

  #------------------------------------------------------------------------------

  fix("HIP 41378 b", "GM", MasEarth(6.89))
  fix("HIP 41378 c", "GM", MasEarth(4.4))
  fix("HIP 41378 d", "GM", MasEarth(4.6))
  fix("HIP 41378 e", "GM", MasEarth(12))
  fix("HIP 41378 f", "GM", MasEarth(12))

  fix("K2-138 b", "GM", MasEarth(3.1))
  fix("K2-138 c", "GM", MasEarth(6.3))
  fix("K2-138 d", "GM", MasEarth(7.9))
  fix("K2-138 e", "GM", MasEarth(13.0))
  fix("K2-138 f", "GM", MasEarth(8.7))
  fix("K2-138 g", "GM", MasEarth(8.94))

  fix("K2-32 b", "GM", MasEarth(2.1))
  fix("K2-32 c", "GM", MasEarth(15.0))
  fix("K2-32 d", "GM", MasEarth(8.1))
  fix("K2-32 e", "GM", MasEarth(6.7))

  fix("Kepler-186 b", "GM", MasEarth(1.24))
  fix("Kepler-186 c", "GM", MasEarth(2.1))
  fix("Kepler-186 d", "GM", MasEarth(2.54))
  fix("Kepler-186 e", "GM", MasEarth(2.15))
  fix("Kepler-186 f", "GM", MasEarth(1.71))

  fix("Kepler-22 b", "GM", MasJupiter(0.11))

  fix("Kepler-32 b", "GM",  MasJupiter(0.011))
  fix("Kepler-32 c", "GM",  MasJupiter(0.012))

  fix("Kepler-442 b", "GM", MasEarth(2.3))

  #fix("Kepler-444 b", "GM", MasEarth(?))
  #fix("Kepler-444 c", "GM", MasEarth(?))
  fix("Kepler-444 d", "GM", MasEarth(0.036))
  fix("Kepler-444 e", "GM", MasEarth(0.034))
  #fix("Kepler-444 f", "GM", MasEarth(?))

  fix("Kepler-452 b", "GM", MasEarth(5))

  fix("Kepler-62 b", "GM",  MasEarth(2.1))
  fix("Kepler-62 c", "GM",  MasEarth(0.1))
  fix("Kepler-62 d", "GM",  MasEarth(5.5))
  fix("Kepler-62 e", "GM",  MasEarth(4.5))
  fix("Kepler-62 f", "GM",  MasEarth(2.8))

  fix("Kepler-84 b", "GM",  MasJupiter(0.126))
  fix("Kepler-84 c", "GM",  MasJupiter(0.064))
  #fix("Kepler-84 d", "GM",  MasEarth(?))
  #fix("Kepler-84 e", "GM",  MasEarth(?))
  #fix("Kepler-84 f", "GM",  MasEarth(?))
