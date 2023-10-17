import csv

#------------------------------------------------------------------------------

def getRows():

  with open("./orbtools/systems/exoplanets/eu/exoplanet.nasa_catalog.csv", newline='') as csvfile:
    rows = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
  return rows[1:]

# COLUMN pl_name:        Planet Name
# COLUMN hostname:       Host Name
# COLUMN default_flag:   Default Parameter Set
# COLUMN discoverymethod: Discovery Method
# COLUMN disc_year:      Discovery Year
# COLUMN pl_orbper:      Orbital Period [days]
# COLUMN pl_orbsmax:     Orbit Semi-Major Axis [au])
# COLUMN pl_radj:        Planet Radius [Jupiter Radius]
# COLUMN pl_massj:       Planet Mass [Jupiter Mass]
# COLUMN pl_eqt:         Equilibrium Temperature [K]
# COLUMN st_spectype:    Spectral Type
# COLUMN st_teff:        Stellar Effective Temperature [K]
# COLUMN st_rad:         Stellar Radius [Solar Radius]
# COLUMN st_mass:        Stellar Mass [Solar mass]
# COLUMN st_lum:         Stellar Luminosity [log(Solar)]
# COLUMN sy_dist:        Distance [pc]

#------------------------------------------------------------------------------

def extractRow(row):
  planet_data = {
    #loc_rowid: row[0]
    "name": row[1],
    #hostname: row[2]
    #default_flag: row[3]
    "detection_type": row[4],
    "discovered": row[5],
    "orbital_period": row[6],
    "semi_major_axis": row[7],
    "radius": row[8],
    "mass": row[9],
    "T": row[10],
    "status": "Confirmed",
  }

  star_data = {
    "name": row[2],
    "sp_type": row[11],
    "T": row[12],
    "radius": row[13],
    "mass": row[14],
    "L": row[15],
    "distance": row[16]
  }

  return planet_data, star_data

#------------------------------------------------------------------------------

fixes = {

}
