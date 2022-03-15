/*
 * Generated by Bluespec Compiler, version 2021.07 (build 4cac6eb)
 * 
 * On Tue Mar  8 15:41:57 GMT 2022
 * 
 */

/* Generation options: */
#ifndef __mkGPR_RegFile_h__
#define __mkGPR_RegFile_h__

#include "bluesim_types.h"
#include "bs_module.h"
#include "bluesim_primitives.h"
#include "bs_vcd.h"


/* Class declaration for the mkGPR_RegFile module */
class MOD_mkGPR_RegFile : public Module {
 
 /* Clock handles */
 private:
  tClock __clk_handle_0;
 
 /* Clock gate handles */
 public:
  tUInt8 *clk_gate[0];
 
 /* Instantiation parameters */
 public:
 
 /* Module state */
 public:
  MOD_Fifo<tUInt8> INST_f_reset_rsps;
  MOD_RegFile<tUInt8,tUWide> INST_regfile;
  MOD_Reg<tUInt8> INST_rg_j;
  MOD_Reg<tUInt8> INST_rg_state;
 
 /* Constructor */
 public:
  MOD_mkGPR_RegFile(tSimStateHdl simHdl, char const *name, Module *parent);
 
 /* Symbol init methods */
 private:
  void init_symbols_0();
 
 /* Reset signal definitions */
 private:
  tUInt8 PORT_RST_N;
 
 /* Port definitions */
 public:
  tUInt8 PORT_EN_write_rd;
  tUWide PORT_write_rd_rd_val;
  tUWide PORT_read_rs1;
  tUWide PORT_read_rs1_port2;
  tUWide PORT_read_rs2;
 
 /* Publicly accessible definitions */
 public:
  tUInt8 DEF_WILL_FIRE_write_rd;
  tUInt8 DEF_rg_state__h349;
 
 /* Local definitions */
 private:
  tUWide DEF_regfile_sub_read_rs2_rs2___d165;
  tUWide DEF_regfile_sub_read_rs1_port2_rs1___d88;
  tUWide DEF_regfile_sub_read_rs1_rs1___d11;
  tUWide DEF_IF_read_rs2_rs2_EQ_0_63_THEN_0_ELSE_regfile_su_ETC___d217;
  tUWide DEF_IF_read_rs2_rs2_EQ_0_63_THEN_0_ELSE_regfile_su_ETC___d216;
  tUWide DEF_IF_read_rs1_rs1_EQ_0_THEN_0_ELSE_regfile_sub_r_ETC___d63;
  tUWide DEF_IF_read_rs1_rs1_EQ_0_THEN_0_ELSE_regfile_sub_r_ETC___d62;
  tUWide DEF_IF_read_rs1_port2_rs1_EQ_0_6_THEN_0_ELSE_regfi_ETC___d140;
  tUWide DEF_IF_read_rs1_port2_rs1_EQ_0_6_THEN_0_ELSE_regfi_ETC___d139;
 
 /* Rules */
 public:
  void RL_rl_reset_start();
  void RL_rl_reset_loop();
 
 /* Methods */
 public:
  void METH_server_reset_request_put(tUInt8 ARG_server_reset_request_put);
  tUInt8 METH_RDY_server_reset_request_put();
  void METH_server_reset_response_get();
  tUInt8 METH_RDY_server_reset_response_get();
  tUWide METH_read_rs1(tUInt8 ARG_read_rs1_rs1);
  tUInt8 METH_RDY_read_rs1();
  tUWide METH_read_rs1_port2(tUInt8 ARG_read_rs1_port2_rs1);
  tUInt8 METH_RDY_read_rs1_port2();
  tUWide METH_read_rs2(tUInt8 ARG_read_rs2_rs2);
  tUInt8 METH_RDY_read_rs2();
  void METH_write_rd(tUInt8 ARG_write_rd_rd, tUWide ARG_write_rd_rd_val);
  tUInt8 METH_RDY_write_rd();
 
 /* Reset routines */
 public:
  void reset_RST_N(tUInt8 ARG_rst_in);
 
 /* Static handles to reset routines */
 public:
 
 /* Pointers to reset fns in parent module for asserting output resets */
 private:
 
 /* Functions for the parent module to register its reset fns */
 public:
 
 /* Functions to set the elaborated clock id */
 public:
  void set_clk_0(char const *s);
 
 /* State dumping routine */
 public:
  void dump_state(unsigned int indent);
 
 /* VCD dumping routines */
 public:
  unsigned int dump_VCD_defs(unsigned int levels);
  void dump_VCD(tVCDDumpType dt, unsigned int levels, MOD_mkGPR_RegFile &backing);
  void vcd_defs(tVCDDumpType dt, MOD_mkGPR_RegFile &backing);
  void vcd_prims(tVCDDumpType dt, MOD_mkGPR_RegFile &backing);
};

#endif /* ifndef __mkGPR_RegFile_h__ */