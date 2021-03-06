/*
 * Generated by Bluespec Compiler, version 2021.07 (build 4cac6eb)
 * 
 * On Tue Mar  8 15:41:57 GMT 2022
 * 
 */

/* Generation options: */
#ifndef __mkDM_System_Bus_h__
#define __mkDM_System_Bus_h__

#include "bluesim_types.h"
#include "bs_module.h"
#include "bluesim_primitives.h"
#include "bs_vcd.h"


/* Class declaration for the mkDM_System_Bus module */
class MOD_mkDM_System_Bus : public Module {
 
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
  MOD_Fifo<tUWide> INST_masterPortShim_arff;
  MOD_Fifo<tUWide> INST_masterPortShim_awff;
  MOD_Fifo<tUInt8> INST_masterPortShim_bff;
  MOD_Fifo<tUWide> INST_masterPortShim_rff;
  MOD_Fifo<tUWide> INST_masterPortShim_wff;
  MOD_Reg<tUInt8> INST_rg_sb_state;
  MOD_Reg<tUInt32> INST_rg_sbaddress0;
  MOD_Reg<tUInt32> INST_rg_sbaddress1;
  MOD_Reg<tUInt64> INST_rg_sbaddress_reading;
  MOD_Reg<tUInt8> INST_rg_sbcs_sbaccess;
  MOD_Reg<tUInt8> INST_rg_sbcs_sbautoincrement;
  MOD_Reg<tUInt8> INST_rg_sbcs_sbbusyerror;
  MOD_Reg<tUInt8> INST_rg_sbcs_sberror;
  MOD_Reg<tUInt8> INST_rg_sbcs_sbreadonaddr;
  MOD_Reg<tUInt8> INST_rg_sbcs_sbreadondata;
  MOD_Reg<tUInt32> INST_rg_sbdata0;
 
 /* Constructor */
 public:
  MOD_mkDM_System_Bus(tSimStateHdl simHdl, char const *name, Module *parent);
 
 /* Symbol init methods */
 private:
  void init_symbols_0();
 
 /* Reset signal definitions */
 private:
  tUInt8 PORT_RST_N;
 
 /* Port definitions */
 public:
  tUWide PORT_master_r_put_val;
  tUWide PORT_master_aw_peek;
  tUWide PORT_master_w_peek;
  tUWide PORT_master_ar_peek;
 
 /* Publicly accessible definitions */
 public:
  tUInt8 DEF_masterPortShim_arff_i_notEmpty____d468;
  tUInt8 DEF_masterPortShim_wff_i_notEmpty____d467;
  tUInt8 DEF_masterPortShim_awff_i_notEmpty____d466;
  tUInt8 DEF_WILL_FIRE_RL_rl_sb_read_finish;
  tUInt8 DEF_rg_sb_state_EQ_0___d98;
  tUInt8 DEF_rg_sbcs_sbbusyerror__h2279;
  tUInt8 DEF_rg_sbcs_sbreadonaddr__h2281;
  tUInt8 DEF_NOT_rg_sb_state_EQ_0_8___d129;
  tUInt8 DEF_rg_sbcs_sbreadondata__h2719;
  tUInt8 DEF_rg_sbcs_sberror__h840;
  tUInt8 DEF_NOT_rg_sbcs_sberror_EQ_0___d125;
  tUInt8 DEF_masterPortShim_arff_i_notFull____d245;
  tUInt8 DEF_rg_sb_state__h828;
  tUInt8 DEF_rg_sbcs_sberror_EQ_0___d7;
 
 /* Local definitions */
 private:
  tUInt8 DEF_rg_sbcs_sbautoincrement__h2283;
  tUWide DEF_masterPortShim_rff_first____d10;
  tUInt32 DEF_v__h2342;
  tUInt32 DEF_v__h2310;
  tUInt8 DEF_rg_sbcs_sbaccess__h1191;
  tUInt32 DEF_x__h2576;
  tUInt64 DEF_rg_sbaddress1_08_CONCAT_rg_sbaddress0_09_10_PL_ETC___d115;
  tUInt32 DEF_x__h2658;
  tUInt64 DEF_IF_rg_sbcs_sbaccess_7_EQ_0_8_THEN_1_ELSE_IF_rg_ETC___d114;
  tUInt8 DEF_NOT_rg_sbcs_sbbusyerror_9___d102;
  tUInt8 DEF_rg_sb_state_EQ_0_8_AND_NOT_rg_sbcs_sbbusyerror_ETC___d127;
  tUInt8 DEF_rg_sb_state_EQ_0_8_AND_rg_sbcs_sbbusyerror_9___d100;
  tUInt8 DEF_rg_sb_state_EQ_0_8_AND_NOT_rg_sbcs_sbbusyerror_ETC___d106;
  tUInt64 DEF_sbaddress__h630;
  tUWide DEF__0_CONCAT_rg_sbaddress1_08_CONCAT_write_dm_word_ETC___d326;
  tUInt32 DEF__0_CONCAT_rg_sbcs_sbaccess_7_CONCAT_65536___d123;
  tUWide DEF__0_CONCAT_rg_sbaddress1_08_CONCAT_rg_sbaddress0_ETC___d124;
  tUWide DEF__0_CONCAT_rg_sbaddress1_08_CONCAT_rg_sbaddress0_ETC___d340;
  tUWide DEF_IF_rg_sbcs_sbaccess_7_EQ_0_8_OR_rg_sbcs_sbacce_ETC___d355;
 
 /* Rules */
 public:
  void RL_rl_sb_read_finish();
  void RL_rl_sb_write_response();
 
 /* Methods */
 public:
  void METH_reset();
  tUInt8 METH_RDY_reset();
  tUInt32 METH_av_read(tUInt8 ARG_av_read_dm_addr);
  tUInt8 METH_RDY_av_read();
  void METH_write(tUInt8 ARG_write_dm_addr, tUInt32 ARG_write_dm_word);
  tUInt8 METH_RDY_write();
  tUInt8 METH_master_aw_canPeek();
  tUInt8 METH_RDY_master_aw_canPeek();
  tUWide METH_master_aw_peek();
  tUInt8 METH_RDY_master_aw_peek();
  void METH_master_aw_drop();
  tUInt8 METH_RDY_master_aw_drop();
  tUInt8 METH_master_w_canPeek();
  tUInt8 METH_RDY_master_w_canPeek();
  tUWide METH_master_w_peek();
  tUInt8 METH_RDY_master_w_peek();
  void METH_master_w_drop();
  tUInt8 METH_RDY_master_w_drop();
  tUInt8 METH_master_b_canPut();
  tUInt8 METH_RDY_master_b_canPut();
  void METH_master_b_put(tUInt8 ARG_master_b_put_val);
  tUInt8 METH_RDY_master_b_put();
  tUInt8 METH_master_ar_canPeek();
  tUInt8 METH_RDY_master_ar_canPeek();
  tUWide METH_master_ar_peek();
  tUInt8 METH_RDY_master_ar_peek();
  void METH_master_ar_drop();
  tUInt8 METH_RDY_master_ar_drop();
  tUInt8 METH_master_r_canPut();
  tUInt8 METH_RDY_master_r_canPut();
  void METH_master_r_put(tUWide ARG_master_r_put_val);
  tUInt8 METH_RDY_master_r_put();
 
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
  void dump_VCD(tVCDDumpType dt, unsigned int levels, MOD_mkDM_System_Bus &backing);
  void vcd_defs(tVCDDumpType dt, MOD_mkDM_System_Bus &backing);
  void vcd_prims(tVCDDumpType dt, MOD_mkDM_System_Bus &backing);
};

#endif /* ifndef __mkDM_System_Bus_h__ */
