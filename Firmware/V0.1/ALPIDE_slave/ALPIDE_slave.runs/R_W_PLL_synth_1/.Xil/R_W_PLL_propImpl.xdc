set_property SRC_FILE_INFO {cfile:d:/Progetti_vivado/ALPIDE_slave/ALPIDE_slave.srcs/sources_1/ip/R_W_PLL/R_W_PLL.xdc rfile:../../../ALPIDE_slave.srcs/sources_1/ip/R_W_PLL/R_W_PLL.xdc id:1 order:EARLY scoped_inst:inst} [current_design]
current_instance inst
set_property src_info {type:SCOPED_XDC file:1 line:57 export:INPUT save:INPUT read:READ} [current_design]
set_input_jitter [get_clocks -of_objects [get_ports clk_in1]] 0.5
