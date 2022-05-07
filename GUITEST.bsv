package GUITEST;
// necessary packages
import Connectable::*;
import Vector::*;
import ExampleAXI4::*;
import AXI4_Types::*;
import AXI4_Interconnect::*;


function Vector #(2, Bool) route_bus3 (r_t x) provisos ( Bits#(r_t,r_l) );
	Bit#(r_l) address = pack(x);
	Vector#(2, Bool) oneHotaddress = replicate (False);
	// instance1 -> 1
	if (address >= 0 && address < 1)
		oneHotaddress[1] = True;
	// instance1 -> 1
	if (address >= 2 && address < 3)
		oneHotaddress[1] = True;
	return oneHotaddress;
endfunction

module top ();
 
	AXI4_Types::AXI4_Slave#(ExampleAXI4::SID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) instance1 <- axiSlave(1);
	AXI4_Types::AXI4_Master#(ExampleAXI4::MID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) instance2 <- axiMaster(4);


	Vector::Vector#(2,AXI4_Types::AXI4_Master#(ExampleAXI4::MID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz)) bus3_masters;
	bus3_masters[0] = instance2;
	bus3_masters[1] = instance2;
	Vector::Vector#(2,AXI4_Types::AXI4_Slave#(ExampleAXI4::SID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz)) bus3_slaves;
	bus3_slaves[0] = instance1;
	bus3_slaves[1] = instance1;
	AXI4_Interconnect::mkAXI4Bus(route_bus3,bus3_masters,bus3_slaves);


endmodule
endpackage
