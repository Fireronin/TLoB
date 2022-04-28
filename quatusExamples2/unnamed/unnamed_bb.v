
module unnamed (
	CLK,
	araddr,
	arburst,
	arcache,
	arid,
	arlen,
	arlock,
	arprot,
	arqos,
	arready,
	arregion,
	arsize,
	arvalid,
	awaddr,
	awburst,
	awcache,
	awid,
	awlen,
	awlock,
	awprot,
	awqos,
	awready,
	awregion,
	awsize,
	awvalid,
	bid,
	bready,
	bresp,
	bvalid,
	rdata,
	rid,
	rlast,
	rready,
	rresp,
	rvalid,
	wdata,
	wlast,
	wready,
	wstrb,
	wvalid,
	RST_N);	

	input		CLK;
	input	[13:0]	araddr;
	input	[1:0]	arburst;
	input	[3:0]	arcache;
	input	[1:0]	arid;
	input	[7:0]	arlen;
	input		arlock;
	input	[2:0]	arprot;
	input	[3:0]	arqos;
	output		arready;
	input	[3:0]	arregion;
	input	[2:0]	arsize;
	input		arvalid;
	input	[13:0]	awaddr;
	input	[1:0]	awburst;
	input	[3:0]	awcache;
	input	[1:0]	awid;
	input	[7:0]	awlen;
	input		awlock;
	input	[2:0]	awprot;
	input	[3:0]	awqos;
	output		awready;
	input	[3:0]	awregion;
	input	[2:0]	awsize;
	input		awvalid;
	output	[1:0]	bid;
	input		bready;
	output	[1:0]	bresp;
	output		bvalid;
	output	[127:0]	rdata;
	output	[1:0]	rid;
	output		rlast;
	input		rready;
	output	[1:0]	rresp;
	output		rvalid;
	input	[127:0]	wdata;
	input		wlast;
	output		wready;
	input	[15:0]	wstrb;
	input		wvalid;
	input		RST_N;
endmodule
