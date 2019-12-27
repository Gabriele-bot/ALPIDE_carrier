library IEEE;
use IEEE.Std_logic_1164.all;
use IEEE.Numeric_Std.all;

entity send_byte_tb is
end;

architecture bench of send_byte_tb is

  component send_byte
      Port ( clk_in : in STD_LOGIC;
             strt : in STD_LOGIC;
             pin_out : out STD_LOGIC; 
             ready : out STD_LOGIC;
             word_sent : out STD_LOGIC; 
             word_in : in STD_LOGIC_VECTOR ( 7 downto 0)
             );
  end component;

  signal clk_in: STD_LOGIC;
  signal strt: STD_LOGIC;
  signal pin_out: STD_LOGIC;
  signal ready: STD_LOGIC;
  signal word_sent: STD_LOGIC;
  signal word_in: STD_LOGIC_VECTOR ( 7 downto 0) ;


begin

  uut: send_byte port map ( clk_in    => clk_in,
                            strt      => strt,
                            pin_out   => pin_out,
                            ready     => ready,
                            word_sent => word_sent,
                            word_in   => word_in );

  
end;
  