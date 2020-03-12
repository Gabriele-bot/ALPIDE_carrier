-makelib ies_lib/xil_defaultlib -sv \
  "D:/Programmi/Vivado/Vivado/2018.3/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
  "D:/Programmi/Vivado/Vivado/2018.3/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \
-endlib
-makelib ies_lib/xpm \
  "D:/Programmi/Vivado/Vivado/2018.3/data/ip/xpm/xpm_VCOMP.vhd" \
-endlib
-makelib ies_lib/xil_defaultlib \
  "../../../ip/R_W_PLL_1/R_W_PLL_clk_wiz.v" \
  "../../../ip/R_W_PLL_1/R_W_PLL.v" \
-endlib
-makelib ies_lib/xil_defaultlib \
  glbl.v
-endlib

