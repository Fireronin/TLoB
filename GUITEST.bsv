package GUITEST;
// necessary packages
import Connectable::*;
import Vector::*;
import ExampleAXI4::*;
import AXI4_Types::*;
import AXI4_Interconnect::*;


function Vector #(2, Bool) route_bus5 (r_t x) provisos ( Bits#(r_t,r_l) );
	Bit#(r_l) address = pack(x);
	Vector#(2, Bool) oneHotaddress = replicate (False);
	// instance4 -> 0
	if (address >= 0 && address < 1)
		oneHotaddress[0] = True;
	// instance3 -> 1
	if (address >= 1 && address < 2)
		oneHotaddress[1] = True;
	return oneHotaddress;
endfunction

module top();
 
	AXI4_Types::AXI4_Master#(ExampleAXI4::MID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) instance1 <- axiMaster(1 );
	AXI4_Types::AXI4_Master#(ExampleAXI4::MID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) instance2 <- axiMaster(2 );
	AXI4_Types::AXI4_Slave#(ExampleAXI4::SID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) instance3 <- axiSlave(3 );
	AXI4_Types::AXI4_Slave#(ExampleAXI4::SID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) instance4 <- axiSlave(13413413);

	Vector::Vector#(2,AXI4_Types::AXI4_Master#(ExampleAXI4::MID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz)) bus5_masters;
	bus5_masters[0] = instance1;
	bus5_masters[1] = instance2;
	Vector::Vector#(2,AXI4_Types::AXI4_Slave#(ExampleAXI4::SID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz)) bus5_slaves;
	bus5_slaves[0] = instance4;
	bus5_slaves[1] = instance3;
	AXI4_Interconnect::mkAXI4Bus(route_bus5,bus5_masters,bus5_slaves);

endmodule
endpackage
