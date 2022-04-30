set_global_assignment -entity "Example3" -library "lib_Example3" -name IP_TOOL_NAME "Qsys"
set_global_assignment -entity "Example3" -library "lib_Example3" -name IP_TOOL_VERSION "21.1"
set_global_assignment -entity "Example3" -library "lib_Example3" -name IP_TOOL_ENV "Qsys"
set_global_assignment -library "lib_Example3" -name SPD_FILE [file join $::quartus(sip_path) "../Example3.spd"]
set_global_assignment -library "lib_Example3" -name MISC_FILE [file join $::quartus(sip_path) "../../Example3.qsys"]

set_global_assignment -library "lib_Example3" -name MISC_FILE [file join $::quartus(sip_path) "Example3.vhd"]
