# TCL File Generated by Component Editor 21.1
# Sun May 08 14:13:47 BST 2022
# DO NOT MODIFY


# 
# axiMaster "axiMaster" v1.0
#  2022.05.08.14:13:47
# 
# 

# 
# request TCL package from ACDS 16.1
# 
package require -exact qsys 16.1


# 
# module axiMaster
# 
set_module_property DESCRIPTION ""
set_module_property NAME axiMaster
set_module_property VERSION 1.0
set_module_property INTERNAL false
set_module_property OPAQUE_ADDRESS_MAP true
set_module_property AUTHOR ""
set_module_property DISPLAY_NAME axiMaster
set_module_property INSTANTIATE_IN_SYSTEM_MODULE true
set_module_property EDITABLE true
set_module_property REPORT_TO_TALKBACK false
set_module_property ALLOW_GREYBOX_GENERATION false
set_module_property REPORT_HIERARCHY false


# 
# file sets
# 
add_fileset QUARTUS_SYNTH QUARTUS_SYNTH "" ""
set_fileset_property QUARTUS_SYNTH TOP_LEVEL axiMaster_synth
set_fileset_property QUARTUS_SYNTH ENABLE_RELATIVE_INCLUDE_PATHS false
set_fileset_property QUARTUS_SYNTH ENABLE_FILE_OVERWRITE_MODE false
add_fileset_file axiMaster_synth.v VERILOG PATH "C:/Users/nudy1/Desktop/Quartus Verilog/axiMaster_synth.v" TOP_LEVEL_FILE


# 
# parameters
# 


# 
# display items
# 


# 
# connection point clock
# 
add_interface clock clock end
set_interface_property clock clockRate 0
set_interface_property clock ENABLED true
set_interface_property clock EXPORT_OF ""
set_interface_property clock PORT_NAME_MAP ""
set_interface_property clock CMSIS_SVD_VARIABLES ""
set_interface_property clock SVD_ADDRESS_GROUP ""

add_interface_port clock CLK clk Input 1


# 
# connection point altera_axi4_master
# 
add_interface altera_axi4_master axi4 start
set_interface_property altera_axi4_master associatedClock clock
set_interface_property altera_axi4_master associatedReset reset_sink
set_interface_property altera_axi4_master readIssuingCapability 1
set_interface_property altera_axi4_master writeIssuingCapability 1
set_interface_property altera_axi4_master combinedIssuingCapability 1
set_interface_property altera_axi4_master ENABLED true
set_interface_property altera_axi4_master EXPORT_OF ""
set_interface_property altera_axi4_master PORT_NAME_MAP ""
set_interface_property altera_axi4_master CMSIS_SVD_VARIABLES ""
set_interface_property altera_axi4_master SVD_ADDRESS_GROUP ""

add_interface_port altera_axi4_master araddr araddr Output 14
add_interface_port altera_axi4_master arburst arburst Output 2
add_interface_port altera_axi4_master arcache arcache Output 4
add_interface_port altera_axi4_master arid arid Output 1
add_interface_port altera_axi4_master arlen arlen Output 8
add_interface_port altera_axi4_master arlock arlock Output 1
add_interface_port altera_axi4_master arprot arprot Output 3
add_interface_port altera_axi4_master arqos arqos Output 4
add_interface_port altera_axi4_master arready arready Input 1
add_interface_port altera_axi4_master arregion arregion Output 4
add_interface_port altera_axi4_master arsize arsize Output 3
add_interface_port altera_axi4_master arvalid arvalid Output 1
add_interface_port altera_axi4_master awaddr awaddr Output 14
add_interface_port altera_axi4_master awburst awburst Output 2
add_interface_port altera_axi4_master awcache awcache Output 4
add_interface_port altera_axi4_master awid awid Output 1
add_interface_port altera_axi4_master awlen awlen Output 8
add_interface_port altera_axi4_master awlock awlock Output 1
add_interface_port altera_axi4_master awprot awprot Output 3
add_interface_port altera_axi4_master awqos awqos Output 4
add_interface_port altera_axi4_master awready awready Input 1
add_interface_port altera_axi4_master awregion awregion Output 4
add_interface_port altera_axi4_master awsize awsize Output 3
add_interface_port altera_axi4_master awvalid awvalid Output 1
add_interface_port altera_axi4_master bid bid Input 1
add_interface_port altera_axi4_master bready bready Output 1
add_interface_port altera_axi4_master bresp bresp Input 2
add_interface_port altera_axi4_master bvalid bvalid Input 1
add_interface_port altera_axi4_master rdata rdata Input 128
add_interface_port altera_axi4_master rid rid Input 1
add_interface_port altera_axi4_master rlast rlast Input 1
add_interface_port altera_axi4_master rready rready Output 1
add_interface_port altera_axi4_master rresp rresp Input 2
add_interface_port altera_axi4_master rvalid rvalid Input 1
add_interface_port altera_axi4_master wdata wdata Output 128
add_interface_port altera_axi4_master wlast wlast Output 1
add_interface_port altera_axi4_master wready wready Input 1
add_interface_port altera_axi4_master wstrb wstrb Output 16
add_interface_port altera_axi4_master wvalid wvalid Output 1


# 
# connection point reset_sink
# 
add_interface reset_sink reset end
set_interface_property reset_sink associatedClock clock
set_interface_property reset_sink synchronousEdges DEASSERT
set_interface_property reset_sink ENABLED true
set_interface_property reset_sink EXPORT_OF ""
set_interface_property reset_sink PORT_NAME_MAP ""
set_interface_property reset_sink CMSIS_SVD_VARIABLES ""
set_interface_property reset_sink SVD_ADDRESS_GROUP ""

add_interface_port reset_sink RST_N reset_n Input 1

