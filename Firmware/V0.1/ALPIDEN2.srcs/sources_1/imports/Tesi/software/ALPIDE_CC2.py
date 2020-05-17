import uhal
import time

def s_ib_tr(node,array):
	hw.getNode(node).writeBlock(array)
	hw.dispatch()	

if __name__ == "__main__":

	manager = uhal.ConnectionManager("file://ALPIDE_connection.xml")
	hw = manager.getDevice("ALPIDE")
	hw.getNode("CSR.ctrl.strt").write(0b0)
	powered=hw.getNode("CSR.status.powered").read()
	initialized=hw.getNode("CSR.status.init").read()
	busy=hw.getNode("CSR.status.busy").read()
	FIFO_full=hw.getNode("CSR.status.FIFO_full").read()
	FIFO_empty=hw.getNode("CSR.status.FIFO_empty").read()
	hw.dispatch()
	print powered
	print initialized
	print busy
	print FIFO_full
	print FIFO_empty
	exit = 0
    	RR_addr = 0xFFFF	#register to be read
    	OP_cmd = 0xFF	#broadcast command to send (shuld be a logical restrictions among the possibilities)
   	Chip_ID = 0x12	#chip identification one of 0x12,0x16,0x1A,0x1E
	WR_addr = 0xFFFF	#register to be written
	WR_data = 0xFFFF	#data to be written in register
	
	
	while exit == 0:
		
		
		#print command console
		print """
			ALPIDE COMMAND console
			power on			:	pon
			power off			:	poff
			initialize			:	init
			change Chip_ID 			:	ci
			write OP command		:	op
			write register			:	wr 
			read register			:	rr
			trigger				:	tr
			clear all error (MASTER)	:	rerr
			read out			:	ro
			print cmd and address		:	pcmd
			list of register addresses	:	lra
			list of cmds			:	lcmd
			list of data			:	ld
			exit programm			:	exit
		"""
		ip = raw_input()
		if ip == "pon":
			hw.getNode("CSR.ctrl.op_sw").write(0b0001)
			hw.getNode("CSR.ctrl.strt").write(0b1)
			hw.dispatch()
			time.sleep(0.01)
			hw.getNode("CSR.ctrl.strt").write(0b0)
			powered=hw.getNode("CSR.status.powered").read()
			hw.dispatch()
		elif ip == "poff":
			hw.getNode("CSR.ctrl.op_sw").write(0b0000)
			hw.getNode("CSR.ctrl.strt").write(0b1)
			hw.dispatch()
			time.sleep(0.01)
			hw.getNode("CSR.ctrl.strt").write(0b0)
			powered = hw.getNode("CSR.status.powered").read()
			hw.dispatch()
		elif ip == "init":
			if powered == True:
				hw.getNode("CSR.ctrl.op_sw").write(0b0010)
				hw.getNode("CSR.ctrl.strt").write(0b1)
				hw.dispatch()
				time.sleep(0.05)
				hw.getNode("CSR.ctrl.strt").write(0b0)
				initialized = hw.getNode("CSR.status.init").read()
				hw.dispatch()
			else:
				print "ALPIDE not powererd"
		elif ip == "ci":
			Chip_ID = input("Write Chip ID, one among 0x12,0x16,0x1A,0x1E\n")
			hw.getNode("cmd_addr.Chip_ID").write(Chip_ID)
			hw.dispatch()
		elif ip == "op":
			if initialized == True:
				OP_cmd = input("Write the OP command to send\n")
				hw.getNode("CSR.ctrl.op_sw").write(0b1000)
				hw.getNode("CSR.ctrl.strt").write(0b1)
				hw.getNode("cmd_addr.OP_command").write(OP_cmd)
				hw.dispatch()
				time.sleep(0.02)
				hw.getNode("CSR.ctrl.strt").write(0b0)
				hw.dispatch()
			else:
				print "ALPIDE not initialized"
		elif ip == "wr":
			if initialized == True:
				WR_addr = input("Write address register\n")
				WR_data = input("Write data to write on address 0x%04x\n" % (WR_addr))
				hw.getNode("CSR.ctrl.op_sw").write(0b1001)
				hw.getNode("CSR.ctrl.strt").write(0b1)
				hw.getNode("cmd_addr.WR_addr").write(WR_addr)
				hw.getNode("cmd_addr.WR_data").write(WR_data)
				hw.dispatch()
				time.sleep(0.02)
				hw.getNode("CSR.ctrl.strt").write(0b0)
				hw.dispatch()
			else:
				print "ALPIDE not initialized"
		elif ip == "rr":
			if initialized == True:
				RR_addr = input("Write address register\n")
				hw.getNode("CSR.ctrl.op_sw").write(0b0100)
				hw.getNode("cmd_addr.RR_addr").write(RR_addr)
				hw.getNode("CSR.ctrl.strt").write(0b1)
				hw.dispatch()
				time.sleep(0.02)
				hw.getNode("CSR.ctrl.strt").write(0b0)
				reg_read = hw.getNode("reg_read").read()
				hw.dispatch()
				print "@ Address [0x%04x] is stored the value : 0x%04x" % (RR_addr,reg_read)
			else:
				print "ALPIDE not initialized"
		elif ip == "tr":
			if initialized == True:
				hw.getNode("CSR.ctrl.op_sw").write(0b1010)
				hw.getNode("CSR.ctrl.strt").write(0b1)
				hw.dispatch()
				time.sleep(0.02)
				hw.getNode("CSR.ctrl.strt").write(0b0)
				hw.dispatch()
			else:
				print "ALPIDE not initialized"
		elif ip == "rerr":
			hw.getNode("CSR.ctrl.op_sw").write(0b1111)
			hw.getNode("CSR.ctrl.strt").write(0b1)			
			hw.dispatch()
			time.sleep(0.001)
			hw.getNode("CSR.ctrl.strt").write(0b0)
			hw.dispatch()
		elif ip == "ro":
			if initialized == True:
				hw.getNode("CSR.ctrl").write(0b01011)
				hw.getNode("CSR.ctrl").write(0b0101)
				time.sleep(0.04)
				hw.getNode("CSR.ctrl").write(0b01010)
				FIFO = hw.getNode("regs").readBlock(0x100)
				hw.dispatch()
				i = 0
				for x in FIFO:
					print "@ Address [0x%06x] is stored the value : 0x%08x" % (i,x)
					i = i + 1
			else:
				print "ALPIDE not initialized"
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
			""" % (RR_addr,OP_command,Chip_ID,WR_addr,WR_data)
		elif ip == "lra":
			print """
				ALPIDE_REG_COMMAND	= 0x0000
				ALPIDE_REG_MODE_CTRL	= 0x0001
				ALPIDE_REG_FROMU_CFG1	= 0x0004
				ALPIDE_REG_FROMU_CFG2	= 0x0005
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
				ALPIDE_DATA_CHIP_HEADER		= 0xA0
				ALPIDE_DATA_CHIP_TRAILER	= 0xB0
				ALPIDE_DATA_CHIP_EMPTY		= 0xE0
				ALPIDE_DATA_REGION_HEADER	= 0xC0
				ALPIDE_DATA_DATA_SHORT		= 0x40
				ALPIDE_DATA_DATA_LONG		= 0x00
				ALPIDE_DATA_BUSY_ON		= 0xF1
				ALPIDE_DATA_BUSY_OFF		= 0xF0
			"""	
		elif ip == "exit":	
			exit = 1
		else:
			print "Command not found\n"