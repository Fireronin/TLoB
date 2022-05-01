	component unnamed is
		port (
			CLK      : in  std_logic                      := 'X';             -- clk
			araddr   : out std_logic_vector(13 downto 0);                     -- araddr
			arburst  : out std_logic_vector(1 downto 0);                      -- arburst
			arcache  : out std_logic_vector(3 downto 0);                      -- arcache
			arid     : out std_logic;                                         -- arid
			arlen    : out std_logic_vector(7 downto 0);                      -- arlen
			arlock   : out std_logic;                                         -- arlock
			arprot   : out std_logic_vector(2 downto 0);                      -- arprot
			arqos    : out std_logic_vector(3 downto 0);                      -- arqos
			arready  : in  std_logic                      := 'X';             -- arready
			arregion : out std_logic_vector(3 downto 0);                      -- arregion
			arsize   : out std_logic_vector(2 downto 0);                      -- arsize
			arvalid  : out std_logic;                                         -- arvalid
			awaddr   : out std_logic_vector(13 downto 0);                     -- awaddr
			awburst  : out std_logic_vector(1 downto 0);                      -- awburst
			awcache  : out std_logic_vector(3 downto 0);                      -- awcache
			awid     : out std_logic;                                         -- awid
			awlen    : out std_logic_vector(7 downto 0);                      -- awlen
			awlock   : out std_logic;                                         -- awlock
			awprot   : out std_logic_vector(2 downto 0);                      -- awprot
			awqos    : out std_logic_vector(3 downto 0);                      -- awqos
			awready  : in  std_logic                      := 'X';             -- awready
			awregion : out std_logic_vector(3 downto 0);                      -- awregion
			awsize   : out std_logic_vector(2 downto 0);                      -- awsize
			awvalid  : out std_logic;                                         -- awvalid
			bid      : in  std_logic                      := 'X';             -- bid
			bready   : out std_logic;                                         -- bready
			bresp    : in  std_logic_vector(1 downto 0)   := (others => 'X'); -- bresp
			bvalid   : in  std_logic                      := 'X';             -- bvalid
			rdata    : in  std_logic_vector(127 downto 0) := (others => 'X'); -- rdata
			rid      : in  std_logic                      := 'X';             -- rid
			rlast    : in  std_logic                      := 'X';             -- rlast
			rready   : out std_logic;                                         -- rready
			rresp    : in  std_logic_vector(1 downto 0)   := (others => 'X'); -- rresp
			rvalid   : in  std_logic                      := 'X';             -- rvalid
			wdata    : out std_logic_vector(127 downto 0);                    -- wdata
			wlast    : out std_logic;                                         -- wlast
			wready   : in  std_logic                      := 'X';             -- wready
			wstrb    : out std_logic_vector(15 downto 0);                     -- wstrb
			wvalid   : out std_logic;                                         -- wvalid
			RST_N    : in  std_logic                      := 'X'              -- reset_n
		);
	end component unnamed;

	u0 : component unnamed
		port map (
			CLK      => CONNECTED_TO_CLK,      --              clock.clk
			araddr   => CONNECTED_TO_araddr,   -- altera_axi4_master.araddr
			arburst  => CONNECTED_TO_arburst,  --                   .arburst
			arcache  => CONNECTED_TO_arcache,  --                   .arcache
			arid     => CONNECTED_TO_arid,     --                   .arid
			arlen    => CONNECTED_TO_arlen,    --                   .arlen
			arlock   => CONNECTED_TO_arlock,   --                   .arlock
			arprot   => CONNECTED_TO_arprot,   --                   .arprot
			arqos    => CONNECTED_TO_arqos,    --                   .arqos
			arready  => CONNECTED_TO_arready,  --                   .arready
			arregion => CONNECTED_TO_arregion, --                   .arregion
			arsize   => CONNECTED_TO_arsize,   --                   .arsize
			arvalid  => CONNECTED_TO_arvalid,  --                   .arvalid
			awaddr   => CONNECTED_TO_awaddr,   --                   .awaddr
			awburst  => CONNECTED_TO_awburst,  --                   .awburst
			awcache  => CONNECTED_TO_awcache,  --                   .awcache
			awid     => CONNECTED_TO_awid,     --                   .awid
			awlen    => CONNECTED_TO_awlen,    --                   .awlen
			awlock   => CONNECTED_TO_awlock,   --                   .awlock
			awprot   => CONNECTED_TO_awprot,   --                   .awprot
			awqos    => CONNECTED_TO_awqos,    --                   .awqos
			awready  => CONNECTED_TO_awready,  --                   .awready
			awregion => CONNECTED_TO_awregion, --                   .awregion
			awsize   => CONNECTED_TO_awsize,   --                   .awsize
			awvalid  => CONNECTED_TO_awvalid,  --                   .awvalid
			bid      => CONNECTED_TO_bid,      --                   .bid
			bready   => CONNECTED_TO_bready,   --                   .bready
			bresp    => CONNECTED_TO_bresp,    --                   .bresp
			bvalid   => CONNECTED_TO_bvalid,   --                   .bvalid
			rdata    => CONNECTED_TO_rdata,    --                   .rdata
			rid      => CONNECTED_TO_rid,      --                   .rid
			rlast    => CONNECTED_TO_rlast,    --                   .rlast
			rready   => CONNECTED_TO_rready,   --                   .rready
			rresp    => CONNECTED_TO_rresp,    --                   .rresp
			rvalid   => CONNECTED_TO_rvalid,   --                   .rvalid
			wdata    => CONNECTED_TO_wdata,    --                   .wdata
			wlast    => CONNECTED_TO_wlast,    --                   .wlast
			wready   => CONNECTED_TO_wready,   --                   .wready
			wstrb    => CONNECTED_TO_wstrb,    --                   .wstrb
			wvalid   => CONNECTED_TO_wvalid,   --                   .wvalid
			RST_N    => CONNECTED_TO_RST_N     --         reset_sink.reset_n
		);

