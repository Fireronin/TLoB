package LoadAllTestWithFLute;
// necessary packages
import Connectable::*;
import Vector::*;
import MemUtils::*;
import MemTypes::*;
import Core::*;
import Core_IFC::*;
import AXI4_Types::*;
import AXI4_Fake_16550::*;
import Simplefifo::*;
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

interface SocExport;
	interface AXI4_Types::AXI4_Master#(5,64,64,0,0,0,0,0) coreImem;
	method Action ffG(Bit#(32) arg0);
	method Bit#(32) ffG2();
endinterface

module top (SocExport);
 

	Vector::Vector#(1,AXI4_Types::AXI4_Master#(6,64,64,0,0,0,0,0)) bus1_masters;
	bus1_masters[0] = core.core_mem_master;
	Vector::Vector#(2,AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0)) bus1_slaves;
	bus1_slaves[0] = memory;
	bus1_slaves[1] = aXI4_Fake_16550;
	AXI4_Interconnect::mkAXI4Bus(route_bus1,bus1_masters,bus1_slaves);
	interface coreImem = core.cpu_imem_master;
	method ffG = fifo1.enq;
	method ffG2 = fifo1.first;

endmodule
endpackage
