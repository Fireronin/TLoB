
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
	output	[13:0]	araddr;
	output	[1:0]	arburst;
	output	[3:0]	arcache;
	output		arid;
	output	[7:0]	arlen;
	output		arlock;
	output	[2:0]	arprot;
	output	[3:0]	arqos;
	input		arready;
	output	[3:0]	arregion;
	output	[2:0]	arsize;
	output		arvalid;
	output	[13:0]	awaddr;
	output	[1:0]	awburst;
	output	[3:0]	awcache;
	output		awid;
	output	[7:0]	awlen;
	output		awlock;
	output	[2:0]	awprot;
	output	[3:0]	awqos;
	input		awready;
	output	[3:0]	awregion;
	output	[2:0]	awsize;
	output		awvalid;
	input		bid;
	output		bready;
	input	[1:0]	bresp;
	input		bvalid;
	input	[127:0]	rdata;
	input		rid;
	input		rlast;
	output		rready;
	input	[1:0]	rresp;
	input		rvalid;
	output	[127:0]	wdata;
	output		wlast;
	input		wready;
	output	[15:0]	wstrb;
	output		wvalid;
	input		RST_N;
endmodule
