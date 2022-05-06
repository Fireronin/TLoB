	component Example1B is
		port (
			clk_clk                  : in std_logic := 'X'; -- clk
			reset_reset_n            : in std_logic := 'X'; -- reset_n
			simplefifo_2_enq_en_wire : in std_logic := 'X'  -- wire
		);
	end component Example1B;

	u0 : component Example1B
		port map (
			clk_clk                  => CONNECTED_TO_clk_clk,                  --                 clk.clk
			reset_reset_n            => CONNECTED_TO_reset_reset_n,            --               reset.reset_n
			simplefifo_2_enq_en_wire => CONNECTED_TO_simplefifo_2_enq_en_wire  -- simplefifo_2_enq_en.wire
		);

