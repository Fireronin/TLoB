package fifoChain;
// necessary packages
import Connectable::*;
import Vector::*;
import FIFO::*;
import GetPut::*;
import Core::*;
import Core_IFC::*;
import MemUtils::*;
import AXI4_Types::*;
import AXI4_Interconnect::*;

typedef 1 DATASIZE;
typedef 4 ADDRWIDTH;

function Vector #(1, Bool) route_mainBus (r_t x) provisos ( Bits#(r_t,r_l) );
	Bit#(r_l) address = pack(x);
	Vector#(1, Bool) oneHotaddress = replicate (False);
	// memory -> 0
	if (address >= 0 && address < 4096)
		oneHotaddress[0] = True;
	if (address >= 5096 && address < 6400)
		oneHotaddress[0] = True;
	return oneHotaddress;
endfunction

module top();
 
	FIFO::FIFO#(Bit#(8)) ff1 <- mkFIFO();
	GetPut::Get#(Bit#(8)) ff1get <- toGet(ff1);
	FIFO::FIFO#(Bit#(8)) ff2 <- mkFIFO();
	GetPut::Put#(Bit#(8)) ff2put <- toPut(ff2);
	Core_IFC::Core_IFC#(SoC_Map::N_External_Interrupt_Sources) core <- mkCore();
	AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0) memory <- mkAXI4SimpleMem(4096, Maybe#("xddd"));

	mkConnection(ff1get,ff2put);
	Vector::Vector#(1,AXI4_Types::AXI4_Master#(6,64,64,0,0,0,0,0)) mainBus_masters;
	mainBus_masters[0] = core.core_mem_master;
	Vector::Vector#(1,AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0)) mainBus_slaves;
	mainBus_slaves[0] = memory;
	AXI4_Interconnect::mkAXI4Bus(route_mainBus,mainBus_masters,mainBus_slaves);

endmodule
endpackage
