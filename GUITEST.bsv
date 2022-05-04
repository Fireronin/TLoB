package GUITEST;
// necessary packages
import Connectable::*;
import Vector::*;
import Core::*;
import Core_IFC::*;


interface Subset;
	interface AXI4_Types::AXI4_Master_Sig#(5,64,64,0,0,0,0,0) aaa;
	method Vector::Vector#(0,PLIC::PLIC_Source_IFC) bbb();
	interface AXI4_Types::AXI4_Master_Sig#(6,64,64,0,0,0,0,0) ccc;
	interface AXI4_Types::AXI4_Slave_Sig#(6,64,512,0,0,0,0,0) dd;
endinterface

module top (Subset);
 
	Core_IFC::Core_IFC_Synth#(SoC_Map::N_External_Interrupt_Sources) core <- mkCore_Synth();


	interface aaa = core.cpu_imem_master;
	method bbb = core.core_external_interrupt_sources;
	interface ccc = core.core_mem_master;
	interface dd = core.dma_server;

endmodule
endpackage
