import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

fig, ax = plt.subplots()

min_val, max_val = 0, 1500

intersection_matrix = np.random.randint(0, 1000, size=(max_val, max_val))

colormap=cm.get_cmap('plasma', 256)
psm = ax.pcolormesh(intersection_matrix, cmap=colormap, rasterized=True, vmin=0, vmax=1000)
fig.colorbar(psm, ax=ax)


plt.show()

