-- Copyright 1986-2018 Xilinx, Inc. All Rights Reserved.
-- --------------------------------------------------------------------------------
-- Tool Version: Vivado v.2018.3 (win64) Build 2405991 Thu Dec  6 23:38:27 MST 2018
-- Date        : Thu Dec 12 19:15:45 2019
-- Host        : DESKTOP-EKOU29H running 64-bit major release  (build 9200)
-- Command     : write_vhdl -force -mode funcsim
--               d:/Progetti_vivado/ALPIDE_Reader/ALPIDE_Reader.srcs/sources_1/ip/selectio_wiz_0/selectio_wiz_0_sim_netlist.vhdl
-- Design      : selectio_wiz_0
-- Purpose     : This VHDL netlist is a functional simulation representation of the design and should not be modified or
--               synthesized. This netlist cannot be used for SDF annotated simulation.
-- Device      : xc7a35ticsg324-1L
-- --------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity selectio_wiz_0_selectio_wiz_0_selectio_wiz is
  port (
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
  attribute DEV_W : integer;
  attribute DEV_W of selectio_wiz_0_selectio_wiz_0_selectio_wiz : entity is 8;
  attribute ORIG_REF_NAME : string;
  attribute ORIG_REF_NAME of selectio_wiz_0_selectio_wiz_0_selectio_wiz : entity is "selectio_wiz_0_selectio_wiz";
  attribute SYS_W : integer;
  attribute SYS_W of selectio_wiz_0_selectio_wiz_0_selectio_wiz : entity is 1;
  attribute num_serial_bits : integer;
  attribute num_serial_bits of selectio_wiz_0_selectio_wiz_0_selectio_wiz : entity is 8;
end selectio_wiz_0_selectio_wiz_0_selectio_wiz;

architecture STRUCTURE of selectio_wiz_0_selectio_wiz_0_selectio_wiz is
  signal \^clk_div_out\ : STD_LOGIC;
  signal clk_fwd_out : STD_LOGIC;
  signal clk_in_int : STD_LOGIC;
  signal clk_in_int_buf : STD_LOGIC;
  signal data_in_from_pins_delay : STD_LOGIC;
  signal data_out_to_pins_predelay : STD_LOGIC;
  signal tristate_int : STD_LOGIC;
  signal NLW_clk_fwd_OFB_UNCONNECTED : STD_LOGIC;
  signal NLW_clk_fwd_SHIFTOUT1_UNCONNECTED : STD_LOGIC;
  signal NLW_clk_fwd_SHIFTOUT2_UNCONNECTED : STD_LOGIC;
  signal NLW_clk_fwd_TBYTEOUT_UNCONNECTED : STD_LOGIC;
  signal NLW_clk_fwd_TFB_UNCONNECTED : STD_LOGIC;
  signal NLW_clk_fwd_TQ_UNCONNECTED : STD_LOGIC;
  signal \NLW_pins[0].iserdese2_master_O_UNCONNECTED\ : STD_LOGIC;
  signal \NLW_pins[0].iserdese2_master_SHIFTOUT1_UNCONNECTED\ : STD_LOGIC;
  signal \NLW_pins[0].iserdese2_master_SHIFTOUT2_UNCONNECTED\ : STD_LOGIC;
  signal \NLW_pins[0].oserdese2_master_OFB_UNCONNECTED\ : STD_LOGIC;
  signal \NLW_pins[0].oserdese2_master_SHIFTOUT1_UNCONNECTED\ : STD_LOGIC;
  signal \NLW_pins[0].oserdese2_master_SHIFTOUT2_UNCONNECTED\ : STD_LOGIC;
  signal \NLW_pins[0].oserdese2_master_TBYTEOUT_UNCONNECTED\ : STD_LOGIC;
  signal \NLW_pins[0].oserdese2_master_TFB_UNCONNECTED\ : STD_LOGIC;
  attribute BOX_TYPE : string;
  attribute BOX_TYPE of bufio_inst : label is "PRIMITIVE";
  attribute BOX_TYPE of clk_fwd : label is "PRIMITIVE";
  attribute BOX_TYPE of clkout_buf_inst : label is "PRIMITIVE";
  attribute BOX_TYPE of ibuf_clk_inst : label is "PRIMITIVE";
  attribute CAPACITANCE : string;
  attribute CAPACITANCE of ibuf_clk_inst : label is "DONT_CARE";
  attribute IBUF_DELAY_VALUE : string;
  attribute IBUF_DELAY_VALUE of ibuf_clk_inst : label is "0";
  attribute IFD_DELAY_VALUE : string;
  attribute IFD_DELAY_VALUE of ibuf_clk_inst : label is "AUTO";
  attribute BOX_TYPE of obuf_inst : label is "PRIMITIVE";
  attribute CAPACITANCE of obuf_inst : label is "DONT_CARE";
  attribute BOX_TYPE of \pins[0].iobuf_inst\ : label is "PRIMITIVE";
  attribute BOX_TYPE of \pins[0].iserdese2_master\ : label is "PRIMITIVE";
  attribute OPT_MODIFIED : string;
  attribute OPT_MODIFIED of \pins[0].iserdese2_master\ : label is "MLO ";
  attribute BOX_TYPE of \pins[0].oserdese2_master\ : label is "PRIMITIVE";
begin
  clk_div_out <= \^clk_div_out\;
bufio_inst: unisim.vcomponents.BUFIO
     port map (
      I => clk_in_int,
      O => clk_in_int_buf
    );
clk_fwd: unisim.vcomponents.OSERDESE2
    generic map(
      DATA_RATE_OQ => "DDR",
      DATA_RATE_TQ => "SDR",
      DATA_WIDTH => 4,
      INIT_OQ => '0',
      INIT_TQ => '0',
      IS_CLKDIV_INVERTED => '0',
      IS_CLK_INVERTED => '0',
      IS_D1_INVERTED => '0',
      IS_D2_INVERTED => '0',
      IS_D3_INVERTED => '0',
      IS_D4_INVERTED => '0',
      IS_D5_INVERTED => '0',
      IS_D6_INVERTED => '0',
      IS_D7_INVERTED => '0',
      IS_D8_INVERTED => '0',
      IS_T1_INVERTED => '0',
      IS_T2_INVERTED => '0',
      IS_T3_INVERTED => '0',
      IS_T4_INVERTED => '0',
      SERDES_MODE => "MASTER",
      SRVAL_OQ => '0',
      SRVAL_TQ => '0',
      TBYTE_CTL => "FALSE",
      TBYTE_SRC => "FALSE",
      TRISTATE_WIDTH => 1
    )
        port map (
      CLK => clk_in_int_buf,
      CLKDIV => \^clk_div_out\,
      D1 => '1',
      D2 => '0',
      D3 => '1',
      D4 => '0',
      D5 => '1',
      D6 => '0',
      D7 => '1',
      D8 => '0',
      OCE => '1',
      OFB => NLW_clk_fwd_OFB_UNCONNECTED,
      OQ => clk_fwd_out,
      RST => io_reset,
      SHIFTIN1 => '0',
      SHIFTIN2 => '0',
      SHIFTOUT1 => NLW_clk_fwd_SHIFTOUT1_UNCONNECTED,
      SHIFTOUT2 => NLW_clk_fwd_SHIFTOUT2_UNCONNECTED,
      T1 => '0',
      T2 => '0',
      T3 => '0',
      T4 => '0',
      TBYTEIN => '0',
      TBYTEOUT => NLW_clk_fwd_TBYTEOUT_UNCONNECTED,
      TCE => '0',
      TFB => NLW_clk_fwd_TFB_UNCONNECTED,
      TQ => NLW_clk_fwd_TQ_UNCONNECTED
    );
clkout_buf_inst: unisim.vcomponents.BUFR
    generic map(
      BUFR_DIVIDE => "8",
      SIM_DEVICE => "7SERIES"
    )
        port map (
      CE => '1',
      CLR => clk_reset,
      I => clk_in_int,
      O => \^clk_div_out\
    );
ibuf_clk_inst: unisim.vcomponents.IBUF
     port map (
      I => clk_in,
      O => clk_in_int
    );
obuf_inst: unisim.vcomponents.OBUF
     port map (
      I => clk_fwd_out,
      O => clk_to_pins
    );
\pins[0].iobuf_inst\: unisim.vcomponents.IOBUF
     port map (
      I => data_out_to_pins_predelay,
      IO => data_to_and_from_pins(0),
      O => data_in_from_pins_delay,
      T => tristate_int
    );
\pins[0].iserdese2_master\: unisim.vcomponents.ISERDESE2
    generic map(
      DATA_RATE => "SDR",
      DATA_WIDTH => 8,
      DYN_CLKDIV_INV_EN => "FALSE",
      DYN_CLK_INV_EN => "FALSE",
      INIT_Q1 => '0',
      INIT_Q2 => '0',
      INIT_Q3 => '0',
      INIT_Q4 => '0',
      INTERFACE_TYPE => "NETWORKING",
      IOBDELAY => "NONE",
      IS_CLKB_INVERTED => '1',
      IS_CLKDIVP_INVERTED => '0',
      IS_CLKDIV_INVERTED => '0',
      IS_CLK_INVERTED => '0',
      IS_D_INVERTED => '0',
      IS_OCLKB_INVERTED => '0',
      IS_OCLK_INVERTED => '0',
      NUM_CE => 2,
      OFB_USED => "FALSE",
      SERDES_MODE => "MASTER",
      SRVAL_Q1 => '0',
      SRVAL_Q2 => '0',
      SRVAL_Q3 => '0',
      SRVAL_Q4 => '0'
    )
        port map (
      BITSLIP => bitslip(0),
      CE1 => '1',
      CE2 => '1',
      CLK => clk_in_int_buf,
      CLKB => clk_in_int_buf,
      CLKDIV => \^clk_div_out\,
      CLKDIVP => '0',
      D => data_in_from_pins_delay,
      DDLY => '0',
      DYNCLKDIVSEL => '0',
      DYNCLKSEL => '0',
      O => \NLW_pins[0].iserdese2_master_O_UNCONNECTED\,
      OCLK => '0',
      OCLKB => '0',
      OFB => '0',
      Q1 => data_in_to_device(7),
      Q2 => data_in_to_device(6),
      Q3 => data_in_to_device(5),
      Q4 => data_in_to_device(4),
      Q5 => data_in_to_device(3),
      Q6 => data_in_to_device(2),
      Q7 => data_in_to_device(1),
      Q8 => data_in_to_device(0),
      RST => io_reset,
      SHIFTIN1 => '0',
      SHIFTIN2 => '0',
      SHIFTOUT1 => \NLW_pins[0].iserdese2_master_SHIFTOUT1_UNCONNECTED\,
      SHIFTOUT2 => \NLW_pins[0].iserdese2_master_SHIFTOUT2_UNCONNECTED\
    );
\pins[0].oserdese2_master\: unisim.vcomponents.OSERDESE2
    generic map(
      DATA_RATE_OQ => "SDR",
      DATA_RATE_TQ => "SDR",
      DATA_WIDTH => 8,
      INIT_OQ => '0',
      INIT_TQ => '0',
      IS_CLKDIV_INVERTED => '0',
      IS_CLK_INVERTED => '0',
      IS_D1_INVERTED => '0',
      IS_D2_INVERTED => '0',
      IS_D3_INVERTED => '0',
      IS_D4_INVERTED => '0',
      IS_D5_INVERTED => '0',
      IS_D6_INVERTED => '0',
      IS_D7_INVERTED => '0',
      IS_D8_INVERTED => '0',
      IS_T1_INVERTED => '0',
      IS_T2_INVERTED => '0',
      IS_T3_INVERTED => '0',
      IS_T4_INVERTED => '0',
      SERDES_MODE => "MASTER",
      SRVAL_OQ => '0',
      SRVAL_TQ => '0',
      TBYTE_CTL => "FALSE",
      TBYTE_SRC => "FALSE",
      TRISTATE_WIDTH => 1
    )
        port map (
      CLK => clk_in_int_buf,
      CLKDIV => \^clk_div_out\,
      D1 => data_out_from_device(0),
      D2 => data_out_from_device(1),
      D3 => data_out_from_device(2),
      D4 => data_out_from_device(3),
      D5 => data_out_from_device(4),
      D6 => data_out_from_device(5),
      D7 => data_out_from_device(6),
      D8 => data_out_from_device(7),
      OCE => '1',
      OFB => \NLW_pins[0].oserdese2_master_OFB_UNCONNECTED\,
      OQ => data_out_to_pins_predelay,
      RST => io_reset,
      SHIFTIN1 => '0',
      SHIFTIN2 => '0',
      SHIFTOUT1 => \NLW_pins[0].oserdese2_master_SHIFTOUT1_UNCONNECTED\,
      SHIFTOUT2 => \NLW_pins[0].oserdese2_master_SHIFTOUT2_UNCONNECTED\,
      T1 => tristate_output,
      T2 => tristate_output,
      T3 => tristate_output,
      T4 => tristate_output,
      TBYTEIN => '0',
      TBYTEOUT => \NLW_pins[0].oserdese2_master_TBYTEOUT_UNCONNECTED\,
      TCE => '1',
      TFB => \NLW_pins[0].oserdese2_master_TFB_UNCONNECTED\,
      TQ => tristate_int
    );
end STRUCTURE;
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity selectio_wiz_0 is
  port (
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
  attribute NotValidForBitStream : boolean;
  attribute NotValidForBitStream of selectio_wiz_0 : entity is true;
  attribute DEV_W : integer;
  attribute DEV_W of selectio_wiz_0 : entity is 8;
  attribute SYS_W : integer;
  attribute SYS_W of selectio_wiz_0 : entity is 1;
end selectio_wiz_0;

architecture STRUCTURE of selectio_wiz_0 is
  attribute DEV_W of inst : label is 8;
  attribute SYS_W of inst : label is 1;
  attribute num_serial_bits : integer;
  attribute num_serial_bits of inst : label is 8;
begin
inst: entity work.selectio_wiz_0_selectio_wiz_0_selectio_wiz
     port map (
      bitslip(0) => bitslip(0),
      clk_div_out => clk_div_out,
      clk_in => clk_in,
      clk_reset => clk_reset,
      clk_to_pins => clk_to_pins,
      data_in_to_device(7 downto 0) => data_in_to_device(7 downto 0),
      data_out_from_device(7 downto 0) => data_out_from_device(7 downto 0),
      data_to_and_from_pins(0) => data_to_and_from_pins(0),
      io_reset => io_reset,
      tristate_output => tristate_output
    );
end STRUCTURE;
