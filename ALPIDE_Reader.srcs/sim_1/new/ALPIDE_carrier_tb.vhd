----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 11.12.2019 11:35:20
-- Design Name: 
-- Module Name: ALPIDE_carrier_tb - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.Std_logic_1164.all;
use IEEE.Numeric_Std.all;

entity ALPIDE_Carrier_tb is
end;

architecture bench of ALPIDE_Carrier_tb is

  component ALPIDE_Carrier
      Port ( CTRL : inout STD_LOGIC;  
           DCLK : out STD_LOGIC;    
           clk_100MHz : in STD_LOGIC;   
           op_sw : in STD_LOGIC_VECTOR (3 downto 0) := "0000";    
           btn : in STD_LOGIC;
           rstn : in STD_LOGIC := '1';
           rst_n_io : out STD_LOGIC;    
           pwr_enable : out STD_LOGIC); 
  end component;

  signal CTRL: STD_LOGIC;
  signal DCLK: STD_LOGIC;
  signal clk_100MHz: STD_LOGIC;
  signal op_sw : STD_LOGIC_VECTOR (3 downto 0);
  signal btn: STD_LOGIC;
  signal rstn : STD_LOGIC;
  signal rst_n_io: STD_LOGIC;
  signal pwr_enable: STD_LOGIC;



begin

  uut: ALPIDE_Carrier port map ( CTRL       => CTRL,
                                 DCLK       => DCLK,
                                 clk_100MHz => clk_100MHz,
                                 op_sw => op_sw,
                                 btn      => btn,
                                 rstn => rstn,
                                 rst_n_io   => rst_n_io,
                                 pwr_enable => pwr_enable );

  


end;
  