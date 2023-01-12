################################################################################
#
# Exoplanets imported from EU Exoplanet Catalog, see:
#
# http://exoplanet.eu/catalog/
#
################################################################################

from orbtools import *

#------------------------------------------------------------------------------

def doStar(star):
  name = star["name"]
  if not name: return
  if name in masses: return masses[name]
  #if name == "Sun": return

  dist = star["distance"] or None
  sptype = star["spectraltype"] or None
  mass = star["mass"] or None
  radius = star["radius"] or None
  T = star["temperature"] or None
  magV = star["magV"] or None

  #if not radius or not T: print("Star:", name, sptype, mass, radius, T)

  if not mass: return
  if sptype is None: return
  #if sptype[0] not in ["F", "G", "K", "M"]: return

  return Star(name, MxSun = mass, RxSun = radius, sptype = sptype, T = T, magV = magV, dist = dist)

#------------------------------------------------------------------------------

def doPlanet(planet, star):
  name = planet["name"]
  if not name: return
  if name in masses: return masses[name]

  mass = planet["mass"]

  radius = planet["radius"] or None

  P = planet["period"]
  A = planet["semimajoraxis"]

  if P:
    orbit = byPeriod(star, float(TasDays(P)))
  elif A:
    orbit = Orbit(star, float(AU2m(A)))
  else:
    orbit = None

  #if not radius or not orbit: print("Planet:", name, mass, radius, P, A)

  if not mass: return

  p = Planet(name, GM = MasJupiter(mass), radius = radius and RasJupiter(radius), orbit = orbit)
  #p.info()

#------------------------------------------------------------------------------

def doRow(row):

  #for key, value in row.items():
  #  print(key, value)

  planet = {
    "name": row["# name"],
    #"status": row["planet_status"],
    "mass": row["mass"],
    # mass_error_min
    # mass_error_max
    # mass_sini 16.1284
    # mass_sini_error_min 1.5
    # mass_sini_error_max 1.5
    "radius": row["radius"],
    # radius_error_min
    # radius_error_max
    "period": row["orbital_period"],
    # orbital_period_error_min 0.32
    # orbital_period_error_max 0.32
    "semimajoraxis": row["semi_major_axis"],
    # semi_major_axis_error_min 0.05
    # semi_major_axis_error_max 0.05
    # eccentricity 0.231
    # eccentricity_error_min 0.005
    # eccentricity_error_max 0.005
    # inclination
    # inclination_error_min
    # inclination_error_max
    # angular_distance 0.011664
    # discovered 2008
    # updated 2021-10-02
    # omega 94.8
    # omega_error_min 1.5
    # omega_error_max 1.5
    # tperi 2452899.6
    # tperi_error_min 1.6
    # tperi_error_max 1.6
    # tconj
    # tconj_error_min
    # tconj_error_max
    # tzero_tr
    # tzero_tr_error_min
    # tzero_tr_error_max
    # tzero_tr_sec
    # tzero_tr_sec_error_min
    # tzero_tr_sec_error_max
    # lambda_angle
    # lambda_angle_error_min
    # lambda_angle_error_max
    # impact_parameter
    # impact_parameter_error_min
    # impact_parameter_error_max
    # tzero_vr
    # tzero_vr_error_min
    # tzero_vr_error_max
    # k 302.8
    # k_error_min 2.6
    # k_error_max 2.6
    # temp_calculated
    # temp_calculated_error_min
    # temp_calculated_error_max
    # temp_measured
    # hot_point_lon
    # geometric_albedo
    # geometric_albedo_error_min
    # geometric_albedo_error_max
    # log_g
    # publication Published in a refereed paper
    # detection_type Radial Velocity
    # mass_detection_type Radial Velocity
    # radius_detection_type
    # alternate_names
    # molecules
  }

  star = {
    "name": row["star_name"],
    # ra 185.1791667
    # dec 17.7927778
    "magV": row["mag_v"],
    # mag_i
    # mag_j
    # mag_h
    # mag_k
    "distance": row["star_distance"],
    # star_distance_error_min 10.5
    # star_distance_error_max 10.5
    # star_metallicity -0.35
    # star_metallicity_error_min 0.09
    # star_metallicity_error_max 0.09
    "mass": row["star_mass"],
    # star_mass_error_min 0.3
    # star_mass_error_max 0.3
    "radius": row["star_radius"],
    # star_radius_error_min 2.0
    # star_radius_error_max 2.0
    "spectraltype": row["star_sp_type"],
    # star_age
    # star_age_error_min
    # star_age_error_max
    "temperature": row["star_teff"],
    # star_teff_error_min 100.0
    # star_teff_error_max 100.0
    # star_detected_disc
    # star_magnetic_field
    # star_alternate_names
  }

  #print(planet)
  #print(star)

  try:
    star = doStar(star)
    if star: doPlanet(planet, star)
  except Exception as e:
    print("Star:", star)
    print("Planet:", planet)
    raise e

  #exit()
  #dist = system.findtext("distance")
  #if dist: dist = parsec2m(dist)

  #for star in system.findall(".//star"):
  #  doStar(star, dist)

#------------------------------------------------------------------------------

import csv

with open('./orbtools/systems/catalogs/exoplanet.eu_catalog.csv', newline='') as csvfile:
    #spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    reader = csv.DictReader(csvfile)
    for row in reader:
      doRow(row)

