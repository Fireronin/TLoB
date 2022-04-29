//
// Generated by Bluespec Compiler, version 2021.07 (build 4cac6eb)
//
// On Fri Apr 29 14:47:13 BST 2022
//
//
// Ports:
// Name                         I/O  size props
// RDY_enq                        O     1
// RDY_deq                        O     1 reg
// first                          O    32 reg
// RDY_first                      O     1 reg
// CLK                            I     1 clock
// RST_N                          I     1 reset
// enq_value                      I    32 reg
// EN_enq                         I     1
// EN_deq                         I     1
//
// No combinational paths from inputs to outputs
//
//

`ifdef BSV_ASSIGNMENT_DELAY
`else
  `define BSV_ASSIGNMENT_DELAY
`endif

`ifdef BSV_POSITIVE_RESET
  `define BSV_RESET_VALUE 1'b1
  `define BSV_RESET_EDGE posedge
`else
  `define BSV_RESET_VALUE 1'b0
  `define BSV_RESET_EDGE negedge
`endif

module mkSimpleFIFO_Synth(CLK,
			  RST_N,

			  enq_value,
			  EN_enq,
			  RDY_enq,

			  EN_deq,
			  RDY_deq,

			  first,
			  RDY_first);
  input  CLK;
  input  RST_N;

  // action method enq
  input  [31 : 0] enq_value;
  input  EN_enq;
  output RDY_enq;

  // action method deq
  input  EN_deq;
  output RDY_deq;

  // value method first
  output [31 : 0] first;
  output RDY_first;

  // signals for module outputs
  wire [31 : 0] first;
  wire RDY_deq, RDY_enq, RDY_first;

  // register fifo_data
  reg [31 : 0] fifo_data;
  wire [31 : 0] fifo_data$D_IN;
  wire fifo_data$EN;

  // register fifo_isFull
  reg fifo_isFull;
  wire fifo_isFull$D_IN, fifo_isFull$EN;

  // ports of submodule fifo_fifo
  wire [31 : 0] fifo_fifo$D_IN;
  wire fifo_fifo$CLR, fifo_fifo$DEQ, fifo_fifo$ENQ, fifo_fifo$FULL_N;

  // ports of submodule fifo_fifo2
  wire [31 : 0] fifo_fifo2$D_IN, fifo_fifo2$D_OUT;
  wire fifo_fifo2$CLR, fifo_fifo2$DEQ, fifo_fifo2$EMPTY_N, fifo_fifo2$ENQ;

  // action method enq
  assign RDY_enq = !fifo_isFull ;

  // action method deq
  assign RDY_deq = fifo_isFull ;

  // value method first
  assign first = fifo_data ;
  assign RDY_first = fifo_isFull ;

  // submodule fifo_fifo
  FIFO2 #(.width(32'd32), .guarded(1'd1)) fifo_fifo(.RST(RST_N),
						    .CLK(CLK),
						    .D_IN(fifo_fifo$D_IN),
						    .ENQ(fifo_fifo$ENQ),
						    .DEQ(fifo_fifo$DEQ),
						    .CLR(fifo_fifo$CLR),
						    .D_OUT(),
						    .FULL_N(fifo_fifo$FULL_N),
						    .EMPTY_N());

  // submodule fifo_fifo2
  FIFO2 #(.width(32'd32), .guarded(1'd1)) fifo_fifo2(.RST(RST_N),
						     .CLK(CLK),
						     .D_IN(fifo_fifo2$D_IN),
						     .ENQ(fifo_fifo2$ENQ),
						     .DEQ(fifo_fifo2$DEQ),
						     .CLR(fifo_fifo2$CLR),
						     .D_OUT(fifo_fifo2$D_OUT),
						     .FULL_N(),
						     .EMPTY_N(fifo_fifo2$EMPTY_N));

  // register fifo_data
  assign fifo_data$D_IN = enq_value ;
  assign fifo_data$EN = EN_enq ;

  // register fifo_isFull
  assign fifo_isFull$D_IN = !EN_deq ;
  assign fifo_isFull$EN = EN_deq || EN_enq ;

  // submodule fifo_fifo
  assign fifo_fifo$D_IN = fifo_fifo2$D_OUT ;
  assign fifo_fifo$ENQ = fifo_fifo$FULL_N && fifo_fifo2$EMPTY_N ;
  assign fifo_fifo$DEQ = 1'b0 ;
  assign fifo_fifo$CLR = 1'b0 ;

  // submodule fifo_fifo2
  assign fifo_fifo2$D_IN = 32'h0 ;
  assign fifo_fifo2$ENQ = 1'b0 ;
  assign fifo_fifo2$DEQ = 1'b0 ;
  assign fifo_fifo2$CLR = 1'b0 ;

  // handling of inlined registers

  always@(posedge CLK)
  begin
    if (RST_N == `BSV_RESET_VALUE)
      begin
        fifo_data <= `BSV_ASSIGNMENT_DELAY 32'd0;
	fifo_isFull <= `BSV_ASSIGNMENT_DELAY 1'd0;
      end
    else
      begin
        if (fifo_data$EN) fifo_data <= `BSV_ASSIGNMENT_DELAY fifo_data$D_IN;
	if (fifo_isFull$EN)
	  fifo_isFull <= `BSV_ASSIGNMENT_DELAY fifo_isFull$D_IN;
      end
  end

  // synopsys translate_off
  `ifdef BSV_NO_INITIAL_BLOCKS
  `else // not BSV_NO_INITIAL_BLOCKS
  initial
  begin
    fifo_data = 32'hAAAAAAAA;
    fifo_isFull = 1'h0;
  end
  `endif // BSV_NO_INITIAL_BLOCKS
  // synopsys translate_on
endmodule  // mkSimpleFIFO_Synth

