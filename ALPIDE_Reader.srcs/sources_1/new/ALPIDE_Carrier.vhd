----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10.12.2019 14:23:50
-- Design Name: 
-- Module Name: ALPIDE_Carrier - Behavioral
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
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
library UNISIM;
use UNISIM.VComponents.all;

entity ALPIDE_Carrier is
    Port ( CTRL : inout STD_LOGIC;  --data pin
           DCLK : out STD_LOGIC;    --40MHz
           clk_100MHz : in STD_LOGIC;   --sys clock 100MHz
           op_sw : in STD_LOGIC_VECTOR (3 downto 0) := "0000";    --16 selectable options
           btn : in STD_LOGIC;  --validate option
           rstn : in STD_LOGIC := '1';
           rst_n_io : out STD_LOGIC := '1' ;    --ALPIDE resetn 
           pwr_enable : out STD_LOGIC);      --ALPIDE power enable
end ALPIDE_Carrier;

architecture Behavioral of ALPIDE_Carrier is

component phase_shifter
    Port (clk_in1 : in STD_LOGIC;   --sys clock 100MHz
          locked : out STD_LOGIC;
          clk_out1 : out STD_LOGIC; --40MHz base clock
          clk_out2 : out STD_LOGIC  --90° phase shifted 40MHz clock
          );
end component;           
    
signal clk_40ph, clk_40, lkd : STD_LOGIC;  

component CMD_ROM   --stored CMD
    PORT (addra : in STD_LOGIC_VECTOR ( 7 downto 0 );
          clka : in STD_LOGIC; 
          douta : out STD_LOGIC_VECTOR ( 7 downto 0 )
          );
end component; 

signal addra, douta : STD_LOGIC_VECTOR ( 7 downto 0 ) ; --need 2 clk cycle to be effective 

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


component send_byte 
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

signal btn1, btn2 : STD_LOGIC := '0' ;  --to detect rising or falling edge of btn

type task is (reading, sending, idling_m, idling_s);
signal current_task : task := idling_m ;

type state is (s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10);
signal i_state : state;
signal rr_state : state;
signal w_state : state;
signal wr_state : state;
type cmd_state is (init, power_on, power_off, readregister, idle, writecommand, writeregister); --may want to add write cmd or something like that
signal ALPIDEC_state : cmd_state := idle;
signal initialized, powered, r_read, chip_id_err, c_write : STD_LOGIC; -- register read
signal data_l, data_h : STD_LOGIC_VECTOR (7 downto 0);
signal command, op_command, id, w_addrl, w_addrh, w_datal, w_datah : STD_LOGIC_VECTOR (7 downto 0); --command change trough ip_bus (to be implemented)



begin

    u1 : read_byte PORT MAP 
    (clk_in => clk_40,
    clk_ph => clk_40ph,
    rstn => rstn,
    strt => re, --read enable
    pin_in => pin_in,
    error => error,
    busy=> busy,
    readable => readable ,
    word_out => word_out);
    
    u2 : send_byte PORT MAP  
    (clk_in => clk_40,
    strt => we, --write enable
    pin_out => pin_out,
    ready => ready_to_send,
    word_sent=> word_sent,
    word_in => word_in) ;
   
    MMCM : phase_shifter PORT MAP
    (clk_in1 => clk_100MHz,
    locked => lkd,
    clk_out1 => clk_40,
    clk_out2 => clk_40ph) ;
    
    ROM : CMD_ROM PORT MAP
    (addra => addra,
    clka => clk_40,
    douta => douta) ;
    
    process(clk_40) is
    begin
    
        if rstn = '0' then
            btn2 <= '0' ;
            btn1 <= '0' ;
        elsif rising_edge(clk_40) then
            btn2 <= btn1 ;
            btn1 <= btn ;
        end if;
            
    end process ;   
    ---------------------------------
    --Command console
    cmd_c : process(clk_40, btn1, btn2) is
    
    
    
    begin
        if rstn = '0' then
            ALPIDEC_state <= idle;
        elsif rising_edge(clk_40) then   --rising edge btn
            case ALPIDEC_state is
            when idle =>
                if btn1= '1' and btn2 = '0' then
                    case op_sw is
                    when x"0" =>
                        ALPIDEC_state <= power_off ;
                    when x"1" =>
                        ALPIDEC_state <= power_on ;
                    when x"2" =>
                        if initialized = '0' and powered = '1' then
                            ALPIDEC_state <= init ;
                        end if;
                    when x"4" =>
                        ALPIDEC_state <= readregister ; --op command, chip_id, addrl, addrh, bus turnaround, chip_id, datal, datah, busturnaround
                    when x"8" =>
                        ALPIDEC_state <= writecommand ; --op command(command)    
                    when x"9" =>
                        ALPIDEC_state <= writeregister ;    --op command, chip_id (or multicast_id), addrl, addrh, datal, datah
                    when others =>
                        null;
                    end case;
                end if;
            when init =>
                if initialized = '1' then
                    ALPIDEC_state <= idle ;
                end if; 
            when power_on =>
                if powered = '1' then 
                    ALPIDEC_state <= idle ;   
                end if;
            when power_off =>
                if powered = '0' then
                    ALPIDEC_state <= idle ;          
                end if;
                ALPIDEC_state <= idle ;
            when readregister =>
                if r_read = '1' then
                     ALPIDEC_state <= idle ;
                end if;
            when writecommand =>
                if c_write = '1' then
                     ALPIDEC_state <= idle ;
                end if;
            when writeregister =>
                if c_write = '1' then
                     ALPIDEC_state <= idle ;
                end if;     
            when others =>
                null; 
            end case;    
        end if;
    end process cmd_c;
    
    
    ---------------------------------
    --Set of CTRL inout port
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
            CTRL <= '1' ;   --idle driven by master (FPGA)    
        when idling_s =>
            CTRL <= 'Z' ;   --idle driven by slave (ALPIDE chip)
        when others =>
            CTRL <= 'Z' ;   -- set high impedace just for safety  
        end case;                   
        
    end process;
    ---------------------------------------
    
    main : process (clk_40, rstn) is
    
    variable cmd_cnt ,cnt : STD_LOGIC_VECTOR( 7 downto 0 ) := x"00" ;
    variable byte_cnt, idle_cnt, chip_id : STD_LOGIC_VECTOR( 7 downto 0 ) := x"00" ;
    
    begin
    
        if rstn = '0' then
            powered <= '0' ;
            i_state <= s0 ; --starting state
            rr_state <= s0 ;
            initialized <= '0' ;
            r_read <= '0' ;
            chip_id_err <= '0' ;
            c_write <= '0' ;
            cmd_cnt := x"00" ;
            byte_cnt := x"00" ;
            idle_cnt := x"00" ;
        elsif rising_edge(clk_40) then
            case ALPIDEC_state is
            when idle =>
                r_read <= '0' ;
                c_write <= '0' ;
            when power_off =>   --power off routine
                if powered = '1' then
                    rst_n_io <= '0' ; 
                    pwr_enable <= '0' ;
                    powered <= '0' ;          
                end if;
            when power_on =>    --power on routine
                if powered = '1' then
                    rst_n_io <= '1' ;
                    pwr_enable <= '1' ; 
                else 
                    rst_n_io <= '0' ;
                    pwr_enable <= '0' ;
                    powered <= '1' ;    
                end if;
            when init =>    --initialization routine
                case i_state is
                when s0 => 
                    if ALPIDEC_state = init and initialized = '0' then
                        addra <= x"00" ; --initialize to base address
                        i_state <= s1 ;
                        rst_n_io <= '1' ;
                    else
                        i_state <= s0 ;
                    end if;
                when s1 =>
                    rst_n_io <= '0' ;
                    i_state <= s2 ;   
                when s2 =>
                    rst_n_io <= '1' ;
                    i_state <= s3 ;
                when s3 =>                
                    current_task <= sending ;
                    if ready_to_send = '1' then
                        word_in <= douta ;   --from ROM
                        we <= '1' ;
                        i_state <= s4 ;
                     else 
                        i_state <= s3 ;
                     end if;
                when s4 =>
                    we <= '0' ;
                    addra <= addra + x"01" ;
                    i_state <= s5 ;
                when s5 =>
                    if word_sent = '1' then
                        if cmd_cnt >= x"10" then
                            addra <= x"00" ; --to base ROM address
                            cmd_cnt := x"00" ;
                            initialized <= '1' ;
                            i_state <= s0 ;
                            current_task <= idling_m ;
                        else 
                            cmd_cnt := cmd_cnt + x"01" ;
                            i_state <= s3 ;   
                        end if;
                    end if;
                when others =>
                    i_state <= s0 ;
                end case;
            when readregister =>    --readregister routine
                case rr_state is
                when s0 => 
                    if ALPIDEC_state = readregister and r_read = '0' then
                        addra <= x"12" ; --initialize ROM to start address (unicast read cmd)
                        rr_state <= s1 ;
                    else
                        rr_state <= s0 ;
                    end if;
                when s1 =>
                    rr_state <= s2 ;
                when s2 =>
                    rr_state <= s3 ;
                when s3 =>
                    current_task <= sending ;
                    if ready_to_send = '1' then
                        case byte_cnt is
                        when x"01" =>
                            chip_id := douta ;  --store chip_id byte  
                        when others => 
                            null;
                        end case;                    
                        word_in <= douta ;   --from ROM
                        we <= '1' ;
                        rr_state <= s4 ;
                     else 
                        rr_state <= s3 ;
                     end if;
                when s4 =>
                    we <= '0' ;
                    addra <= addra + x"01" ;    --go to next ROM address
                    rr_state <= s5 ;
                when s5 =>
                    if word_sent = '1' then
                        if byte_cnt >= x"03" then
                            addra <= x"12" ; --to start address
                            byte_cnt := x"00" ;
                            rr_state <= s6 ;
                            current_task <= idling_m ;  --5 idle cycle driven by master
                        else
                            byte_cnt := byte_cnt + x"01" ;
                            rr_state <= s3 ;        
                        end if;
                    end if;
                when s6 =>  --idle m and idle s phase, bus turnaround
                    if idle_cnt < x"05" then
                        current_task <= idling_m ;
                        idle_cnt := idle_cnt + x"01" ;
                    elsif  idle_cnt >= x"05" and idle_cnt <= x"09" then 
                        current_task <= idling_s ;  --idle driven by slave
                        idle_cnt := idle_cnt + x"01" ;
                    else
                        idle_cnt := x"00" ;
                        rr_state <= s7 ;
                    end if;
                when s7 =>
                    current_task <= reading ;
                    re <= '1' ;
                    rr_state <= s8 ;  
                when s8 =>
                    if busy = '1' then
                        re <= '0' ;
                        rr_state <= s9 ;
                    else
                        re <= '1' ;
                        rr_state <= s8 ;  
                    end if;
                when s9 => 
                    if readable = '1' then
                        case byte_cnt is
                        when x"00" =>
                            if word_out = chip_id then
                                byte_cnt := byte_cnt + x"01" ;
                                rr_state <= s7 ;
                                chip_id_err <= '0' ;
                            else 
                                chip_id_err <= '1' ;
                                byte_cnt := byte_cnt + x"01" ;
                                rr_state <= s7 ;
                            end if;   
                        when x"01" =>
                            data_l <= word_out ;    --load data low
                            byte_cnt := byte_cnt + x"01" ;
                            rr_state <= s7 ;
                        when x"02" =>
                            data_h <= word_out ;    --load data high
                            byte_cnt := x"00" ;
                            r_read <= '1' ; --register read
                            rr_state <= s10 ;
                        when others =>
                            byte_cnt := x"00" ;
                            r_read <= '0' ;
                            chip_id_err <= '1' ;
                            rr_state <= s10 ;
                        end case;
                    else
                        re <= '1' ;
                        rr_state <= s9 ;  
                    end if;
                when s10 => --bus turnaround
                    if idle_cnt < x"05" then
                        current_task <= idling_s ;  --idle driven by slave
                        idle_cnt := idle_cnt + x"01" ;
                    elsif  idle_cnt >= x"05" and idle_cnt <= x"09" then 
                        current_task <= idling_m ;  --idle driven by master
                        idle_cnt := idle_cnt + x"01" ;
                    else
                        idle_cnt := x"00" ;
                        rr_state <= s0 ;
                    end if;            
                when others =>
                    rr_state <= s0 ;
                end case;
            when writecommand =>
            case w_state is
                when s0 => 
                    if ALPIDEC_state = writecommand and c_write = '0' then
                        w_state <= s1 ;
                    else
                        w_state <= s0 ;
                    end if;
                when s1 =>
                    current_task <= sending ;
                    if ready_to_send = '1' then
                        word_in <= command ;   
                        we <= '1' ;
                        w_state <= s2 ;
                     else 
                        w_state <= s1 ;
                     end if;   
                when s2 =>
                    we <= '0' ;
                    w_state <= s3 ;
                when s3 =>                
                    if word_sent = '1' then
                        w_state <= s0 ;
                        c_write <= '1' ;
                    end if;
                when others =>
                    w_state <= s0 ;
                end case;
            when writeregister =>
                case wr_state is
                when s0 => 
                    if c_write = '0' then
                        wr_state <= s1 ;
                    else
                        wr_state <= s0 ;
                    end if;
                when s1 =>
                    current_task <= sending ;
                    if ready_to_send = '1' then
                        we <= '1' ;
                        case cnt is
                        when x"00" =>
                            word_in <= op_command ;     
                        when x"01" =>
                            word_in <= id ;
                        when x"02" =>
                            word_in <= w_addrl ;
                        when x"03" =>
                            word_in <= w_addrh ;
                        when x"04" =>
                            word_in <= w_datal ;
                        when x"05" =>
                            word_in <= w_datah ;
                        when others => 
                            null; 
                        end case;
                        wr_state <= s2 ;
                    else
                        wr_state <= s1 ;
                    end if;
                when s2 =>
                    we <= '0' ;
                    wr_state <= s3 ;
               when s3 =>
                    if word_sent = '1' then
                        if cnt >= x"05" then
                            cnt := x"00" ;
                            wr_state <= s0 ;
                            c_write <= '1' ;
                        else
                            cnt := cnt + x"01" ;
                            wr_state <= s1 ;
                        end if ;
                    end if;
                when others =>
                    wr_state <= s0 ;
                end case;  
            when others =>
                null ;    
            end case;
        end if;
    end process main;
    
       
    DCLK <= clk_40 ;
    
end Behavioral;


---------------------------------------
--need fix starting address in the read register process
--need to fix the 2 cycles delay when chage address write read command 
--need to implement some costants such as initialization routine and readregister start address
--can I use only one cnt on main process?
------------------------------------------
--TODO
--add byte sequence (ROM) in init routine
--add write register and write command options 
--add FIFO REGISTER high and low addresses in read register routine
--check number of clk cycles on bus turnaround 