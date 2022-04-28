package LoadAllTestWithFLute;
// necessary packages
import Connectable::*;
import Vector::*;
import Simplefifo::*;
import Core::*;
import Core_IFC::*;
import MemUtils::*;
import AXI4_Types::*;
import AXI4_Fake_16550::*;
import ExampleAXI4::*;
import AXI4_Interconnect::*;

typedef 6 ID;
typedef 64 ADDR;
typedef 64 DATA;
typedef 0 AWUSER;
typedef 0 WUSER;
typedef 0 BUSER;
typedef 0 ARUSER;
typedef 0 RUSER;
typedef 64 DATASIZE;

function Vector #(2, Bool) route_mainBus (r_t x) provisos ( Bits#(r_t,r_l) );
	Bit#(r_l) address = pack(x);
	Vector#(2, Bool) oneHotaddress = replicate (False);
	// slave1 -> 0
	if (address >= 0 && address < 1)
		oneHotaddress[0] = True;
	// slave2 -> 1
	if (address >= 1 && address < 2)
		oneHotaddress[1] = True;
	return oneHotaddress;
endfunction

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

module top();
 
	Simplefifo::FIFOIfc#(Bit#(32)) fifo1 <- mkSimpleFIFO();
	Simplefifo::FIFOIfc#(Bit#(32)) fifo2 <- mkSimpleFIFO();
	Core_IFC::Core_IFC#(SoC_Map::N_External_Interrupt_Sources) core <- mkCore();
	AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0) memory <- mkAXI4SimpleMem(4096, tagged Invalid);
	AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0) fakeExternalConnection <- mkAXI4_Fake_16550_Simple();
	AXI4_Types::AXI4_Master#(ExampleAXI4::MID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) master1 <- axiMaster(10);
	AXI4_Types::AXI4_Master#(ExampleAXI4::MID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) master2 <- axiMaster(11);
	AXI4_Types::AXI4_Slave#(ExampleAXI4::SID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) slave1 <- axiSlave(12);
	AXI4_Types::AXI4_Slave#(ExampleAXI4::SID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz) slave2 <- axiSlave(13);
	AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0) aXI4_Fake_16550 <- mkAXI4_Fake_16550_Simple();

	mkConnection(fifo1,fifo2);
	Vector::Vector#(2,AXI4_Types::AXI4_Master#(ExampleAXI4::MID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz)) mainBus_masters;
	mainBus_masters[0] = master1;
	mainBus_masters[1] = master2;
	Vector::Vector#(2,AXI4_Types::AXI4_Slave#(ExampleAXI4::SID_sz,ExampleAXI4::ADDR_sz,ExampleAXI4::DATA_sz,ExampleAXI4::AWUSER_sz,ExampleAXI4::WUSER_sz,ExampleAXI4::BUSER_sz,ExampleAXI4::ARUSER_sz,ExampleAXI4::RUSER_sz)) mainBus_slaves;
	mainBus_slaves[0] = slave1;
	mainBus_slaves[1] = slave2;
	AXI4_Interconnect::mkAXI4Bus(route_mainBus,mainBus_masters,mainBus_slaves);
	Vector::Vector#(1,AXI4_Types::AXI4_Master#(6,64,64,0,0,0,0,0)) bus1_masters;
	bus1_masters[0] = core.core_mem_master;
	Vector::Vector#(2,AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0)) bus1_slaves;
	bus1_slaves[0] = memory;
	bus1_slaves[1] = aXI4_Fake_16550;
	AXI4_Interconnect::mkAXI4Bus(route_bus1,bus1_masters,bus1_slaves);

endmodule
endpackage
