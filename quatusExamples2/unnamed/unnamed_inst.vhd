	component unnamed is
		port (
			CLK      : in  std_logic                      := 'X';             -- clk
			araddr   : in  std_logic_vector(13 downto 0)  := (others => 'X'); -- araddr
			arburst  : in  std_logic_vector(1 downto 0)   := (others => 'X'); -- arburst
			arcache  : in  std_logic_vector(3 downto 0)   := (others => 'X'); -- arcache
			arid     : in  std_logic_vector(1 downto 0)   := (others => 'X'); -- arid
			arlen    : in  std_logic_vector(7 downto 0)   := (others => 'X'); -- arlen
			arlock   : in  std_logic                      := 'X';             -- arlock
			arprot   : in  std_logic_vector(2 downto 0)   := (others => 'X'); -- arprot
			arqos    : in  std_logic_vector(3 downto 0)   := (others => 'X'); -- arqos
			arready  : out std_logic;                                         -- arready
			arregion : in  std_logic_vector(3 downto 0)   := (others => 'X'); -- arregion
			arsize   : in  std_logic_vector(2 downto 0)   := (others => 'X'); -- arsize
			arvalid  : in  std_logic                      := 'X';             -- arvalid
			awaddr   : in  std_logic_vector(13 downto 0)  := (others => 'X'); -- awaddr
			awburst  : in  std_logic_vector(1 downto 0)   := (others => 'X'); -- awburst
			awcache  : in  std_logic_vector(3 downto 0)   := (others => 'X'); -- awcache
			awid     : in  std_logic_vector(1 downto 0)   := (others => 'X'); -- awid
			awlen    : in  std_logic_vector(7 downto 0)   := (others => 'X'); -- awlen
			awlock   : in  std_logic                      := 'X';             -- awlock
			awprot   : in  std_logic_vector(2 downto 0)   := (others => 'X'); -- awprot
			awqos    : in  std_logic_vector(3 downto 0)   := (others => 'X'); -- awqos
			awready  : out std_logic;                                         -- awready
			awregion : in  std_logic_vector(3 downto 0)   := (others => 'X'); -- awregion
			awsize   : in  std_logic_vector(2 downto 0)   := (others => 'X'); -- awsize
			awvalid  : in  std_logic                      := 'X';             -- awvalid
			bid      : out std_logic_vector(1 downto 0);                      -- bid
			bready   : in  std_logic                      := 'X';             -- bready
			bresp    : out std_logic_vector(1 downto 0);                      -- bresp
			bvalid   : out std_logic;                                         -- bvalid
			rdata    : out std_logic_vector(127 downto 0);                    -- rdata
			rid      : out std_logic_vector(1 downto 0);                      -- rid
			rlast    : out std_logic;                                         -- rlast
			rready   : in  std_logic                      := 'X';             -- rready
			rresp    : out std_logic_vector(1 downto 0);                      -- rresp
			rvalid   : out std_logic;                                         -- rvalid
			wdata    : in  std_logic_vector(127 downto 0) := (others => 'X'); -- wdata
			wlast    : in  std_logic                      := 'X';             -- wlast
			wready   : out std_logic;                                         -- wready
			wstrb    : in  std_logic_vector(15 downto 0)  := (others => 'X'); -- wstrb
			wvalid   : in  std_logic                      := 'X';             -- wvalid
			RST_N    : in  std_logic                      := 'X'              -- reset_n
		);
	end component unnamed;

	u0 : component unnamed
		port map (
			CLK      => CONNECTED_TO_CLK,      --             clock.clk
			araddr   => CONNECTED_TO_araddr,   -- altera_axi4_slave.araddr
			arburst  => CONNECTED_TO_arburst,  --                  .arburst
			arcache  => CONNECTED_TO_arcache,  --                  .arcache
			arid     => CONNECTED_TO_arid,     --                  .arid
			arlen    => CONNECTED_TO_arlen,    --                  .arlen
			arlock   => CONNECTED_TO_arlock,   --                  .arlock
			arprot   => CONNECTED_TO_arprot,   --                  .arprot
			arqos    => CONNECTED_TO_arqos,    --                  .arqos
			arready  => CONNECTED_TO_arready,  --                  .arready
			arregion => CONNECTED_TO_arregion, --                  .arregion
			arsize   => CONNECTED_TO_arsize,   --                  .arsize
			arvalid  => CONNECTED_TO_arvalid,  --                  .arvalid
			awaddr   => CONNECTED_TO_awaddr,   --                  .awaddr
			awburst  => CONNECTED_TO_awburst,  --                  .awburst
			awcache  => CONNECTED_TO_awcache,  --                  .awcache
			awid     => CONNECTED_TO_awid,     --                  .awid
			awlen    => CONNECTED_TO_awlen,    --                  .awlen
			awlock   => CONNECTED_TO_awlock,   --                  .awlock
			awprot   => CONNECTED_TO_awprot,   --                  .awprot
			awqos    => CONNECTED_TO_awqos,    --                  .awqos
			awready  => CONNECTED_TO_awready,  --                  .awready
			awregion => CONNECTED_TO_awregion, --                  .awregion
			awsize   => CONNECTED_TO_awsize,   --                  .awsize
			awvalid  => CONNECTED_TO_awvalid,  --                  .awvalid
			bid      => CONNECTED_TO_bid,      --                  .bid
			bready   => CONNECTED_TO_bready,   --                  .bready
			bresp    => CONNECTED_TO_bresp,    --                  .bresp
			bvalid   => CONNECTED_TO_bvalid,   --                  .bvalid
			rdata    => CONNECTED_TO_rdata,    --                  .rdata
			rid      => CONNECTED_TO_rid,      --                  .rid
			rlast    => CONNECTED_TO_rlast,    --                  .rlast
			rready   => CONNECTED_TO_rready,   --                  .rready
			rresp    => CONNECTED_TO_rresp,    --                  .rresp
			rvalid   => CONNECTED_TO_rvalid,   --                  .rvalid
			wdata    => CONNECTED_TO_wdata,    --                  .wdata
			wlast    => CONNECTED_TO_wlast,    --                  .wlast
			wready   => CONNECTED_TO_wready,   --                  .wready
			wstrb    => CONNECTED_TO_wstrb,    --                  .wstrb
			wvalid   => CONNECTED_TO_wvalid,   --                  .wvalid
			RST_N    => CONNECTED_TO_RST_N     --        reset_sink.reset_n
		);

