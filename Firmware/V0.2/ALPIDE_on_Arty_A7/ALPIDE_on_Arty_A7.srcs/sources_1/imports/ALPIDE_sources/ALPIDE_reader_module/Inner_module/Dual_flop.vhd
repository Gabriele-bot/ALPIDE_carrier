----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 11.05.2020 12:11:57
-- Design Name: 
-- Module Name: Dual_flop - Behavioral
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
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity Dual_flop is
    Generic (IO_DATA_WIDTH : integer := 1);
    Port ( I_s : in STD_LOGIC_VECTOR (IO_DATA_WIDTH-1 downto 0);
           Clk : in STD_LOGIC;
           O_s : out STD_LOGIC_VECTOR (IO_DATA_WIDTH-1 downto 0));
end Dual_flop;

architecture Behavioral of Dual_flop is

signal Q1, Q2 : STD_LOGIC_VECTOR (IO_DATA_WIDTH-1 downto 0);

begin

    process (Clk) is
    begin
        if rising_edge(Clk) then
            Q1 <= I_s ;
            Q2 <= Q1 ;
        end if;
    end process;    
    
    O_s <= Q2 ;

end Behavioral;
