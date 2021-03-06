/*
 * Generated by Bluespec Compiler, version 2021.07 (build 4cac6eb)
 * 
 * On Tue Mar  8 15:41:57 GMT 2022
 * 
 */

/* Generation options: */
#ifndef __mkTLB_h__
#define __mkTLB_h__

#include "bluesim_types.h"
#include "bs_module.h"
#include "bluesim_primitives.h"
#include "bs_vcd.h"


/* Class declaration for the mkTLB module */
class MOD_mkTLB : public Module {
 
 /* Clock handles */
 private:
  tClock __clk_handle_0;
 
 /* Clock gate handles */
 public:
  tUInt8 *clk_gate[0];
 
 /* Instantiation parameters */
 public:
  tUInt8 const PARAM_dmem_not_imem;
  tUInt8 const PARAM_verbosity;
 
 /* Module state */
 public:
  MOD_Wire<tUInt8> INST_pw_flushing;
  MOD_Reg<tUInt64> INST_rg_va;
  MOD_ConfigReg<tUInt8> INST_tlb0_entries_clearIx;
  MOD_Fifo<tUInt8> INST_tlb0_entries_clearReqQ;
  MOD_ConfigReg<tUInt32> INST_tlb0_entries_lookupReg;
  MOD_Wire<tUInt32> INST_tlb0_entries_lookupWire;
  MOD_BRAM<tUInt8,tUWide,tUInt8> INST_tlb0_entries_mem_0_bram;
  MOD_BRAM<tUInt8,tUWide,tUInt8> INST_tlb0_entries_mem_1_bram;
  MOD_BRAM<tUInt8,tUInt32,tUInt8> INST_tlb0_entries_updateKeys_0_bram;
  MOD_BRAM<tUInt8,tUInt32,tUInt8> INST_tlb0_entries_updateKeys_1_bram;
  MOD_Reg<tUWide> INST_tlb0_entries_updateReg;
  MOD_Reg<tUInt8> INST_tlb0_entries_updateRegFresh;
  MOD_Wire<tUInt8> INST_tlb0_entries_updateRegFresh_1;
  MOD_Wire<tUWide> INST_tlb0_entries_updateWire;
  MOD_ConfigReg<tUInt8> INST_tlb0_entries_wayNext;
  MOD_Reg<tUInt8> INST_tlb1_entries_clearCount;
  MOD_Reg<tUInt8> INST_tlb1_entries_clearReg;
  MOD_Wire<tUInt8> INST_tlb1_entries_didUpdate;
  MOD_RegFile<tUInt8,tUWide> INST_tlb1_entries_mem_0;
  MOD_Reg<tUInt8> INST_tlb2_entries_clearCount;
  MOD_Reg<tUInt8> INST_tlb2_entries_clearReg;
  MOD_Wire<tUInt8> INST_tlb2_entries_didUpdate;
  MOD_RegFile<tUInt8,tUWide> INST_tlb2_entries_mem_0;
 
 /* Constructor */
 public:
  MOD_mkTLB(tSimStateHdl simHdl,
	    char const *name,
	    Module *parent,
	    tUInt8 ARG_dmem_not_imem,
	    tUInt8 ARG_verbosity);
 
 /* Symbol init methods */
 private:
  void init_symbols_0();
 
 /* Reset signal definitions */
 private:
  tUInt8 PORT_RST_N;
 
 /* Port definitions */
 public:
  tUInt8 PORT_EN_ma_insert;
  tUWide PORT_mv_vm_get_xlate;
 
 /* Publicly accessible definitions */
 public:
  tUInt8 DEF_WILL_FIRE_ma_insert;
  tUInt8 DEF_tlb1_entries_clearReg__h993;
  tUInt8 DEF_tlb2_entries_clearReg__h421;
  tUInt8 DEF_NOT_tlb2_entries_clearReg___d78;
  tUInt8 DEF_NOT_tlb1_entries_clearReg___d79;
 
 /* Local definitions */
 private:
  tUWide DEF__0_CONCAT_DONTCARE___d22;
  tUInt8 DEF_tlb0_entries_updateReg_8_BIT_171___d29;
  tUInt8 DEF_tlb0_entries_clearReqQ_i_notEmpty____d20;
  tUWide DEF__dfoo16;
  tUWide DEF__1_CONCAT_tlb0_entries_updateReg_8_BITS_170_TO__ETC___d55;
  tUInt8 DEF_x__h3157;
  tUWide DEF__dfoo12;
  tUInt32 DEF_v__h6249;
  tUInt32 DEF_v__h4392;
  tUWide DEF_tlb0_entries_updateReg___d28;
  tUWide DEF_tlb0_entries_updateWire_wget____d71;
  tUWide DEF_tlb0_entries_mem_1_bram_a_read____d100;
  tUWide DEF_tlb0_entries_mem_0_bram_a_read____d105;
  tUWide DEF_tlb1_entries_mem_0_sub_rg_va_28_BITS_22_TO_21_29___d130;
  tUWide DEF_tlb2_entries_mem_0_sub_rg_va_28_BITS_31_TO_30_43___d144;
  tUInt32 DEF_tlb0_entries_lookupReg_read____d65;
  tUWide DEF_tlb0_entries_updateReg_8_BITS_143_TO_0___d35;
  tUWide DEF_IF_tlb0_entries_updateReg_8_BIT_171_9_AND_tlb0_ETC___d276;
  tUWide DEF_IF_tlb0_entries_updateReg_8_BIT_171_9_AND_tlb0_ETC___d175;
  tUInt32 DEF_x__h3173;
  tUInt8 DEF__read_index__h3599;
  tUWide DEF_IF_tlb2_entries_mem_0_sub_rg_va_28_BITS_31_TO__ETC___d174;
  tUWide DEF_tlb2_entries_mem_0_sub_rg_va_28_BITS_31_TO_30__ETC___d173;
  tUWide DEF_IF_tlb1_entries_mem_0_sub_rg_va_28_BITS_22_TO__ETC___d169;
  tUWide DEF_tlb1_entries_mem_0_sub_rg_va_28_BITS_22_TO_21__ETC___d168;
  tUInt8 DEF_NOT_tlb0_entries_clearReqQ_i_notEmpty__0___d27;
  tUInt8 DEF_NOT_verbosity_ULE_1_4___d85;
  tUWide DEF_IF_tlb0_entries_updateReg_8_BIT_171_9_AND_tlb0_ETC___d170;
  tUWide DEF_IF_tlb0_entries_updateReg_8_BIT_171_9_AND_tlb0_ETC___d165;
  tUWide DEF_IF_mv_vm_get_xlate_priv_ULE_0b1_1_AND_mv_vm_ge_ETC___d278;
  tUWide DEF_mv_vm_get_xlate_priv_ULE_0b1_1_AND_mv_vm_get_x_ETC___d277;
  tUWide DEF_NOT_tlb0_entries_clearReqQ_i_notEmpty__0_7_CON_ETC___d72;
  tUWide DEF_ma_insert_vpn_CONCAT_ma_insert_asid_CONCAT_ma__ETC___d283;
  tUWide DEF_ma_insert_asid_CONCAT_ma_insert_pte_CONCAT_ma__ETC___d282;
  tUWide DEF__1_CONCAT_ma_insert_vpn_BITS_26_TO_11_86_CONCAT_ETC___d287;
  tUWide DEF__0_CONCAT_DONTCARE___d14;
  tUWide DEF__1_CONCAT_ma_insert_vpn_BITS_26_TO_20_90_CONCAT_ETC___d291;
  tUWide DEF__0_CONCAT_DONTCARE___d6;
 
 /* Rules */
 public:
  void RL_tlb2_entries_doClear();
  void RL_tlb1_entries_doClear();
  void RL_tlb0_entries_updateRegFresh__dreg_update();
  void RL_tlb0_entries_updateCanonClear();
  void RL_tlb0_entries_writeUpdateReg();
  void RL_rl_flush();
 
 /* Methods */
 public:
  void METH_mv_vm_put_va(tUInt64 ARG_mv_vm_put_va_full_va);
  tUInt8 METH_RDY_mv_vm_put_va();
  tUWide METH_mv_vm_get_xlate(tUInt64 ARG_mv_vm_get_xlate_satp,
			      tUInt8 ARG_mv_vm_get_xlate_read_not_write,
			      tUInt8 ARG_mv_vm_get_xlate_cap,
			      tUInt8 ARG_mv_vm_get_xlate_priv,
			      tUInt8 ARG_mv_vm_get_xlate_sstatus_SUM,
			      tUInt8 ARG_mv_vm_get_xlate_mstatus_MXR);
  tUInt8 METH_RDY_mv_vm_get_xlate();
  void METH_ma_insert(tUInt32 ARG_ma_insert_asid,
		      tUInt32 ARG_ma_insert_vpn,
		      tUInt64 ARG_ma_insert_pte,
		      tUInt8 ARG_ma_insert_level,
		      tUInt64 ARG_ma_insert_pte_pa);
  tUInt8 METH_RDY_ma_insert();
  void METH_ma_flush();
  tUInt8 METH_RDY_ma_flush();
 
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
  void dump_VCD(tVCDDumpType dt, unsigned int levels, MOD_mkTLB &backing);
  void vcd_defs(tVCDDumpType dt, MOD_mkTLB &backing);
  void vcd_prims(tVCDDumpType dt, MOD_mkTLB &backing);
};

#endif /* ifndef __mkTLB_h__ */
