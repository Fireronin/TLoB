package ConnectedAXI4;
// necessary packages
import Connectable::*;
import Vector::*;
import ExampleAXI4::*;
import AXI4_Interconnect::*;


function Vector #(2, Bool) route_mainBus (r_t x) provisos ( Bits#(r_t,r_l) );
	Bit#(r_l) adress = pack(x);
	Vector#(2, Bool) oneHotAdress = replicate (False);
	// slave1 -> 0
	if (adress == 0)
		oneHotAdress[0] = True;
	// slave2 -> 1
	if (adress == 10)
		oneHotAdress[1] = True;
	return oneHotAdress;
endfunction

module top();
 
	AXI4_Types::AXI4_Master#(ExampleAXI4::MID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) master1 <- axiMaster(1);
	AXI4_Types::AXI4_Master#(ExampleAXI4::MID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) master2 <- axiMaster(2);
	AXI4_Types::AXI4_Slave#(ExampleAXI4::SID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) slave1 <- axiSlave(5);
	AXI4_Types::AXI4_Slave#(ExampleAXI4::SID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) slave2 <- axiSlave(7);

	Vector::Vector#(2,AXI4_Types::AXI4_Master#(ExampleAXI4::MID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz)) mainBus_masters;
	mainBus_masters[0] = master1;
	mainBus_masters[1] = master2;
	Vector::Vector#(2,AXI4_Types::AXI4_Slave#(ExampleAXI4::SID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz)) mainBus_slaves;
	mainBus_slaves[0] = slave1;
	mainBus_slaves[1] = slave2;
	AXI4_Interconnect::mkAXI4Bus(route_mainBus,mainBus_masters,mainBus_slaves);

endmodule
endpackage
