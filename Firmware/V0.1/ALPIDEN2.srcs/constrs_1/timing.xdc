create_clock -period 10.000 -name sys_clk_pin -waveform {0.000 5.000} -add [get_ports clk_base_xc7a_i]
create_clock -period 40.000 -name clk_tx_mac -waveform {0.000 20.000} -add [get_ports mii_tx_clk_i]
create_clock -period 40.000 -name clk_rx -waveform {0.000 20.000} -add [get_ports mii_rx_clk_i]


set_false_path -from [get_clocks clk_rx] -to [get_clocks clk_tx_mac]
set_false_path -from [get_clocks clk_rx] -to [get_clocks -of_objects [get_pins Inst_system_clocks/MMCME2_ADV_TX_PLL/CLKOUT1]]
set_false_path -from [get_clocks clk_tx_mac] -to [get_clocks -of_objects [get_pins Inst_system_clocks/MMCME2_ADV_TX_PLL/CLKOUT1]]
set_false_path -from [get_clocks -of_objects [get_pins Inst_system_clocks/MMCME2_ADV_TX_PLL/CLKOUT1]] -to [get_clocks clk_rx]
set_false_path -from [get_clocks -of_objects [get_pins Inst_system_clocks/MMCME2_ADV_TX_PLL/CLKOUT1]] -to [get_clocks clk_tx_mac]


