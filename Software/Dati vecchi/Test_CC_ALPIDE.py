import uhal
import time
from subprocess import call

def send_cmd(cmd):
	hw.getNode("CSR.ctrl.op_sw").write(cmd)
	hw.getNode("CSR.ctrl.strt").write(0b1)
	hw.dispatch()
	time.sleep(0.001)
	hw.getNode("CSR.ctrl.strt").write(0b0)
	hw.dispatch()

def get_status():
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

	manager = uhal.ConnectionManager("file://ALPIDE_connection.xml")
	hw = manager.getDevice("ALPIDE")
	hw.getNode("CSR.ctrl.strt").write(0b0)

	
	get_status()
	exit = 0
	cnt = 0
	byte_cnt = 0	#byte conter	
	err_cnt	= 0	#count error on read out
    	RR_addr = 0xFFFF	#register to be read
    	OP_cmd = 0xFF	#broadcast command to send (shuld be a logical restriction among the possibilities)
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
			send_cmd(power_on)
			get_status()
		elif ip == "poff":
			send_cmd(power_off)
			get_status()
		elif ip == "init":
			if powered == True:
				send_cmd(initialize)
				get_status()
			else:
				print "ALPIDE not powererd"
		elif ip == "ci":
			Chip_ID = input("Write Chip ID, one among 0x12,0x16,0x1A,0x1E\n")
			hw.getNode("cmd_addr.Chip_ID").write(Chip_ID)
			hw.dispatch()
		elif ip == "op":
			if initialized == True:
				OP_cmd = input("Write the OP command to send\n")
				hw.getNode("cmd_addr.OP_command").write(OP_cmd)
				hw.dispatch()
				send_cmd(write_cmd)
			else:
				print "ALPIDE not initialized"
		elif ip == "wr":
			if initialized == True:
				WR_addr = input("Write address register\n")
				WR_data = input("Write data to write on address 0x%04x\n" % (WR_addr))
				hw.getNode("cmd_addr.WR_addr").write(WR_addr)
				hw.getNode("cmd_addr.WR_data").write(WR_data)
				hw.dispatch()
				send_cmd(write_register)
			else:
				print "ALPIDE not initialized"
		elif ip == "rr":
			if initialized == True:
				RR_addr = input("Write address register\n")
				hw.getNode("cmd_addr.RR_addr").write(RR_addr)
				send_cmd(read_register)
				reg_read = hw.getNode("DATA.reg_read").read()
				hw.dispatch()
				print "@ Address [0x%04x] is stored the value : 0x%04x" % (RR_addr,reg_read)
			else:
				print "ALPIDE not initialized"
		elif ip == "tr":
			if initialized == True:
				send_cmd(trigger_cmd)
			else:
				print "ALPIDE not initialized"
		elif ip == "rerr":
			send_cmd(clear_err)
		elif ip == "ro":
			if initialized == True:
				send_cmd(read_out)
				while True:
					try:
						mem_readable=hw.getNode("CSR.status.mem_readable").read()
						hw.dispatch()
						if mem_readable == True:
							FIFO = hw.getNode("DATA.ro_data").readBlock(0x200)
							hw.dispatch()
							for x in FIFO:
								if x != cnt:
									err_cnt = err_cnt +1
								cnt = cnt + 1
								byte_cnt = byte_cnt + 1
								if cnt == 16777216:
									cnt = 0
							hw.getNode("CSR.ctrl.mem_read").write(0b1)
							hw.getNode("CSR.ctrl.mem_read").write(0b0)
							hw.dispatch()
					except KeyboardInterrupt:
						hw.getNode("CSR.ctrl.ro_stop").write(0b1)
						hw.dispatch()
        					break
				time.sleep(0.005)
				hw.getNode("CSR.ctrl.ro_stop").write(0b0)
				hw.dispatch()
				print "\n %d data of %d is/are corrupted" % (err_cnt,byte_cnt)
				cnt = 0
				byte_cnt = 0
				err_cnt = 0
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
