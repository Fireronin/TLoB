package GUITEST;
// necessary packages
import Connectable::*;
import Vector::*;
import Simplefifo::*;
import Core::*;
import Core_IFC::*;
import MemUtils::*;
import AXI4Lite_Types::*;
import AXI4_AXI4Lite_Bridges::*;
import AXI4_Types::*;


module top();
 
	Simplefifo::FIFOIfc#(Bit#(32)) instance1 <- mkSimpleFIFO();
	Simplefifo::FIFOIfc#(Bit#(32)) instance3 <- mkSimpleFIFO();
	Core_IFC::Core_IFC#(SoC_Map::N_External_Interrupt_Sources) instance4 <- mkCore();
	AXI4Lite_Types::AXI4Lite_Slave#(64,64,0,0,0,0,0) instance5 <- mkAXI4LiteMem(ExampleAXI4::ADDR_sz, tagged Invalid);
	AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0) instance6 <- fromAXI4LiteToAXI4_Slave(instance5);

	mkConnection(instance1,instance3);

endmodule
endpackage
