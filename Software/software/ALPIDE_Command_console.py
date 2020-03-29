import uhal
import time
from subprocess import call
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.colors as colors
import matplotlib.cbook as cbook

def send_cmd(cmd):	#send command to perform into FPGA
	hw.getNode("CSR.ctrl.op_sw").write(cmd)
	hw.getNode("CSR.ctrl.strt").write(0b1)
	#hw.dispatch()
	#time.sleep(0.001)
	hw.getNode("CSR.ctrl.strt").write(0b0)
	hw.dispatch()

def get_status():	#get all status of ALPIDE CARRIER
	global powered
	global initialized
	global busy
	global FIFO_full
	global FIFO_empty
	global FIFO_prg_full
	global mem_readable
	global err_slave
	global err_idle
	global err_read
	global err_chip_id
	global lkd_AC
	global lkd_ipbus 
	powered = hw.getNode("CSR.status.powered").read()
	initialized = hw.getNode("CSR.status.init").read()
	busy = hw.getNode("CSR.status.busy").read()
	FIFO_full = hw.getNode("CSR.status.FIFO_full").read()
	FIFO_empty = hw.getNode("CSR.status.FIFO_empty").read()
	FIFO_prg_full = hw.getNode("CSR.status.FIFO_prog_full").read()
	mem_readable = hw.getNode("CSR.status.mem_readable").read()
	err_slave = hw.getNode("CSR.status.err_slave").read()
	err_idle = hw.getNode("CSR.status.err_idle").read()
	err_read = hw.getNode("CSR.status.err_read").read()
	err_chip_id = hw.getNode("CSR.status.err_chip_id").read()
	lkd_AC = hw.getNode("CSR.status.lkd_AC").read()
	lkd_ipbus = hw.getNode("CSR.status.lkd_ipbus").read()
	hw.dispatch()

def writeregister(addr,data):	#Write ALPIDE register
	hw.getNode("cmd_addr.WR_addr").write(addr)
	hw.getNode("cmd_addr.WR_data").write(data)
	hw.dispatch()
	send_cmd(write_register)

def readregister(addr):	#Read ALPIDE register
	hw.getNode("cmd_addr.RR_addr").write(addr)
	send_cmd(read_register)
	reg_read = hw.getNode("DATA.reg_read").read()
	hw.dispatch()
	return reg_read

def send_broadcast(CMD):	#send broadcast command
	hw.getNode("cmd_addr.OP_command").write(CMD)
	hw.dispatch()
	send_cmd(write_cmd)

def pulse_test(mode_cfg):
	hitmap_matrix = np.zeros((512, 1024))
	region = 0
	n_events = 0
	writeregister(0x0001, mode_cfg)  # mode cotrol register configuration (see above)
	writeregister(0x0005, 0x0002)  # STROBE duration 3 clk clycles
	writeregister(0x0006, 0x0000)  # gap between 2 STROBES
	writeregister(0x0007, 0x0008)  # delay from PULSE to STROBE 8+1 clk cycles
	writeregister(0x0008, 0x000E)  # PULSE duration 12 clk cylces
	send_broadcast(0x78)  # send PULSE command
	send_cmd(read_out)
	for i in range(800):
		time.sleep(0.00001)
		mem_readable = hw.getNode("CSR.status.mem_readable").read()
		hw.dispatch()
		if mem_readable:
			FIFO = hw.getNode("DATA.ro_data").readBlock(0x200)
			hw.dispatch()
			for word in FIFO:
				if (word & 0xF00000) == 0xA00000:  # chip header
					plane_id = (word & 0x0F0000) >> 16
					bc = (word & 0x00FF00) >> 8
				elif (word & 0xF00000) == 0xB00000:  # chip trailer
					ro_flags = (word & 0x0F0000) >> 16
				elif (word & 0xF00000) == 0xE00000:  # chip empty
					plane_id = (word & 0x0F0000) >> 16
					bc = (word & 0x00FF00) >> 8
				elif (word & 0xE00000) == 0xC00000:  # reagion header
					region = (word >> 16) & 0x1F
				elif (word & 0xC00000) == 0x400000:  # short
					word_shifted = word >> 8
					x = region << 5 | word_shifted >> 9 & 0x1E | (
								word_shifted ^ word_shifted >> 1) & 0x1  # region*32 + encoderid*2 + addr correction
					y = word_shifted >> 1 & 0x1FF  # addr/2
					hitmap_matrix[y, x] = hitmap_matrix[y, x] + 1
					n_events = n_events + 1
				elif (word & 0xC00000) == 0x000000:  # long
					word_shifted = word >> 8
					address = word_shifted & 0x3ff
					x = region << 5 | word_shifted >> 9 & 0x1E | (word_shifted ^ word_shifted >> 1) & 0x1
					y = word_shifted >> 1 & 0x1FF
					hitmap_matrix[y, x] = hitmap_matrix[y, x] + 1
					hitmap = word & 0x7F
					n_events = n_events + 1
					for i in range(7):
						hitmap_shifted = hitmap >> i
						if (hitmap_shifted & 0x1) == 0x1:
							addressmap = address + i + 1
							xhm = region << 5 | word_shifted >> 9 & 0x1E | (
										addressmap ^ addressmap >> 1) & 0x1  # x hit map
							yhm = addressmap >> 1  # y hit map
							hitmap_matrix[yhm, xhm] = hitmap_matrix[yhm, xhm] + 1
							n_events = n_events + 1
			# elif word == 0xFFFFFF:	#idle
			# elif word == 0xF1FFFF:	#busy on
			# elif word == 0xF0FFFF:	#busy off
			# else:
			hw.getNode("CSR.ctrl.mem_read").write(0b1)
			hw.getNode("CSR.ctrl.mem_read").write(0b0)
			hw.dispatch()
	hw.getNode("CSR.ctrl.ro_stop").write(0b1)
	hw.dispatch()
	#save_hitmap(hitmap_matrix, 'PulseHitmap.png')
	pixel_fraction = float(n_events) / 200
	string_1 = 'Pulse test, %f' % (pixel_fraction * 100)
	string = string_1 + chr(37) + ' pixels respond\n'
	print string
	writeregister(0x0007, 0x0000)
	writeregister(0x0008, 0x0000)
	get_status()
	if err_slave:  # more then 51 clk cycles driven by slave
		print
		"Slave drive on time out"
	if err_idle:
		print
		"high signal not detected on idle phase"
	if err_read:
		print
		"stop bit not detected"
	if err_chip_id:
		print
		"different chip ID recieved"
	time.sleep(0.001)
	hw.getNode("CSR.ctrl.ro_stop").write(0b0)
	hw.dispatch()
	return pixel_fraction

def decode_data(): #decode data and save as txt file DecodedData.txt
	n_events = 0
	rawdata = np.load('Rawdata.npy')
	file = open("DecodedData.txt", "w")
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
			file.write("CHIP EMPTY: plane=%d\n" % plane_id)
			file.write("Bunch counter=%d\n\n" % bc)
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
	print "File saved as DecodedData.txt"

def save_hitmap(matrix, file_name):
	fig, ax = plt.subplots()
	colormap = cm.get_cmap('jet')
	psm = ax.pcolormesh(matrix, cmap=colormap, vmin=0, vmax=np.max(matrix))
	cbar=plt.colorbar(psm, shrink=0.5, ax=ax)
	cbar.set_label("N. hits")
	plt.axis('scaled')
	plt.xlabel("Column")
	plt.ylabel("Row")
	plt.savefig(file_name, dpi=2000)

def save_hitmap_logscale(matrix, file_name):
	fig, ax = plt.subplots()
	colormap = cm.get_cmap('jet')
	psm = ax.pcolormesh(matrix, cmap=colormap, norm=colors.LogNorm(), vmin=1, vmax=np.max(matrix))
	cbar=plt.colorbar(psm, shrink=0.5, ax=ax)
	cbar.set_label("N. hits")
	plt.axis('scaled')
	plt.xlabel("Column")
	plt.ylabel("Row")
	plt.savefig(file_name, dpi=2000)

def ADC_calibration():
	writeregister(0x0610, 0x0001)  # calibration mode and AVSS ADC input discriminator = 0
	writeregister(0x0000, 0xFF20)  # mesure command
	time.sleep(0.01)
	val1 = readregister(0x0612)  # store value with dis = 0
	writeregister(0x0610, 0x0101)  # calibration mode and AVSS ADC input discriminator = 1
	writeregister(0x0000, 0xFF20)  # mesure command
	time.sleep(0.01)
	val2 = readregister(0x0612)  # store value with dis = 1
	if val1 > val2 :
		writeregister(0x0610, 0x001D)  # calibration mode and Bandgap ADC input disc=0 HBT=0
		writeregister(0x0000, 0xFF20)  # mesure command
		time.sleep(0.01)
		val3 = readregister(0x0612)  # store value with HBT = 0
		writeregister(0x0610, 0x081D)  # calibration mode and Bandgap ADC input disc=0 HBT=1
		writeregister(0x0000, 0xFF20)  # mesure command
		time.sleep(0.01)
		val4 = readregister(0x0612)  # store value with dis = 1
		if val3 > val4:
			writeregister(0x0610,0x0001)	#cal mode dis=0 HBT=0
			ADC_reg_data = 0x0000
			print 'Discriminator=0 HBT=0\n'
		else :
			writeregister(0x0610, 0x0801)	#cal mode dis=0 HBT=1
			ADC_reg_data = 0x0800
			print 'Discriminator=0 HBT=1\n'
	else :
		writeregister(0x0610, 0x011D)  # calibration mode and Bandgap ADC input disc=1 HBT=0
		writeregister(0x0000, 0xFF20)  # mesure command
		time.sleep(0.01)
		val3 = readregister(0x0612)  # store value with HBT = 0
		writeregister(0x0610, 0x091D)  # calibration mode and Bandgap ADC input disc=1 HBT=1
		writeregister(0x0000, 0xFF20)  # mesure command
		time.sleep(0.01)
		val4 = readregister(0x0612)  # store value with dis = 1
		if val3 > val4:
			writeregister(0x0610, 0x0101)	#cal mode dis=1 HBT=0
			ADC_reg_data = 0x0100
			print 'Discriminator=1 HBT=0\n'
		else :
			writeregister(0x0610, 0x0901)	#cal mode dis=1 HBT=1
			ADC_reg_data = 0x0900
			print 'Discriminator=1 HBT=1\n'
	writeregister(0x0000, 0xFF20)  # mesure command, manual measure on AVSS(0mV)
	time.sleep(0.01)
	offset = readregister(0x0612)
	print "ADC measure offset = %d\n" % offset
	writeregister(0x0610,ADC_reg_data + 2)	#auto mode and whatever dis and HBT
	return offset

def V_out(ADC_VALUE, ADC_OFFSET):
	V_mis = (ADC_VALUE - ADC_OFFSET)*2*1.068 #mV
	return V_mis

def I_out(ADC_VALUE, ADC_OFFSET):
	I_mis = (ADC_VALUE - ADC_OFFSET)*1.068/5 #uA
	return I_mis

def measure_ADC():
	ADC_offset = ADC_calibration()
	writeregister(0x0000,0xFF20)	#mesure ADC
	time.sleep(0.100)	#wait 100ms
	ADC_VRSTP = readregister(0x61B)
	ADC_VRSTD = readregister(0x61C)
	ADC_AVDD= readregister(0x616)
	ADC_VPULSEH = readregister(0x619)
	ADC_VPULSEL = readregister(0x61A)
	ADC_VCASN = readregister(0x617)
	ADC_VCASP = readregister(0x618)
	ADC_VCASN2 = readregister(0x61D)
	ADC_ITHR = readregister(0x620)
	ADC_TEMP = readregister(0x627)
	VRSTP = V_out(ADC_VRSTP, ADC_offset)
	print "VRSTP=%d mV\n" % (VRSTP - 370)
	VRSTD = V_out(ADC_VRSTD,ADC_offset)
	print "VRSTD=%d mV\n" % (VRSTD-370)
	AVDD = V_out(ADC_AVDD,ADC_offset)
	print "AVDD=%d mV\n" % AVDD
	VPULSEH = V_out(ADC_VPULSEH, ADC_offset)
	print "VPULSEH=%d mV\n" % (VPULSEH-370)
	VPULSEL = V_out(ADC_VPULSEL, ADC_offset)
	print "VPULSEL=%d mV\n" % (VPULSEL-370)
	VCASN = V_out(ADC_VCASN, ADC_offset)
	print "VCASN=%d mV\n" % VCASN
	VCASP = V_out(ADC_VCASP, ADC_offset)
	print "VCASP=%d mV\n" % VCASP
	VCASN2 = V_out(ADC_VCASN2, ADC_offset)
	print "VCASN2=%d mV\n" % VCASN2
	ITHR = I_out(ADC_ITHR, ADC_offset)
	print "(this one should be divided by 54000)ITHR=%d uA\n" % ITHR
	#TEMP_read = (ADC_TEMP - ADC_offset)*0.147-51.5
	TEMP_read = (ADC_TEMP - ADC_offset) * 0.147
	print "Temperature=%d C" % TEMP_read

def maskAllPixels(enable):
  writeregister(0x0487,0x0000)
  writeregister(0x0500,0x0002 if enable == True else 0x0000)
  writeregister(0x0487,0xFFFF)
  writeregister(0x0487,0x0000)


def enablePulserAllPixels(enable):
  writeregister(0x0487,0x0000)
  writeregister(0x0500,0x0003 if enable == True  else 0x0001)
  writeregister(0x0487,0xFFFF)
  writeregister(0x0487,0x0000)


def maskPixel(x,y,enable):
  writeregister(0x0487,0x0000)
  writeregister(0x0500,0x0002 if enable == True else 0x0000)
  writeregister((x&0x3E0)<<6|0x0400|(1+(x>>4&0x1)),1<<(x&0xF))
  writeregister((y&0x1F0)<<7|0x0404               ,1<<(y&0xF))
  writeregister(0x0487,0x0000)

def enablePulserPixel(x,y,enable):
  writeregister(0x0487,0x0000)
  writeregister(0x0500,0x0003 if enable == True else 0x0001)
  writeregister(((x&0x3E0)<<6)|0x0400|(1+(x>>4&0x1)),1<<(x&0xF))
  writeregister(((y&0x1F0)<<7)|0x0404               ,1<<(y&0xF))
  writeregister(0x0487,0x0000)

def cc_print():
	print """
		ALPIDE COMMAND console
		power on			:	pon
		power off			:	poff
		initialize			:	init
		change Chip_ID 			:	ci
		write broadcast command	:	bc
		write register			:	wr 
		multicast write			:	mw
		read register			:	rr
		trigger				:	tr
		clear all error (MASTER)	:	rerr
		readout options				:	roop
		continous read out			:	roc
		raw data read out				:rord
		decode raw data					:dd
		pulse all pixels		:	pa
		pulse a pixel			:	ps
		mask all pixels			:	ma
		mask pixel			:	ms
		start pulse test		:	spt
		test threshold			: tt
		print cmd and address		:	pcmd
		list of register addresses	:	lra
		list of cmds			:	lcmd
		list of data			:	ld
		command console			:	cc
		measure				: 	me
		mask noisy pixels : mnp
		exit programm			:	exit
	"""

#routine list
power_off = 0b0000
power_on = 0b0001
initialize = 0b0010
read_register = 0b0100
read_out = 0b0101
write_cmd = 0b1000
write_register = 0b1001
trigger_cmd = 0b1010
clear_err = 0b1111	


if __name__ == "__main__":

	#connection to the arty via ipbus
	manager = uhal.ConnectionManager("file://ALPIDE_connection.xml")
	hw = manager.getDevice("ALPIDE")
	hw.getNode("CSR.ctrl.strt").write(0b0)	#stet start to 0
	hw.dispatch()

	
	get_status()	#get all status
	exit = 0
	RR_addr = 0xFFFF	#register to be read
	OP_cmd = 0xFF	#broadcast command to send (should be a logical restriction among the possibilities)
	Chip_ID = 0x12	#chip identification one of 0x12,0x16,0x1A,0x1E
	WR_addr = 0xFFFF	#register to be written
	WR_data = 0xFFFF	#data to be written in register
	mode_cfg = 0x0208	#0x0208 matrix readout speed every 2 clk cycles and read out form CMU
	#print command console
	cc_print()

	while exit == 0:
		
		ip = raw_input()
		if ip == "pon":
			send_cmd(power_on)
			get_status()

		elif ip == "poff":
			send_cmd(power_off)
			get_status()

		elif ip == "init":
			if powered:
				send_cmd(initialize)
				get_status()
			else:
				print "ALPIDE not powererd"

		elif ip == "ci":
			Chip_ID = input("Write Chip ID, one among 0x12,0x16,0x1A,0x1E or 0x0F for multicast(only write)\n")
			hw.getNode("cmd_addr.Chip_ID").write(Chip_ID)
			hw.dispatch()

		elif ip == "bc":
			if initialized:
				OP_cmd = input("Write the OP command to send\n")
				send_broadcast(OP_cmd)
			else:
				print "ALPIDE not initialized"

		elif ip == "wr":
			if initialized:
				WR_addr = input("Write address register\n")
				WR_data = input("Write data to write on address 0x%04x\n" % (WR_addr))
				writeregister(WR_addr, WR_data)
				get_status()
			else:
				print "ALPIDE not initialized"

		elif ip == "mw":
			if initialized:
				hw.getNode("cmd_addr.Chip_ID").write(0x0F)	#multicast ID
				hw.dispatch()
				WR_addr = input("Write address register\n")
				WR_data = input("Write data to write on address 0x%04x\n" % (WR_addr))
				writeregister(WR_addr, WR_data)
				hw.getNode("cmd_addr.Chip_ID").write(Chip_ID)	#reset previous CHIP ID
				hw.dispatch()
			else:
				print "ALPIDE not initialized"

		elif ip == "rr":
			if initialized:
				RR_addr = input("Write address register\n")
				reg_read = readregister(RR_addr)
				print "@ Address [0x%04x] is stored the value : 0x%04x" % (RR_addr, reg_read)
				get_status()
				if err_slave:	#more then 51 clk cycles driven by slave
					print "Slave drive on time out"
				if err_idle:
					print "high signal not detected on idle phase"
				if err_read:
					print "stop bit not detected"
				if err_chip_id:
					print "different chip ID recieved"
			else:
				print "ALPIDE not initialized"

		elif ip == "tr":
			if initialized:
				send_cmd(trigger_cmd)
			else:
				print "ALPIDE not initialized"

		elif ip == "rerr":
			send_cmd(clear_err)

		elif ip == "roop":	#read out option
			ro_op_mask = 0x000000
			en_op = input("Select read out mode?(0->Triggered 1->Coninous)\n")
			if en_op == 0:
				ro_op_mask = ro_op_mask | 0x000001  # 1 triggered 2 continous
			elif en_op == 1:
				ro_op_mask = ro_op_mask | 0x000002  # 1 triggered 2 continous
			en_op = input("Enable clustering?(True or False)\n")
			if en_op:
				ro_op_mask = ro_op_mask | 0x000004	#enable on bit 2
			mode_cfg = 0x0208 | ro_op_mask	#0x0208 matrix readout speed every 2 clk cycles and read out form CMU
			writeregister(0x0001, mode_cfg)	#mode cotrol register

		elif ip == "roc":
			if initialized:
				n_events = 0	#events detected
				n_idle = 0	#data idle recieved
				n_busy = 0 #data busy recieved
				n_data = 0	#data recieved
				file = open("Read_out_flags.txt", "w")	#Here read out falgs will be saved
				STB_dur = input("Clk cycles strobe duration =\n")
				STB_gap = input("Clk cycles strobe gap =\n")
				hitmap_matrix  = np.zeros((512,1024))	#hitmap matrix set all to zeros
				writeregister(0x0001, mode_cfg)  # mode cotrol register configuration (see above)
				writeregister(0x0004, 0x0018)	# FROMU CFG reg 1, enable internal STROBE(bit 3), enable busy monitoring (bit 4)
				writeregister(0x0005, STB_dur)	#STROBE duration STB_dur*25ns
				writeregister(0x0006, STB_gap)	#gap between 2 STROBES	STB_gap*25ns
				send_cmd(trigger_cmd)	#need to first external start the STROBE generation
				send_cmd(read_out)
				while True:
					try:
						mem_readable = hw.getNode("CSR.status.mem_readable").read()	#get memory readable status from FPGA
						hw.dispatch()
						if mem_readable:
							FIFO = hw.getNode("DATA.ro_data").readBlock(0x200)
							hw.dispatch()
							for word in FIFO:
								n_data = n_data + 1
								if (word & 0xF00000) == 0xA00000:  # chip header
									plane_id = (word & 0x0F0000) >> 16
									bc = (word & 0x00FF00) >> 8
								elif (word & 0xF00000) == 0xB00000:  # chip trailer
									ro_flags = (word & 0x0F0000) >> 16
									if ro_flags != 0x0 :
										file.write("Read out flags [0x%x] detected on bunch counter  %d\n" % (ro_flags, bc))
								elif (word & 0xF00000) == 0xE00000:  # chip empty
									plane_id = (word & 0x0F0000) >> 16
									bc = (word & 0x00FF00) >> 8
								elif (word & 0xE00000) == 0xC00000:  # reagion header
									region= (word>>16) & 0x1F
								elif (word & 0xC00000) == 0x400000:  # short
									word_shifted = word>>8
									x = region<<5 | word_shifted>>9 & 0x1E | (word_shifted ^ word_shifted>>1) & 0x1	#region*32 + encoderid*2 + addr correction
									y = word_shifted>>1 & 0x1FF	#addr/2
									hitmap_matrix[y,x] = hitmap_matrix[y,x] + 1
									n_events = n_events +1
								elif (word & 0xC00000) == 0x000000:  # long
									word_shifted = word>>8
									address = word_shifted & 0x3ff
									x = region<<5 | word_shifted>>9 & 0x1E | (word_shifted ^ word_shifted>>1) & 0x1
									y = word_shifted>>1 & 0x1FF
									hitmap_matrix[y,x] = hitmap_matrix[y,x] + 1
									hitmap = word & 0x7F
									n_events = n_events + 1
									for i in range(7):
										hitmap_shifted = hitmap>>i
										if (hitmap_shifted & 0x1) == 0x1:
											addressmap = address + i + 1
											xhm = region<<5 | word_shifted>>9 & 0x1E | (addressmap ^ addressmap>>1) & 0x1	#x hit map
											yhm = addressmap>>1	#y hit map
											hitmap_matrix[yhm, xhm] = hitmap_matrix[yhm, xhm] + 1
											n_events = n_events + 1
								elif word == 0xFFFFFF:	#idle
									n_idle = n_idle + 1
								elif word == 0xF1FFFF:	#busy on
									n_busy = n_busy + 1
								elif word == 0xF0FFFF:	#busy off
									n_busy = n_busy + 1
								#else:
						hw.getNode("CSR.ctrl.mem_read").write(0b1)
						hw.getNode("CSR.ctrl.mem_read").write(0b0)
						hw.dispatch()
					except KeyboardInterrupt:
						hw.getNode("CSR.ctrl.ro_stop").write(0b1)
						hw.dispatch()
						break
				get_status()
				if err_slave:  # more then 51 clk cycles driven by slave
					print
					"Slave drive on time out"
				if err_idle:
					print
					"high signal not detected on idle phase"
				if err_read:
					print
					"stop bit not detected"
				if err_chip_id:
					print
					"different chip ID recieved"
				dead_time = float(n_idle)/n_data*100
				print """
				Data recieved	= %d
				Data idle recieved	= %d
				Data busy recieved	= %d
				Dead time [percentage] = %f
				Events detected	= %d
				""" % (n_data, n_idle, n_busy, dead_time, n_events)
				np.save('hitmap_matrix', hitmap_matrix)
				file.close()	#close Read out flags txt file
				save_hitmap(hitmap_matrix, 'Hitmap.png')
				save_hitmap_logscale(hitmap_matrix, 'Hitmap_log.png')
				time.sleep(0.001)
				hw.getNode("CSR.ctrl.ro_stop").write(0b0)
				hw.dispatch()
			else:
				print "ALPIDE not initialized"
		elif ip == "rord":	#raw data readout
			if initialized:
				raw_data=[]
				writeregister(0x0001, mode_cfg)  # mode cotrol register configuration (see above)
				# FROMU CFG reg 1, enable internal STROBE(bit 3), enable busy monitoring (bit 4)
				writeregister(0x0004, 0x0018)
				writeregister(0x0005, 0x000F)	#STROBE duration 4 clk cycles (400ns)
				writeregister(0x0006, 0x0640)	#gap between 2 STROBES	640 clk cycles (16us)
				send_cmd(trigger_cmd)	#need to first external start the STROBE generation
				send_cmd(read_out)
				while True:
					try:
						mem_readable = hw.getNode("CSR.status.mem_readable").read()	#get memory readable status from FPGA
						hw.dispatch()
						if mem_readable:
							FIFO = hw.getNode("DATA.ro_data").readBlock(0x200)
							hw.dispatch()
							raw_data.extend(FIFO)
							hw.getNode("CSR.ctrl.mem_read").write(0b1)	#send memory read signal to FPGA
							hw.getNode("CSR.ctrl.mem_read").write(0b0)
							hw.dispatch()
					except KeyboardInterrupt:
						hw.getNode("CSR.ctrl.ro_stop").write(0b1)	#send stop  read out to FPGA
						hw.dispatch()
						time.sleep(0.001)
						writeregister(0x0004, 0x0000)  # FROMU CFG reg 1, disable internal STROBE
						np.save('Rawdata', raw_data)  # save data on npy file
						raw_data = []
						break
				get_status()
				if err_slave:  # more then 51 clk cycles driven by slave
					print
					"Slave drive on time out"
				if err_idle:
					print
					"high signal not detected on idle phase"
				if err_read:
					print
					"stop bit not detected"
				if err_chip_id:
					print
					"different chip ID recieved"
				time.sleep(0.001)
				hw.getNode("CSR.ctrl.ro_stop").write(0b0)
				hw.dispatch()
			else:
				print "ALPIDE not initialized"
		elif ip == "dd":
			decode_data()
		elif ip == "pa":
			en = input("Enable Pulser on all pixels? (True or False)\n")
			enablePulserAllPixels(en)
		elif ip == "ps":
			x = input("pixel x coordinate\n")
			y = input("pixel y coordinate\n")
			en = input("Enable or disable pulse on selected pixel(True or False)\n")
			enablePulserPixel(x,y,en)
		elif ip == "spt":	#start pulse test
			Pt = raw_input("Pulse type Analog(a) or Digital(d)\n")
			if Pt == "a":
				writeregister(0x0004,0x0060)	#Analog pulse, automatic strobe after pulse command
			elif Pt == "d":
				writeregister(0x0004, 0x0040)  # Digital pulse, automatic strobe after pulse command
			else:
				print "Bad input"
				break
			pixel_react=pulse_test(mode_cfg)
			writeregister(0x0004, 0x0000)
		elif ip == "tt":  # start test threshold
			file = open("Threshold_test.txt", "w")
			enablePulserAllPixels(False)	#disable pulse on all pixels
			maskAllPixels(True)	#mask all pixels
			for k in range(20):
				for i in range(10):
					maskPixel(30+k, 485+i, False)	#unmask selected pixel
					enablePulserPixel(30+k, 485+i, True) #enable pulse on 200 pixels
			writeregister(0x0004, 0x0060)  # Analog pulse, automatic strobe after pulse command
			writeregister(0x0606, 0x0000)  # Set PULSEL to 0.37V (DAC offset)
			for k in range (120):
				pulse_test_array = []  # initialize empty array
				Q_inj = ((k)*7.06e-3*230e-18)/(1.602e-19)
				writeregister(0x0605,k)  # Set PULSEH to k*7.06 mV
				time.sleep(0.0001)
				for j in range (15):
					time.sleep(0.0001)
					ppf = pulse_test(mode_cfg) #pixel pulsed fraction
					pulse_test_array.append(ppf)
					#np.append(pulse_test_array, ppf)
				mean = np.mean(pulse_test_array)
				std = np.nanstd(pulse_test_array)
				file.write("%f	%f	0	%f\n" % (Q_inj, mean, std))
			file.close()
			writeregister(0x0004, 0x0000)
			maskAllPixels(False)	#unmask all pixels
		elif ip == "ma":
			en = input("Mask or unmask all pixels? (True for masking)\n")
			maskAllPixels(en)
		elif ip == "ms":
			x = input("pixel x coordinate\n")
			y = input("pixel y coordinate\n")
			en = input("Mask or unmask(True or False)\n")
			maskPixel(x,y,en)
		elif ip == "pcmd":
			RR_addr = hw.getNode("cmd_addr.RR_addr").read()
			OP_command = hw.getNode("cmd_addr.OP_command").read()
			Chip_ID = hw.getNode("cmd_addr.Chip_ID").read()
			WR_addr = hw.getNode("cmd_addr.WR_addr").read()
			WR_data = hw.getNode("cmd_addr.WR_data").read()
			hw.dispatch()
			print """
				RR_addr	= 0x%04x
				OP_cmd	= 0x%02x
				Chip_ID	= 0x%02x
				WR_addr	= 0x%04x
				WR_data	= 0x%04x
				""" % (RR_addr, OP_command, Chip_ID, WR_addr, WR_data)
		elif ip == "lra":
			print """
				ALPIDE_REG_COMMAND	= 0x0000
				ALPIDE_REG_MODE_CTRL	= 0x0001
				ALPIDE_REG_FROMU_CFG1	= 0x0004
				ALPIDE_REG_FROMU_CFG2	= 0x0005
				ALPIDE_REG_FROMU_CFG3	= 0x0006
				ALPIDE_REG_CMUDMU_CFG	= 0x0010
				ALPIDE_REG_DMU_FIFO_LOW	= 0x0012
				ALPIDE_REG_DMU_FIFO_HI	= 0x0013
				ALPIDE_REG_DAC_VRESETD	= 0x0602
				ALPIDE_REG_DAC_VCASN	= 0x0604
				ALPIDE_REG_DAC_VPULSEH	= 0x0605
				ALPIDE_REG_DAC_VPULSEL	= 0x0606
				ALPIDE_REG_DAC_VCASN2	= 0x0607
				ALPIDE_REG_DAC_ITHR	= 0x060E
			"""
		elif ip == "lcmd":
			print """
				ALPIDE_CMD_TRIGGER	= 0x0055
				ALPIDE_CMD_GRST		= 0x00D2
				ALPIDE_CMD_PRST		= 0x00E4
				ALPIDE_CMD_PULSE	= 0x0078
				ALPIDE_CMD_BCRST	= 0x0036
				ALPIDE_CMD_RORST	= 0x0063
				ALPIDE_CMD_DEBUG	= 0x00AA
				ALPIDE_CMD_WROP		= 0x009C
				ALPIDE_CMD_RDOP		= 0x004E
				ALPIDE_CMD_CMU_CLEAR_ERR= 0xFF00
				ALPIDE_CMD_FIFOTEST	= 0xFF01
				ALPIDE_CMD_LOADOBDEFCFG	= 0xFF02
				ALPIDE_CMD_XOFF		= 0xFF10
				ALPIDE_CMD_XON		= 0xFF11
				ALPIDE_CMD_ADCMEASURE	= 0xFF20
			""" 
		elif ip == "ld":
			print """
				ALPIDE_DATA_CHIP_HEADER[16]	= 0xA(ID[4])(BC[8])
				ALPIDE_DATA_CHIP_TRAILER[8]	= 0xB(ID[4])
				ALPIDE_DATA_CHIP_EMPTY[16]	= 0xE(ID[4])(BC[8])
				ALPIDE_DATA_REGION_HEADER[8]	= 0b110(RH[5])
				ALPIDE_DATA_DATA_SHORT[16]	= 0b01(ENID[4])(addr[10])
				ALPIDE_DATA_DATA_LONG[24]	= 0b00(ENID[4])(addr[10])0(HITMAP[7])
				ALPIDE_DATA_BUSY_ON[8]		= 0xF1
				ALPIDE_DATA_BUSY_OFF[8]		= 0xF0
			"""
		elif ip == "cc":
			cc_print()
		elif ip == "me":
			measure_ADC()
		elif ip == "mnp":
			if initialized:
				raw_data=[]
				read_cnt = 0
				hitmap_matrix  = np.zeros((512,1024))
				writeregister(0x0001, mode_cfg)  # mode cotrol register configuration (see above)
				# FROMU CFG reg 1, enable internal STROBE(bit 3), enable busy monitoring (bit 4)
				writeregister(0x0004, 0x0018)
				writeregister(0x0005, 400)	#STROBE duration 16 clk cycles (10us)
				writeregister(0x0006, 9600)	#gap between 2 STROBES	384 clk cycles (240us) sample every 250 us-->4kHz
				send_cmd(trigger_cmd)	#need to first external start the STROBE generation
				send_cmd(read_out)
				while read_cnt < 10000:
					mem_readable = hw.getNode("CSR.status.mem_readable").read()	#get memory readable status from FPGA
					hw.dispatch()
					if mem_readable:
						read_cnt = read_cnt + 1
						FIFO = hw.getNode("DATA.ro_data").readBlock(0x200)
						hw.dispatch()
						for word in FIFO:
							if (word & 0xF00000) == 0xA00000:  # chip header
								plane_id = (word & 0x0F0000) >> 16
								bc = (word & 0x00FF00) >> 8
							elif (word & 0xF00000) == 0xB00000:  # chip trailer
								ro_flags = (word & 0x0F0000) >> 16
							elif (word & 0xF00000) == 0xE00000:  # chip empty
								plane_id = (word & 0x0F0000) >> 16
								bc = (word & 0x00FF00) >> 8
							elif (word & 0xE00000) == 0xC00000:  # reagion header
								region= (word>>16) & 0x1F
							elif (word & 0xC00000) == 0x400000:  # short
								word_shifted = word>>8
								x = region<<5 | word_shifted>>9 & 0x1E | (word_shifted ^ word_shifted>>1) & 0x1	#region*32 + encoderid*2 + addr correction
								y = word_shifted>>1 & 0x1FF	#addr/2
								hitmap_matrix[y,x] = hitmap_matrix[y,x] + 1
							elif (word & 0xC00000) == 0x000000:  # long
								word_shifted = word>>8
								address = word_shifted & 0x3ff
								x = region<<5 | word_shifted>>9 & 0x1E | (word_shifted ^ word_shifted>>1) & 0x1
								y = word_shifted>>1 & 0x1FF
								hitmap_matrix[y,x] = hitmap_matrix[y,x] + 1
								hitmap = word & 0x7F
								for i in range(7):
									hitmap_shifted = hitmap>>i
									if (hitmap_shifted & 0x1) == 0x1:
										addressmap = address + i + 1
										xhm = region<<5 | word_shifted>>9 & 0x1E | (addressmap ^ addressmap>>1) & 0x1	#x hit map
										yhm = addressmap>>1	#y hit map
										hitmap_matrix[yhm, xhm] = hitmap_matrix[yhm, xhm] + 1
							#elif word == 0xFFFFFF:	#idle
							#elif word == 0xF1FFFF:	#busy on
							#elif word == 0xF0FFFF:	#busy off
							#else:
						hw.getNode("CSR.ctrl.mem_read").write(0b1)	#send memory read signal to FPGA
						hw.getNode("CSR.ctrl.mem_read").write(0b0)
						hw.dispatch()
				hw.getNode("CSR.ctrl.ro_stop").write(0b1)	#send stop  read out to FPGA
				hw.dispatch()
				writeregister(0x0004, 0x0000)  # FROMU CFG reg 1, disable internal STROBE
				hw.dispatch()
				n_pixel_masked = 0
				for row in range(512):
					for column in range (1024):
						if hitmap_matrix[row,column] > 3:
							n_pixel_masked = n_pixel_masked + 1
							maskPixel(column,row, True)
							print "\nMasked pixel x=%d  y=%d\n" % (column, row)
				print "Masked %d Pixels in total" % n_pixel_masked
				get_status()
				if err_slave:  # more then 51 clk cycles driven by slave
					print
					"Slave drive on time out"
				if err_idle:
					print
					"high signal not detected on idle phase"
				if err_read:
					print
					"stop bit not detected"
				if err_chip_id:
					print
					"different chip ID recieved"
				time.sleep(0.001)
				hw.getNode("CSR.ctrl.ro_stop").write(0b0)
				hw.dispatch()
			else:
				print "ALPIDE not initialized"	
		elif ip == "exit":	
			exit = 1
		else:
			print "Command not found\n"

	send_cmd(power_off)	
