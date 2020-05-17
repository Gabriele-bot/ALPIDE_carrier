set_property SRC_FILE_INFO {cfile:D:/Progetti_vivado/ALPIDE_slave/ALPIDE_slave.srcs/constrs_1/imports/digilent-xdc-master/Arty-Z7-10-Master.xdc rfile:../../../ALPIDE_slave.srcs/constrs_1/imports/digilent-xdc-master/Arty-Z7-10-Master.xdc id:1} [current_design]
set_property src_info {type:XDC file:1 line:11 export:INPUT save:INPUT read:READ} [current_design]
set_property -dict { PACKAGE_PIN M20  IOSTANDARD LVCMOS33 } [get_ports { sw }]; #IO_L7N_T1_AD2N_35 Sch=SW0
set_property src_info {type:XDC file:1 line:23 export:INPUT save:INPUT read:READ} [current_design]
set_property -dict { PACKAGE_PIN R14    IOSTANDARD LVCMOS33 } [get_ports { read_err }]; #IO_L6N_T0_VREF_34 Sch=LED0
set_property src_info {type:XDC file:1 line:29 export:INPUT save:INPUT read:READ} [current_design]
set_property -dict { PACKAGE_PIN D19    IOSTANDARD LVCMOS33 } [get_ports { rst }]; #IO_L4P_T0_35 Sch=BTN0
set_property src_info {type:XDC file:1 line:44 export:INPUT save:INPUT read:READ} [current_design]
set_property CLOCK_DEDICATED_ROUTE FALSE [get_nets MMCM/inst/clk_in1_R_W_PLL];
set_property src_info {type:XDC file:1 line:47 export:INPUT save:INPUT read:READ} [current_design]
set_property -dict { PACKAGE_PIN Y14   IOSTANDARD LVCMOS33 } [get_ports { CTRL }]; #IO_L8N_T1_34 Sch=JB1_N
set_property src_info {type:XDC file:1 line:54 export:INPUT save:INPUT read:READ} [current_design]
set_property -dict { PACKAGE_PIN V12   IOSTANDARD LVCMOS33 } [get_ports { DCLK }]; #IO_L4P_T0_34 Sch=JB4_P
