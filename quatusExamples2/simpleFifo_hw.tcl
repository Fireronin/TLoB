# TCL File Generated by Component Editor 21.1
# Fri Apr 29 16:43:52 BST 2022
# DO NOT MODIFY


# 
# simpleFifo "simpleFifo" v1.0
#  2022.04.29.16:43:52
# 
# 

# 
# request TCL package from ACDS 16.1
# 
package require -exact qsys 16.1


# 
# module simpleFifo
# 
set_module_property DESCRIPTION ""
set_module_property NAME simpleFifo
set_module_property VERSION 1.0
set_module_property INTERNAL false
set_module_property OPAQUE_ADDRESS_MAP true
set_module_property AUTHOR ""
set_module_property DISPLAY_NAME simpleFifo
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
add_fileset_file mkSimpleFIFO.v VERILOG PATH C:/Users/nudy1/Desktop/QuartusVerilog/mkSimpleFIFO.v TOP_LEVEL_FILE


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
# connection point enable_deq
# 
add_interface enable_deq conduit end
set_interface_property enable_deq associatedClock clock
set_interface_property enable_deq associatedReset reset_sink
set_interface_property enable_deq ENABLED true
set_interface_property enable_deq EXPORT_OF ""
set_interface_property enable_deq PORT_NAME_MAP ""
set_interface_property enable_deq CMSIS_SVD_VARIABLES ""
set_interface_property enable_deq SVD_ADDRESS_GROUP ""

add_interface_port enable_deq EN_deq wire Input 1


# 
# connection point enable_enq
# 
add_interface enable_enq conduit end
set_interface_property enable_enq associatedClock clock
set_interface_property enable_enq associatedReset reset_sink
set_interface_property enable_enq ENABLED true
set_interface_property enable_enq EXPORT_OF ""
set_interface_property enable_enq PORT_NAME_MAP ""
set_interface_property enable_enq CMSIS_SVD_VARIABLES ""
set_interface_property enable_enq SVD_ADDRESS_GROUP ""

add_interface_port enable_enq EN_enq wire Input 1


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
# connection point ready_deq
# 
add_interface ready_deq conduit end
set_interface_property ready_deq associatedClock clock
set_interface_property ready_deq associatedReset reset_sink
set_interface_property ready_deq ENABLED true
set_interface_property ready_deq EXPORT_OF ""
set_interface_property ready_deq PORT_NAME_MAP ""
set_interface_property ready_deq CMSIS_SVD_VARIABLES ""
set_interface_property ready_deq SVD_ADDRESS_GROUP ""

add_interface_port ready_deq RDY_deq wire Output 1


# 
# connection point ready_enq
# 
add_interface ready_enq conduit end
set_interface_property ready_enq associatedClock clock
set_interface_property ready_enq associatedReset reset_sink
set_interface_property ready_enq ENABLED true
set_interface_property ready_enq EXPORT_OF ""
set_interface_property ready_enq PORT_NAME_MAP ""
set_interface_property ready_enq CMSIS_SVD_VARIABLES ""
set_interface_property ready_enq SVD_ADDRESS_GROUP ""

add_interface_port ready_enq RDY_enq wire Output 1


# 
# connection point first
# 
add_interface first conduit end
set_interface_property first associatedClock clock
set_interface_property first associatedReset reset_sink
set_interface_property first ENABLED true
set_interface_property first EXPORT_OF ""
set_interface_property first PORT_NAME_MAP ""
set_interface_property first CMSIS_SVD_VARIABLES ""
set_interface_property first SVD_ADDRESS_GROUP ""

add_interface_port first first wire Output 32


# 
# connection point enq_value
# 
add_interface enq_value conduit end
set_interface_property enq_value associatedClock clock
set_interface_property enq_value associatedReset reset_sink
set_interface_property enq_value ENABLED true
set_interface_property enq_value EXPORT_OF ""
set_interface_property enq_value PORT_NAME_MAP ""
set_interface_property enq_value CMSIS_SVD_VARIABLES ""
set_interface_property enq_value SVD_ADDRESS_GROUP ""

add_interface_port enq_value enq_value wire Input 32


# 
# connection point ready_first
# 
add_interface ready_first conduit end
set_interface_property ready_first associatedClock clock
set_interface_property ready_first associatedReset reset_sink
set_interface_property ready_first ENABLED true
set_interface_property ready_first EXPORT_OF ""
set_interface_property ready_first PORT_NAME_MAP ""
set_interface_property ready_first CMSIS_SVD_VARIABLES ""
set_interface_property ready_first SVD_ADDRESS_GROUP ""

add_interface_port ready_first RDY_first wire Output 1
