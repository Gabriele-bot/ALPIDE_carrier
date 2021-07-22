# ALPIDE_carrier

## Firmware

### Simple ALPIDE-to-FPGA comuniction (via CTRL port @40MHZ)  
**` V0.4/ALPIDE_firmware `**: Arty-A7 firmware, it controls the ALPIDE mountend on an Arduino shield;  
The pinout is the following:  
Signals and controls   
- **`DCLK`**:  IO10(Chipkit);
- **`PW_EN`**: IO09(Chipkit);
- **`CTRL`**:  IO08(Chipkit);
- **`RSTN`**:  IO07(Chipkit);  
 
Voltages and grounds
- **`5V`**:   5V(Chipkit);
- **`3.3V`**: IOREF(Chipkit);
- **`GND`**:  GND(Chipkit);
- **`GND`**:  GND(Chipkit);  

Error LEDs:  
- **`Read_err`**: Stop bit not detected;
- **`Idle_err`**: High bit non detected on idle phase;
- **`Slave_err`**: Slave drive the line for 51 or more clk cycles;
- **`Chip_id_err`**: Wrong CHIP ID recived;  

  
Available routines:  
- **`POWER ON/OF`**: Set PW_EN to 1 or 0; 
- **`INIT`**: ALPIDE initialization that set some register at a specific values (VCASN for example);
- **`BROAADCAST`**:  Send a broadcast command (e.g TRIGGER); 
- **`READ/WRITE REG`**: Read/writes a specific register;
- **`READOUT`**:  Continuous reading of the two register that contain the data acquired;


### ALPIDE simulation with DE0 nano
ALPIDE simulation with a DE0-nano board for debugging and testing purposes;  
- listend to the read command
- store the address of the target register
- send back the address as data or a data pattern taht will be checked via software

## Software

- **`ALPIDE_CLI.py`**: command line interace to send command to the FPGA employing ipBUS protocol;
- **`xml files`**: files that contain the FPGA's ethernet address and the definition of the nodes utilized;
- **`Analyzer`** : Decode the packets into clusters via DBSACN or AGGLOMERATIVE clustering; 


