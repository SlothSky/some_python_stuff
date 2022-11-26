import requests
import json
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

BASE_API_URL = 'https://api.le-systeme-solaire.net/rest'
BODIES_AMENDMENT = '/bodies'
STARS = json.loads('[]')
PLANETS = json.loads('[]')
DWARF_PLANETS = json.loads('[]')
ASTEROIDS = json.loads('[]')
COMETS = json.loads('[]')
MOONS = json.loads('[]')
PLANET_ID = np.arange(1, 8 + 1)

all_bodies = json.loads(requests.get(BASE_API_URL + BODIES_AMENDMENT).text)

for body in all_bodies['bodies']:
    match body['bodyType']:
        case 'Star':
            STARS.append(body)
        case 'Planet':
            PLANETS.append(body)
        case 'Dwarf Planet':
            DWARF_PLANETS.append(body)
        case 'Asteroid':
            ASTEROIDS.append(body)
        case 'Comet':
            COMETS.append(body)
        case 'Moon':
            MOONS.append(body)
        case _:
            pass

dataset_names = []
dataset_masses = []
dataset_mass_labels = []
dataset_colors = []

# CREATE FIGURE AND AXIS INSTANCES
fig, ax0 = plt.subplots(1, 1, sharex=True, sharey=True)

for planet in PLANETS:
    dataset_names.append(planet['name'])
    #mass_temp = planet['mass']['massValue'] * 10 ** planet['mass']['massExponent'] / (10 ** 26)
    mass_temp = 10
    dataset_mass_labels.append('$' + str(planet['mass']['massValue']) + ' *10^{' + str(planet['mass']['massExponent']) + '}$')
    dataset_masses.append(mass_temp)
    match planet['englishName']:
        case 'Mercury':
            dataset_colors.append('#575245')
        case 'Venus':
            dataset_colors.append('#a37800')
        case 'Earth':
            dataset_colors.append('#4a78c7')
        case 'Mars':
            dataset_colors.append('#701515')
        case 'Jupiter':
            dataset_colors.append('#d17b38')
        case 'Saturn':
            dataset_colors.append('#99964b')
        case 'Uranus':
            dataset_colors.append('#0f104a')
        case 'Neptune':
            dataset_colors.append('#636491')
        case _:
            print('THIS WILL ONLY HAPPEN IF THERE IS A NEW PLANET IN THE SOLAR SYSTEM xD')

#plt.style.use('_mpi-gallery')

dataset_adaption = [1, 4]


# CREATE BAR CONTAINER FOR THE AXIS INSTANCE
masses_ax = ax0.bar(dataset_names, dataset_masses, 0.6, color=dataset_colors, log=True)

# CUSTOMIZE BAR CONTAINERS
for e in ax0.bar_label(masses_ax, dataset_mass_labels, label_type='center', rotation=90):
    e.set_fontsize('xx-small')
    #e.set_verticalalignment('top')

plt.savefig("foo.pdf")










