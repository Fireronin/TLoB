# TCL File Generated by Component Editor 21.1
# Thu Apr 21 17:07:13 CEST 2022
# DO NOT MODIFY


# 
# fifo "fifo" v1.0
#  2022.04.21.17:07:13
# 
# 

# 
# request TCL package from ACDS 16.1
# 
package require -exact qsys 16.1


# 
# module fifo
# 
set_module_property DESCRIPTION ""
set_module_property NAME fifo
set_module_property VERSION 1.0
set_module_property INTERNAL false
set_module_property OPAQUE_ADDRESS_MAP true
set_module_property AUTHOR ""
set_module_property DISPLAY_NAME fifo
set_module_property INSTANTIATE_IN_SYSTEM_MODULE true
set_module_property EDITABLE true
set_module_property REPORT_TO_TALKBACK false
set_module_property ALLOW_GREYBOX_GENERATION false
set_module_property REPORT_HIERARCHY false


# 
# file sets
# 
add_fileset QUARTUS_SYNTH QUARTUS_SYNTH "" ""
set_fileset_property QUARTUS_SYNTH TOP_LEVEL mkSimpleFIFO
set_fileset_property QUARTUS_SYNTH ENABLE_RELATIVE_INCLUDE_PATHS false
set_fileset_property QUARTUS_SYNTH ENABLE_FILE_OVERWRITE_MODE false
add_fileset_file mkSimpleFIFO.v VERILOG PATH C:/Users/nudy1/Desktop/mkSimpleFIFO.v TOP_LEVEL_FILE


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
# connection point conduit_end
# 
add_interface conduit_end conduit end
set_interface_property conduit_end associatedClock clock
set_interface_property conduit_end associatedReset ""
set_interface_property conduit_end ENABLED true
set_interface_property conduit_end EXPORT_OF ""
set_interface_property conduit_end PORT_NAME_MAP ""
set_interface_property conduit_end CMSIS_SVD_VARIABLES ""
set_interface_property conduit_end SVD_ADDRESS_GROUP ""

add_interface_port conduit_end EN_enq beginbursttransfer Input 1
add_interface_port conduit_end enq_value writebyteenable_n Input 32
add_interface_port conduit_end RDY_enq writeresponsevalid_n Output 1


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


# 
# connection point conduitIn
# 
add_interface conduitIn conduit end
set_interface_property conduitIn associatedClock clock
set_interface_property conduitIn associatedReset ""
set_interface_property conduitIn ENABLED true
set_interface_property conduitIn EXPORT_OF ""
set_interface_property conduitIn PORT_NAME_MAP ""
set_interface_property conduitIn CMSIS_SVD_VARIABLES ""
set_interface_property conduitIn SVD_ADDRESS_GROUP ""

add_interface_port conduitIn RDY_deq writeresponsevalid_n Output 1
add_interface_port conduitIn EN_deq beginbursttransfer Input 1


# 
# connection point conduit_end_1
# 
add_interface conduit_end_1 conduit end
set_interface_property conduit_end_1 associatedClock clock
set_interface_property conduit_end_1 associatedReset ""
set_interface_property conduit_end_1 ENABLED true
set_interface_property conduit_end_1 EXPORT_OF ""
set_interface_property conduit_end_1 PORT_NAME_MAP ""
set_interface_property conduit_end_1 CMSIS_SVD_VARIABLES ""
set_interface_property conduit_end_1 SVD_ADDRESS_GROUP ""

add_interface_port conduit_end_1 first readdata Output 32
add_interface_port conduit_end_1 RDY_first writeresponsevalid_n Output 1

