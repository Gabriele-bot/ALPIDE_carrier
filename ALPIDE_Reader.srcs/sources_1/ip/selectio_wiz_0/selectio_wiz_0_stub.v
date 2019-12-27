// Copyright 1986-2018 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2018.3 (win64) Build 2405991 Thu Dec  6 23:38:27 MST 2018
// Date        : Thu Dec 12 19:15:45 2019
// Host        : DESKTOP-EKOU29H running 64-bit major release  (build 9200)
// Command     : write_verilog -force -mode synth_stub
//               d:/Progetti_vivado/ALPIDE_Reader/ALPIDE_Reader.srcs/sources_1/ip/selectio_wiz_0/selectio_wiz_0_stub.v
// Design      : selectio_wiz_0
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7a35ticsg324-1L
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
module selectio_wiz_0(data_to_and_from_pins, data_in_to_device, 
  data_out_from_device, clk_to_pins, bitslip, tristate_output, clk_in, clk_div_out, clk_reset, 
  io_reset)
/* synthesis syn_black_box black_box_pad_pin="data_to_and_from_pins[0:0],data_in_to_device[7:0],data_out_from_device[7:0],clk_to_pins,bitslip[0:0],tristate_output,clk_in,clk_div_out,clk_reset,io_reset" */;
  inout [0:0]data_to_and_from_pins;
  output [7:0]data_in_to_device;
  input [7:0]data_out_from_device;
  output clk_to_pins;
  input [0:0]bitslip;
  input tristate_output;
  input clk_in;
  output clk_div_out;
  input clk_reset;
  input io_reset;
endmodule
