import uhal
import time

def s_ib_tr(node,array):
	hw.getNode(node).writeBlock(array)
	hw.dispatch()	

if __name__ == "__main__":

	manager = uhal.ConnectionManager("file://arty7_connection.xml")
	hw = manager.getDevice("arty7")
	powered = False
	initialized = False
	exit = 0
    	RR_addr = 0xFFFF	#register to be read
    	OP_cmd = 0xFF	#broadcast command to send (shuld be a logical restrictions among the possibilities)
   	Chip_ID = 0x12	#chip identification one of 0x12,0x16,0x1A,0x1E
	WR_addr = 0xFFFF	#register to be written
	WR_data = 0xFFFF	#data to be written in register
	CFG_Run = 0b00000	#bit[4:1] command to perform( Power on/of, init, ecc) bit[0] validates the command
	
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
			CFG_Run = 0b00011
			arraycmd = [RR_addr,OP_cmd,Chip_ID,WR_addr,WR_data,CFG_Run]
			s_ib_tr("cmd",arraycmd)
			powered = True
		elif ip == "poff":
			CFG_Run = 0b00001
			arraycmd = [RR_addr, OP_cmd, Chip_ID, WR_addr, WR_data,CFG_Run]
			s_ib_tr("cmd",arraycmd)
			powered = False
			initialized = False
		elif ip == "init":
			if powered == True:
				CFG_Run = 0b00101
				arraycmd = [RR_addr, OP_cmd, Chip_ID, WR_addr, WR_data,CFG_Run]
				s_ib_tr("cmd",arraycmd)
				initialized = True
			else:
				print "ALPIDE not powererd"
		elif ip == "ci":
			CFG_Run = 0b00010
			Chip_ID = input("Write Chip ID, one among 0x12,0x16,0x1A,0x1E\n")
			arraycmd = [RR_addr, OP_cmd, Chip_ID, WR_addr, WR_data,CFG_Run]
			s_ib_tr("cmd",arraycmd)
		elif ip == "op":
			if initialized == True:
				OP_cmd = input("Write the OP command to send\n")
				CFG_Run = 0b10001
				arraycmd = [RR_addr, OP_cmd, Chip_ID, WR_addr, WR_data,CFG_Run]
				s_ib_tr("cmd",arraycmd)
			else:
				print "ALPIDE not initialized"
		elif ip == "wr":
			if initialized == True:
				WR_addr = input("Write address register\n")
				WR_data = input("Write data to write on address 0x%04x\n" % (WR_addr))
				CFG_Run = 0b10011
				arraycmd = [RR_addr, OP_cmd, Chip_ID, WR_addr, WR_data,CFG_Run]
				s_ib_tr("cmd",arraycmd)
			else:
				print "ALPIDE not initialized"
		elif ip == "rr":
			if initialized == True:
				RR_addr = input("Write address register\n")
				CFG_Run = 0b01001
				arraycmd = [RR_addr, OP_cmd, Chip_ID, WR_addr, WR_data,CFG_Run]
				s_ib_tr("cmd",arraycmd)
				time.sleep(0.02)
				CFG_Run = CFG_Run - 0b1
				arraycmd = [RR_addr, OP_cmd, Chip_ID, WR_addr, WR_data,CFG_Run]
				hw.getNode("cmd").writeBlock(arraycmd)
				reg_read = hw.getNode("reg_read").read()
				hw.dispatch()
				print "@ Address [0x%04x] is stored the value : 0x%04x" % (arraycmd[0],reg_read)
			else:
				print "ALPIDE not initialized"
		elif ip == "tr":
			if initialized == True:
				CFG_Run = 0b10101
				arraycmd = [RR_addr, OP_cmd, Chip_ID, WR_addr, WR_data,CFG_Run]
				s_ib_tr("cmd",arraycmd)
			else:
				print "ALPIDE not initialized"
		elif ip == "rerr":
			CFG_Run = 0b11111
			arraycmd = [RR_addr, OP_cmd, Chip_ID, WR_addr, WR_data,CFG_Run]
			s_ib_tr("cmd",arraycmd)
		elif ip == "ro":
			if initialized == True:
				CFG_Run = 0b01011
				arraycmd = [RR_addr, OP_cmd, Chip_ID, WR_addr, WR_data,CFG_Run]
				s_ib_tr("cmd",arraycmd)
				time.sleep(0.04)
				CFG_Run = CFG_Run - 0b1
				arraycmd = [RR_addr, OP_cmd, Chip_ID, WR_addr, WR_data,CFG_Run]
				s_ib_tr("cmd",arraycmd)
				FIFO = hw.getNode("regs").readBlock(0x100)
				hw.dispatch()
				i = 0
				for x in FIFO:
					print "@ Address [0x%06x] is stored the value : 0x%08x" % (i,x)
					i = i + 1
			else:
				print "ALPIDE not initialized"
		elif ip == "pcmd":
			cmd = hw.getNode("cmd").readBlock(5)
			hw.dispatch()
			print """
				RR_addr	= 0x%04x
				OP_cmd	= 0x%02x
				Chip_ID	= 0x%02x
				WR_addr	= 0x%04x
				WR_data	= 0x%04x
			""" % (cmd[0],cmd[1],cmd[2],cmd[3],cmd[4])
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
		
		
