package GUITEST;
// necessary packages
import Connectable::*;
import Vector::*;
import ExampleAXI4::*;


module top();
 
	AXI4_Types::AXI4_Slave#(ExampleAXI4::SID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) instance1 <- axiSlave(1);


endmodule
endpackage
