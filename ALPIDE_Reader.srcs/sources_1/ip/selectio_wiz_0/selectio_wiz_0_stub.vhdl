-- Copyright 1986-2018 Xilinx, Inc. All Rights Reserved.
-- --------------------------------------------------------------------------------
-- Tool Version: Vivado v.2018.3 (win64) Build 2405991 Thu Dec  6 23:38:27 MST 2018
-- Date        : Thu Dec 12 19:15:45 2019
-- Host        : DESKTOP-EKOU29H running 64-bit major release  (build 9200)
-- Command     : write_vhdl -force -mode synth_stub
--               d:/Progetti_vivado/ALPIDE_Reader/ALPIDE_Reader.srcs/sources_1/ip/selectio_wiz_0/selectio_wiz_0_stub.vhdl
-- Design      : selectio_wiz_0
-- Purpose     : Stub declaration of top-level module interface
-- Device      : xc7a35ticsg324-1L
-- --------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity selectio_wiz_0 is
  Port ( 
    data_to_and_from_pins : inout STD_LOGIC_VECTOR ( 0 to 0 );
    data_in_to_device : out STD_LOGIC_VECTOR ( 7 downto 0 );
    data_out_from_device : in STD_LOGIC_VECTOR ( 7 downto 0 );
    clk_to_pins : out STD_LOGIC;
    bitslip : in STD_LOGIC_VECTOR ( 0 to 0 );
    tristate_output : in STD_LOGIC;
    clk_in : in STD_LOGIC;
    clk_div_out : out STD_LOGIC;
    clk_reset : in STD_LOGIC;
    io_reset : in STD_LOGIC
  );

end selectio_wiz_0;

architecture stub of selectio_wiz_0 is
attribute syn_black_box : boolean;
attribute black_box_pad_pin : string;
attribute syn_black_box of stub : architecture is true;
attribute black_box_pad_pin of stub : architecture is "data_to_and_from_pins[0:0],data_in_to_device[7:0],data_out_from_device[7:0],clk_to_pins,bitslip[0:0],tristate_output,clk_in,clk_div_out,clk_reset,io_reset";
begin
end;
