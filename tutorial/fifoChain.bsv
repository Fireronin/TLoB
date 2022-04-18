package fifoChain;
// necessary packages
import Core::*;
import Connectable::*;
import MemUtils::*;
import AXI4_Interconnect::*;
import FIFO::*;
import GetPut::*;
// imported packages
import Clocks::*;
import AXI4_Types::*;
import MemSim::*;
import SourceSink::*;
import Prelude::*;
import FIFOF_::*;
import Routable::*;
import AXI4_B_Utils::*;
import Core_IFC::*;
import MasterSlave::*;
import ConfigReg::*;
import Printf::*;
import FIFOF::*;
import AXI4_Common_Types::*;
import AXI4_R_Utils::*;
import AXI4Stream_Types::*;
import AXI4_W_Utils::*;
import AXI4_AR_Utils::*;
import Array::*;
import Real::*;
import RevertingVirtualReg::*;
import AXI4_Utils::*;
import AXI4_Fake_16550::*;
import Interconnect::*;
import AddressFlit::*;
import OneHotArbiter::*;
import Inout::*;
import DefaultValue::*;
import AXI4Lite_Types::*;
import Monitored::*;
import ListExtra::*;
import ListN::*;
import FIFOLevel::*;
import PreludeBSV::*;
import ClientServer::*;
import SpecialFIFOs::*;
import TwoWayBus::*;
import Vector::*;
import AXI4_AW_Utils::*;
import OneWayBus::*;
import List::*;

typedef 1 DATASIZE;
typedef 4 ADDRWIDTH;

function Vector #(1, Bool) route_mainBus (r_t x) provisos ( Bits#(r_t,r_l) );
	Bit#(r_l) adress = pack(x);
	Vector#(1, Bool) oneHotAdress = replicate (False);
	// memory -> 0
	if (adress >= 0 && adress < 4096)
		oneHotAdress[0] = True;
	if (adress >= 5096 && adress < 6400)
		oneHotAdress[0] = True;
	return oneHotAdress;
endfunction

module top();
 
	FIFO::FIFO#(Bit#(8)) ff1 <- mkFIFO();
	GetPut::Get#(Bit#(8)) ff1get <- toGet(ff1);
	FIFO::FIFO#(Bit#(8)) ff2 <- mkFIFO();
	GetPut::Put#(Bit#(8)) ff2put <- toPut(ff2);
	Core_IFC::Core_IFC#(SoC_Map::N_External_Interrupt_Sources) core <- mkCore();
	AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0) memory <- mkAXI4SimpleMem(4096, Maybe#("xddd"));

	mkConnection(ff1get,ff2put);
	AXI4_Interconnect::mkAXI4Bus(route_mainBus,mainBus_masters,mainBus_slaves);

endmodule
endpackage
