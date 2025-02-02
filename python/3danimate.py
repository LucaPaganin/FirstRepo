from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
from pathlib import Path
import re
import json
import functions as fnc
import argparse

#Parameters parsing
parser = argparse.ArgumentParser(description="A python script to animate the planets motion starting from a txt file containing the simulated data.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-f", "--filepath", required=False, default="../c++/output/temporal_evolution.txt", help="The name of the file containing time evolution data.")

parser.add_argument("-p", "--planets", nargs="+", default=None, help="The list of the planets to be plotted.")

args = parser.parse_args()

filepath = Path(args.filepath)
planets = args.planets

#Setting up paths and load data into dictionary of numpy arrays
solar_system = fnc.load_from_file(filepath=filepath)

if planets is None:
    planets = list(solar_system.keys())

"""
Choose the planets to animate and put data into right form for animation
The data matrix for the given planet must have the following shape:
3 x Ntimesteps
"""

#Check if the chosen planets are in the list loaded from the file:
if not all([p in solar_system.keys() for p in planets]):
    print("Some of the planets you have chosen are not in the full list of available planets. The available planets are:")
    print(*list(solar_system.keys()), sep="\n")
    quit()

planets_data = [solar_system[k] for k in planets]

fig = plt.figure()
ax = p3.Axes3D(fig)

colors = matplotlib.cm.rainbow(np.linspace(0, 1, len(planets)))

lines = []
for p,c in zip(planets, colors):
    line, = ax.plot(solar_system[p][0, 0:1],
                    solar_system[p][1, 0:1],
                    solar_system[p][2, 0:1],
                    label=p, markersize=5,
                    marker='o',
                    color=c)
    lines.append(line)


limits = fnc.get_plot_limits(planets_data)

# Setting the axes properties
ax.set_xlabel('X [A.U.]')
ax.set_ylabel('Y [A.U.]')
ax.set_zlabel('Z [A.U.]')
ax.set_xlim3d([limits[0,0], limits[0,1]])
ax.set_ylim3d([limits[1,0], limits[1,1]])
ax.set_zlim3d([limits[2,0], limits[2,1]])

ax.legend(loc="lower left")

ani = animation.FuncAnimation(fig,
                              fnc.update_solar_system,
                              planets_data[0].shape[1],
                              fargs=(planets_data, lines),
                              interval=fnc.get_animation_interval(planets_data[0], 2.5),
                              blit=False)

#ani.save('animation.gif')

if args.moviefilename is not None:
    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=90.7, metadata=dict(artist='Me'), bitrate=3600)
    ani.save(args.moviefilename, writer=writer)

plt.show()
