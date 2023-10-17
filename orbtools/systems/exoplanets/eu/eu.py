
import csv

def getRows():
  with open("./orbtools/systems/exoplanets/eu/exoplanet.eu_catalog.csv", newline='') as csvfile:
    rows = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
  return rows[1:]

def extractRow(row):
  planet_data = {
    "name": row[0],
    "status": row[1],
    "mass": row[2],
    #"mass_error_min": row[3],
    #"mass_error_max": row[4],
    #"mass_sini": row[5],
    #"mass_sini_error_min": row[6],
    #"mass_sini_error_max": row[7],
    "radius": row[8],
    #"radius_error_min": row[9],
    #"radius_error_max": row[10],
    "orbital_period": row[11],
    #"orbital_period_error_min": row[12],
    #"orbital_period_error_max": row[13],
    "semi_major_axis": row[14],
    #"semi_major_axis_error_min": row[15],
    #"semi_major_axis_error_max": row[16],
    #"eccentricity": row[17],
    #"eccentricity_error_min": row[18],
    #"eccentricity_error_max": row[19],
    #"inclination": row[20],
    #"inclination_error_min": row[21],
    #"inclination_error_max": row[22],
    #"angular_distance": row[23],
    "discovered": row[24],
    #"updated": row[25],
    #"omega": row[26],
    #"omega_error_min": row[27],
    #"omega_error_max": row[28],
    #"tperi": row[29],
    #"tperi_error_min": row[30],
    #"tperi_error_max": row[31],
    #"tconj": row[32],
    #"tconj_error_min": row[33],
    #"tconj_error_max": row[34],
    #"tzero_tr": row[35],
    #"tzero_tr_error_min": row[36],
    #"tzero_tr_error_max": row[37],
    #"tzero_tr_sec": row[38],
    #"tzero_tr_sec_error_min": row[39],
    #"tzero_tr_sec_error_max": row[40],
    #"lambda_angle": row[41],
    #"lambda_angle_error_min": row[42],
    #"lambda_angle_error_max": row[43],
    #"impact_parameter": row[44],
    #"impact_parameter_error_min": row[45],
    #"impact_parameter_error_max": row[46],
    #"tzero_vr": row[47],
    #"tzero_vr_error_min": row[48],
    #"tzero_vr_error_max": row[49],
    #"k": row[50],
    #"k_error_min": row[51],
    #"k_error_max": row[52],
    #"temp_calculated": row[53],
    #"temp_calculated_error_min": row[54],
    #"temp_calculated_error_max": row[55],
    "T": row[56],
    #"hot_point_lon": row[57],
    #"geometric_albedo": row[58],
    #"geometric_albedo_error_min": row[59],
    #"geometric_albedo_error_max": row[60],
    #"log_g": row[61],
    #"publication": row[62],
    "detection_type": row[63],
    #"mass_detection_type": row[64],
    #"radius_detection_type": row[65],
    #"alternate_names": row[66],
    #"molecules": row[67],
  }

  #-----------------------------------------------------------------------------
  # Extract star data
  #-----------------------------------------------------------------------------

  star_data = {
    "name": row[68],
    #"ra": row[69],
    #"dec": row[70],
    #"mag_v": row[71],
    #"mag_i": row[72],
    #"mag_j": row[73],
    #"mag_h": row[74],
    #"mag_k": row[75],
    "distance": row[76],
    #"distance_error_min": row[77],
    #"distance_error_max": row[78],
    #"metallicity": row[79],
    #"metallicity_error_min": row[80],
    #"metallicity_error_max": row[81],
    "mass": row[82],
    #"mass_error_min": row[83],
    #"mass_error_max": row[84],
    "radius": row[85],
    #"radius_error_min": row[86],
    #"radius_error_max": row[87],
    "sp_type": row[88],
    #"age": row[89],
    #"age_error_min": row[90],
    #"age_error_max": row[91],
    "T": row[92],
    #"teff_error_min": row[93],
    #"teff_error_max": row[94],
    #"detected_disc": row[95],
    #"magnetic_field": row[96],
    #"alternate_names": row[97],
    "L": "",
  }

  return planet_data, star_data

################################################################################
#
# Fixes & skips for EU exoplanet catalog. See:
#
# https://exoplanet.eu/catalog/#downloads-section
#
################################################################################

from orbtools import *

#-------------------------------------------------------------------------------

fixes = {

  "Sun": None, # Comes from Solar System data

  #----------------------------------------------------------------------------
  # Unfixable
  #----------------------------------------------------------------------------

  "2MASS J1450-7841 A": None, # duplicate
  "2MASS J1450-7841 B": None, # duplicate
  "G 196-3 b": None, # no orbital parameters
  "GD 140 b": None, # no orbital parameters
  "[GKH94]41": None, # Star & planet with same name / massless star
  "GSC 08047-00232 b": None, # no orbital parameters
  "HD 167665": None, # Star & planet with same name / massless star

  #----------------------------------------------------------------------------

  #fix("Rigel A", "T", 12100)
  #fix("Betelgeuse", "T", 3600)

  #stars["16 Cygni C"].radius =
  #stars["16 Cygni C"].T =
  #stars["16 Cygni C"].L =

  "1RXS J0342.5+1216": None, # massless: 1RXS J0342.5+1216 b
  "2M0838+15": None, # massless: "2M0838+15 b", "2M0838+15 c",
  "2M 1252+2735": None, # massless: "2M 1252+2735 b",
  "2M 1253+2734": None, # "2M 1253+2734 b",
  "2M 1258+2630": None, # "2M 1258+2630 b",
  "2MASS 1534-29": None, # "2MASS 1534-29 b",
  "2MASS J0850+1057": None, # "2MASS J0850+1057 b",
  "2MASS J1119-1137": None, # "2MASS J1119-1137 b",
  "2MASS J1155-7919": None, # "2MASS J1155-7919 b",
  "2MASS J155947+440359": None, # "2MASS J155947+440359 b",
  "2MASS J13243553+6358281": None, #Skipping: J1324+63 @ 2MASS J13243553+6358281 - massless star
  "2MASS J2250+2325": None, # "2MASS J2250+2325 b",

  "51 Eri": {
    "T": 7331,
    "L": 6.7,
  },

  "AB Pic": None, # "AB Pic b",
  "BD+45 564": None, # "BD+45 564 b",
  "BD+55 362": None, # "BD+55 362 b",
  "BD+63 1405": None, # "BD+63 1405 b",
  "CFBDSIR J2149-0403": None, # "CFBDSIR J2149-0403 b",
  "COCONUTS-3": None, # "COCONUTS-3 b",
  "CoRoT-15": None, # "CoRoT-15 b",
  "CT Cha": None, # "CT Cha b",
  "DE CVn": None, # "DE CVn b",
  "DW Lyn": None, # "DW Lyn b",
  "DW Uma": None, # "DW Uma b",
  "EPIC 201170410": None, # "EPIC 201170410 b",
  "EPIC 201757695": None, # "EPIC 201757695 b",
  "EPIC 206061524": None, # "EPIC 206061524 b",
  #fix("EPIC 211089792", "T", 5387.060)
  #fix("EPIC 211089792", "L", Star.LasLog10(-0.2953329))
  "Gaia14aae": None, # "Gaia14aae b",
  "gam Psc": None, # "gam Psc b",

  "BD-00 4475": {
    "mass": 0.810,
    "radius": None,
    "T": 5040,
  },

  #----------------------------------------------------------------------------

  #fix("GJ 229", "radius", RasSun(0.69))
  #fix("GJ 229", "T", 3700)
  #fix("GJ 229", "L", 0.0430)

  #fix("GJ 27.1", "radius", RasSun(0.5188870))
  #fix("GJ 27.1", "T", 3687.0)
  #fix("GJ 27.1", "L", Star.LasLog10(-1.34847))

  #fix("GJ 3082", "radius", RasSun(0.4652160))
  #fix("GJ 3082", "T", 3910.0)
  #fix("GJ 3082", "L", Star.LasLog10(-1.46273))

  #fix("GJ 3090", "sptype", "M2V")

  #fix("GJ 317", "radius", RasSun(0.4170))
  #fix("GJ 317", "T", 3510)
  #fix("GJ 317", "L", 0.02175)

  #fix("GJ 433", "radius", RasSun(0.529))
  #fix("GJ 433", "T", 3445)
  #fix("GJ 433", "L", 0.034)

  #fix("GJ 687", "radius", RasSun(0.492))
  #fix("GJ 687", "T", 3095)
  #fix("GJ 687", "L", 0.0213)

  #fix("GJ 9066", "radius", RasSun(0.164))
  #fix("GJ 9066", "T", 3154)
  #fix("GJ 9066", "L", Star.LasLog10(-2.60))

  #fix("GJ 96", "radius", RasSun(0.5806120))
  #fix("GJ 96", "T", 3782.0)
  #fix("GJ 96", "L", Star.LasLog10(-1.20665))

  #fix("Gliese 1002", "radius", RasSun(0.137))
  #fix("Gliese 1002", "T", 3024)
  #fix("Gliese 1002", "L", 0.001406)

  #Planet("Gliese 1002 a", MasEarth(1.08), orbit = Orbit("Gliese 1002", AU2m(0.0457)))
  #Planet("Gliese 1002 b", MasEarth(1.36), orbit = Orbit("Gliese 1002", AU2m(0.0738)))

  #fix("Gliese 221", "radius", RasSun(0.613))
  #fix("Gliese 221", "T", 4324)
  #fix("Gliese 221", "L", 0.001406)

  #fix("Gliese 328", "radius", RasSun(???))
  #fix("Gliese 328", "T", 3989)
  #fix("Gliese 328", "L", 0.10)

  #fix("Gliese 649", "radius", RasSun(0.531))
  #fix("Gliese 649", "T", 3621)
  #fix("Gliese 649", "L", 0.04373)

  #fix("Gliese 674", "radius", RasSun(0.361))
  #fix("Gliese 674", "T", 3404)
  #fix("Gliese 674", "L", 0.01575)

  #fix("Gliese 676 A", "radius", RasSun(0.617))
  #fix("Gliese 676 A", "T", 4014)
  #fix("Gliese 676 A", "L", 0.08892)

  "GJ 1002": {
    "mass": 0.120,
    "radius": 0.137,
    "T": 3024,
  },
  "GJ 163": {
    "radius": 0.409,
    "T": 3460,
    "L": 0.02163,
  },
  "GJ 176": {
    "T": 3632,
    "L": 0.03516,
  },
  "GJ 180": {
    "radius": 0.4229,
    "T": 3634,
    "L": 0.02427,
  },
  "GJ 2030": {
    "mass": 0.96,
    "radius": 2.2410400,
    "T": 5485,
    "L": Star.LasLog10(0.61229940),
  },
  "GJ 2056": {
    "mass": 0.62,
    "radius": 0.68,
    "T": 4017,
  },
  "GJ 480": {
    "mass": 0.41,
    "radius": 0.52,
    "T": 3350,
  },
  "GJ 740": {
    "mass": 0.58,
    "radius": 0.56,
    "T": 3913,
  },

  #----------------------------------------------------------------------------

  #fix("HD 158259", "radius", RasSun(???))
  #fix("HD 158259", "T", 6068)
  #fix("HD 158259", "L", 1.6)

  #fix("HD 159868", "radius", RasSun(1.97))
  #fix("HD 159868", "T", 5558)
  #fix("HD 159868", "L", 3.59)

  #fix("HD 163296", "radius", RasSun(???))
  #fix("HD 163296", "T", ???)
  #fix("HD 163296", "L", ???)

  #fix("HD 181433", "radius", RasSun(0.8108410))
  #fix("HD 181433", "T", 4929.630)
  #fix("HD 181433", "L", Star.LasLog10(-0.4561762))

  #fix("HD 204313", "radius", RasSun(1.08))
  #fix("HD 204313", "T", 5783)
  #fix("HD 204313", "L", 1.18)

  #fix("HD 20794", "radius", RasSun(0.92))
  #fix("HD 20794", "T", 5401)
  #fix("HD 20794", "L", 0.74)

  #fix("HD 27894", "T", 4920)

  #fix("HD 40307", "radius", RasSun(0.716))
  #fix("HD 40307", "T", 4977)
  #fix("HD 40307", "L", 0.23)

  #fix("HD 80653", "T", 5910.000)
  #fix("HD 80653", "L", Star.LasLog10(0.24))

  "HD 10975": None, # "HD 10975 b",
  #fix("HD 110113 b", "GM", MasEarth(4.55))
  "HD 1160": None, # "HD 1160 b",
  "HD 118865 A": None, #"HD 118865 B",
  "HD 124330": None, #"HD 124330 b",
  "HD 126525": None, #"HD 126525 b",

  "HD 130948 B": None, #"HD 130948 B b",
  "HD 134060": None, #"HD 134060 b", "HD 134060 c",

  "HD 134606": {
    "mass": 0.998,
    "T": 5614,
    "L": 1.25,
    "radius": RtoSun(Star.LTtoR(1.25, 5614)),
  },
  "HD 136352": {
    "mass": 0.87,
    "radius": 1.058,
    "T": 5664,
    "L": Star.LasLog10(0.01620),
  },

  "HD 136925": None, #"HD 136925 b",
  "HD 137496": None, #"HD 137496 b", "HD 137496 c",
  "HD 13808": None, #"HD 13808 b", "HD 13808 c",
  "HD 150433": None, #"HD 150433 b",
  "HD 154088": None, #"HD 154088 b",
  "HD 155193": None, #"HD 155193 b",
  "HD 157172": None, #"HD 157172 b",
  "HD 161178": None, #"HD 161178 b",
  "HD 166724": None, #"HD 166724 b",
  "HD 184601": None, #"HD 184601 b",
  "HD 189567": None, #"HD 189567 b", "HD 189567 c",
  "HD 195689": None, # Skipping: KELT-9 b - massless star
  "HD 196067": None, #"HD 196067 b",

  "HD 20003": None, #"HD 20003 b", "HD 20003 c",
  "HD 205521": None, #"HD 205521 b",
  "HD 20781": {
    "mass": 0.7,
    "T": 5256,
    "L": 0.49,
    "radius": RtoSun(Star.LTtoR(0.49, 5256)),
  },
  "HD 213472": None, #"HD 213472 b",
  "HD 215456": None, #"HD 215456 b", "HD 215456 c",
  "HD 21693": None, #"HD 21693 b", "HD 21693 c",
  "HD 219139": None, #"HD 219139 b",
  "HD 220689": None, #"HD 220689 b",
  "HD 26161": None, #"HD 26161 b",
  "HD 27631": None, #"HD 27631 b",
  "HD 31527": {
    "mass": 1.070000,
    "radius": 1.0773600,
    "T": 5909.59,
    "L": Star.LasLog10(0.10564369),
  },
  "HD 331093": None, # HD 331093 b
  "HD 360": None, # HD 360 b
  "HD 38858": None, # HD 38858 b
  "HD 39194": { # HD 39194 b, 39194 c, 39194 d
    "mass": 0.71,
    "radius": 0.74,
    "L": 0.389,
    "T": 5205,
  },
  "HD 45184": { # HD 45184 b, HD 45184 c
    "mass": 1.08,
    "radius": 1.05,
    "L": 1.178,
    "T": 5862,
  },
  "HD 46588 c": None, # - no orbital parameters
  "HD 51608": { # HD 51608 b, HD 51608 c
    "T": 5352.6,
    "L": Star.LasLog10(-0.2059246),
    "mass": 0.9300000,
    "radius": 0.9174040,
  },

  "HD 5433": None, # HD 5433 b  - massless star
  "HD 6860": None, # HD 6860 b @  - massless star
  "HD 74014": None, # HD 74014 b @  - massless star
  "HD 79181": None, # HD 79181 b @  - massless star
  "HD 80869": {
    "T": 5837, # 58.37
  },
  "HD 93385 A": { # HD 93385 A b, c, d
    "mass": 1.07,
    "radius": 1.17,
    "L": 1.42,
    "T": 5823,
  },
  "HD 96700": { # HD 96700 b, c, d
    "mass": 0.96,
    "radius": 0.96,
    "T": 5879,
    "L": Star.TtoL(5879, RasSun(0.96)),
  },
  "HD 99283": None, #HD 99283 b @ HD 99283 - massless star

  "HII 1348": None, #Skipping: HII 1348 b @ HII 1348 - massless star
  "HIP 107772": None, #Skipping: HIP 107772 b @ HIP 107772 - massless star
  "HIP 38594": None, #Skipping: HIP 38594 b, HIP 38594 c - massless star
  "HIP 38939 A": None, #Skipping: HIP 38939 B @ HIP 38939 A - massless star
  #fix("HIP 41378 b", "GM", MasEarth(6.89))
  #fix("HIP 41378 c", "GM", MasEarth(4.4))
  #fix("HIP 41378 d", "GM", MasEarth(4.6))
  #fix("HIP 41378 e", "GM", MasEarth(12))
  #fix("HIP 41378 f", "GM", MasEarth(12))
  "HIP 4845": None, #Skipping: HIP 4845 b @ HIP 4845 - massless star
  "HIP 48714": None, #Skipping: HIP 48714 b @ HIP 48714 - massless star
  "HIP 75056": None, #Skipping: HIP 75056 b @ HIP 75056 - massless star
  "HIP 77900": None, #Skipping: HIP 77900 b @ HIP 77900 - massless star
  "HIP 79098 (AB)": None, #Skipping: HIP 79098 (AB) b @ HIP 79098 (AB) - massless star
  "HR 3549": None, #Skipping: HR 3549 b @ HR 3549 - massless star
  "HR 7329": None, #Skipping: HR 7329 B @ HR 7329 - massless star
  "HR 7672": None, #Skipping: HR 7672 b @ HR 7672 - massless star
  "IM Lup": None, #Skipping: IM Lup b @ IM Lup - massless star
  "ISO-Oph176": None, #Skipping: ISO-Oph176 @ ISO-Oph176 - massless star

  #----------------------------------------------------------------------------

  #fix("K2-16", "radius", RasSun(0.703181))
  #fix("K2-16", "T", 4627.07)
  #fix("K2-16", "L", Star.LasLog10(-0.689946))

  #fix("K2-165", "radius", RasSun(0.8376060))
  #fix("K2-165", "T", 5141.6700)
  #fix("K2-165", "L", Star.LasLog10(-0.3548089))

  #fix("K2-183", "radius", RasSun(0.87))
  #fix("K2-183", "T", 5482)
  #fix("K2-183", "L", Star.LasLog10(-0.1317863))

  #fix("K2-187", "radius", RasSun(0.894913))
  #fix("K2-187", "T", 5477)
  #fix("K2-187", "L", Star.LasLog10(-0.1960678))

  #fix("K2-219", "radius", RasSun(1.2561700))
  #fix("K2-219", "T", 5712.000)
  #fix("K2-219", "L", Star.LasLog10(0.17994742))

  #fix("K2-32", "radius", RasSun(0.845))
  #fix("K2-32", "T", 5271)
  #fix("K2-32", "L", Star.LasLog10(-0.2960749))

  #fix("K2-58", "radius", RasSun(0.8364240))
  #fix("K2-58", "T", 5020.000)
  #fix("K2-58", "L", Star.LasLog10(-0.3976375))

  #fix("K2-80", "radius", RasSun(0.8680660))
  #fix("K2-80", "T", 5203.000)
  #fix("K2-80", "L", Star.LasLog10(-0.3031848))

  #fix("K2-138 b", "GM", MasEarth(3.1))
  #fix("K2-138 c", "GM", MasEarth(6.3))
  #fix("K2-138 d", "GM", MasEarth(7.9))
  #fix("K2-138 e", "GM", MasEarth(13.0))
  #fix("K2-138 f", "GM", MasEarth(8.7))
  #fix("K2-138 g", "GM", MasEarth(8.94))

  #fix("K2-32 b", "GM", MasEarth(2.1))
  #fix("K2-32 c", "GM", MasEarth(15.0))
  #fix("K2-32 d", "GM", MasEarth(8.1))
  #fix("K2-32 e", "GM", MasEarth(6.7))

  "K2-352": {
    "mass": 0.980,
    "radius": 0.95,
    "T": 5791,
    "L": Star.LasLog10(-0.06325590),
  },

  "K2-416": None, #Skipping: K2-416 b @ K2-416 - massless star
  "K2-417": None, #Skipping: K2-417 b @ K2-417 - massless star

  #----------------------------------------------------------------------------

  #stars["Kepler-108 B"].radius = RasSun()
  #fix("Kepler-108 B", "T", 5584.260)
  #stars["Kepler-108 B"].L =

  #fix("Kepler-411", "radius", RasSun(0.76))
  #fix("Kepler-411", "T", 4773)
  #fix("Kepler-411", "L", 0.27)

  #fix("Kepler-42", "radius", RasSun(0.175))
  #fix("Kepler-42", "T", 3269)
  #fix("Kepler-42", "L", 3.08e-3)

  #fix("Kepler-450 A", "radius", RasSun(1.600))
  #fix("Kepler-450 A", "T", 6298)
  #fix("Kepler-450 A", "L", Star.LasLog10(0.53147524))

  #fix("Kepler-595", "radius", RasSun(1.600))
  #fix("Kepler-595", "T", 5138.50)
  #fix("Kepler-595", "L", Star.LasLog10(-0.3476832))

  #fix("Kepler-82", "radius", RasSun(0.955127))
  #fix("Kepler-82", "T", 5309.190)
  #fix("Kepler-82", "L", Star.LasLog10(-0.1850697))

  #fix("Kepler-186 b", "GM", MasEarth(1.24))
  #fix("Kepler-186 c", "GM", MasEarth(2.1))
  #fix("Kepler-186 d", "GM", MasEarth(2.54))
  #fix("Kepler-186 e", "GM", MasEarth(2.15))
  #fix("Kepler-186 f", "GM", MasEarth(1.71))

  #fix("Kepler-22 b", "GM", MasJupiter(0.11))

  #fix("Kepler-32 b", "GM",  MasJupiter(0.011))
  #fix("Kepler-32 c", "GM",  MasJupiter(0.012))

  #fix("Kepler-442 b", "GM", MasEarth(2.3))

  #fix("Kepler-444 b", "GM", MasEarth(?))
  #fix("Kepler-444 c", "GM", MasEarth(?))
  #fix("Kepler-444 d", "GM", MasEarth(0.036))
  #fix("Kepler-444 e", "GM", MasEarth(0.034))
  #fix("Kepler-444 f", "GM", MasEarth(?))

  #fix("Kepler-452 b", "GM", MasEarth(5))

  #fix("Kepler-62 b", "GM",  MasEarth(2.1))
  #fix("Kepler-62 c", "GM",  MasEarth(0.1))
  #fix("Kepler-62 d", "GM",  MasEarth(5.5))
  #fix("Kepler-62 e", "GM",  MasEarth(4.5))
  #fix("Kepler-62 f", "GM",  MasEarth(2.8))

  #fix("Kepler-84 b", "GM",  MasJupiter(0.126))
  #fix("Kepler-84 c", "GM",  MasJupiter(0.064))
  #fix("Kepler-84 d", "GM",  MasEarth(?))
  #fix("Kepler-84 e", "GM",  MasEarth(?))
  #fix("Kepler-84 f", "GM",  MasEarth(?))

  "Kepler-110": None, # Kepler-110 b, c - massless star
  "Kepler-111": None, # Kepler-111 b, c - massless star
  "Kepler-112": None, # Kepler-112 b, c - massless star
  "Kepler-119": None, # Kepler-119 b, c - massless star
  "Kepler-120": None, # Kepler-120 b, c - massless star
  "Kepler-121": None, # Kepler-121 b, c - massless star
  "Kepler-124": None, # Kepler-124 b, c, d - massless star
  "Kepler-126": None, # Kepler-126 b, c, d - massless star
  "Kepler-127": None, # Kepler-127 b, c, d - massless star
  "Kepler-132": None, # Kepler-132 b, c, d, e - massless star
  "Kepler-133": None, # Kepler-133 b, c - massless star
  "Kepler-134": None, # Kepler-134 b, c - massless star
  "Kepler-135": None, # Kepler-135 b, c - massless star
  "Kepler-137": None, # Kepler-137 b, c - massless star
  "Kepler-140": None, # Kepler-140 b, c - massless star
  "Kepler-143": None, # Kepler-143 b, c - massless star
  "Kepler-148": None, # Kepler-148 b, c, d - massless star
  "Kepler-149": None, # Kepler-149 b, c, d - massless star
  "Kepler-150": None, # Kepler-150 b, c, d, e, f - massless star
  "Kepler-152": None, # Kepler-152 b, c - massless star
  "Kepler-153": None, # Kepler-153 b, c - massless star
  "Kepler-156": None, # Kepler-156 b, c - massless star
  "Kepler-157": None, # Kepler-157 b, c, d - massless star
  "Kepler-158": None, # Kepler-158 b, c - massless star
  "Kepler-159": None, # Kepler-159 b, c - massless star
  "Kepler-160": None, # Kepler-160 b, c, d - massless star
  "Kepler-162": None, # Kepler-162 b, c - massless star
  "Kepler-165": None, # Kepler-165 b, c - massless star
  "Kepler-1663": None, # Kepler-1663 b - massless star
  "Kepler-166": None, # Kepler-166 b, c, d - massless star
  "Kepler-168": None, # Kepler-168 b, c - massless star
  "Kepler-170": None, # Kepler-170 b, c - massless star
  "Kepler-171": None, # Kepler-171 b, c, d - massless star
  "Kepler-174": None, # Kepler-174 b, c, d - massless star
  "Kepler-176": None, # Kepler-176 b, c, d, e - massless star
  "Kepler-178": None, # Kepler-178 b, c, d - massless star
  "Kepler-179": None, # Kepler-179 b, c - massless star
  "Kepler-181": None, # Kepler-181 b, c - massless star
  "Kepler-183": None, # Kepler-183 b, c - massless star
  "Kepler-184": None, # Kepler-184 b, c, d - massless star
  "Kepler-188": None, # Kepler-188 b, c - massless star
  "Kepler-192": None, # Kepler-192 b, c, d - massless star
  "Kepler-193": None, # Kepler-193 b, c - massless star
  "Kepler-194": None, # Kepler-194 b, c, d - massless star
  "Kepler-195": None, # Kepler-195 b, c - massless star
  "Kepler-196": None, # Kepler-196 b, c - massless star
  "Kepler-197": None, # Kepler-197 b, c, d, e - massless star
  "Kepler-199": None, # Kepler-199 b, c - massless star
  "Kepler-200": None, # Kepler-200 b, c - massless star
  "Kepler-202": None, # Kepler-202 b, c - massless star
  "Kepler-205": None, # Kepler-205 b, c - massless star
  "Kepler-207": None, # Kepler-207 b, c, d - massless star
  "Kepler-209": None, # Kepler-209 b, c - massless star
  "Kepler-214": None, # Kepler-214 b, c - massless star
  "Kepler-216": None, # Kepler-216 b, c - massless star
  "Kepler-217": None, # Kepler-217 b, c, d - massless star
  "Kepler-218": None, # Kepler-218 b, c, d - massless star
  "Kepler-219": None, # Kepler-219 b, c, d - massless star
  "Kepler-220": None, # Kepler-220 b, c, d, e - massless star
  "Kepler-222": None, # Kepler-222 b, c, d - massless star
  "Kepler-225": None, # Kepler-225 b, c - massless star
  "Kepler-227": None, # Kepler-227 b, c - massless star
  "Kepler-228": None, # Kepler-228 b, c, d - massless star
  "Kepler-229": None, # Kepler-229 b, c, d - massless star
  "Kepler-230": None, # Kepler-230 b, c - massless star
  "Kepler-232": None, # Kepler-232 b, c - massless star
  "Kepler-233": None, # Kepler-233 b, c - massless star
  "Kepler-234": None, # Kepler-234 b, c - massless star
  "Kepler-240": None, # Kepler-240 b, c - massless star
  "Kepler-241": None, # Kepler-241 b, c - massless star
  "Kepler-242": None, # Kepler-242 b, c - massless star
  "Kepler-244": None, # Kepler-244 b, c, d - massless star
  "Kepler-248": None, # Kepler-248 b, c - massless star
  "Kepler-249": None, # Kepler-249 b, c, d - massless star
  "Kepler-253": None, # Kepler-253 b, c, d - massless star
  "Kepler-254": None, # Kepler-254 b, c, d - massless star
  "Kepler-257": None, # Kepler-257 b, c, d - massless star
  "Kepler-259": None, # Kepler-259 b, c - massless star
  "Kepler-262": None, # Kepler-262 b, c - massless star
  "Kepler-263": None, # Kepler-263 b, c - massless star
  "Kepler-268": None, # Kepler-268 b, c - massless star
  "Kepler-270": None, # Kepler-270 b, c - massless star
  "Kepler-273": None, # Kepler-273 b, c - massless star
  "Kepler-274": None, # Kepler-274 b, c - massless star
  "Kepler-278": None, # Kepler-278 b, c - massless star
  "Kepler-283": None, # Kepler-283 b, c - massless star
  "Kepler-284": None, # Kepler-284 b, c - massless star
  "Kepler-286": None, # Kepler-286 b, c, d, e - massless star
  "Kepler-287": None, # Kepler-287 b, c - massless star
  "Kepler-290": None, # Kepler-290 b, c - massless star
  "Kepler-294": None, # Kepler-294 b, c - massless star
  "Kepler-295": None, # Kepler-295 b, c, d - massless star
  "Kepler-297": None, # Kepler-297 b, c - massless star
  "Kepler-302": None, # Kepler-302 b, c - massless star
  "Kepler-308": None, # Kepler-308 b, c - massless star
  "Kepler-309": None, # Kepler-309 b, c - massless star
  "Kepler-320": None, # Kepler-320 b, c - massless star
  "Kepler-397": None, # Kepler-397 b, c - massless star
  "Kepler-398": None, # Kepler-398 b, c, d - massless star
  "Kepler-399": None, # Kepler-399 b, c, d - massless star
  "Kepler-400": None, # Kepler-400 b, c - massless star
  "Kepler-401": None, # Kepler-401 b, c, d - massless star
  "Kepler-402": None, # Kepler-402 b, c, d, e - massless star
  "Kepler-403": None, # Kepler-403 b, c, d - massless star
  "Kepler-404": None, # Kepler-404 b, c - massless star
  "Kepler-405": None, # Kepler-405 b, c - massless star

  #----------------------------------------------------------------------------

  "KIC 10544976 (AB)": None, # KIC 10544976 (AB) b - massless star
  "KIC 3526061": None, # KIC 3526061 b - massless star
  "KIC 9413313 b": None, # no orbital parameters

  "KMT-2016-BLG-0212 b": None, # - no orbital parameters
  "KMT-2016-BLG-0625": None, # KMT-2016-BLG-0625 b - massless star
  "KMT-2016-BLG-1751": None, #Skipping: KMT-2016-BLG-1751 @  - massless star
  "KMT-2019-BLG-0298": None, #Skipping: KMT-2019-BLG-0298 b @  - massless star
  "KMT-219:BLG-2783": None, #Skipping: KMT-2019-BLG-2783 b @  - massless star
  "KMT-2021-BLG-0119": None, #Skipping: KMT-2021-BLG-0119 b @  - massless star
  "KMT-2021-BLG-0322": None, #Skipping: KMT-2021-BLG-0322 b @  - massless star
  "KMT-2021-BLG-1110": None, #Skipping: KMT-2021-BLG-1110 b @  - massless star
  "KMT-2021-BLG-1643": None, #Skipping: KMT-2021-BLG-1643 b @  - massless star
  "KMT-2021-BLG-1770": None, #Skipping: KMT-2021-BLG-1770 b @  - massless star
  "KMT-2022-BLG-1013": None, #Skipping: KMT-2022-BLG-1013 b @  - massless star

  #fix("KOI-1860", "radius", RasSun(1.08916))
  #fix("KOI-1860", "T", 5620.270)
  #fix("KOI-1860", "L", Star.LasLog10(0.02790548))

  #fix("KOI-1599", "T", 5833.0)
  #fix("KOI-1599", "L", Star.LasLog10(0.1619642))

  "KOI-4777": None, # - duplicate
  "KOI-5": None, # KOI-5 b @  - massless star

  "LHS 6176 A": None, #Skipping: LHS 6176 B @ - massless star
  "LP 791-18 d": None, # - no orbital parameters
  "LSR J1835": None, #Skipping: LSR J1835 @  - massless star
  "MOA-2011-BLG-274": None, #Skipping: MOA-2011-BLG-274 b @  - massless star
  "MOA-2016-BLG-532": None, #Skipping: MOA-2016-BLG-532 b @  - massless star
  "MOA-2019-BLG-008L b": None, # - no orbital parameters
  "NGTS-7A": None, #Skipping: NGTS-7A b @  - massless star
  "NLTT 25473": None, #Skipping: NLTT 25473 b @  - massless star
  "NSVS 7453183": None, #Skipping: NSVS 7453183 b @  - massless star
  "OGLE-2014-BLG-1186L b": None, # - no orbital parameters
  "OGLE-2016-BLG-0596L": None, #Skipping: OGLE-2016-BLG-0596L b @  - massless star
  "OGLE-2016-BLG-0693L": None, #Skipping: OGLE-2016-BLG-0693L b @  - massless star
  "OGLE-2016-BLG-1635": None, #Skipping: OGLE-2016-BLG-1635 b @  - massless star
  "OGLE-2016-BLG-1850": None, #Skipping: OGLE-2016-BLG-1850 b @  - massless star
  "OGLE-2017-BLG-0114": None, #Skipping: OGLE-2017-BLG-0114 b @  - massless star
  "OGLE-2017-BLG-0373L b": None, # - no orbital parameters
  "OGLE-2017-BLG-1237 b": None, # - no orbital parameters
  "OGLE-2018-BLG-0360": None, # - duplicate
  "OGLE-2019-BLG-0249": None, #Skipping: OGLE-2019-BLG-0249 b @  - massless star
  "OGLE-2019-BLG-0679": None, #Skipping: OGLE-2019-BLG-0679 b @  - massless star
  "OY Car": None, #Skipping: OY Car b @  - massless star
  "Proplyd 133-353": None, #Skipping: Proplyd 133-353 @  - massless star
  "PSR 1257+12": None, #Skipping: PSR 1257+12 b, c, d @  - massless star
  "PSR B0329+54": None, #Skipping: PSR B0329+54 b @  - massless star
  "PSR J0952-0607": None, #Skipping: PSR J0952-0607 b @  - massless star
  "PSR J1301+0833": None, #Skipping: PSR J1301+0833 b @  - massless star
  "PSR J1311-3430": None, #Skipping: PSR J1311-3430 b @  - massless star
  "PSR J1502-6752": None, #Skipping: PSR J1502-6752 b @  - massless star
  "PSR J1653-0158": None, #Skipping: PSR J1653-0158 b @  - massless star
  "PSR J1745+1017": None, #Skipping: PSR J1745+1017 b @  - massless star
  "PSR J1953+1844E": None, #Skipping: PSR J1953+1844E b @  - massless star
  "PSR J1959+2048": None, #Skipping: PSR J1959+2048 b @  - massless star
  "PSR M13E": None, #Skipping: PSR M13E b @  - massless star
  "Sand 178": None, #Skipping: Sand 178 b @  - massless star
  "SCR 1845": None, #Skipping: SCR 1845 b @  - massless star
  "SDSS 1021-03": None, #Skipping: SDSS 1021-03 b @  - massless star
  "SDSS J1110+0116": None, #Skipping: SDSS J1110+0116 @  - massless star
  "SOI-1": None, #Skipping: SOI-1 b @  - massless star
  "SOI-2": None, #Skipping: SOI-2 b @  - massless star
  "SOI-3": None, #Skipping: SOI-3 b @  - massless star
  "SOI-4": None, #Skipping: SOI-4 b @  - massless star
  "SOI-5": None, #Skipping: SOI-5 b @  - massless star
  "SOI-6": None, #Skipping: SOI-6 b @  - massless star
  "SOI-7": None, #Skipping: SOI-7 b @  - massless star
  "SOI-8": None, #Skipping: SOI-8 b @  - massless star
  "2MASS J05383888-0228016": None, #Skipping: S Ori 68 @  - massless star
  "SR 12 (AB)": None, #Skipping: SR 12 (AB) c @  - massless star
  "SW Sex": None, #Skipping: SW Sex b @  - massless star
  "TIC 156514476": None, #Skipping: TIC 156514476.01 @  - massless star

  #----------------------------------------------------------------------------

  "TOI-1062 c": None, #- no orbital parameters
  "TOI-1272": None, #TOI-1272 b, c  - massless star
  "TOI-1338": None, #TOI-1338 b, c  - massless star
  "TOI-1669": None, #TOI-1669 b, c  - massless star
  "TOI-1683": None, #TOI-1683 b  - massless star
  "TOI-1694": None, #TOI-1694 b, c  - massless star
  "TOI-203": None, #TOI-203 b  - massless star
  "TOI-2236": None, #TOI-2236 b  - massless star
  "TOI-2421": None, #TOI-2421 b  - massless star
  "TOI-2567": None, #TOI-2567 b  - massless star
  "TOI-2570": None, #TOI-2570 b  - massless star
  "TOI-262": None, #TOI-262 b  - massless star
  "TOI-2641": None, #TOI-2641 b  - massless star
  "TOI-3331": None, #TOI-3331 b  - massless star
  "TOI-3540": None, #TOI-3540 b  - massless star
  "TOI-3693": None, #TOI-3593 b  - massless star
  "TOI-3984 A": None, #TOI-3984 A b  - massless star
  "TOI-4127": None, #TOI-4127 b  - massless star
  "TOI-4137": None, #TOI-4137 b  - massless star
  "TOI-421": None, #TOI-421 b, c  - massless star
  "TOI-4406": None, #TOI-4406 b  - massless star
  "TOI-481": None, #TOI-481 b  - massless star
  "TOI-5293 A": None, #TOI-5293 A b  - massless star
  "TOI-615": None, #TOI-615 b  - massless star
  "TOI-622": None, #TOI-622 b  - massless star
  "TOI-717": None, #TOI-717 b  - massless star
  "TOI-811": None, #TOI-811 b  - massless star
  "TOI-852": None, #TOI-852 b  - massless star
  "TOI-892": None, #TOI-892 b  - massless star

  #----------------------------------------------------------------------------

  #fix("V1298 Tau", "radius", RasSun(1.33))
  #fix("V1298 Tau", "T", 4970)
  #fix("V1298 Tau", "L", 0.934)

  "ups Leo": None, # Skipping: ups Leo b @  - massless star
  "USco1610-1913": None, # Skipping: USco1610-1913 b @  - massless star
  "USco1612-1800": None, # Skipping: USco1612-1800 b @  - massless star
  "V2051 Oph": None, # Skipping: V2051 Oph (AB) b @  - massless star
  "V396 Hya b": None, # Skipping:  - no orbital parameters
  "V470 Cam (AB)": None, # Skipping: V470 Cam (AB) b, c @  - massless star
  "WASP-139": None, # Skipping: WASP-139 b @  - massless star
  "WASP-13": None, # Skipping: WASP-13 b @  - massless star
  "WASP-185": None, # Skipping: WASP-185 b @  - massless star
  "WASP-192": None, # Skipping: WASP-192 b @  - massless star
  "WASP-35": None, # Skipping: WASP-35 b @  - massless star
  "WASP-42": None, # Skipping: WASP-42 b @  - massless star
  "WASP-54": None, # Skipping: WASP-54 b @  - massless star
  "WASP-56": None, # Skipping: WASP-56 b @  - massless star
  "WASP-57": None, # Skipping: WASP-57 b @  - massless star
  "WASP-64": None, # Skipping: WASP-64 b @  - massless star
  "WASP-68": None, # Skipping: WASP-68 b @  - massless star
  "WD 1032+011": None, # Skipping: WD 1032+011 b @  - massless star
  "WD 1145+017": None, # Skipping: WD 1145+017 b @  - massless star
  "WD 1856+534": None, # Skipping: WD 1856+534 b @  - massless star
  "WISE J0720-0846": None, # Skipping:  - duplicate
  "WISE J1355-8258 b": None, # Skipping:  - no orbital parameters
  "Wolf 359": None, # Skipping: Wolf 359 c @  - massless star

}
