/*
 * Generated by Bluespec Compiler, version 2021.07 (build 4cac6eb)
 * 
 * On Tue Mar  8 15:41:57 GMT 2022
 * 
 */

/* Generation options: */
#ifndef __mkPLIC_16_2_7_h__
#define __mkPLIC_16_2_7_h__

#include "bluesim_types.h"
#include "bs_module.h"
#include "bluesim_primitives.h"
#include "bs_vcd.h"


/* Class declaration for the mkPLIC_16_2_7 module */
class MOD_mkPLIC_16_2_7 : public Module {
 
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
  MOD_ConfigReg<tUInt8> INST_m_cfg_verbosity;
  MOD_Fifo<tUInt8> INST_m_f_reset_reqs;
  MOD_Fifo<tUInt8> INST_m_f_reset_rsps;
  MOD_Reg<tUInt64> INST_m_rg_addr_base;
  MOD_Reg<tUInt64> INST_m_rg_addr_lim;
  MOD_Fifo<tUWide> INST_m_slavePortShim_arff;
  MOD_Fifo<tUWide> INST_m_slavePortShim_awff;
  MOD_Fifo<tUInt8> INST_m_slavePortShim_bff;
  MOD_Fifo<tUWide> INST_m_slavePortShim_rff;
  MOD_Fifo<tUWide> INST_m_slavePortShim_wff;
  MOD_Reg<tUInt8> INST_m_vrg_source_busy_0;
  MOD_ConfigReg<tUInt8> INST_m_vrg_source_ip_0;
  MOD_Reg<tUInt8> INST_m_vrg_source_prio_0;
  MOD_Reg<tUInt8> INST_m_vrg_target_threshold_0;
  MOD_Reg<tUInt8> INST_m_vrg_target_threshold_1;
  MOD_Reg<tUInt8> INST_m_vvrg_ie_0_0;
  MOD_Reg<tUInt8> INST_m_vvrg_ie_1_0;
 
 /* Constructor */
 public:
  MOD_mkPLIC_16_2_7(tSimStateHdl simHdl, char const *name, Module *parent);
 
 /* Symbol init methods */
 private:
  void init_symbols_0();
 
 /* Reset signal definitions */
 private:
  tUInt8 PORT_RST_N;
 
 /* Port definitions */
 public:
  tUWide PORT_axi4_slave_aw_put_val;
  tUWide PORT_axi4_slave_w_put_val;
  tUWide PORT_axi4_slave_ar_put_val;
  tUWide PORT_axi4_slave_r_peek;
 
 /* Publicly accessible definitions */
 public:
  tUInt8 DEF_m_slavePortShim_rff_i_notEmpty____d508;
  tUInt8 DEF_m_slavePortShim_bff_i_notEmpty____d507;
 
 /* Local definitions */
 private:
  tUInt8 DEF_x__h17767;
  tUInt32 DEF_v__h19255;
  tUInt32 DEF_v__h19128;
  tUInt32 DEF_v__h19022;
  tUInt32 DEF_v__h17795;
  tUInt32 DEF_v__h17547;
  tUInt32 DEF_v__h17366;
  tUInt32 DEF_v__h17272;
  tUInt32 DEF_v__h16863;
  tUInt32 DEF_v__h16561;
  tUInt32 DEF_v__h14460;
  tUInt32 DEF_v__h13789;
  tUInt32 DEF_v__h13528;
  tUInt32 DEF_v__h13191;
  tUInt32 DEF_v__h12958;
  tUInt32 DEF_v__h12730;
  tUInt32 DEF_v__h12465;
  tUInt32 DEF_v__h6980;
  tUInt32 DEF_v__h3535;
  tUInt32 DEF_v__h3068;
  tUInt32 DEF_v__h2855;
  tUInt32 DEF_v__h1651;
  tUWide DEF_m_slavePortShim_arff_first____d21;
  tUWide DEF_m_slavePortShim_awff_first____d300;
  tUWide DEF_m_slavePortShim_wff_first____d326;
  tUInt64 DEF_y__h13759;
  tUInt8 DEF__read__h1316;
  tUInt8 DEF__read__h1285;
  tUInt8 DEF_m_vvrg_ie_1_0__h8981;
  tUInt8 DEF_m_vvrg_ie_0_0__h8969;
  tUInt8 DEF_m_vrg_source_ip_0_read____d71;
  tUInt8 DEF_NOT_m_cfg_verbosity_read_EQ_0___d6;
  tUInt8 DEF_NOT_m_cfg_verbosity_read_ULE_1_7___d18;
  tUWide DEF_m_slavePortShim_arff_first__1_BITS_97_TO_93_2__ETC___d274;
 
 /* Rules */
 public:
  void RL_m_rl_reset();
  void RL_m_rl_process_rd_req();
  void RL_m_rl_process_wr_req();
 
 /* Methods */
 public:
  tUInt8 METH_v_targets_0_m_eip();
  tUInt8 METH_RDY_v_targets_0_m_eip();
  tUInt8 METH_v_targets_1_m_eip();
  tUInt8 METH_RDY_v_targets_1_m_eip();
  void METH_set_verbosity(tUInt8 ARG_set_verbosity_verbosity);
  tUInt8 METH_RDY_set_verbosity();
  void METH_show_PLIC_state();
  tUInt8 METH_RDY_show_PLIC_state();
  void METH_server_reset_request_put(tUInt8 ARG_server_reset_request_put);
  tUInt8 METH_RDY_server_reset_request_put();
  void METH_server_reset_response_get();
  tUInt8 METH_RDY_server_reset_response_get();
  void METH_set_addr_map(tUInt64 ARG_set_addr_map_addr_base, tUInt64 ARG_set_addr_map_addr_lim);
  tUInt8 METH_RDY_set_addr_map();
  tUInt8 METH_axi4_slave_aw_canPut();
  tUInt8 METH_RDY_axi4_slave_aw_canPut();
  void METH_axi4_slave_aw_put(tUWide ARG_axi4_slave_aw_put_val);
  tUInt8 METH_RDY_axi4_slave_aw_put();
  tUInt8 METH_axi4_slave_w_canPut();
  tUInt8 METH_RDY_axi4_slave_w_canPut();
  void METH_axi4_slave_w_put(tUWide ARG_axi4_slave_w_put_val);
  tUInt8 METH_RDY_axi4_slave_w_put();
  tUInt8 METH_axi4_slave_b_canPeek();
  tUInt8 METH_RDY_axi4_slave_b_canPeek();
  tUInt8 METH_axi4_slave_b_peek();
  tUInt8 METH_RDY_axi4_slave_b_peek();
  void METH_axi4_slave_b_drop();
  tUInt8 METH_RDY_axi4_slave_b_drop();
  tUInt8 METH_axi4_slave_ar_canPut();
  tUInt8 METH_RDY_axi4_slave_ar_canPut();
  void METH_axi4_slave_ar_put(tUWide ARG_axi4_slave_ar_put_val);
  tUInt8 METH_RDY_axi4_slave_ar_put();
  tUInt8 METH_axi4_slave_r_canPeek();
  tUInt8 METH_RDY_axi4_slave_r_canPeek();
  tUWide METH_axi4_slave_r_peek();
  tUInt8 METH_RDY_axi4_slave_r_peek();
  void METH_axi4_slave_r_drop();
  tUInt8 METH_RDY_axi4_slave_r_drop();
 
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
  void dump_VCD(tVCDDumpType dt, unsigned int levels, MOD_mkPLIC_16_2_7 &backing);
  void vcd_defs(tVCDDumpType dt, MOD_mkPLIC_16_2_7 &backing);
  void vcd_prims(tVCDDumpType dt, MOD_mkPLIC_16_2_7 &backing);
};

#endif /* ifndef __mkPLIC_16_2_7_h__ */
