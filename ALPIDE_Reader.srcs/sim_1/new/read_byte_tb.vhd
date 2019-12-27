library IEEE;
use IEEE.Std_logic_1164.all;
use IEEE.Numeric_Std.all;

entity read_byte_tb is
end;

architecture bench of read_byte_tb is

  component read_byte
      Port ( clk_in : in STD_LOGIC;
             clk_ph : in STD_LOGIC;
             rstn : in STD_LOGIC;
             strt : in STD_LOGIC;
             pin_in : in STD_LOGIC;
             error, busy, readable : out STD_LOGIC;
             word_out : out STD_LOGIC_VECTOR (7 downto 0) 
             );
  end component;

  signal clk_in: STD_LOGIC;
  signal clk_ph: STD_LOGIC;
  signal rstn: STD_LOGIC;
  signal strt: STD_LOGIC;
  signal pin_in: STD_LOGIC;
  signal error, busy, readable: STD_LOGIC;
  signal word_out: STD_LOGIC_VECTOR (7 downto 0) ;

  constant clock_period: time := 10 ns;
  signal stop_the_clock: boolean;

begin

  uut: read_byte port map ( clk_in    => clk_in,
                            clk_ph    => clk_ph,
                            rstn       => rstn,
                            strt => strt,
                            pin_in    => pin_in,
                            error     => error,
                            busy      => busy,
                            readable  => readable,
                            word_out  => word_out );

  stimulus: process
  begin
  
    -- Put initialisation code here


    -- Put test bench stimulus code here

    stop_the_clock <= true;
    wait;
  end process;

  
end;
  


  
