// Example3.v

// Generated using ACDS version 21.1 842

`timescale 1 ps / 1 ps
module Example3 (
		input  wire  clk_clk,       //   clk.clk
		input  wire  reset_reset_n  // reset.reset_n
	);

	wire    [1:0] aximaster_0_altera_axi4_master_awburst;                   // axiMaster_0:awburst -> mm_interconnect_0:axiMaster_0_altera_axi4_master_awburst
	wire    [3:0] aximaster_0_altera_axi4_master_arregion;                  // axiMaster_0:arregion -> mm_interconnect_0:axiMaster_0_altera_axi4_master_arregion
	wire    [7:0] aximaster_0_altera_axi4_master_arlen;                     // axiMaster_0:arlen -> mm_interconnect_0:axiMaster_0_altera_axi4_master_arlen
	wire    [3:0] aximaster_0_altera_axi4_master_arqos;                     // axiMaster_0:arqos -> mm_interconnect_0:axiMaster_0_altera_axi4_master_arqos
	wire          aximaster_0_altera_axi4_master_wready;                    // mm_interconnect_0:axiMaster_0_altera_axi4_master_wready -> axiMaster_0:wready
	wire   [15:0] aximaster_0_altera_axi4_master_wstrb;                     // axiMaster_0:wstrb -> mm_interconnect_0:axiMaster_0_altera_axi4_master_wstrb
	wire          aximaster_0_altera_axi4_master_rid;                       // mm_interconnect_0:axiMaster_0_altera_axi4_master_rid -> axiMaster_0:rid
	wire          aximaster_0_altera_axi4_master_rready;                    // axiMaster_0:rready -> mm_interconnect_0:axiMaster_0_altera_axi4_master_rready
	wire    [7:0] aximaster_0_altera_axi4_master_awlen;                     // axiMaster_0:awlen -> mm_interconnect_0:axiMaster_0_altera_axi4_master_awlen
	wire    [3:0] aximaster_0_altera_axi4_master_awqos;                     // axiMaster_0:awqos -> mm_interconnect_0:axiMaster_0_altera_axi4_master_awqos
	wire    [3:0] aximaster_0_altera_axi4_master_arcache;                   // axiMaster_0:arcache -> mm_interconnect_0:axiMaster_0_altera_axi4_master_arcache
	wire   [13:0] aximaster_0_altera_axi4_master_araddr;                    // axiMaster_0:araddr -> mm_interconnect_0:axiMaster_0_altera_axi4_master_araddr
	wire          aximaster_0_altera_axi4_master_wvalid;                    // axiMaster_0:wvalid -> mm_interconnect_0:axiMaster_0_altera_axi4_master_wvalid
	wire    [2:0] aximaster_0_altera_axi4_master_arprot;                    // axiMaster_0:arprot -> mm_interconnect_0:axiMaster_0_altera_axi4_master_arprot
	wire          aximaster_0_altera_axi4_master_arvalid;                   // axiMaster_0:arvalid -> mm_interconnect_0:axiMaster_0_altera_axi4_master_arvalid
	wire    [2:0] aximaster_0_altera_axi4_master_awprot;                    // axiMaster_0:awprot -> mm_interconnect_0:axiMaster_0_altera_axi4_master_awprot
	wire  [127:0] aximaster_0_altera_axi4_master_wdata;                     // axiMaster_0:wdata -> mm_interconnect_0:axiMaster_0_altera_axi4_master_wdata
	wire          aximaster_0_altera_axi4_master_arid;                      // axiMaster_0:arid -> mm_interconnect_0:axiMaster_0_altera_axi4_master_arid
	wire    [3:0] aximaster_0_altera_axi4_master_awcache;                   // axiMaster_0:awcache -> mm_interconnect_0:axiMaster_0_altera_axi4_master_awcache
	wire          aximaster_0_altera_axi4_master_arlock;                    // axiMaster_0:arlock -> mm_interconnect_0:axiMaster_0_altera_axi4_master_arlock
	wire          aximaster_0_altera_axi4_master_awlock;                    // axiMaster_0:awlock -> mm_interconnect_0:axiMaster_0_altera_axi4_master_awlock
	wire   [13:0] aximaster_0_altera_axi4_master_awaddr;                    // axiMaster_0:awaddr -> mm_interconnect_0:axiMaster_0_altera_axi4_master_awaddr
	wire          aximaster_0_altera_axi4_master_arready;                   // mm_interconnect_0:axiMaster_0_altera_axi4_master_arready -> axiMaster_0:arready
	wire    [1:0] aximaster_0_altera_axi4_master_bresp;                     // mm_interconnect_0:axiMaster_0_altera_axi4_master_bresp -> axiMaster_0:bresp
	wire  [127:0] aximaster_0_altera_axi4_master_rdata;                     // mm_interconnect_0:axiMaster_0_altera_axi4_master_rdata -> axiMaster_0:rdata
	wire    [1:0] aximaster_0_altera_axi4_master_arburst;                   // axiMaster_0:arburst -> mm_interconnect_0:axiMaster_0_altera_axi4_master_arburst
	wire          aximaster_0_altera_axi4_master_awready;                   // mm_interconnect_0:axiMaster_0_altera_axi4_master_awready -> axiMaster_0:awready
	wire    [2:0] aximaster_0_altera_axi4_master_arsize;                    // axiMaster_0:arsize -> mm_interconnect_0:axiMaster_0_altera_axi4_master_arsize
	wire          aximaster_0_altera_axi4_master_bready;                    // axiMaster_0:bready -> mm_interconnect_0:axiMaster_0_altera_axi4_master_bready
	wire          aximaster_0_altera_axi4_master_rlast;                     // mm_interconnect_0:axiMaster_0_altera_axi4_master_rlast -> axiMaster_0:rlast
	wire          aximaster_0_altera_axi4_master_wlast;                     // axiMaster_0:wlast -> mm_interconnect_0:axiMaster_0_altera_axi4_master_wlast
	wire    [3:0] aximaster_0_altera_axi4_master_awregion;                  // axiMaster_0:awregion -> mm_interconnect_0:axiMaster_0_altera_axi4_master_awregion
	wire    [1:0] aximaster_0_altera_axi4_master_rresp;                     // mm_interconnect_0:axiMaster_0_altera_axi4_master_rresp -> axiMaster_0:rresp
	wire          aximaster_0_altera_axi4_master_awid;                      // axiMaster_0:awid -> mm_interconnect_0:axiMaster_0_altera_axi4_master_awid
	wire          aximaster_0_altera_axi4_master_bid;                       // mm_interconnect_0:axiMaster_0_altera_axi4_master_bid -> axiMaster_0:bid
	wire          aximaster_0_altera_axi4_master_bvalid;                    // mm_interconnect_0:axiMaster_0_altera_axi4_master_bvalid -> axiMaster_0:bvalid
	wire    [2:0] aximaster_0_altera_axi4_master_awsize;                    // axiMaster_0:awsize -> mm_interconnect_0:axiMaster_0_altera_axi4_master_awsize
	wire          aximaster_0_altera_axi4_master_awvalid;                   // axiMaster_0:awvalid -> mm_interconnect_0:axiMaster_0_altera_axi4_master_awvalid
	wire          aximaster_0_altera_axi4_master_rvalid;                    // mm_interconnect_0:axiMaster_0_altera_axi4_master_rvalid -> axiMaster_0:rvalid
	wire    [1:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_awburst;  // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_awburst -> axi4Slave_0:awburst
	wire    [3:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_arregion; // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_arregion -> axi4Slave_0:arregion
	wire    [7:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_arlen;    // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_arlen -> axi4Slave_0:arlen
	wire    [3:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_arqos;    // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_arqos -> axi4Slave_0:arqos
	wire   [15:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_wstrb;    // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_wstrb -> axi4Slave_0:wstrb
	wire          mm_interconnect_0_axi4slave_0_altera_axi4_slave_wready;   // axi4Slave_0:wready -> mm_interconnect_0:axi4Slave_0_altera_axi4_slave_wready
	wire    [1:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_rid;      // axi4Slave_0:rid -> mm_interconnect_0:axi4Slave_0_altera_axi4_slave_rid
	wire          mm_interconnect_0_axi4slave_0_altera_axi4_slave_rready;   // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_rready -> axi4Slave_0:rready
	wire    [7:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_awlen;    // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_awlen -> axi4Slave_0:awlen
	wire    [3:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_awqos;    // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_awqos -> axi4Slave_0:awqos
	wire    [3:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_arcache;  // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_arcache -> axi4Slave_0:arcache
	wire          mm_interconnect_0_axi4slave_0_altera_axi4_slave_wvalid;   // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_wvalid -> axi4Slave_0:wvalid
	wire   [13:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_araddr;   // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_araddr -> axi4Slave_0:araddr
	wire    [2:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_arprot;   // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_arprot -> axi4Slave_0:arprot
	wire    [2:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_awprot;   // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_awprot -> axi4Slave_0:awprot
	wire  [127:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_wdata;    // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_wdata -> axi4Slave_0:wdata
	wire          mm_interconnect_0_axi4slave_0_altera_axi4_slave_arvalid;  // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_arvalid -> axi4Slave_0:arvalid
	wire    [3:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_awcache;  // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_awcache -> axi4Slave_0:awcache
	wire    [1:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_arid;     // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_arid -> axi4Slave_0:arid
	wire    [0:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_arlock;   // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_arlock -> axi4Slave_0:arlock
	wire    [0:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_awlock;   // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_awlock -> axi4Slave_0:awlock
	wire   [13:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_awaddr;   // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_awaddr -> axi4Slave_0:awaddr
	wire    [1:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_bresp;    // axi4Slave_0:bresp -> mm_interconnect_0:axi4Slave_0_altera_axi4_slave_bresp
	wire          mm_interconnect_0_axi4slave_0_altera_axi4_slave_arready;  // axi4Slave_0:arready -> mm_interconnect_0:axi4Slave_0_altera_axi4_slave_arready
	wire  [127:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_rdata;    // axi4Slave_0:rdata -> mm_interconnect_0:axi4Slave_0_altera_axi4_slave_rdata
	wire          mm_interconnect_0_axi4slave_0_altera_axi4_slave_awready;  // axi4Slave_0:awready -> mm_interconnect_0:axi4Slave_0_altera_axi4_slave_awready
	wire    [1:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_arburst;  // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_arburst -> axi4Slave_0:arburst
	wire    [2:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_arsize;   // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_arsize -> axi4Slave_0:arsize
	wire          mm_interconnect_0_axi4slave_0_altera_axi4_slave_bready;   // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_bready -> axi4Slave_0:bready
	wire          mm_interconnect_0_axi4slave_0_altera_axi4_slave_rlast;    // axi4Slave_0:rlast -> mm_interconnect_0:axi4Slave_0_altera_axi4_slave_rlast
	wire          mm_interconnect_0_axi4slave_0_altera_axi4_slave_wlast;    // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_wlast -> axi4Slave_0:wlast
	wire    [3:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_awregion; // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_awregion -> axi4Slave_0:awregion
	wire    [1:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_rresp;    // axi4Slave_0:rresp -> mm_interconnect_0:axi4Slave_0_altera_axi4_slave_rresp
	wire    [1:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_awid;     // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_awid -> axi4Slave_0:awid
	wire    [1:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_bid;      // axi4Slave_0:bid -> mm_interconnect_0:axi4Slave_0_altera_axi4_slave_bid
	wire          mm_interconnect_0_axi4slave_0_altera_axi4_slave_bvalid;   // axi4Slave_0:bvalid -> mm_interconnect_0:axi4Slave_0_altera_axi4_slave_bvalid
	wire    [2:0] mm_interconnect_0_axi4slave_0_altera_axi4_slave_awsize;   // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_awsize -> axi4Slave_0:awsize
	wire          mm_interconnect_0_axi4slave_0_altera_axi4_slave_awvalid;  // mm_interconnect_0:axi4Slave_0_altera_axi4_slave_awvalid -> axi4Slave_0:awvalid
	wire          mm_interconnect_0_axi4slave_0_altera_axi4_slave_rvalid;   // axi4Slave_0:rvalid -> mm_interconnect_0:axi4Slave_0_altera_axi4_slave_rvalid
	wire          rst_controller_reset_out_reset;                           // rst_controller:reset_out -> [axi4Slave_0:RST_N, axiMaster_0:RST_N, mm_interconnect_0:axiMaster_0_reset_sink_reset_bridge_in_reset_reset]

	Example3_axi4Slave_0 axi4slave_0 (
		.CLK      (clk_clk),                                                  //             clock.clk
		.araddr   (mm_interconnect_0_axi4slave_0_altera_axi4_slave_araddr),   // altera_axi4_slave.araddr
		.arburst  (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arburst),  //                  .arburst
		.arcache  (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arcache),  //                  .arcache
		.arid     (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arid),     //                  .arid
		.arlen    (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arlen),    //                  .arlen
		.arlock   (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arlock),   //                  .arlock
		.arprot   (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arprot),   //                  .arprot
		.arqos    (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arqos),    //                  .arqos
		.arready  (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arready),  //                  .arready
		.arregion (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arregion), //                  .arregion
		.arsize   (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arsize),   //                  .arsize
		.arvalid  (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arvalid),  //                  .arvalid
		.awaddr   (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awaddr),   //                  .awaddr
		.awburst  (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awburst),  //                  .awburst
		.awcache  (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awcache),  //                  .awcache
		.awid     (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awid),     //                  .awid
		.awlen    (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awlen),    //                  .awlen
		.awlock   (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awlock),   //                  .awlock
		.awprot   (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awprot),   //                  .awprot
		.awqos    (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awqos),    //                  .awqos
		.awready  (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awready),  //                  .awready
		.awregion (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awregion), //                  .awregion
		.awsize   (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awsize),   //                  .awsize
		.awvalid  (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awvalid),  //                  .awvalid
		.bid      (mm_interconnect_0_axi4slave_0_altera_axi4_slave_bid),      //                  .bid
		.bready   (mm_interconnect_0_axi4slave_0_altera_axi4_slave_bready),   //                  .bready
		.bresp    (mm_interconnect_0_axi4slave_0_altera_axi4_slave_bresp),    //                  .bresp
		.bvalid   (mm_interconnect_0_axi4slave_0_altera_axi4_slave_bvalid),   //                  .bvalid
		.rdata    (mm_interconnect_0_axi4slave_0_altera_axi4_slave_rdata),    //                  .rdata
		.rid      (mm_interconnect_0_axi4slave_0_altera_axi4_slave_rid),      //                  .rid
		.rlast    (mm_interconnect_0_axi4slave_0_altera_axi4_slave_rlast),    //                  .rlast
		.rready   (mm_interconnect_0_axi4slave_0_altera_axi4_slave_rready),   //                  .rready
		.rresp    (mm_interconnect_0_axi4slave_0_altera_axi4_slave_rresp),    //                  .rresp
		.rvalid   (mm_interconnect_0_axi4slave_0_altera_axi4_slave_rvalid),   //                  .rvalid
		.wdata    (mm_interconnect_0_axi4slave_0_altera_axi4_slave_wdata),    //                  .wdata
		.wlast    (mm_interconnect_0_axi4slave_0_altera_axi4_slave_wlast),    //                  .wlast
		.wready   (mm_interconnect_0_axi4slave_0_altera_axi4_slave_wready),   //                  .wready
		.wstrb    (mm_interconnect_0_axi4slave_0_altera_axi4_slave_wstrb),    //                  .wstrb
		.wvalid   (mm_interconnect_0_axi4slave_0_altera_axi4_slave_wvalid),   //                  .wvalid
		.RST_N    (~rst_controller_reset_out_reset)                           //        reset_sink.reset_n
	);

	Example3_axiMaster_0 aximaster_0 (
		.CLK      (clk_clk),                                 //              clock.clk
		.araddr   (aximaster_0_altera_axi4_master_araddr),   // altera_axi4_master.araddr
		.arburst  (aximaster_0_altera_axi4_master_arburst),  //                   .arburst
		.arcache  (aximaster_0_altera_axi4_master_arcache),  //                   .arcache
		.arid     (aximaster_0_altera_axi4_master_arid),     //                   .arid
		.arlen    (aximaster_0_altera_axi4_master_arlen),    //                   .arlen
		.arlock   (aximaster_0_altera_axi4_master_arlock),   //                   .arlock
		.arprot   (aximaster_0_altera_axi4_master_arprot),   //                   .arprot
		.arqos    (aximaster_0_altera_axi4_master_arqos),    //                   .arqos
		.arready  (aximaster_0_altera_axi4_master_arready),  //                   .arready
		.arregion (aximaster_0_altera_axi4_master_arregion), //                   .arregion
		.arsize   (aximaster_0_altera_axi4_master_arsize),   //                   .arsize
		.arvalid  (aximaster_0_altera_axi4_master_arvalid),  //                   .arvalid
		.awaddr   (aximaster_0_altera_axi4_master_awaddr),   //                   .awaddr
		.awburst  (aximaster_0_altera_axi4_master_awburst),  //                   .awburst
		.awcache  (aximaster_0_altera_axi4_master_awcache),  //                   .awcache
		.awid     (aximaster_0_altera_axi4_master_awid),     //                   .awid
		.awlen    (aximaster_0_altera_axi4_master_awlen),    //                   .awlen
		.awlock   (aximaster_0_altera_axi4_master_awlock),   //                   .awlock
		.awprot   (aximaster_0_altera_axi4_master_awprot),   //                   .awprot
		.awqos    (aximaster_0_altera_axi4_master_awqos),    //                   .awqos
		.awready  (aximaster_0_altera_axi4_master_awready),  //                   .awready
		.awregion (aximaster_0_altera_axi4_master_awregion), //                   .awregion
		.awsize   (aximaster_0_altera_axi4_master_awsize),   //                   .awsize
		.awvalid  (aximaster_0_altera_axi4_master_awvalid),  //                   .awvalid
		.bid      (aximaster_0_altera_axi4_master_bid),      //                   .bid
		.bready   (aximaster_0_altera_axi4_master_bready),   //                   .bready
		.bresp    (aximaster_0_altera_axi4_master_bresp),    //                   .bresp
		.bvalid   (aximaster_0_altera_axi4_master_bvalid),   //                   .bvalid
		.rdata    (aximaster_0_altera_axi4_master_rdata),    //                   .rdata
		.rid      (aximaster_0_altera_axi4_master_rid),      //                   .rid
		.rlast    (aximaster_0_altera_axi4_master_rlast),    //                   .rlast
		.rready   (aximaster_0_altera_axi4_master_rready),   //                   .rready
		.rresp    (aximaster_0_altera_axi4_master_rresp),    //                   .rresp
		.rvalid   (aximaster_0_altera_axi4_master_rvalid),   //                   .rvalid
		.wdata    (aximaster_0_altera_axi4_master_wdata),    //                   .wdata
		.wlast    (aximaster_0_altera_axi4_master_wlast),    //                   .wlast
		.wready   (aximaster_0_altera_axi4_master_wready),   //                   .wready
		.wstrb    (aximaster_0_altera_axi4_master_wstrb),    //                   .wstrb
		.wvalid   (aximaster_0_altera_axi4_master_wvalid),   //                   .wvalid
		.RST_N    (~rst_controller_reset_out_reset)          //         reset_sink.reset_n
	);

	Example3_mm_interconnect_0 mm_interconnect_0 (
		.axi4Slave_0_altera_axi4_slave_awid                 (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awid),     //                axi4Slave_0_altera_axi4_slave.awid
		.axi4Slave_0_altera_axi4_slave_awaddr               (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awaddr),   //                                             .awaddr
		.axi4Slave_0_altera_axi4_slave_awlen                (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awlen),    //                                             .awlen
		.axi4Slave_0_altera_axi4_slave_awsize               (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awsize),   //                                             .awsize
		.axi4Slave_0_altera_axi4_slave_awburst              (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awburst),  //                                             .awburst
		.axi4Slave_0_altera_axi4_slave_awlock               (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awlock),   //                                             .awlock
		.axi4Slave_0_altera_axi4_slave_awcache              (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awcache),  //                                             .awcache
		.axi4Slave_0_altera_axi4_slave_awprot               (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awprot),   //                                             .awprot
		.axi4Slave_0_altera_axi4_slave_awqos                (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awqos),    //                                             .awqos
		.axi4Slave_0_altera_axi4_slave_awregion             (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awregion), //                                             .awregion
		.axi4Slave_0_altera_axi4_slave_awvalid              (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awvalid),  //                                             .awvalid
		.axi4Slave_0_altera_axi4_slave_awready              (mm_interconnect_0_axi4slave_0_altera_axi4_slave_awready),  //                                             .awready
		.axi4Slave_0_altera_axi4_slave_wdata                (mm_interconnect_0_axi4slave_0_altera_axi4_slave_wdata),    //                                             .wdata
		.axi4Slave_0_altera_axi4_slave_wstrb                (mm_interconnect_0_axi4slave_0_altera_axi4_slave_wstrb),    //                                             .wstrb
		.axi4Slave_0_altera_axi4_slave_wlast                (mm_interconnect_0_axi4slave_0_altera_axi4_slave_wlast),    //                                             .wlast
		.axi4Slave_0_altera_axi4_slave_wvalid               (mm_interconnect_0_axi4slave_0_altera_axi4_slave_wvalid),   //                                             .wvalid
		.axi4Slave_0_altera_axi4_slave_wready               (mm_interconnect_0_axi4slave_0_altera_axi4_slave_wready),   //                                             .wready
		.axi4Slave_0_altera_axi4_slave_bid                  (mm_interconnect_0_axi4slave_0_altera_axi4_slave_bid),      //                                             .bid
		.axi4Slave_0_altera_axi4_slave_bresp                (mm_interconnect_0_axi4slave_0_altera_axi4_slave_bresp),    //                                             .bresp
		.axi4Slave_0_altera_axi4_slave_bvalid               (mm_interconnect_0_axi4slave_0_altera_axi4_slave_bvalid),   //                                             .bvalid
		.axi4Slave_0_altera_axi4_slave_bready               (mm_interconnect_0_axi4slave_0_altera_axi4_slave_bready),   //                                             .bready
		.axi4Slave_0_altera_axi4_slave_arid                 (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arid),     //                                             .arid
		.axi4Slave_0_altera_axi4_slave_araddr               (mm_interconnect_0_axi4slave_0_altera_axi4_slave_araddr),   //                                             .araddr
		.axi4Slave_0_altera_axi4_slave_arlen                (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arlen),    //                                             .arlen
		.axi4Slave_0_altera_axi4_slave_arsize               (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arsize),   //                                             .arsize
		.axi4Slave_0_altera_axi4_slave_arburst              (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arburst),  //                                             .arburst
		.axi4Slave_0_altera_axi4_slave_arlock               (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arlock),   //                                             .arlock
		.axi4Slave_0_altera_axi4_slave_arcache              (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arcache),  //                                             .arcache
		.axi4Slave_0_altera_axi4_slave_arprot               (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arprot),   //                                             .arprot
		.axi4Slave_0_altera_axi4_slave_arqos                (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arqos),    //                                             .arqos
		.axi4Slave_0_altera_axi4_slave_arregion             (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arregion), //                                             .arregion
		.axi4Slave_0_altera_axi4_slave_arvalid              (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arvalid),  //                                             .arvalid
		.axi4Slave_0_altera_axi4_slave_arready              (mm_interconnect_0_axi4slave_0_altera_axi4_slave_arready),  //                                             .arready
		.axi4Slave_0_altera_axi4_slave_rid                  (mm_interconnect_0_axi4slave_0_altera_axi4_slave_rid),      //                                             .rid
		.axi4Slave_0_altera_axi4_slave_rdata                (mm_interconnect_0_axi4slave_0_altera_axi4_slave_rdata),    //                                             .rdata
		.axi4Slave_0_altera_axi4_slave_rresp                (mm_interconnect_0_axi4slave_0_altera_axi4_slave_rresp),    //                                             .rresp
		.axi4Slave_0_altera_axi4_slave_rlast                (mm_interconnect_0_axi4slave_0_altera_axi4_slave_rlast),    //                                             .rlast
		.axi4Slave_0_altera_axi4_slave_rvalid               (mm_interconnect_0_axi4slave_0_altera_axi4_slave_rvalid),   //                                             .rvalid
		.axi4Slave_0_altera_axi4_slave_rready               (mm_interconnect_0_axi4slave_0_altera_axi4_slave_rready),   //                                             .rready
		.axiMaster_0_altera_axi4_master_awid                (aximaster_0_altera_axi4_master_awid),                      //               axiMaster_0_altera_axi4_master.awid
		.axiMaster_0_altera_axi4_master_awaddr              (aximaster_0_altera_axi4_master_awaddr),                    //                                             .awaddr
		.axiMaster_0_altera_axi4_master_awlen               (aximaster_0_altera_axi4_master_awlen),                     //                                             .awlen
		.axiMaster_0_altera_axi4_master_awsize              (aximaster_0_altera_axi4_master_awsize),                    //                                             .awsize
		.axiMaster_0_altera_axi4_master_awburst             (aximaster_0_altera_axi4_master_awburst),                   //                                             .awburst
		.axiMaster_0_altera_axi4_master_awlock              (aximaster_0_altera_axi4_master_awlock),                    //                                             .awlock
		.axiMaster_0_altera_axi4_master_awcache             (aximaster_0_altera_axi4_master_awcache),                   //                                             .awcache
		.axiMaster_0_altera_axi4_master_awprot              (aximaster_0_altera_axi4_master_awprot),                    //                                             .awprot
		.axiMaster_0_altera_axi4_master_awqos               (aximaster_0_altera_axi4_master_awqos),                     //                                             .awqos
		.axiMaster_0_altera_axi4_master_awregion            (aximaster_0_altera_axi4_master_awregion),                  //                                             .awregion
		.axiMaster_0_altera_axi4_master_awvalid             (aximaster_0_altera_axi4_master_awvalid),                   //                                             .awvalid
		.axiMaster_0_altera_axi4_master_awready             (aximaster_0_altera_axi4_master_awready),                   //                                             .awready
		.axiMaster_0_altera_axi4_master_wdata               (aximaster_0_altera_axi4_master_wdata),                     //                                             .wdata
		.axiMaster_0_altera_axi4_master_wstrb               (aximaster_0_altera_axi4_master_wstrb),                     //                                             .wstrb
		.axiMaster_0_altera_axi4_master_wlast               (aximaster_0_altera_axi4_master_wlast),                     //                                             .wlast
		.axiMaster_0_altera_axi4_master_wvalid              (aximaster_0_altera_axi4_master_wvalid),                    //                                             .wvalid
		.axiMaster_0_altera_axi4_master_wready              (aximaster_0_altera_axi4_master_wready),                    //                                             .wready
		.axiMaster_0_altera_axi4_master_bid                 (aximaster_0_altera_axi4_master_bid),                       //                                             .bid
		.axiMaster_0_altera_axi4_master_bresp               (aximaster_0_altera_axi4_master_bresp),                     //                                             .bresp
		.axiMaster_0_altera_axi4_master_bvalid              (aximaster_0_altera_axi4_master_bvalid),                    //                                             .bvalid
		.axiMaster_0_altera_axi4_master_bready              (aximaster_0_altera_axi4_master_bready),                    //                                             .bready
		.axiMaster_0_altera_axi4_master_arid                (aximaster_0_altera_axi4_master_arid),                      //                                             .arid
		.axiMaster_0_altera_axi4_master_araddr              (aximaster_0_altera_axi4_master_araddr),                    //                                             .araddr
		.axiMaster_0_altera_axi4_master_arlen               (aximaster_0_altera_axi4_master_arlen),                     //                                             .arlen
		.axiMaster_0_altera_axi4_master_arsize              (aximaster_0_altera_axi4_master_arsize),                    //                                             .arsize
		.axiMaster_0_altera_axi4_master_arburst             (aximaster_0_altera_axi4_master_arburst),                   //                                             .arburst
		.axiMaster_0_altera_axi4_master_arlock              (aximaster_0_altera_axi4_master_arlock),                    //                                             .arlock
		.axiMaster_0_altera_axi4_master_arcache             (aximaster_0_altera_axi4_master_arcache),                   //                                             .arcache
		.axiMaster_0_altera_axi4_master_arprot              (aximaster_0_altera_axi4_master_arprot),                    //                                             .arprot
		.axiMaster_0_altera_axi4_master_arqos               (aximaster_0_altera_axi4_master_arqos),                     //                                             .arqos
		.axiMaster_0_altera_axi4_master_arregion            (aximaster_0_altera_axi4_master_arregion),                  //                                             .arregion
		.axiMaster_0_altera_axi4_master_arvalid             (aximaster_0_altera_axi4_master_arvalid),                   //                                             .arvalid
		.axiMaster_0_altera_axi4_master_arready             (aximaster_0_altera_axi4_master_arready),                   //                                             .arready
		.axiMaster_0_altera_axi4_master_rid                 (aximaster_0_altera_axi4_master_rid),                       //                                             .rid
		.axiMaster_0_altera_axi4_master_rdata               (aximaster_0_altera_axi4_master_rdata),                     //                                             .rdata
		.axiMaster_0_altera_axi4_master_rresp               (aximaster_0_altera_axi4_master_rresp),                     //                                             .rresp
		.axiMaster_0_altera_axi4_master_rlast               (aximaster_0_altera_axi4_master_rlast),                     //                                             .rlast
		.axiMaster_0_altera_axi4_master_rvalid              (aximaster_0_altera_axi4_master_rvalid),                    //                                             .rvalid
		.axiMaster_0_altera_axi4_master_rready              (aximaster_0_altera_axi4_master_rready),                    //                                             .rready
		.clk_0_clk_clk                                      (clk_clk),                                                  //                                    clk_0_clk.clk
		.axiMaster_0_reset_sink_reset_bridge_in_reset_reset (rst_controller_reset_out_reset)                            // axiMaster_0_reset_sink_reset_bridge_in_reset.reset
	);

	altera_reset_controller #(
		.NUM_RESET_INPUTS          (1),
		.OUTPUT_RESET_SYNC_EDGES   ("deassert"),
		.SYNC_DEPTH                (2),
		.RESET_REQUEST_PRESENT     (0),
		.RESET_REQ_WAIT_TIME       (1),
		.MIN_RST_ASSERTION_TIME    (3),
		.RESET_REQ_EARLY_DSRT_TIME (1),
		.USE_RESET_REQUEST_IN0     (0),
		.USE_RESET_REQUEST_IN1     (0),
		.USE_RESET_REQUEST_IN2     (0),
		.USE_RESET_REQUEST_IN3     (0),
		.USE_RESET_REQUEST_IN4     (0),
		.USE_RESET_REQUEST_IN5     (0),
		.USE_RESET_REQUEST_IN6     (0),
		.USE_RESET_REQUEST_IN7     (0),
		.USE_RESET_REQUEST_IN8     (0),
		.USE_RESET_REQUEST_IN9     (0),
		.USE_RESET_REQUEST_IN10    (0),
		.USE_RESET_REQUEST_IN11    (0),
		.USE_RESET_REQUEST_IN12    (0),
		.USE_RESET_REQUEST_IN13    (0),
		.USE_RESET_REQUEST_IN14    (0),
		.USE_RESET_REQUEST_IN15    (0),
		.ADAPT_RESET_REQUEST       (0)
	) rst_controller (
		.reset_in0      (~reset_reset_n),                 // reset_in0.reset
		.clk            (clk_clk),                        //       clk.clk
		.reset_out      (rst_controller_reset_out_reset), // reset_out.reset
		.reset_req      (),                               // (terminated)
		.reset_req_in0  (1'b0),                           // (terminated)
		.reset_in1      (1'b0),                           // (terminated)
		.reset_req_in1  (1'b0),                           // (terminated)
		.reset_in2      (1'b0),                           // (terminated)
		.reset_req_in2  (1'b0),                           // (terminated)
		.reset_in3      (1'b0),                           // (terminated)
		.reset_req_in3  (1'b0),                           // (terminated)
		.reset_in4      (1'b0),                           // (terminated)
		.reset_req_in4  (1'b0),                           // (terminated)
		.reset_in5      (1'b0),                           // (terminated)
		.reset_req_in5  (1'b0),                           // (terminated)
		.reset_in6      (1'b0),                           // (terminated)
		.reset_req_in6  (1'b0),                           // (terminated)
		.reset_in7      (1'b0),                           // (terminated)
		.reset_req_in7  (1'b0),                           // (terminated)
		.reset_in8      (1'b0),                           // (terminated)
		.reset_req_in8  (1'b0),                           // (terminated)
		.reset_in9      (1'b0),                           // (terminated)
		.reset_req_in9  (1'b0),                           // (terminated)
		.reset_in10     (1'b0),                           // (terminated)
		.reset_req_in10 (1'b0),                           // (terminated)
		.reset_in11     (1'b0),                           // (terminated)
		.reset_req_in11 (1'b0),                           // (terminated)
		.reset_in12     (1'b0),                           // (terminated)
		.reset_req_in12 (1'b0),                           // (terminated)
		.reset_in13     (1'b0),                           // (terminated)
		.reset_req_in13 (1'b0),                           // (terminated)
		.reset_in14     (1'b0),                           // (terminated)
		.reset_req_in14 (1'b0),                           // (terminated)
		.reset_in15     (1'b0),                           // (terminated)
		.reset_req_in15 (1'b0)                            // (terminated)
	);

endmodule