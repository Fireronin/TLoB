package TopBus;
import Vector :: * ;


function Vector #(r_s, Bool) route (r_t x) provisos ( Bits#(r_t,r_s) );
    Bit#(r_s) r_t_b = pack(x);
    // create empty vector
    Vector#(r_s, Bool) r_t_v = replicate (False);
    r_t_v[0] = False;
    // check if r_t_b is in the range of 5-10 if so set 1 bit in r_t_v
    if (r_t_b >= 5 && r_t_b <= 10)
        r_t_v[1] = True;
    return r_t_v;
endfunction


module top (Empty);

    Reg#(Bit#(4)) data <- mkReg(0);

    rule test;
        data <= data + 1;
        $display("%d", data);
        Vector#(4,Bool) xd = route(data);
        $display("%b", xd);
        // if data is max then finish
        if (data == 15)
            $finish(1);
    endrule

endmodule

endpackage