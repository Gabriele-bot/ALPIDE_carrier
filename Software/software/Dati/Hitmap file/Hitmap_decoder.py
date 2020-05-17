import time
from subprocess import call
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.colors as colors
import matplotlib.cbook as cbook

def save_hitmap(matrix, file_name):
	fig, ax = plt.subplots()
	colormap = cm.get_cmap('jet')
	psm = ax.pcolormesh(matrix, cmap=colormap, vmin=0, vmax=np.max(matrix))
	cbar=plt.colorbar(psm, shrink=0.5, ax=ax)
	cbar.set_label("N. hits")
	plt.axis('scaled')
	ax.set(xlim=(0, 1023), ylim=(0, 511))
	plt.xlabel("Column")
	plt.ylabel("Row")
	plt.savefig(file_name, dpi=1600)

def save_hitmap_logscale(matrix, file_name):
	fig, ax = plt.subplots()
	colormap = cm.get_cmap('jet')
	psm = ax.pcolormesh(matrix, cmap=colormap, norm=colors.LogNorm(), vmin=1, vmax=np.max(matrix))
	cbar=plt.colorbar(psm, shrink=0.5, ax=ax)
	cbar.set_label("N. hits")
	plt.axis('scaled')
	ax.set(xlim=(0, 1023), ylim=(0, 511))
	plt.xlabel("Column")
	plt.ylabel("Row")
	plt.savefig(file_name, dpi=1600)

def find_next_pixel(yf,xf,hmap):
	#global hitmap
	if xf!=1023:
		if hmap[yf,xf+1]>=1:
			next_pixel = [yf,xf+1]
			#hitmap[yf,xf+1]=0
			return next_pixel
	if xf!=1023 and yf !=511:
		if hmap[yf+1,xf+1]>=1:
			next_pixel = [yf+1,xf+1]
			#hitmap[yf+1,xf+1]=0
			return next_pixel
	if yf !=511:
		if hmap[yf+1,xf]>=1:
			next_pixel = [yf+1,xf]
			#hitmap[yf+1,xf]=0
			return next_pixel
	if xf!=0 and yf !=511:
		if hmap[yf+1,xf-1]>=1:
			next_pixel = [yf+1,xf-1]
			#hitmap[yf+1,xf-1]=0
			return next_pixel
	if xf!=0:
		if hmap[yf,xf-1]>=1:
			next_pixel = [yf,xf-1]
			#hitmap[yf,xf-1]=0
			return next_pixel
	if xf!=0 and yf !=0:
		if hmap[yf-1,xf-1]>=1:
			next_pixel = [yf-1,xf-1]
			#hitmap[yf-1,xf-1]=0
			return next_pixel
	if yf !=0:
		if hmap[yf-1,xf]>=1:
			next_pixel = [yf-1,xf]
			#hitmap[yf-1,xf]=0
			return next_pixel
	if xf!=1023 and yf !=0:
		if hmap[yf-1,xf+1]>=1:
			next_pixel = [yf-1,xf+1]
			#hitmap[yf-1,xf+1]=0
			return next_pixel
	next_pixel = [-1,-1]
	return next_pixel

hitmap_name=raw_input("Insert hitmap file_name\n")
image_name=raw_input("Insert image_name\n")
hitmap_matrix=np.load(hitmap_name + '.npy')
for x in range(1024):
	for y in range(512):
		if hitmap_matrix[y,x] >= 1:
			nextpixel = find_next_pixel(y,x,hitmap_matrix)
			if nextpixel == [-1,-1]:
				hitmap_matrix[y,x]=0

while True:
	max_index=np.unravel_index(np.argmax(hitmap_matrix, axis=None), hitmap_matrix.shape)
	print max_index
	print hitmap_matrix[max_index]
	value=raw_input("Delete this max? (y/n)")
	if value == "y":
		hitmap_matrix[max_index]=0
	elif value == "n":
		break
	else:
		print "Bad input"
hitmap_matrix[max_index]=0
save_hitmap(hitmap_matrix,image_name + '.png')
save_hitmap_logscale(hitmap_matrix,image_name + '_log.png')
