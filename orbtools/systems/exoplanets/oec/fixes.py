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

#-------------------------------------------------------------------------------
# Post-fixes to catalog data:
#
# 1) I have mainly added mass and/or luminosity information to stars which have
# multiple planets around them.
#
# 2) I have tried to retain the values in the catalog. But sometimes they are
# changed, for example many times the radius/temperature is changed to match
# the value given to luminosity.
#
# This is due that the catalog values can be from study, which does not
# include luminosity: the study that does, has found slightly different values
# for other parameters, too.
#
# 3) None: this is used as mark to tell, that we know that the entry is
# incomplete: planets missing either mass or radius, stars missing mass,
# radius or luminosity. So, the software does not report missing data for
# these objects.
#
#-------------------------------------------------------------------------------

fixes = {
  "Sun": None, # Comes from Solar System data

  "1SWASP J1407": None, # massless star: 1 planets
  "2M 044144": None, # Fluxless, planets: 1
  "2M1207": None, # Fluxless, planets: 1
  "2M 1252+2735": None, # massless star: 1 planets
  "2M 1253+2734": None, # massless star: 1 planets
  "2M 1258+2630": None, # massless star: 1 planets
  "2MASS J01225093-2439505 A": None, # Fluxless, planets: 1
  "2MASS J0030-1450": None, # - massless star: 1 planets
  "2MASS J01033563-5515561 A": None, # Fluxless, planets: 1
  "2MASS J0459-2853": None, # - massless star: 1 planets
  "2MASS J06023447-0034369": None, # - massless star: 1 planets
  "2MASS J0642+4101": None, # - massless star: 1 planets
  "2MASS J0718-6415": None, # - massless star: 1 planets
  "2MASS J0809+4434": None, # - massless star: 1 planets
  "2MASS J0951-8023": None, # - massless star: 1 planets
  "2MASS J1119-1137": None, # - massless star: 1 planets
  "2MASS J2002-0521": None, # - massless star: 1 planets
  "2MASS J2117-2940": None, # - massless star: 1 planets
  "2MASS J2206+3301": None, # - massless star: 1 planets
  "2MASS J22362452+4751425": None, # Fluxless, planets: 1
  "51 Eri": { # Fluxless, planets: 1
    "radius": 1.45,
    "T": 7331,
    "L": 6.7,
  },
  "AB Aur": None, # Fluxless, planets: 1
  "AB Pic": None, # Massless, planets 1
  "BD-08 2823": None, # Fluxless, planets: 2
  "BD+14 4559": None, # Fluxless, planets: 1
  "BD+20 1790": None, # Fluxless, planets: 1
  "BD+20 2457": None, # Fluxless, planets: 2
  "BD+26 1888": None, # Fluxless, planets: 1
  "beta Pic": None, # Fluxless, planets: 2
  "Betelgeuse": {
    "T": 3600,
  },
  "CFBDS 1458": None, # Fluxless, planets: 1
  "CHXR 73": None, # Fluxless, planets: 1
  "CI Tau": None, # Fluxless, planets: 1
  "CT Cha": None, # Massless, planets 1
  "DE CVn": None, # Fluxless, planets: 1
  "DH Tau": None, # Fluxless, planets: 1

  "EPIC 201238110": None, # Fluxless, planets: 1
  "EPIC 201497682": None, # Fluxless, planets: 1
  "EPIC 201841433": None, # Fluxless, planets: 1
  "EPIC 206024342": None, # Fluxless, planets: 1
  "EPIC 206032309": None, # Fluxless, planets: 1
  "EPIC 206042996": None, # Fluxless, planets: 1
  "EPIC 206215704": None, # Fluxless, planets: 1
  "EPIC 206317286": None, # Fluxless, planets: 1
  "EPIC 211089792": None, # Fluxless, planets: 1
  "EPIC 212297394": None, # Fluxless, planets: 1
  "EPIC 212424622": None, # Fluxless, planets: 1
  "EPIC 212499991": None, # Fluxless, planets: 1

  "FN Lyr": None, # Fluxless, planets: 1
  "FU Tau A": None, # Fluxless, planets: 1
  "gam Psc": None, # Massless, planets 1

  #----------------------------------------------------------------------------

  "GJ 1151": None, # Fluxless, planets: 1
  "GJ 160.2": None, # Fluxless, planets: 1
  "GJ 163": { # Fluxless, planets: 5
    "radius": 0.409,
    "L": 0.02163,
    "T": 3460,
  },
  "GJ 180": { # Fluxless, planets: 3
    "radius": 0.4229,
    "T": 3634,
    "L": 0.02427,
  },
  "GJ 2056": { # Fluxless, planets: 1
    "radius": 0.68,
    "T": 4017,
    "L": Star.LasLog10(-0.8863611)
  },
  "GJ 229": { # Fluxless, planets: 2
    "radius": 0.69,
    "T": 3700,
    "L": 0.0430,
  },
  "GJ 27.1": { # Fluxless, planets: 1
    "radius": 0.5188870,
    "T": 3687.0,
    "L": Star.LasLog10(-1.34847),
  },
  "GJ 3082": { # Fluxless, planets: 1
    "radius": 0.4652160,
    "T": 3910.0,
    "L": Star.LasLog10(-1.46273),
  },
  #fix("GJ 3090", "sptype", "M2V")
  "GJ 317": { # Fluxless, planets: 2
    "radius": 0.4170,
    "T": 3510,
    "L": 0.02175,
  },
  "GJ 367": None, # Massless, planets 1
  "GJ 422": None, # Fluxless, planets: 1
  "GJ 433": { # Fluxless, planets: 3
    "radius": 0.529,
    "T": 3445,
    "L": 0.034,
  },
  "GJ 480": { # Fluxless, planets: 1
    "mass": 0.41,
    "radius": 0.52,
    "T": 3350,
  },
  "GJ 682": { # Fluxless, planets: 2
    "radius": 0.492,
    "T": 3095,
    "L": 0.0213,
  },
  "GJ 687": { # Fluxless, planets: 2
    "radius": 0.492,
    "L": 0.0213,
    "T": 3095,
  },
  "GJ 740": { # Massless, planets 1
    "mass": 0.58,
    "radius": 0.56,
    "T": 3913,
  },
  "GJ 896 A": None, # Fluxless, planets: 1
  "GJ 9066": { # Fluxless, planets: 2
    "radius": 0.164,
    "T": 3154,
    "L": Star.LasLog10(-2.60),
  },
  "GJ 96": { # Fluxless, planets: 1
    "radius": 0.5806120,
    "T": 3782.0,
    "L": Star.LasLog10(-1.20665),
  },

  #"Gliese 1002": None, # Fluxless, planets: 0
    # #fix("Gliese 1002", "radius", RasSun(0.137))
    # #fix("Gliese 1002", "T", 3024)
    # #fix("Gliese 1002", "L", 0.001406)
    # #Planet("Gliese 1002 a", MasEarth(1.08), orbit = Orbit("Gliese 1002", AU2m(0.0457)))
    # #Planet("Gliese 1002 b", MasEarth(1.36), orbit = Orbit("Gliese 1002", AU2m(0.0738)))
  "Gliese 221": { # Fluxless, planets: 4
    "radius": 0.613,
    "T": 4324,
    "L": 0.001406,
  },

  "Gliese 328": { # Fluxless, planets: 1
    "radius": 0.63,
    "T": 3897,
    "L": 0.08,
  },
  "Gliese 649": { # Fluxless, planets: 2
    "radius": 0.531,
    "T": 3621,
    "L": 0.04373,
  },
  "Gliese 674": { # Fluxless, planets: 1
    "radius": 0.361,
    "T": 3404,
    "L": 0.01575,
  },
  "Gliese 676 A": { # Fluxless, planets: 4
    "radius": 0.617,
    "T": 4014,
    "L": 0.08892,
  },
  "Gliese 777 A": None, # Fluxless, planets: 2
  "Gliese 785": None, # Fluxless, planets: 2
  "Gliese 832": None, # Fluxless, planets: 2

  #----------------------------------------------------------------------------

  "GQ Lup": None, # Fluxless, planets: 1
  "GSC 06214-00210": None, # Fluxless, planets: 1
  "GU Psc": None, # Fluxless, planets: 1

  #----------------------------------------------------------------------------

  "HD 100546": None, # Fluxless, planets: 2
  "HD 100777": None, # Fluxless, planets: 1
  "HD 101930": None, # Fluxless, planets: 1
  "HD 102365": None, # Fluxless, planets: 1
  "HD 102843": None, # Fluxless, planets: 1
  "HD 103197": None, # Fluxless, planets: 1
  "HD 103774": None, # Fluxless, planets: 1
  "HD 103949": None, # Fluxless, planets: 1
  "HD 104067": None, # Fluxless, planets: 1
  "HD 10442": None, # Fluxless, planets: 1
  "HD 106515 A": None, # Fluxless, planets: 1
  "HD 109271": None, # Fluxless, planets: 2
  "HD 109749 A": None, # Fluxless, planets: 1
  "HD 10975": None, # Massless, planets 1
  # "HD 110113 b", "GM", MasEarth(4.55))
  "HD 111232": None, # Fluxless, planets: 1
  "HD 113337": None, # Fluxless, planets: 1
  "HD 114613": None, # Fluxless, planets: 1
  "HD 114729 A": None, # Fluxless, planets: 1
  "HD 118203": None, # Fluxless, planets: 1
  "HD 11964 A": None, # Fluxless, planets: 2
  "HD 121504": None, # Fluxless, planets: 1
  "HD 122562": None, # Fluxless, planets: 1
  "HD 12484": None, # Fluxless, planets: 1
  "HD 125595": None, # Fluxless, planets: 1
  "HD 126525": None, # Massless, planets 1
  "HD 129445": None, # Fluxless, planets: 1
  "HD 132406": None, # Fluxless, planets: 1
  "HD 132563 B": None, # Fluxless, planets: 1
  "HD 133131 A": None, # Fluxless, planets: 2
  "HD 133131 B": None, # Fluxless, planets: 1
  "HD 134060": None, # Massless, planets 2
  "HD 134606": { # Massless, planets 3
    "mass": 0.998,
    "T": 5614,
    "L": 1.25,
    "radius": RtoSun(Star.LTtoR(1.25, 5614)),
  },
  "HD 136352": { # Massless, planets 3
    "mass": 0.87,
    "radius": 1.058,
    "T": 5664,
    "L": Star.LasLog10(0.01620),
  },
  "HD 136925": None, # Massless, planets 1
  "HD 137496": None, # Massless, planets 2
  "HD 13808": None, # Massless, planets 2
  "HD 143105": None, # Fluxless, planets: 1
  "HD 143361": None, # Fluxless, planets: 1
  "HD 145934": None, # Fluxless, planets: 1
  "HD 147018": None, # Fluxless, planets: 2
  "HD 147513 A": None, # Fluxless, planets: 1
  "HD 149143": None, # Fluxless, planets: 1
  "HD 150433": None, # Massless, planets 1
  "HD 152079": None, # Fluxless, planets: 1
  "HD 154088": None, # Massless, planets 1
  "HD 154345": None, # Fluxless, planets: 1
  "HD 155358": None, # Fluxless, planets: 2
  "HD 156279": None, # Fluxless, planets: 2
  "HD 157172": None, # Massless, planets 1
  "HD 158259": { # Fluxless, planets: 5
    "radius": 1.3,
    "L": 1.6,
    "T": 6068,
  },
  "HD 159868": { # Fluxless, planets: 2
    "radius": 1.97,
    "T": 5558,
    "L": 3.59,
  },
  "HD 161178": None, # Massless, planets 1
  "HD 163296": None, # Fluxless, planets: 2
  "HD 16417": None, # Fluxless, planets: 1
  "HD 164595": None, # Fluxless, planets: 1
  "HD 164604": None, # Fluxless, planets: 1
  "HD 166724": None, # Fluxless, planets: 1
  "HD 17092": None, # Fluxless, planets: 1
  "HD 171238": None, # Fluxless, planets: 1
  "HD 175167": None, # Fluxless, planets: 1
  "HD 176051 B": None, # Fluxless, planets: 1
  "HD 177565": None, # Fluxless, planets: 1
  "HD 177830 A": None, # Fluxless, planets: 2
  "VB 10": None, # Fluxless, planets: 1
  "HD 181433": { # Fluxless, planets: 3
    "radius": 0.8108410,
    "T": 4929.630,
    "L": Star.LasLog10(-0.4561762),
  },
  "HD 181720": None, # Fluxless, planets: 1
  "HD 187085": None, # Fluxless, planets: 1
  "HD 188015 A": None, # Fluxless, planets: 1
  "HD 189567": None, # Massless, planets 1
  "HD 190647": None, # Fluxless, planets: 1
  "HD 191806": None, # Fluxless, planets: 1
  "HD 195019 A": None, # Fluxless, planets: 1
  "HD 195689": None, # Massless, planets 1
  "HD 197037 A": None, # Fluxless, planets: 1
  "HD 19994 A": None, # Fluxless, planets: 1
  "HD 20003": None, # Massless, planets 2
  "HD 203030": None, # Massless, planets 1
  "HD 204313": { # Fluxless, planets: 3
    "radius": 1.08,
    "T": 5783,
    "L": 1.18,
  },
  "HD 206255": None, # Fluxless, planets: 1
  "HD 20781": { # Fluxless, planets: 2
    "T": 5256,
    "L": 0.49,
    "radius": RtoSun(Star.LTtoR(0.49, 5256)),
  },
  "HD 20794": { # Fluxless, planets: 4
    "radius": 0.92,
    "T": 5401,
    "L": 0.74,
  },
  "HD 210193": None, # Fluxless, planets: 1
  "HD 211970": None, # Fluxless, planets: 1
  "HD 212301": None, # Fluxless, planets: 1
  "HD 213240 A": None, # Fluxless, planets: 1
  "HD 213472": None, # Massless, planets 1
  "HD 21411": None, # Fluxless, planets: 1
  "HD 214823": None, # Fluxless, planets: 1
  "HD 215456": None, # Massless, planets 2
  "HD 215497": None, # Fluxless, planets: 2
  "HD 21693": None, # Massless, planets 2
  "HD 219139": None, # Massless, planets 1
  "HD 220773": None, # Fluxless, planets: 1
  "HD 220842": None, # Fluxless, planets: 1
  "HD 221287": None, # Fluxless, planets: 1
  "HD 221420": None, # Fluxless, planets: 1
  "HD 221585": None, # Fluxless, planets: 1
  "HD 222582 A": None, # Fluxless, planets: 1
  "HD 22781": None, # Fluxless, planets: 1
  "HD 23127": None, # Fluxless, planets: 1
  "HD 23472": None, # Fluxless, planets: 2
  "HD 240210": None, # Fluxless, planets: 1
  "HD 24085": None, # Fluxless, planets: 1
  "HD 26161": None, # Massless, planets 1
  "HD 2638": None, # Fluxless, planets: 1
  "HD 27442 A": None, # Fluxless, planets: 1
  "HD 27894": { # Fluxless, planets: 3
    "T": 4912.17,
    "L": Star.LasLog10(-0.4193195),
    "radius": 0.8520130,
  },
  "HD 31527": { # Massless, planets 3
    "mass": 1.070000,
    "radius": 1.0773600,
    "T": 5909.59,
    "L": Star.LasLog10(0.10564369),
  },
  "HD 32963": None, # Fluxless, planets: 1
  "HD 330075": None, # Fluxless, planets: 1
  "HD 35759": None, # Fluxless, planets: 1
  "HD 360": None, # Massless, planets 1
  "HD 37605": None, # Fluxless, planets: 2
  "HD 38283": None, # Fluxless, planets: 1
  "HD 38529 A": None, # Fluxless, planets: 2
  "HD 38858": None, # Massless, planets 1
  "HD 39194": { # Massless, planets 3
    "mass": 0.71,
    "radius": 0.74,
    "L": 0.389,
    "T": 5205,
  },
  "HD 39392": None, # Fluxless, planets: 1
  "HD 39855": None, # Fluxless, planets: 1
  "HD 40307": { # Fluxless, planets: 6
    "radius": 0.716,
    "T": 4977,
    "L": 0.23,
  },
  "HD 40979 A": None, # Fluxless, planets: 1
  "HD 41004 A": None, # Fluxless, planets: 1
  "HD 4113 A": None, # Fluxless, planets: 1
  "HD 43691": None, # Fluxless, planets: 1
  "HD 45184": { # Fluxless, planets: 2
    "mass": 1.08,
    "radius": 1.05,
    "L": 1.178,
    "T": 5862,
  },
  "HD 45364": None, # Fluxless, planets: 2
  "HD 45652": None, # Fluxless, planets: 1
  "HD 47186": None, # Fluxless, planets: 2
  "HD 48265": None, # Fluxless, planets: 1
  "HD 51608": { # Massless, planets 2
    "T": 5352.6,
    "L": Star.LasLog10(-0.2059246),
    "mass": 0.9300000,
    "radius": 0.9174040,
  },

  "HD 60532": None, # Fluxless, planets: 2
  "HD 63454": None, # Fluxless, planets: 1
  "HD 63765": None, # Fluxless, planets: 1
  "HD 64114": None, # Fluxless, planets: 1
  "HD 65216": None, # Fluxless, planets: 2
  "HD 66428": None, # Fluxless, planets: 2
  "HD 70573": None, # Fluxless, planets: 1
  "HD 75289 A": None, # Fluxless, planets: 1
  "HD 79181": None, # Massless, planets 1
  "HD 79498": None, # Fluxless, planets: 1
  "HD 80653": { # Fluxless, planets: 1
    "T": 5959,
    #"L": Star.TtoL(5959, RasSun(1.22)),
  },
  "HD 80869": {
    "T": 5837, # 58.37
  },
  "HD 8326": None, # Fluxless, planets: 1
  "HD 85390": None, # Fluxless, planets: 1
  "HD 85512": None, # Fluxless, planets: 1
  "HD 89744 A": None, # Fluxless, planets: 1
  "HD 90156": None, # Fluxless, planets: 1
  "HD 93083": None, # Fluxless, planets: 1
  "HD 93385": { # Massless, planets 2
    "mass": 1.07,
    "radius": 1.17,
    "L": 1.42,
    "T": 5823,
  },
  "HD 95086": None, # Fluxless, planets: 1
  "HD 9578": None, # Fluxless, planets: 1
  "HD 95872": None, # Fluxless, planets: 1
  "HD 96700": { # Massless, planets 2
    "mass": 0.96,
    "radius": 0.96,
    #"T": 5940.00,
    "L": Star.TtoL(5940.00, RasSun(0.96)),
  },
  "HD 984": None, # Fluxless, planets: 1
  "HD 99109": None, # Fluxless, planets: 1
  "HD 99283": None, # Massless, planets 1

  #----------------------------------------------------------------------------

  "HIP 105854": None, # Fluxless, planets: 1
  "HIP 107772": None, # Fluxless, planets: 1
  "HIP 109384": None, # Fluxless, planets: 1
  "HIP 109600": None, # Fluxless, planets: 1
  "HIP 11915": None, # Fluxless, planets: 1
  "HIP 12961": None, # Fluxless, planets: 1
  "HIP 3206": None, # Massless, planets 1
  "HIP 34222": None, # Fluxless, planets: 1
  "HIP 35173": None, # Fluxless, planets: 1
  "HIP 38594": None, # Fluxless, planets: 2
  # #fix("HIP 41378 b", "GM", MasEarth(6.89))
  # #fix("HIP 41378 c", "GM", MasEarth(4.4))
  # #fix("HIP 41378 d", "GM", MasEarth(4.6))
  # #fix("HIP 41378 e", "GM", MasEarth(12))
  # #fix("HIP 41378 f", "GM", MasEarth(12))
  "HIP 4845": None, # Fluxless, planets: 1
  "HIP 48714": None, # Fluxless, planets: 1
  "HIP 5158": None, # Fluxless, planets: 2
  "HIP 54373": None, # Fluxless, planets: 2
  "HIP 5763": None, # Fluxless, planets: 1
  "HIP 63242": None, # Fluxless, planets: 1
  "HIP 63734": None, # Fluxless, planets: 1
  "HIP 65407": None, # Fluxless, planets: 2
  "HIP 68468": None, # Fluxless, planets: 2
  "HIP 70849": None, # Fluxless, planets: 1
  "HIP 71135": None, # Fluxless, planets: 1
  "HIP 77257": None, # Massless, planets 1
  "HIP 78530": None, # Fluxless, planets: 1
  "HIP 79431": None, # Fluxless, planets: 1
  "HIP 86221": None, # Fluxless, planets: 1
  "HIP 89474": None, # Massless, planets 1
  "HIP 94235": None, # Massless, planets 1

  "HN Peg": None, # Fluxless, planets: 1
  "IC 4651 9122": None, # Fluxless, planets: 1
  "ITG 15B": None, # Massless, planets 1

  #----------------------------------------------------------------------------

  "K2-110": None, # Fluxless, planets: 1
  "K2-121": None, # Fluxless, planets: 1
  "K2-126": None, # Fluxless, planets: 1
  "K2-128": None, # Fluxless, planets: 1
  "K2-130": None, # Fluxless, planets: 1
  "K2-131": None, # Fluxless, planets: 1
  # #fix("K2-138 b", "GM", MasEarth(3.1))
  # #fix("K2-138 c", "GM", MasEarth(6.3))
  # #fix("K2-138 d", "GM", MasEarth(7.9))
  # #fix("K2-138 e", "GM", MasEarth(13.0))
  # #fix("K2-138 f", "GM", MasEarth(8.7))
  # #fix("K2-138 g", "GM", MasEarth(8.94))
  "K2-156": None, # Fluxless, planets: 1
  "K2-157": None, # Fluxless, planets: 1
  "K2-159": None, # Fluxless, planets: 1
  "K2-160": None, # Fluxless, planets: 1
  "K2-161": None, # Fluxless, planets: 1
  "K2-162": None, # Fluxless, planets: 1
  "K2-163": None, # Fluxless, planets: 1
  "K2-164": None, # Fluxless, planets: 1
  "K2-165": { # Fluxless, planets: 3
    "radius": 0.8376060,
    "T": 5141.6700,
    "L": Star.LasLog10(-0.3548089),
  },
  #"K2-166": None, # Fluxless, planets: 2
  "K2-167": None, # Fluxless, planets: 1
  "K2-169": None, # Fluxless, planets: 1
  "K2-16": { # Fluxless, planets: 3
    "radius": 0.703181,
    "T": 4627.07,
    "L": Star.LasLog10(-0.689946),
  },
  #K2-170 # Fluxless, planets: 2
  "K2-171": None, # Fluxless, planets: 1
  #K2-172 # Fluxless, planets: 2
  "K2-173": None, # Fluxless, planets: 1
  "K2-174": None, # Fluxless, planets: 1
  "K2-175": None, # Fluxless, planets: 1
  "K2-176": None, # Fluxless, planets: 1
  "K2-177": None, # Fluxless, planets: 1
  "K2-178": None, # Fluxless, planets: 1
  "K2-179": None, # Fluxless, planets: 1
  "K2-180": None, # Fluxless, planets: 1
  "K2-181": None, # Fluxless, planets: 1
  "K2-182": None, # Fluxless, planets: 1
  "K2-183": { # Fluxless, planets: 3
    "T": 5482,
    "L": Star.LasLog10(-0.1317863),
  },
  "K2-184": None, # Fluxless, planets: 1
  "K2-185": None, # Fluxless, planets: 1
  "K2-186": None, # Fluxless, planets: 1
  "K2-187": { # Fluxless, planets: 4
    "T": 5477,
    "L": Star.LasLog10(-0.1960678),
  },
  #K2-188 # Fluxless, planets: 2
  #K2-189 # Fluxless, planets: 2
  #K2-190 # Fluxless, planets: 2
  "K2-191": None, # Fluxless, planets: 1
  "K2-192": None, # Fluxless, planets: 1
  "K2-193": None, # Fluxless, planets: 1
  "K2-194": None, # Fluxless, planets: 1
  #K2-195 # Fluxless, planets: 2
  "K2-196": None, # Fluxless, planets: 1
  "K2-197": None, # Fluxless, planets: 1
  #K2-199 # Fluxless, planets: 2
  "K2-200": None, # Fluxless, planets: 1
  "K2-2016-BLG-0005L": None, # Fluxless, planets: 1
  #K2-201 # Fluxless, planets: 2
  "K2-202": None, # Fluxless, planets: 1
  "K2-203": None, # Fluxless, planets: 1
  "K2-204": None, # Fluxless, planets: 1
  "K2-205": None, # Fluxless, planets: 1
  "K2-206": None, # Fluxless, planets: 1
  "K2-207": None, # Fluxless, planets: 1
  "K2-208": None, # Fluxless, planets: 1
  "K2-209": None, # Fluxless, planets: 1
  "K2-210": None, # Fluxless, planets: 1
  "K2-211": None, # Fluxless, planets: 1
  "K2-212": None, # Fluxless, planets: 1
  "K2-213": None, # Fluxless, planets: 1
  "K2-214": None, # Fluxless, planets: 1
  "K2-215": None, # Fluxless, planets: 1
  "K2-216": None, # Fluxless, planets: 1
  "K2-217": None, # Fluxless, planets: 1
  "K2-218": None, # Fluxless, planets: 1
  "K2-219": { # Fluxless, planets: 3
    "radius": 1.2561700,
    "T": 5712.000,
    "L": Star.LasLog10(0.17994742),
  },
  "K2-220": None, # Fluxless, planets: 1
  "K2-221": None, # Fluxless, planets: 1
  "K2-222": None, # Fluxless, planets: 1
  #K2-223 # Fluxless, planets: 2
  "K2-225": None, # Fluxless, planets: 1
  "K2-226": None, # Fluxless, planets: 1
  "K2-227": None, # Fluxless, planets: 1
  "K2-228": None, # Fluxless, planets: 1
  #K2-229 # Fluxless, planets: 2
  "K2-230": None, # Fluxless, planets: 1
  #K2-282 # Fluxless, planets: 2
  "K2-32": { # Fluxless, planets: 4
    # "radius", RasSun(0.845))
    "T": 5271,
    "L": Star.LasLog10(-0.2960749),
  },
  # #fix("K2-32 b", "GM", MasEarth(2.1))
  # #fix("K2-32 c", "GM", MasEarth(15.0))
  # #fix("K2-32 d", "GM", MasEarth(8.1))
  # #fix("K2-32 e", "GM", MasEarth(6.7))
  "K2-41": None, # Fluxless, planets: 1
  #K2-50 # Fluxless, planets: 2
  "K2-58": { # Fluxless, planets: 3
    #"radius", RasSun(0.8364240))
    "T": 5020.000,
    "L": Star.LasLog10(-0.3976375),
  },
  "K2-61": None, # Fluxless, planets: 1
  #K2-62 # Fluxless, planets: 2
  "K2-65": None, # Fluxless, planets: 1
  "K2-68": None, # Fluxless, planets: 1
  "K2-70": None, # Fluxless, planets: 1
  "K2-73": None, # Fluxless, planets: 1
  "K2-74": None, # Fluxless, planets: 1
  #K2-75 # Fluxless, planets: 2
  "K2-79": None, # Fluxless, planets: 1
  "K2-80": { # Fluxless, planets: 3
    # "radius", RasSun(0.8680660))
    "T": 5203.000,
    "L": Star.LasLog10(-0.3031848),
  },
  "K2-85": None, # Fluxless, planets: 1
  "K2-86": None, # Fluxless, planets: 1
  "K2-97": None, # Fluxless, planets: 1

  # #----------------------------------------------------------------------------

  # #fix("Kepler-186 b", "GM", MasEarth(1.24))
  # #fix("Kepler-186 c", "GM", MasEarth(2.1))
  # #fix("Kepler-186 d", "GM", MasEarth(2.54))
  # #fix("Kepler-186 e", "GM", MasEarth(2.15))
  # #fix("Kepler-186 f", "GM", MasEarth(1.71))

  # #fix("Kepler-22 b", "GM", MasJupiter(0.11))

  # #fix("Kepler-32 b", "GM",  MasJupiter(0.011))
  # #fix("Kepler-32 c", "GM",  MasJupiter(0.012))

  # #fix("Kepler-442 b", "GM", MasEarth(2.3))

  # #fix("Kepler-444 b", "GM", MasEarth(?))
  # #fix("Kepler-444 c", "GM", MasEarth(?))
  # #fix("Kepler-444 d", "GM", MasEarth(0.036))
  # #fix("Kepler-444 e", "GM", MasEarth(0.034))
  # #fix("Kepler-444 f", "GM", MasEarth(?))

  # #fix("Kepler-452 b", "GM", MasEarth(5))

  # #fix("Kepler-62 b", "GM",  MasEarth(2.1))
  # #fix("Kepler-62 c", "GM",  MasEarth(0.1))
  # #fix("Kepler-62 d", "GM",  MasEarth(5.5))
  # #fix("Kepler-62 e", "GM",  MasEarth(4.5))
  # #fix("Kepler-62 f", "GM",  MasEarth(2.8))

  # #fix("Kepler-84 b", "GM",  MasJupiter(0.126))
  # #fix("Kepler-84 c", "GM",  MasJupiter(0.064))
  # #fix("Kepler-84 d", "GM",  MasEarth(?))
  # #fix("Kepler-84 e", "GM",  MasEarth(?))
  # #fix("Kepler-84 f", "GM",  MasEarth(?))

  #Kepler-108 B # Fluxless, planets: 2
  #Kepler-123 # Massless, planets 2
  "Kepler-132": { # Massless, planets 4
    "mass": 1.045000,
    "radius": 1.1156600,
    "T": 5812.0000,
    "L": Star.LasLog10(0.10706269),
  },
  #Kepler-152 # Massless, planets 2
  "Kepler-154": { # Massless, planets 5
    "mass": 1.03,
    "radius": 1.0506,
    "T": 5740.0,
    "L": Star.LasLog10(0.03321742),
  },
  #Kepler-160 # Massless, planets 3
  "Kepler-1663": None, # Massless, planets 1
  "Kepler-1664": None, # Massless, planets 1
  "Kepler-1665": None, # Massless, planets 1
  #Kepler-1666 # Massless, planets 2
  "Kepler-1667": None, # Massless, planets 1
  "Kepler-1668": None, # Massless, planets 1
  "Kepler-1669": None, # Massless, planets 1
  "Kepler-1670": None, # Massless, planets 1
  "Kepler-1671": None, # Massless, planets 1
  "Kepler-1672": None, # Massless, planets 1
  "Kepler-1673": None, # Massless, planets 1
  "Kepler-1674": None, # Massless, planets 1
  "Kepler-1675": None, # Massless, planets 1
  "Kepler-1676": None, # Massless, planets 1
  "Kepler-1677": None, # Massless, planets 1
  "Kepler-1678": None, # Massless, planets 1
  "Kepler-1679": None, # Massless, planets 1
  "Kepler-1680": None, # Massless, planets 1
  "Kepler-1681": None, # Massless, planets 1
  "Kepler-1682": None, # Massless, planets 1
  "Kepler-1683": None, # Massless, planets 1
  "Kepler-1684": None, # Massless, planets 1
  "Kepler-1685": None, # Massless, planets 1
  "Kepler-1686": None, # Massless, planets 1
  "Kepler-1687": None, # Massless, planets 1
  "Kepler-1688": None, # Massless, planets 1
  "Kepler-1689": None, # Massless, planets 1
  "Kepler-1690": None, # Massless, planets 1
  "Kepler-1691": None, # Massless, planets 1
  "Kepler-1692": None, # Massless, planets 1
  "Kepler-1693": None, # Massless, planets 1
  "Kepler-1694": None, # Massless, planets 1
  "Kepler-1695": None, # Massless, planets 1
  "Kepler-1696": None, # Massless, planets 1
  "Kepler-1697": None, # Massless, planets 1
  "Kepler-1698": None, # Massless, planets 1
  "Kepler-1699": None, # Massless, planets 1
  "Kepler-1700": None, # Massless, planets 1
  "Kepler-1701": None, # Massless, planets 1
  "Kepler-1702": None, # Massless, planets 1
  "Kepler-176": { # Massless, planets 4
    "mass": 0.84,
    "radius": 0.821202,
    "T": 5047.0,
    "L": Star.LasLog10(-0.4042719),
  },
  #Kepler-196 # Massless, planets 2
  #Kepler-225 # Massless, planets 2
  #Kepler-248 # Massless, planets 2
  #Kepler-262 # Massless, planets 2
  "Kepler-271": { # Massless, planets 3
    "mass": 1.0,
  },
  #Kepler-274 # Massless, planets 2
  "Kepler-305": { # Massless, planets 4
    "mass": 0.82,
    "radius": 0.827279,
    "T": 4974.0,
    "L": Star.LasLog10(-0.4231784),
  },
  #Kepler-311 # Massless, planets 2
  #Kepler-312 # Massless, planets 2
  #Kepler-315 # Massless, planets 2
  "Kepler-332": { # Massless, planets 3
    "mass": 0.808,
  },
  #Kepler-335 # Massless, planets 2
  #Kepler-340 # Massless, planets 2
  "Kepler-342": { # Massless, planets 4
    "mass": 1.160000,
    "radius": 1.4899400,
    "T": 6139.0900,
    "L": Star.LasLog10(0.4534506),
  },
  #Kepler-343 # Massless, planets 2
  #Kepler-347 # Massless, planets 2
  #Kepler-348 # Massless, planets 2
  "Kepler-351": { # Massless, planets 3
    "mass": 0.91,
  },
  #Kepler-352 # Massless, planets 2
  #Kepler-354 # Massless, planets 3
  "Kepler-359": { # Massless, planets 3
    "mass": 1.140,
  },
  #Kepler-361 # Massless, planets 2
  #Kepler-362 # Massless, planets 2
  #Kepler-365 # Massless, planets 2
  #Kepler-370 # Massless, planets 2
  #Kepler-371 # Massless, planets 2
  "Kepler-385": { # Massless, planets 3
    "mass": 1.120,
  },
  #Kepler-389 # Massless, planets 2
  #Kepler-391 # Massless, planets 2
  #Kepler-392 # Massless, planets 2
  "Kepler-401": { # Massless, planets 3
    "mass": 1.170,
  },
  "Kepler-402": { # Massless, planets 4
    "mass": 1.200000,
    "radius": 1.0872900,
    "T": 6223.390,
    "L": Star.LasLog10(0.20349687),
  },
  "Kepler-403": { # Massless, planets 3
    "mass": 1.250,
  },
  "Kepler-411": { # Fluxless, planets: 4
    "radius": 0.76,
    "T": 4773,
    "L": 0.27,
  },
  "Kepler-42": { # Fluxless, planets: 3
    "radius": 0.175,
    "T": 3269,
    "L": 3.08e-3,
  },
  "Kepler-450 A": { # Fluxless, planets: 3
    "radius": 1.5014101,
    "T": 6396.545,
    "L": Star.LasLog10(0.53147524),
  },
  "Kepler-595": { # Fluxless, planets: 2
    "radius": 0.8210,
    "T": 5138.50,
    "L": Star.LasLog10(-0.3476832),
  },
  "Kepler-82": { # Fluxless, planets: 5
    "radius": 0.955127,
    "T": 5309.190,
    "L": Star.LasLog10(-0.1850697),
  },

  #----------------------------------------------------------------------------

  "KIC 10905746": None, # Fluxless, planets: 1
  "KIC 5095269(AB)": None, # Massless, planets 1
  "KIC 7821010": None, # Massless, planets 1
  "KIC 7917485": None, # Fluxless, planets: 1

  #----------------------------------------------------------------------------

  "KMT-2016-BLG-0212L": None, # Fluxless, planets: 1
  "KMT-2016-BLG-1107L": None, # Fluxless, planets: 1
  "KMT-2016-BLG-1397L": None, # Fluxless, planets: 1
  "KMT-2016-BLG-1820L": None, # Fluxless, planets: 1
  "KMT-2016-BLG-1836L": None, # Fluxless, planets: 1
  "KMT-2016-BLG-2142L": None, # Fluxless, planets: 1
  "KMT-2016-BLG-2364L": None, # Fluxless, planets: 1
  "KMT-2016-BLG-2397L": None, # Fluxless, planets: 1
  "KMT-2016-BLG-2605": None, # Fluxless, planets: 1
  "KMT-2017-BLG-0165L": None, # Fluxless, planets: 1
  "KMT-2017-BLG-0673L": None, # Fluxless, planets: 1
  "KMT-2017-BLG-1038L": None, # Fluxless, planets: 1
  "KMT-2017-BLG-1146L": None, # Fluxless, planets: 1
  #KMT-2017-BLG-2509 # Fluxless, planets: 2
  "KMT-2018-BLG-0029L": None, # Fluxless, planets: 1
  "KMT-2018-BLG-0030": None, # Fluxless, planets: 1
  "KMT-2018-BLG-0087": None, # Fluxless, planets: 1
  "KMT-2018-BLG-0247": None, # Fluxless, planets: 1
  "KMT-2018-BLG-0748L": None, # Fluxless, planets: 1
  "KMT-2018-BLG-1025L": None, # Fluxless, planets: 1
  "KMT-2018-BLG-1292L": None, # Fluxless, planets: 1
  "KMT-2018-BLG-1743": None, # Fluxless, planets: 1
  "KMT-2018-BLG-1976L": None, # Fluxless, planets: 1
  "KMT-2018-BLG-1988L": None, # Fluxless, planets: 1
  "KMT-2018-BLG-1990L": None, # Fluxless, planets: 1
  "KMT-2018-BLG-1996L": None, # Fluxless, planets: 1
  "KMT-2018-BLG-2004": None, # Fluxless, planets: 1
  "KMT-2018-BLG-2602": None, # Fluxless, planets: 1
  "KMT-2018-BLG-2718": None, # Fluxless, planets: 1
  "KMT-2019-BLG-0253": None, # Fluxless, planets: 1
  "KMT-2019-BLG-0371L": None, # Fluxless, planets: 1
  "KMT-2019-BLG-0414L": None, # Fluxless, planets: 1
  "KMT-2019-BLG-0842L": None, # Fluxless, planets: 1
  "KMT-2019-BLG-1042": None, # Fluxless, planets: 1
  "KMT-2019-BLG-1339L": None, # Fluxless, planets: 1
  "KMT-2019-BLG-1552": None, # Fluxless, planets: 1
  "KMT-2019-BLG-1715": None, # Fluxless, planets: 1
  "KMT-2019-BLG-1953L": None, # Fluxless, planets: 1
  "KMT-2019-BLG-2974": None, # Fluxless, planets: 1
  "KMT-2021-BLG-0119L": None, # Fluxless, planets: 1
  "KMT-2021-BLG-0171L": None, # Fluxless, planets: 1
  "KMT-2021-BLG-0240L": None, # Fluxless, planets: 1
  #"KMT-2021-BLG-0240": None, # Fluxless, planets: 2
  "KMT-2021-BLG-0320": None, # Fluxless, planets: 1
  "KMT-2021-BLG-0712": None, # Fluxless, planets: 1
  "KMT-2021-BLG-0748": None, # Fluxless, planets: 1
  "KMT-2021-BLG-0909": None, # Fluxless, planets: 1
  "KMT-2021-BLG-0912": None, # Fluxless, planets: 1
  #KMT-2021-BLG-1077L # Fluxless, planets: 2
  "KMT-2021-BLG-1105": None, # Fluxless, planets: 1
  "KMT-2021-BLG-1253": None, # Fluxless, planets: 1
  "KMT-2021-BLG-1303L": None, # Fluxless, planets: 1
  "KMT-2021-BLG-1303": None, # Fluxless, planets: 1
  "KMT-2021-BLG-1372": None, # Fluxless, planets: 1
  "KMT-2021-BLG-1554L": None, # Fluxless, planets: 1
  "KMT-2021-BLG-1554": None, # Fluxless, planets: 1
  "KMT-2021-BLG-1689L": None, # Fluxless, planets: 1
  "KMT-2021-BLG-1898": None, # Fluxless, planets: 1
  "KMT-2021-BLG-1931": None, # Fluxless, planets: 1
  "KMT-2021-BLG-2478": None, # Fluxless, planets: 1

  #----------------------------------------------------------------------------

  #KOI-12 # Fluxless, planets: 2
  "KOI-1599": { # Fluxless, planets: 2
    "radius": 1.17992,
    "T": 5833.0,
    "L": Star.LasLog10(0.1619642),
  },
  "KOI-1860": { # Fluxless, planets: 4
    #"radius": 1.08916,
    "T": 5620.270,
    "L": Star.LasLog10(0.02790548),
  },
  "KOI-428": None, # Fluxless, planets: 1
  "KOI-7913": None, # Fluxless, planets: 1

  #----------------------------------------------------------------------------

  #LkCa 15 # Fluxless, planets: 3
  "MOA-2007-BLG-192L": None, # Fluxless, planets: 1
  "MOA-2007-BLG-400L": None, # Fluxless, planets: 1
  "MOA-2008-BLG-310L": None, # Fluxless, planets: 1
  "MOA-2008-BLG-379L": None, # Fluxless, planets: 1
  "MOA-2009-BLG-266L": None, # Fluxless, planets: 1
  "MOA-2009-BLG-319L": None, # Fluxless, planets: 1
  "MOA-2009-BLG-387L": None, # Fluxless, planets: 1
  "MOA-2010-BLG-073L": None, # Fluxless, planets: 1
  "MOA-2010-BLG-117L": None, # Fluxless, planets: 1
  "MOA-2010-BLG-311L": None, # Massless, planets 1
  "MOA-2010-BLG-328L": None, # Fluxless, planets: 1
  "MOA-2010-BLG-353L": None, # Fluxless, planets: 1
  "MOA-2010-BLG-477L": None, # Fluxless, planets: 1
  "MOA-2011-BLG-028L": None, # Fluxless, planets: 1
  "MOA-2011-BLG-262L": None, # Fluxless, planets: 1
  "MOA-2011-BLG-291L": None, # Fluxless, planets: 1
  "MOA-2011-BLG-322L": None, # Fluxless, planets: 1
  "MOA-2012-BLG-006L": None, # Fluxless, planets: 1
  "MOA-2012-BLG-505L": None, # Fluxless, planets: 1
  "MOA-2013-BLG-220L": None, # Fluxless, planets: 1
  "MOA-2013-BLG-605L": None, # Fluxless, planets: 1
  "MOA-2014-BLG-472": None, # Fluxless, planets: 1
  "MOA-2015-BLG-337L": None, # Fluxless, planets: 1
  "MOA-2016-BLG-227L": None, # Fluxless, planets: 1
  "MOA-2016-BLG-231": None, # Fluxless, planets: 1
  "MOA-2016-BLG-319L": None, # Fluxless, planets: 1
  "MOA-2020-BLG-135L": None, # Fluxless, planets: 1
  "MOA-2020-BLG-135": None, # Fluxless, planets: 1
  "MOA-bin-1L": None, # Fluxless, planets: 1
  "MOA-bin-29": None, # Fluxless, planets: 1
  "NGC 2423 3": None, # Fluxless, planets: 1
  "NGC 4349 No 127": None, # Fluxless, planets: 1
  "OGLE-2003-BLG-235L": None, # Fluxless, planets: 1
  "OGLE-2005-BLG-071L": None, # Fluxless, planets: 1
  "OGLE-2005-BLG-169L": None, # Fluxless, planets: 1
  "OGLE-2005-BLG-390L": None, # Fluxless, planets: 1
  #"OGLE-2006-BLG-109L": None, # Fluxless, planets: 2
  "OGLE-2007-BLG-368L": None, # Fluxless, planets: 1
  "OGLE-2008-BLG-092L A": None, # Fluxless, planets: 1
  "OGLE-2008-BLG-355L": None, # Fluxless, planets: 1
  "OGLE-2011-BLG-0173L": None, # Fluxless, planets: 1
  "OGLE-2011-BLG-0251L": None, # Fluxless, planets: 1
  "OGLE-2011-BLG-0265L": None, # Fluxless, planets: 1
  #"OGLE-2012-BLG-0026L": None, # Fluxless, planets: 2
  "OGLE-2012-BLG-0358L": None, # Fluxless, planets: 1
  "OGLE-2012-BLG-0406L": None, # Fluxless, planets: 1
  "OGLE-2015-BLG-0563L": None, # Fluxless, planets: 1
  "OGLE-2012-BLG-0724L": None, # Fluxless, planets: 1
  "OGLE-2012-BLG-0838L": None, # Fluxless, planets: 1
  "OGLE-2012-BLG-0950L": None, # Fluxless, planets: 1
  "OGLE-2013-BLG-0102L A": None, # Fluxless, planets: 1
  "OGLE-2013-BLG-0132L": None, # Fluxless, planets: 1
  "OGLE-2013-BLG-0341L B": None, # Fluxless, planets: 1
  "OGLE-2013-BLG-0723L B": None, # Fluxless, planets: 1
  "OGLE-2013-BLG-0911L": None, # Fluxless, planets: 1
  "OGLE-2013-BLG-1721L": None, # Fluxless, planets: 1
  "OGLE-2013-BLG-1761L": None, # Fluxless, planets: 1
  "OGLE-2014-BLG-0124L": None, # Fluxless, planets: 1
  "OGLE-2014-BLG-0319": None, # Fluxless, planets: 1
  "OGLE-2014-BLG-0676L": None, # Fluxless, planets: 1
  #OGLE-2014-BLG-1722L # Fluxless, planets: 2
  "OGLE-2014-BLG-1760L": None, # Fluxless, planets: 1
  "OGLE-2015-BLG-0051L": None, # Fluxless, planets: 1
  "OGLE-2015-BLG-0954L": None, # Fluxless, planets: 1
  "OGLE-2015-BLG-0966L": None, # Fluxless, planets: 1
  "OGLE-2015-BLG-1649L": None, # Fluxless, planets: 1
  "OGLE-2015-BLG-1670L": None, # Fluxless, planets: 1
  "OGLE-2015-BLG-1771L": None, # Fluxless, planets: 1
  "OGLE-2016-BLG-0263L": None, # Fluxless, planets: 1
  "OGLE-2016-BLG-1067L": None, # Fluxless, planets: 1
  "OGLE-2016-BLG-1093L": None, # Fluxless, planets: 1
  "OGLE-2016-BLG-1190L": None, # Fluxless, planets: 1
  "OGLE-2016-BLG-1195L": None, # Fluxless, planets: 1
  "OGLE-2016-BLG-1227L": None, # Fluxless, planets: 1
  "OGLE-2016-BLG-1928": None, # Massless, planets 1
  "OGLE-2017-BLG-0114": None, # Massless, planets 1
  "OGLE-2017-BLG-0173L": None, # Fluxless, planets: 1
  "OGLE-2017-BLG-0373L": None, # Fluxless, planets: 1
  "OGLE-2017-BLG-0406L": None, # Fluxless, planets: 1
  "OGLE-2017-BLG-0482L": None, # Fluxless, planets: 1
  "OGLE-2017-BLG-0604L": None, # Fluxless, planets: 1
  "OGLE-2017-BLG-1049": None, # Fluxless, planets: 1
  "OGLE-2017-BLG-1099": None, # Fluxless, planets: 1
  "OGLE-2017-BLG-1140L": None, # Fluxless, planets: 1
  "OGLE-2017-BLG-1375L": None, # Fluxless, planets: 1
  "OGLE-2017-BLG-1434L": None, # Fluxless, planets: 1
  "OGLE-2017-BLG-1522L": None, # Fluxless, planets: 1
  "OGLE-2017-BLG-1691L": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-0298": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-0383": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-0506": None, # Fluxless, planets: 1
  "OGLE--2018-BLG-0516": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-0567L": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-0596L": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-0677L": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-0740L": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-0799": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-0962L": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-0977": None, # Fluxless, planets: 1
  #"OGLE-2018-BLG-1011L": None, # Fluxless, planets: 2
  "OGLE-2018-BLG-1119": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-1185": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-1269L": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-1428L": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-1544": None, # Fluxless, planets: 1
  "OGLE-2018-BLG-1700L": None, # Fluxless, planets: 1
  #OGLE-2019-BLG-0468L # Fluxless, planets: 2
  "OGLE-2019-BLG-0954L": None, # Fluxless, planets: 1
  "OGLE-2019-BLG-0960": None, # Fluxless, planets: 1
  "OGLE-2019-BLG-1470LAB": None, # Fluxless, planets: 1
  "OGLE-2019-BLG-1492": None, # Fluxless, planets: 1
  "Oph 11 A": None, # Fluxless, planets: 1
  #PDS 70 # Massless, planets 2
  "Psi-1 Draconis B": None, # Fluxless, planets: 1
  "PSR 1257+12": None, # Pulsar / Fluxless, planets: 3
  "PSR B0329+54": None, # Fluxless, planets: 1
  "PSR J1311-3430": None, # Massless, planets 1
  "PSR J1719-1438": None, # Fluxless, planets: 1
  "PSR J2322-2650": None, # Fluxless, planets: 1
  "ROXs 12": None, # Fluxless, planets: 1
  "Sand 178": None, # Massless, planets 1
  "SAND978": None, # Fluxless, planets: 1
  "SWEEPS-11": None, # Fluxless, planets: 1
  "SWEEPS-4": None, # Fluxless, planets: 1
  "TAP 26": None, # Fluxless, planets: 1
  "TCP J05074264+2447555L": None, # Fluxless, planets: 1

  #----------------------------------------------------------------------------

  "TOI-1246": { # Massless, planets 4
    "mass": 0.868000,
    "radius": 0.876154,
    "T": 5141.000,
    "L": Star.LasLog10(-0.3159538),
  },
  "TOI-1272": { # Massless, planets 2
    "mass": 0.8250000,
    "radius": 0.8090320,
    "T": 4987.0000,
    "L": Star.LasLog10(-0.4380164),
  },
  "TOI-1430": None, # Massless, planets 1
  "TOI-1683": None, # Massless, planets 1
  "TOI-178": { # Massless, planets 6
    "mass": 0.650,
    "radius": 0.651,
    "L": 0.132,
    "T": 4316,
  },
  "TOI-203": None, # Massless, planets 1
  "TOI-2236": None, # Massless, planets 1
  "TOI-2421": None, # Massless, planets 1
  "TOI-2567": None, # Massless, planets 1
  "TOI-3540": None, # Massless, planets 1
  "TOI-3693": None, # Massless, planets 1
  "TOI-4137": None, # Massless, planets 1
  "TOI-4138": None, # Fluxless, planets: 1

  #----------------------------------------------------------------------------

  "TVLM 513-46546": None, # Fluxless, planets: 1
  "TYC 8998-760-1": None, # Fluxless, planets: 2
  "TYC 9486-927-1": None, # Fluxless, planets: 1
  "UKIRT-2017-BLG-001L": None, # Fluxless, planets: 1
  "ups Leo": None, # Massless, planets 1
  "USco1556 A": None, # Fluxless, planets: 1
  "USco1621 A": None, # Fluxless, planets: 1
  "UScoCTIO 108": None, # Fluxless, planets: 1
  "UZ For (AB)": None, # Fluxless, planets: 1
  "V1298 Tau": { # Fluxless, planets: 4
    "T": 4970 - 70,
    "L": 0.934,
  },
  "WASP-119": None, # Fluxless, planets: 1
  "WASP-124": None, # Fluxless, planets: 1
  "WASP-129": None, # Fluxless, planets: 1
  "WASP-133": None, # Fluxless, planets: 1
  "WASP-180 A": None, # Fluxless, planets: 1
  "WD 0806-661": None, # Fluxless, planets: 1
  "WISEA J083011.95+283716.0": None, # Massless, planets 1
  "WISE J1355-8258": None, # Fluxless, planets: 1
  "WISE J2216+1952": None, # Massless, planets 1
  "Wolf 359": { # Massless, planets 2
    "mass": 0.110,
    "radius": 0.144,
    "L": 0.00106,
    "T": 2749,
  },
  "YBP401": None, # Fluxless, planets: 1
}
