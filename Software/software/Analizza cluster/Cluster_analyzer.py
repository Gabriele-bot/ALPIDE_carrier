import numpy as np

def find_next_pixel(yf,xf,hmap):
	global hitmap
	if yf!=511 and yf!=0 and xf!=1023 and xf!=0:
		if hmap[yf,xf+1]>=1:
			next_pixel = [yf,xf+1]
			hitmap[yf,xf+1]=0
			return next_pixel
		if hmap[yf+1,xf+1]>=1:
			next_pixel = [yf+1,xf+1]
			hitmap[yf+1,xf+1]=0
			return next_pixel
		if hmap[yf+1,xf]>=1:
			next_pixel = [yf+1,xf]
			hitmap[yf+1,xf]=0
			return next_pixel
		if hmap[yf+1,xf-1]>=1:
			next_pixel = [yf+1,xf-1]
			hitmap[yf+1,xf-1]=0
			return next_pixel
		if hmap[yf,xf-1]>=1:
			next_pixel = [yf,xf-1]
			hitmap[yf,xf-1]=0
			return next_pixel
		if hmap[yf-1,xf-1]>=1:
			next_pixel = [yf-1,xf-1]
			hitmap[yf-1,xf-1]=0
			return next_pixel
		if hmap[yf-1,xf]>=1:
			next_pixel = [yf-1,xf]
			hitmap[yf-1,xf]=0
			return next_pixel
		if hmap[yf-1,xf+1]>=1:
			next_pixel = [yf-1,xf+1]
			hitmap[yf-1,xf+1]=0
			return next_pixel
		next_pixel = [-1,-1]
	else:
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


mean = np.mean(cluster_size)
std=np.nanstd(cluster_size)
print "%d clusters found [threshold >1 & <26]" % len(cluster_size)
print "Cluster size = %f +/- %f" % (mean,std)
			
