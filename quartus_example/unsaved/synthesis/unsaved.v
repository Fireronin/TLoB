// unsaved.v

// Generated using ACDS version 21.1 842

`timescale 1 ps / 1 ps
module unsaved (
		input  wire  clk_clk,       //   clk.clk
		input  wire  reset_reset_n  // reset.reset_n
	);

	wire    rst_controller_reset_out_reset; // rst_controller:reset_out -> SOmeName_0:RST_N

	mkP2_Core somename_0 (
		.CLK              (clk_clk),                         //      clock.clk
		.RST_N            (~rst_controller_reset_out_reset), // reset_sink.reset_n
		.master0_araddr   (),                                //    master0.araddr
		.master0_arburst  (),                                //           .arburst
		.master0_arcache  (),                                //           .arcache
		.master0_arid     (),                                //           .arid
		.master0_arlen    (),                                //           .arlen
		.master0_arlock   (),                                //           .arlock
		.master0_arprot   (),                                //           .arprot
		.master0_arqos    (),                                //           .arqos
		.master0_arready  (),                                //           .arready
		.master0_arregion (),                                //           .arregion
		.master0_arsize   (),                                //           .arsize
		.master0_arvalid  (),                                //           .arvalid
		.master0_awaddr   (),                                //           .awaddr
		.master0_awburst  (),                                //           .awburst
		.master0_awcache  (),                                //           .awcache
		.master0_awid     (),                                //           .awid
		.master0_awlen    (),                                //           .awlen
		.master0_awlock   (),                                //           .awlock
		.master0_awprot   (),                                //           .awprot
		.master0_awqos    (),                                //           .awqos
		.master0_awready  (),                                //           .awready
		.master0_awregion (),                                //           .awregion
		.master0_awsize   (),                                //           .awsize
		.master0_awvalid  (),                                //           .awvalid
		.master0_bid      (),                                //           .bid
		.master0_bready   (),                                //           .bready
		.master0_bresp    (),                                //           .bresp
		.master0_bvalid   (),                                //           .bvalid
		.master0_rdata    (),                                //           .rdata
		.master0_rid      (),                                //           .rid
		.master0_rlast    (),                                //           .rlast
		.master0_rready   (),                                //           .rready
		.master0_rresp    (),                                //           .rresp
		.master0_rvalid   (),                                //           .rvalid
		.master0_wdata    (),                                //           .wdata
		.master0_wlast    (),                                //           .wlast
		.master0_wready   (),                                //           .wready
		.master0_wstrb    (),                                //           .wstrb
		.master0_wvalid   (),                                //           .wvalid
		.master1_araddr   (),                                //    master1.araddr
		.master1_arburst  (),                                //           .arburst
		.master1_arcache  (),                                //           .arcache
		.master1_arid     (),                                //           .arid
		.master1_arlen    (),                                //           .arlen
		.master1_arlock   (),                                //           .arlock
		.master1_arprot   (),                                //           .arprot
		.master1_arqos    (),                                //           .arqos
		.master1_arready  (),                                //           .arready
		.master1_arregion (),                                //           .arregion
		.master1_arsize   (),                                //           .arsize
		.master1_arvalid  (),                                //           .awvalid
		.master1_awaddr   (),                                //           .awaddr
		.master1_awburst  (),                                //           .awburst
		.master1_awcache  (),                                //           .awcache
		.master1_awid     (),                                //           .awid
		.master1_awlen    (),                                //           .awlen
		.master1_awlock   (),                                //           .awlock
		.master1_awprot   (),                                //           .awprot
		.master1_awqos    (),                                //           .awqos
		.master1_awready  (),                                //           .awready
		.master1_awregion (),                                //           .awregion
		.master1_awsize   (),                                //           .awsize
		.master1_awvalid  (),                                //           .arvalid
		.master1_bid      (),                                //           .bid
		.master1_bready   (),                                //           .bready
		.master1_bresp    (),                                //           .bresp
		.master1_bvalid   (),                                //           .bvalid
		.master1_rdata    (),                                //           .rdata
		.master1_rid      (),                                //           .rid
		.master1_rlast    (),                                //           .rlast
		.master1_rready   (),                                //           .rready
		.master1_rresp    (),                                //           .rresp
		.master1_rvalid   (),                                //           .rvalid
		.master1_wdata    (),                                //           .wdata
		.master1_wlast    (),                                //           .wlast
		.master1_wready   (),                                //           .wready
		.master1_wstrb    (),                                //           .wstrb
		.master1_wvalid   ()                                 //           .wvalid
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
