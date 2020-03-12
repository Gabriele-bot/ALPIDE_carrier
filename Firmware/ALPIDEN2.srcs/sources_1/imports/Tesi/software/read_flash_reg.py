import uhal

if __name__ == "__main__":

   # Code for the connection with the board

   manager = uhal.ConnectionManager("file://arty7_connection.xml")
   hw = manager.getDevice("arty7")

   

   regs = hw.getNode("regs").readBlock(0x100) 
   hw.dispatch()
   
   i = 0
   for x in regs:
      print "@ Address [0x%06x] is stored the value : 0x%08x" % (i,x)
      i = i + 1 
   
   data = hw.getNode("reg_read").read() 
   hw.dispatch()
   print "@ Address [0x0200] is stored the value : 0x%04x" % (data)
   
