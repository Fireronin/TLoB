package TopBus;


module top (Empty);

    Reg#(Bit#(32)) data <- mkReg(0);

    rule test;
        data <= data + 1;
        $display("%d", data);
    endrule

endmodule

endpackage