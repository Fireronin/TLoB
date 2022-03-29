package FluteSoc;
// necessary packages
import Core::*;
import MemUtils::*;
import Connectable::*;
import AXI4_Fake_16550::*;
import GetPut::*;
// imported packages
import AXI4_Types::*;
import MasterSlave::*;
import Routable::*;
import AXI4_Interconnect::*;
import SourceSink::*;
import FIFOF::*;
import ClientServer::*;
import Core_IFC::*;
import FIFO::*;
import Vector::*;


function Vector #(2, Bool) route_axi4_bus (r_t x) provisos ( Bits#(r_t,r_l) );
	Bit#(r_l) adress = pack(x);
	Vector#(2, Bool) oneHotAdress = replicate (False);
	// memory -> 0
	if (adress >= 0 && adress <= 2)
		oneHotAdress[0] = True;
	// aXI4_Fake_16550 -> 1
	if (adress >= 3 && adress <= 64)
		oneHotAdress[1] = True;
	return oneHotAdress;
endfunction

module top();
 
	Core_IFC#(SoC_Map::N_External_Interrupt_Sources) core <- mkCore();
	AXI4_Slave#(6, 64, 64, 0, 0, 0, 0, 0) memory <- mkAXI4SimpleMem(32, Invalid);
	AXI4_Slave#(6, 64, 64, 0, 0, 0, 0, 0) aXI4_Fake_16550 <- mkAXI4_Fake_16550_Simple();


	Vector#(1, AXI4_Master#(6, 64, 64, 0, 0, 0, 0, 0)) axi4_bus_masters;
	axi4_bus_masters[0] = core.core_mem_master;
	Vector#(2, AXI4_Slave#(6, 64, 64, 0, 0, 0, 0, 0)) axi4_bus_slaves;
	axi4_bus_slaves[0] = memory;
	axi4_bus_slaves[1] = aXI4_Fake_16550;
	mkAXI4Bus(route_axi4_bus,axi4_bus_masters,axi4_bus_slaves);

endmodule
endpackage
