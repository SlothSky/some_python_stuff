import requests
import json
import matplotlib.pyplot as plt

BASE_API_URL = 'https://api.le-systeme-solaire.net/rest'
BODIES_AMENDMENT = '/bodies'
X_TEXT_PERCENTAGE = 2
Y_TEXT_PERCENTAGE = 5

all_bodies = json.loads(requests.get(BASE_API_URL + BODIES_AMENDMENT).text)
max_min_bodies = []
first_planet = True
first_dwarf = True
first_asteroid = True
first_comet = True
first_moon = True

# THERE IS NO INT / NUMBER MAX SIZE IN PYTHON 3 -> CREATE HUGE NUMBER FOR MIN VALUE
rotation_max = 0
rotation_min = 10 ** 999
orbit_max = 0
orbit_min = 10 ** 999

fig, ax = plt.subplots(nrows=1, ncols=1)

for body in all_bodies['bodies']:
    if body['sideralOrbit'] != 0 and body['sideralRotation'] != 0:
        match body['bodyType']:
            case 'Planet':
                plt.scatter(body['sideralOrbit'] / 365, body['sideralRotation'] / 24, marker='^', c='#f33', label='Planet' if first_planet else '')
                first_planet = False
            case 'Dwarf Planet':
                plt.scatter(body['sideralOrbit'] / 365, body['sideralRotation'] / 24, marker='o', c='#1a9936', label='Dwarf Planet' if first_dwarf else '')
                first_dwarf = False
            case 'Asteroid':
                plt.scatter(body['sideralOrbit'] / 365, body['sideralRotation'] / 24, marker='o', c='#33f', label='Asteroid' if first_asteroid else '')
                first_asteroid = False
            case 'Comet':
                plt.scatter(body['sideralOrbit'] / 365, body['sideralRotation'] / 24, marker='o', c='#ccc', label='Comet' if first_comet else '')
                first_comet = False
            case 'Moon':
                plt.scatter(body['sideralOrbit'] / 365, body['sideralRotation'] / 24, marker='v', c='#3ff', label='Moon' if first_moon else '')
                first_moon = False
            case _:
                pass

        if body['sideralOrbit'] > orbit_max:
            orbit_max = body['sideralOrbit']
            if body['sideralOrbit'] / 365 < 1:
                orbit_max_object = [body, 'Sideral Orbit: ' + '{:.2f}'.format(body['sideralOrbit']) + 'd']
            else: 
                orbit_max_object = [body, 'Sideral Orbit: ' + '{:.2f}'.format(body['sideralOrbit'] / 365) + 'y']
        elif body['sideralOrbit'] < orbit_min:
            orbit_min = body['sideralOrbit']
            if body['sideralOrbit'] / 365 < 1 and not body['sideralOrbit'] / 365 < -1:
                orbit_min_object = [body, 'Sideral Orbit: ' + '{:.2f}'.format(body['sideralOrbit']) + 'd']
            else: 
                orbit_min_object = [body, 'Sideral Orbit: ' + '{:.2f}'.format(body['sideralOrbit'] / 365) + 'y']

        if body['sideralRotation'] > rotation_max:
            rotation_max = body['sideralRotation']
            if body['sideralRotation'] / 24 < 1:
                rotation_max_object = [body, 'Sideral Rotation: ' + '{:.2f}'.format(body['sideralRotation']) + 'h']
            else: 
                rotation_max_object = [body, 'Sideral Rotation: ' + '{:.2f}'.format(body['sideralRotation'] / 24) + 'd']

        elif body['sideralRotation'] < rotation_min:
            rotation_min = body['sideralRotation']
            if body['sideralRotation'] / 24 < 1 and not body['sideralRotation'] / 24 < -1:
                rotation_min_object = [body, 'Sideral Rotation: ' + '{:.2f}'.format(body['sideralRotation']) + 'h']
            else: 
                rotation_min_object = [body, 'Sideral Rotation: ' + '{:.2f}'.format(body['sideralRotation'] / 24) + 'd']

max_min_bodies.extend([orbit_max_object, orbit_min_object, rotation_max_object, rotation_min_object])

# CALCULATE RANGES FOR LATER TEXT POSITION CALCULATION
range_orbit = (max_min_bodies[0][0]['sideralOrbit'] - max_min_bodies[1][0]['sideralOrbit']) / 365
range_rotation = (max_min_bodies[2][0]['sideralRotation'] - max_min_bodies[3][0]['sideralRotation']) / 24

cleaned_range_orbit = range_orbit if range_orbit > 0 else range_orbit * -1
cleaned_range_rotation = range_rotation if range_rotation > 0 else range_rotation * -1

# ADD ANNOTATION TO ALL MAXIMUM AND MINIMUM BODIES
for body in max_min_bodies:
    # first calculate a nicer position (a little bit more to the upper left of the object)
    cleaned_x = body[0]['sideralOrbit'] / 365 + cleaned_range_orbit / (100 / X_TEXT_PERCENTAGE)
    cleaned_y = body[0]['sideralRotation'] / 24 + cleaned_range_rotation / (100 / Y_TEXT_PERCENTAGE)

    # and then add the text to the calculated position
    plt.text(cleaned_x, cleaned_y, body[0]['name'] + ' - ' + body[1], c='#878380')

# SET DARKER BACKGROUND COLOR
ax.set_facecolor('#343536')
fig.patch.set_facecolor('#343536')

ax.tick_params(axis='x', colors='#878380')
ax.tick_params(axis='y', colors='#878380')

ax.spines['left'].set_color('#878380')
ax.spines['bottom'].set_color('#878380')
ax.spines['right'].set_color('#343536')
ax.spines['top'].set_color('#343536')

plt.xlabel('Sideral Orbit in years',  c='#878380')
plt.ylabel('Sideral Rotation in days', c='#878380')

plt.legend(loc='lower right', facecolor='#343536', labelcolor='#878380', edgecolor='#878380')

plt.savefig('bar.pdf', bbox_inches='tight')

