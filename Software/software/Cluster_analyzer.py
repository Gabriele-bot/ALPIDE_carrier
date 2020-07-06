import numpy as np
import matplotlib.pyplot as plt

import math

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

def save_hitmap(matrix, file_name, quality_dpi):
	fig, ax = plt.subplots()
	colormap = cm.get_cmap('jet')
	psm = ax.pcolormesh(matrix, cmap=colormap, vmin=0, vmax=np.max(matrix))
	cbar=plt.colorbar(psm, shrink=0.5, ax=ax)
	cbar.set_label("N. hits")
	plt.axis('scaled')
	ax.set(xlim=(0, 1023), ylim=(0, 511))
	plt.xlabel("Column")
	plt.ylabel("Row")
	plt.savefig(file_name, dpi=quality_dpi)

def save_hitmap_logscale(matrix, file_name, quality_dpi):
	fig, ax = plt.subplots()
	colormap = cm.get_cmap('jet')
	psm = ax.pcolormesh(matrix, cmap=colormap, norm=colors.LogNorm(), vmin=1, vmax=np.max(matrix))
	cbar=plt.colorbar(psm, shrink=0.5, ax=ax)
	cbar.set_label("N. hits")
	plt.axis('scaled')
	ax.set(xlim=(0, 1023), ylim=(0, 511))
	plt.xlabel("Column")
	plt.ylabel("Row")
	plt.savefig(file_name, dpi=quality_dpi)


#define which file to decode and give it a name
hitmap_name=raw_input("Insert file_name\n")
particle_name=raw_input("Insert particle_name\n")
Cluster_title=particle_name + ' cluster map'
Histo_title=particle_name + ' cluster histogram'

file_name=particle_name + '_Cluster_Map'
hitmap=np.load('Dati/Hitmap_file/' + hitmap_name + '.npy')

#generate the sample list
X=[]
for row in range(512):
	for column in range(1024):
		if hitmap[row,column] > 0:
			X.append([row,column])
#perform the dbscan
db = DBSCAN(eps=1, min_samples=2).fit(X)

core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)


nc = 0	#noise counter
clusters = [[] for _ in range(n_clusters_)]	#initialize an empty list to accomodate the sample coordinates whitin the cluster
cluster_size = []	#initialize an empty list to accomodate the clusters' sizes
for j in range(len(db.labels_)):	
	if db.labels_[j] == -1:	#noise sample has label -1
		nc = nc + 1	#noise counter
	else: 
		index = db.labels_[j]
		clusters[index].append(db.components_[j - nc]) #subtract noise counter to the index

cluster_zeroed = np.zeros_like(clusters)	#initialize a list to accomodate all clussters centered to [0,0]
result_shape = []	#all samples coordinates

top_thr=100	#maximum number of samples per feature
			
for i in range(len(clusters)):
	if len(clusters[i]) < top_thr:	#cut all clusters with size >top_thr
		cluster_size.append(len(clusters[i]))
	temp_arr=np.reshape(clusters[i],(len(clusters[i]),2))
	cluster_zeroed[i]=np.reshape(clusters[i],(len(clusters[i]),2)) 
	centre = [np.mean(temp_arr[:,0]),np.mean(temp_arr[:,1])]	#yx 
	cluster_zeroed[i] = temp_arr - centre
	if len(cluster_zeroed[i]) < top_thr:	#cut all clusters with size >top_thr
		for j in cluster_zeroed[i]:
			result_shape.append(j)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)
print('Estimated number of clusters rejected[size>%d]: %d\n' % (top_thr,(n_clusters_-len(cluster_size))))
print ('Cluster size = %f +/- %f' % (np.mean(cluster_size),np.nanstd(cluster_size)))

result_shape=np.reshape(result_shape,(len(result_shape),2))	#reshape 
#plt.scatter(result_shape[:,1], result_shape[:,0])
#plt.show()

#define the boundaries and bins
xmax=math.ceil(max(result_shape[:,1]))
ymax=math.ceil(max(result_shape[:,0]))
xmin=math.floor(min(result_shape[:,1]))
ymin=math.floor(min(result_shape[:,0]))
xbins=int(xmax-xmin)
ybins=int(ymax-ymin)

#generate the graph
fig, ax = plt.subplots()
plt.hist2d(result_shape[:,1], result_shape[:,0], bins=[xbins,ybins], range=[[xmin, xmax], [ymin, ymax]], cmap='inferno')
cbar = plt.colorbar()
cbar.set_label('N. hits')
plt.axis('scaled')
plt.xlabel('Pixel')
plt.ylabel('Pixel')
ax.set_title(Cluster_title)
plt.xticks(np.arange(xmin, xmax, step=1))
plt.yticks(np.arange(ymin, ymax, step=1))
plt.grid(True)
plt.savefig(file_name, dpi=300)

fig, ax = plt.subplots()
hitogram=ax.hist(cluster_size, bins=int(math.ceil(np.mean(cluster_size)+3*np.nanstd(cluster_size)-1)), range=[1,int(math.ceil(np.mean(cluster_size)+3*np.nanstd(cluster_size)))])
ax.set_title(Histo_title)
plt.show()




