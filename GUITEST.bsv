package GUITEST;
// necessary packages
import Connectable::*;
import Vector::*;
import Core::*;
import Core_IFC::*;
import MemUtils::*;
import AXI4_Types::*;
import AXI4_Fake_16550::*;
import AXI4_Interconnect::*;


function Vector #(2, Bool) route_bus4 (r_t x) provisos ( Bits#(r_t,r_l) );
	Bit#(r_l) address = pack(x);
	Vector#(2, Bool) oneHotaddress = replicate (False);
	// memory -> 0
	if (address >= 0 && address < 4096)
		oneHotaddress[0] = True;
	// fake16550 -> 1
	if (address >= 4096 && address < 8192)
		oneHotaddress[1] = True;
	return oneHotaddress;
endfunction

module top ();
 
	Core_IFC::Core_IFC#(SoC_Map::N_External_Interrupt_Sources) core <- mkCore();
	AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0) memory <- mkAXI4Mem(4096, tagged Invalid);
	AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0) fake16550 <- mkAXI4_Fake_16550_Simple();


	Vector::Vector#(1,AXI4_Types::AXI4_Master#(6,64,64,0,0,0,0,0)) bus4_masters;
	bus4_masters[0] = core.core_mem_master;
	Vector::Vector#(2,AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0)) bus4_slaves;
	bus4_slaves[0] = memory;
	bus4_slaves[1] = fake16550;
	AXI4_Interconnect::mkAXI4Bus(route_bus4,bus4_masters,bus4_slaves);


endmodule
endpackage
