import os
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json, re
import argparse

def get_energies_vs_time(inputfile_path):

    names = None

    with open(inputfile_path, "r") as infile:
        name_line = infile.readline().strip()
        name_line = re.sub("#", "", name_line)
        names = name_line.split()

    data = np.loadtxt(inputfile_path)

    n_planets = len(names)

    times = data[:,0]
    energies = [data[:,i] for i in range(1, n_planets+1)]

    planets_energies = dict(zip(names, energies))

    return times, planets_energies


parser = argparse.ArgumentParser(description="A python script to animate the planets motion starting from a txt file containing the simulated data.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-p", "--planets", nargs="+", default=None, help="The list of the planets to be plotted.")

args = parser.parse_args()

planets = args.planets

data_filename = "Single_Energies.txt"

cwd = Path(os.getcwd())
datafile_path = cwd.parent / "c++" / "output" / data_filename

times, energies = get_energies_vs_time(datafile_path)

if planets is None:
    print("You can choose between these planets:")
    print(energies.keys())
    quit()

if not all([p in energies.keys() for p in planets]):
    print(f"Error: some planets you entered are not present in the data file {datafile_path}")
    quit()

colors = matplotlib.cm.rainbow(np.linspace(0, 1, len(energies)))
fig = plt.figure(figsize=(10,6))



for p in planets:
    plt.plot(times, energies[p], label=p)


plt.legend(loc="lower left")
plt.show()
