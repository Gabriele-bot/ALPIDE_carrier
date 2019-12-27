-makelib ies_lib/xil_defaultlib -sv \
  "D:/Programmi/Vivado/Vivado/2018.3/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
-endlib
-makelib ies_lib/xpm \
  "D:/Programmi/Vivado/Vivado/2018.3/data/ip/xpm/xpm_VCOMP.vhd" \
-endlib
-makelib ies_lib/xil_defaultlib \
  "../../../../ALPIDE_Reader.srcs/sources_1/ip/phase_shifter/phase_shifter_clk_wiz.v" \
  "../../../../ALPIDE_Reader.srcs/sources_1/ip/phase_shifter/phase_shifter.v" \
-endlib
-makelib ies_lib/xil_defaultlib \
  glbl.v
-endlib

