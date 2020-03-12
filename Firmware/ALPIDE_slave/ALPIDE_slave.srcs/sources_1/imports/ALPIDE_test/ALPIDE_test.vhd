library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;


entity ALPIDE_Test is
    Port ( CTRL : inout STD_LOGIC;  --data pin
           DCLK : in STD_LOGIC;    --40MHz
           sw: in STD_LOGIC;  
           rst : in STD_LOGIC ; 
           pwr_enable : in STD_LOGIC ; --ALPIDE power enable
		   read_err : out STD_LOGIC   );      
end ALPIDE_Test;

architecture Behavioral of ALPIDE_Test is

signal rstn : STD_LOGIC ;

component R_W_PLL
	Port (clk_in1 : in STD_LOGIC;
         clk_out1 : out STD_LOGIC; --base clock
         clk_out2 : out STD_LOGIC  --160° phase shifted clock
         );
end component;  

signal clk_out1, clk_out2 : STD_LOGIC;

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

signal re, error, busy, readable, pin_in : STD_LOGIC;
signal word_out, word_buff : STD_LOGIC_VECTOR (7 downto 0);


component Write_byte 
    Port ( clk_in : in STD_LOGIC;
           strt: in STD_LOGIC;
           pin_out : out STD_LOGIC; 
           ready : out STD_LOGIC;
           word_sent : out STD_LOGIC;
           word_in : in STD_LOGIC_VECTOR ( 7 downto 0)
           );
end component;

signal we, word_sent, ready_to_send : STD_LOGIC;
signal pin_out : STD_LOGIC;
signal word_in : STD_LOGIC_VECTOR ( 7 downto 0);

type task is (reading, sending, idling_m, idling_s);
signal current_task : task := idling_m ;
type state is (s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10);
signal rr_state : state;
signal CHIP_ID : STD_LOGIC_VECTOR (7 downto 0) ;
signal RR_addr : STD_LOGIC_VECTOR (15 downto 0) ;
signal can_read : STD_LOGIC;

begin


	Read_FSM : read_byte PORT MAP(
		clk_in => clk_out1,
		clk_ph => clk_out2,
		rstn => rstn,
		strt => re, --read enable
		pin_in => pin_in,
		error => error,
		busy=> busy,
		readable => readable ,
		word_out => word_out
		);
    
   Write_FSM : Write_byte PORT MAP(
		clk_in => clk_out1,
		strt => we, --write enable
		pin_out => pin_out,
		ready => ready_to_send,
		word_sent=> word_sent,
		word_in => word_in
		);

	MMCM : R_W_PLL PORT MAP (
		clk_in1	 => DCLK,
		clk_out1	 => clk_out1,
		clk_out2	 => clk_out2
	);
	
	
	--CTRL inout port
    ------------------------------------
    process(current_task, pin_in, pin_out, CTRL) is
    
    begin
        case current_task is
        when sending =>
            CTRL <= pin_out ;
        when reading =>
            CTRL <= 'Z'  ; 
            pin_in <= CTRL ;
        when idling_m =>    
            CTRL <= 'Z' ;      
        when idling_s =>
            CTRL <= '1' ;   
        when others =>
            CTRL <= 'Z' ;   --set high impedace just for safety  
        end case;                   
        
    end process;
    ---------------------------------------
	
	process(clk_out1,rstn) is  --counter to create a slow clk
	
	variable byte_cnt, idle_cnt : STD_LOGIC_VECTOR( 7 downto 0 ) := x"00" ;
	
	begin
	
	if rstn = '0' then
            byte_cnt := x"00" ;
			idle_cnt := x"00" ;
			current_task <= idling_m ;
            rr_state <= s0 ;
            read_err <= '0' ;
   elsif rising_edge(clk_out1) then
		case rr_state is
                when s0 => 	
					current_task <= idling_m ;
                    if can_read = '1' then	--button
                        rr_state <= s1 ;
                    else
                        rr_state <= s0 ;
                    end if;
                when s1 =>
                    current_task <= reading ;
                    re <= '1' ;
                    rr_state <= s2 ;  
                when s2 =>
                    if busy = '1' then
                        re <= '0' ;
                        rr_state <= s3 ;
                    else
                        re <= '1' ;
                        rr_state <= s2 ;  
                    end if;
                when s3 =>
                    if readable = '1' then
                        case byte_cnt is
                        when x"00" =>
                            if word_out = x"4E" then
										byte_cnt := byte_cnt + x"01" ;
                            else 
										byte_cnt := x"00" ;
                            end if; 
                            re <= '1' ;
                            rr_state <= s2 ;  
                        when x"01" =>
                            CHIP_ID <= word_out ;    
                            byte_cnt := byte_cnt + x"01" ;
                            re <= '1' ;
                            rr_state <= s2 ;
                        when x"02" =>
                            RR_addr( 7 downto 0 ) <= word_out ;       
                            byte_cnt := byte_cnt + x"01" ;
                            re <= '1' ;
                            rr_state <= s2 ;
								when x"03" =>
                            RR_addr( 15 downto 8 ) <= word_out ;      
                            byte_cnt := x"00" ;
                            re <= '0' ;
                            rr_state <= s4 ;
                        when others =>
                            byte_cnt := x"00" ;
									 re <= '1' ;
                            rr_state <= s2 ;
                        end case;
                    elsif error = '1' then
                        read_err <= '1' ; 
								if byte_cnt >= x"03" then
									byte_cnt := x"00" ;
									re <= '0' ;
									rr_state <= s4 ;
								else
									byte_cnt := byte_cnt + x"01" ;
									re <= '1' ;
									rr_state <= s2 ;
								end if;
                    else
                        re <= '1' ;
                        rr_state <= s3 ;  
                    end if;
                when s4 => --bus turnaround
                    if idle_cnt < x"04" then
                        current_task <= idling_m ;  --master driver on
                        idle_cnt := idle_cnt + x"01" ;
                    elsif  idle_cnt >= x"04" and idle_cnt < x"08" then 
                        current_task <= idling_s ;  --turnaround
                        idle_cnt := idle_cnt + x"01" ;
                    elsif  idle_cnt >= x"08" and idle_cnt < x"0A" then 
                        current_task <= sending ;  --slave driver on
                        idle_cnt := idle_cnt + x"01" ;
                    else    
                        current_task <= sending ;  --slave driver on
                        idle_cnt := x"00" ;
                        rr_state <= s5 ;
                    end if;
						when s5 =>
                    current_task <= sending ;
                    if ready_to_send = '1' then
                        we <= '1' ;
                        case byte_cnt is
                        when x"00" =>
                            word_in <= CHIP_ID ; 
                        when x"01" =>
                            word_in <= RR_addr( 7 downto 0 ) ;
                        when x"02" =>
                            word_in <= RR_addr( 15 downto 8 ) ;  
                        when others => 
                            null; 
                        end case;
                        rr_state <= s6 ;
                     else 
                        rr_state <= s5 ;
                     end if;
                when s6 =>
                    we <= '0' ;
                    rr_state <= s7 ;
                when s7 =>
                    if word_sent = '1' then
                        if byte_cnt >= x"02" then
                            byte_cnt := x"00" ;
                            current_task <= idling_s ;
                            rr_state <= s8 ;
                        else
                            byte_cnt := byte_cnt + x"01" ;
                            rr_state <= s5 ;        
                        end if;
                    end if;
						when s8 => --bus turnaround
                    if idle_cnt < x"05" then
                        current_task <= idling_s ;  --slave driver on and turnaround
                        idle_cnt := idle_cnt + x"01" ;
                    elsif  idle_cnt >= x"05" and idle_cnt <= x"0A" then 
                        current_task <= idling_m ;  --turnaround and master driver on
                        idle_cnt := idle_cnt + x"01" ;
                    else
                        idle_cnt := x"00" ;
                        rr_state <= s0 ;
                    end if;
                
                when others =>
                    rr_state <= s0 ;
                end case;
		end if;
	end process ;
	
	rstn <= not rst ;
	can_read <= sw ;
	
end Behavioral;