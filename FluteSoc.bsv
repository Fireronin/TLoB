package FluteSoc;
// necessary packages
import Connectable::*;
import Vector::*;
import Core::*;
import Core_IFC::*;
import MemUtils::*;
import AXI4_Types::*;
import AXI4_Fake_16550::*;
import AXI4_Interconnect::*;

typedef 64 DATASIZE;

function Vector #(2, Bool) route_bus1 (r_t x) provisos ( Bits#(r_t,r_l) );
	Bit#(r_l) address = pack(x);
	Vector#(2, Bool) oneHotaddress = replicate (False);
	// memory -> 0
	if (address >= 0 && address < 4096)
		oneHotaddress[0] = True;
	// aXI4_Fake_16550 -> 1
	if (address >= 4096 && address < 8192)
		oneHotaddress[1] = True;
	return oneHotaddress;
endfunction

module top ();
 
	Core_IFC::Core_IFC#(SoC_Map::N_External_Interrupt_Sources) core <- mkCore();
	AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0) memory <- mkAXI4SimpleMem(4096, tagged Invalid);
	AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0) aXI4_Fake_16550 <- mkAXI4_Fake_16550_Simple();

	Vector::Vector#(1,AXI4_Types::AXI4_Master#(6,64,64,0,0,0,0,0)) bus1_masters;
	bus1_masters[0] = core.core_mem_master;
	Vector::Vector#(2,AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0)) bus1_slaves;
	bus1_slaves[0] = memory;
	bus1_slaves[1] = aXI4_Fake_16550;
	AXI4_Interconnect::mkAXI4Bus(route_bus1,bus1_masters,bus1_slaves);

endmodule
endpackage
