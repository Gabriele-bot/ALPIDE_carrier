
from subprocess import call
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.colors as colors
import matplotlib.cbook as cbook


n_events = 0
rawdata = np.load('Rawdata.npy')
file = open("Decodeddata.txt", "w")
hitmap_matrix  = np.zeros((512,1024))
for word in rawdata:
	if (word & 0xF00000) == 0xA00000:  # chip header
		plane_id = (word & 0x0F0000) >> 16
		bc = (word & 0x00FF00) >> 8
		file.write("CHIP HEADER: plane=%d\n" % plane_id)
		file.write("Bunch counter=%d\n" % bc)
	elif (word & 0xF00000) == 0xB00000:  # chip trailer
		ro_flags = (word & 0x0F0000) >> 16
		file.write("CHIP TRAILER: flags=0x%x\n\n" % ro_flags)
	elif (word & 0xF00000) == 0xE00000:  # chip empty
		plane_id = (word & 0x0F0000) >> 16
		bc = (word & 0x00FF00) >> 8
		#file.write("CHIP EMPTY: plane=%d\n" % plane_id)
		#file.write("Bunch counter=%d\n\n" % bc)
	elif (word & 0xE00000) == 0xC00000:  # reagion header
		region= (word>>16) & 0x1F
		file.write("REAGION_HEADER: region=%d\n" % region)
	elif (word & 0xC00000) == 0x400000:  # short
		word_shifted = word>>8
		x = region<<5 | word_shifted>>9 & 0x1E | (word_shifted ^ word_shifted>>1) & 0x1	#region*32 + encoderid*2 + addr correction
		y = word_shifted>>1 & 0x1FF	#addr/2
		hitmap_matrix[y,x] = hitmap_matrix[y,x] + 1
		file.write("DATA_SHORT: \nx=%d , y=%d \n" % (x, y))
		n_events = n_events +1
	elif (word & 0xC00000) == 0x000000:  # long
		word_shifted = word>>8
		address = word_shifted & 0x3ff
		x = region<<5 | word_shifted>>9 & 0x1E | (word_shifted ^ word_shifted>>1) & 0x1
		y = word_shifted>>1 & 0x1FF
		hitmap_matrix[y,x] = hitmap_matrix[y,x] + 1
		hitmap = word & 0x7F
		file.write("DATA LONG: \nx=%d , y=%d \n" % (x, y))
		n_events = n_events + 1
		for i in range(7):
			hitmap_shifted = hitmap>>i
			if (hitmap_shifted & 0x1) == 0x1:
				addressmap = address + i + 1
				xhm = region<<5 | word_shifted>>9 & 0x1E | (addressmap ^ addressmap>>1) & 0x1	#x hit map
				yhm = addressmap>>1	#y hit map
				hitmap_matrix[yhm, xhm] = hitmap_matrix[yhm, xhm] + 1
				file.write("x=%d , y=%d \n" % (xhm, yhm))
				n_events = n_events + 1
	#elif word == 0xFFFFFF:	#idle
	elif word == 0xF1FFFF:	#busy on
		file.write("BUSY ON\n")
	elif word == 0xF0FFFF:	#busy off
		file.write("BUSY OFF\n")
	# else:
file.write("Total events detected=%d \n" % n_events)
file.close()
fig, ax = plt.subplots()
colormap = cm.get_cmap('jet')
psm = ax.pcolormesh(hitmap_matrix, cmap=colormap, norm=colors.LogNorm(), vmin=1, vmax=np.max(hitmap_matrix))
#fig.colorbar(psm, shrink=0.5, ax=ax)
cbar=plt.colorbar(psm, shrink=0.5, ax=ax)
cbar.set_label("N. hits")
plt.axis('scaled')
plt.xlabel("Column")
plt.ylabel("Raw")
plt.savefig('Hit_map.png', dpi=2000)

