import numpy as np
from subprocess import call

def find_next_pixel(yf,xf,hmap):
	global hitmap
	if xf!=1023:
		if hmap[yf,xf+1]>=1:
			next_pixel = [yf,xf+1]
			hitmap[yf,xf+1]=0
			return next_pixel
	if xf!=1023 and yf !=511:
		if hmap[yf+1,xf+1]>=1:
			next_pixel = [yf+1,xf+1]
			hitmap[yf+1,xf+1]=0
			return next_pixel
	if yf !=511:
		if hmap[yf+1,xf]>=1:
			next_pixel = [yf+1,xf]
			hitmap[yf+1,xf]=0
			return next_pixel
	if xf!=0 and yf !=511:
		if hmap[yf+1,xf-1]>=1:
			next_pixel = [yf+1,xf-1]
			hitmap[yf+1,xf-1]=0
			return next_pixel
	if xf!=0:
		if hmap[yf,xf-1]>=1:
			next_pixel = [yf,xf-1]
			hitmap[yf,xf-1]=0
			return next_pixel
	if xf!=0 and yf !=0:
		if hmap[yf-1,xf-1]>=1:
			next_pixel = [yf-1,xf-1]
			hitmap[yf-1,xf-1]=0
			return next_pixel
	if yf !=0:
		if hmap[yf-1,xf]>=1:
			next_pixel = [yf-1,xf]
			hitmap[yf-1,xf]=0
			return next_pixel
	if xf!=1023 and yf !=0:
		if hmap[yf-1,xf+1]>=1:
			next_pixel = [yf-1,xf+1]
			hitmap[yf-1,xf+1]=0
			return next_pixel
	next_pixel = [-1,-1]
	return next_pixel


hitmap_name=raw_input("Insert file_name.npy\n")
hitmap=np.load(hitmap_name)
cluster_size = []
for x in range(1024):
	for y in range(512):
		if hitmap[y,x] >= 1:
			hitmap[y,x] = 0
			i = 1
			xp = x
			yp = y
			while True:
				nextpixel = find_next_pixel(yp,xp,hitmap)
				if nextpixel != [-1, -1]:
					yp = nextpixel[0]
					xp = nextpixel[1]
					i = i + 1
				else:
					break
			cluster_size.append(i)

k=0
while k < len(cluster_size):
	if cluster_size[k]==1:
		del cluster_size[k]
	elif cluster_size[k]>=26:
		del cluster_size[k]
	else:
		k=k+1

file = open("Cluster_histo.txt", "w")
histo = np.zeros(26)
for j in range(26):
	for l in range(len(cluster_size)):
		if cluster_size[l] == j+1:
			histo[j] = histo[j] + 1

for j in range(len(histo)):
	file.write("%d	%d\n" % (j+1, histo[j]))

file.close()

mean = np.mean(cluster_size)
std=np.nanstd(cluster_size)
print "%d clusters found [threshold >1 & <26]" % len(cluster_size)
print "Cluster size = %f +/- %f" % (mean,std)
			
