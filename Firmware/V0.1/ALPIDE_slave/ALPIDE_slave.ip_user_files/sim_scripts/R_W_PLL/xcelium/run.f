-makelib xcelium_lib/xil_defaultlib -sv \
  "D:/Programmi/Vivado/Vivado/2018.3/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
-endlib
-makelib xcelium_lib/xpm \
  "D:/Programmi/Vivado/Vivado/2018.3/data/ip/xpm/xpm_VCOMP.vhd" \
-endlib
-makelib xcelium_lib/xil_defaultlib \
  "../../../../ALPIDE_slave.srcs/sources_1/ip/R_W_PLL/R_W_PLL_clk_wiz.v" \
  "../../../../ALPIDE_slave.srcs/sources_1/ip/R_W_PLL/R_W_PLL.v" \
-endlib
-makelib xcelium_lib/xil_defaultlib \
  glbl.v
-endlib

