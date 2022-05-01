package LoadAllTestWithFLute;
// necessary packages
import Connectable::*;
import Vector::*;
import Core::*;
import Core_IFC::*;
import MemUtils::*;
import AXI4_Types::*;
import AXI4_Fake_16550::*;
import Simplefifo::*;

typedef 64 DATASIZE;

interface SocExport;
	interface AXI4_Types::AXI4_Master#(5,64,64,0,0,0,0,0) coreImem;
	method Action ffG(Bit#(32) arg0);
	method Bit#(32) ffG2();
endinterface

module top (SocExport);
 

	interface coreImem = core.cpu_imem_master;
	method ffG = fifo1.enq;
	method ffG2 = fifo1.first;

endmodule
endpackage
