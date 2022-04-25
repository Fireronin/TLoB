package GUITEST;
// necessary packages
import Connectable::*;
import Vector::*;
import ExampleAXI4::*;


module top();
 
	AXI4_Types::AXI4_Master#(ExampleAXI4::MID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) instance1 <- axiMaster(1);


endmodule
endpackage
