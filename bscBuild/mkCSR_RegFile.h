/*
 * Generated by Bluespec Compiler, version 2021.07 (build 4cac6eb)
 * 
 * On Fri Mar 25 15:59:20 CET 2022
 * 
 */

/* Generation options: */
#ifndef __mkCSR_RegFile_h__
#define __mkCSR_RegFile_h__

#include "bluesim_types.h"
#include "bs_module.h"
#include "bluesim_primitives.h"
#include "bs_vcd.h"
#include "mkCSR_MIE.h"
#include "mkCSR_MIP.h"
#include "mkPerfCountersFlute.h"
#include "mkSoC_Map.h"


/* Class declaration for the mkCSR_RegFile module */
class MOD_mkCSR_RegFile : public Module {
 
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
  MOD_ConfigReg<tUInt8> INST_cfg_verbosity;
  MOD_mkCSR_MIE INST_csr_mie;
  MOD_mkCSR_MIP INST_csr_mip;
  MOD_Reg<tUInt64> INST_csr_mstatus_rg_mstatus;
  MOD_Fifo<tUInt8> INST_f_reset_rsps;
  MOD_mkPerfCountersFlute INST_perf_counters;
  MOD_Wire<tUInt8> INST_pw_minstret_incr;
  MOD_Reg<tUInt8> INST_rg_ctr_inhib_ir_cy;
  MOD_Reg<tUInt32> INST_rg_dcsr;
  MOD_Reg<tUWide> INST_rg_dpcc;
  MOD_Reg<tUInt64> INST_rg_dscratch0;
  MOD_Reg<tUInt64> INST_rg_dscratch1;
  MOD_Reg<tUInt8> INST_rg_fflags;
  MOD_Reg<tUInt8> INST_rg_frm;
  MOD_Reg<tUInt8> INST_rg_mcause;
  MOD_Reg<tUInt32> INST_rg_mccsr;
  MOD_Reg<tUInt32> INST_rg_mcounteren;
  MOD_Reg<tUInt64> INST_rg_mcycle;
  MOD_Reg<tUInt32> INST_rg_medeleg;
  MOD_Reg<tUWide> INST_rg_mepcc;
  MOD_Reg<tUInt32> INST_rg_mideleg;
  MOD_Reg<tUInt64> INST_rg_minstret;
  MOD_Reg<tUInt64> INST_rg_mscratch;
  MOD_Reg<tUWide> INST_rg_mscratchc;
  MOD_Reg<tUWide> INST_rg_mtcc;
  MOD_Reg<tUWide> INST_rg_mtdc;
  MOD_Reg<tUInt64> INST_rg_mtime;
  MOD_Reg<tUInt64> INST_rg_mtval;
  MOD_Reg<tUInt8> INST_rg_nmi;
  MOD_Reg<tUInt64> INST_rg_nmi_vector;
  MOD_Reg<tUInt64> INST_rg_satp;
  MOD_Reg<tUInt8> INST_rg_scause;
  MOD_Reg<tUInt32> INST_rg_sccsr;
  MOD_Reg<tUWide> INST_rg_sepcc;
  MOD_Reg<tUInt64> INST_rg_sscratch;
  MOD_Reg<tUWide> INST_rg_sscratchc;
  MOD_Reg<tUInt8> INST_rg_state;
  MOD_Reg<tUWide> INST_rg_stcc;
  MOD_Reg<tUWide> INST_rg_stdc;
  MOD_Reg<tUInt64> INST_rg_stval;
  MOD_Reg<tUInt64> INST_rg_tdata1;
  MOD_Reg<tUInt64> INST_rg_tdata2;
  MOD_Reg<tUInt64> INST_rg_tdata3;
  MOD_Reg<tUInt64> INST_rg_tselect;
  MOD_Wire<tUInt64> INST_rw_mcycle;
  MOD_Wire<tUInt64> INST_rw_minstret;
  MOD_mkSoC_Map INST_soc_map;
  MOD_Wire<tUInt8> INST_w_ctr_inhib_ir_cy;
 
 /* Constructor */
 public:
  MOD_mkCSR_RegFile(tSimStateHdl simHdl, char const *name, Module *parent);
 
 /* Symbol init methods */
 private:
  void init_symbols_0();
 
 /* Reset signal definitions */
 private:
  tUInt8 PORT_RST_N;
 
 /* Port definitions */
 public:
  tUInt8 PORT_EN_mav_csr_write;
  tUWide PORT_mav_scr_write_cap;
  tUWide PORT_csr_trap_actions_pcc;
  tUWide PORT_send_performance_events_evts;
  tUWide PORT_write_dpcc_pcc;
  tUWide PORT_read_csr;
  tUWide PORT_read_csr_port2;
  tUWide PORT_read_scr;
  tUWide PORT_mav_read_csr;
  tUWide PORT_mav_csr_write;
  tUWide PORT_mav_scr_write;
  tUWide PORT_csr_trap_actions;
  tUWide PORT_csr_ret_actions;
  tUWide PORT_read_dpcc;
  tUInt8 PORT_RDY_send_performance_events;
 
 /* Publicly accessible definitions */
 public:
  tUInt8 DEF_WILL_FIRE_mav_csr_write;
  tUInt8 DEF_rg_state___d1;
  tUInt8 DEF_rg_ctr_inhib_ir_cy__h5940;
  tUInt8 DEF_rg_ctr_inhib_ir_cy_BIT_1___h5942;
 
 /* Local definitions */
 private:
  tUWide DEF_rg_dpcc___d402;
  tUWide DEF_rg_mepcc___d355;
  tUWide DEF_rg_mscratchc___d654;
  tUWide DEF_rg_mtdc___d653;
  tUWide DEF_rg_mtcc___d325;
  tUWide DEF_rg_sepcc___d283;
  tUWide DEF_rg_sscratchc___d652;
  tUWide DEF_rg_stdc___d651;
  tUWide DEF_rg_stcc___d255;
  tUWide DEF_soc_map_m_mepcc_reset_value____d4;
  tUWide DEF_soc_map_m_mtcc_reset_value____d3;
  tUWide DEF_soc_map_m_pcc_reset_value____d5;
  tUInt64 DEF_mstatus__h38080;
  tUInt64 DEF_rg_dscratch1___d418;
  tUInt64 DEF_rg_dscratch0___d417;
  tUInt64 DEF_rg_tdata3___d395;
  tUInt64 DEF_rg_tdata2___d394;
  tUInt64 DEF_rg_tdata1___d393;
  tUInt64 DEF_rg_tselect___d392;
  tUInt64 DEF_rg_minstret___d47;
  tUInt64 DEF_rg_mtime___d36;
  tUInt64 DEF_rg_mcycle___d33;
  tUInt64 DEF_tval__h32618;
  tUInt64 DEF_rg_mscratch___d354;
  tUInt64 DEF_mip__h55943;
  tUInt64 DEF_csr_mip_mv_sip_read____d312;
  tUInt64 DEF_mie__h55944;
  tUInt64 DEF_csr_mie_mv_sie_read____d254;
  tUInt64 DEF_tval__h32038;
  tUInt64 DEF_rg_sscratch___d282;
  tUInt64 DEF__1__read__h7526;
  tUInt64 DEF__1__read__h7529;
  tUInt64 DEF__1__read__h7532;
  tUInt64 DEF__1__read__h7535;
  tUInt64 DEF__1__read__h7538;
  tUInt64 DEF__1__read__h7541;
  tUInt64 DEF__1__read__h7544;
  tUInt64 DEF__1__read__h7547;
  tUInt64 DEF__1__read__h7550;
  tUInt64 DEF__1__read__h7553;
  tUInt64 DEF__1__read__h7556;
  tUInt64 DEF__1__read__h7559;
  tUInt64 DEF__1__read__h7562;
  tUInt64 DEF__1__read__h7565;
  tUInt64 DEF__1__read__h7568;
  tUInt64 DEF__1__read__h7571;
  tUInt64 DEF__1__read__h7574;
  tUInt64 DEF__1__read__h7577;
  tUInt64 DEF__1__read__h7580;
  tUInt64 DEF__1__read__h7583;
  tUInt64 DEF__1__read__h7586;
  tUInt64 DEF__1__read__h7589;
  tUInt64 DEF__1__read__h7592;
  tUInt64 DEF__1__read__h7595;
  tUInt64 DEF__1__read__h7598;
  tUInt64 DEF__1__read__h7601;
  tUInt64 DEF__1__read__h7604;
  tUInt64 DEF__1__read__h7607;
  tUInt64 DEF__1__read__h7610;
  tUInt64 DEF_rg_satp___d316;
  tUInt32 DEF_rg_dcsr__h56340;
  tUInt32 DEF_x__h12865;
  tUInt32 DEF_medeleg__h33308;
  tUInt32 DEF_ctr_inhibit_hpm__h5802;
  tUInt32 DEF_mideleg__h33309;
  tUInt8 DEF_rg_mcause___d379;
  tUInt8 DEF_rg_scause___d307;
  tUInt8 DEF__1__read__h8759;
  tUInt8 DEF__1__read__h8762;
  tUInt8 DEF__1__read__h8765;
  tUInt8 DEF__1__read__h8768;
  tUInt8 DEF__1__read__h8771;
  tUInt8 DEF__1__read__h8774;
  tUInt8 DEF__1__read__h8777;
  tUInt8 DEF__1__read__h8780;
  tUInt8 DEF__1__read__h8783;
  tUInt8 DEF__1__read__h8786;
  tUInt8 DEF__1__read__h8789;
  tUInt8 DEF__1__read__h8792;
  tUInt8 DEF__1__read__h8795;
  tUInt8 DEF__1__read__h8798;
  tUInt8 DEF__1__read__h8801;
  tUInt8 DEF__1__read__h8804;
  tUInt8 DEF__1__read__h8807;
  tUInt8 DEF__1__read__h8810;
  tUInt8 DEF__1__read__h8813;
  tUInt8 DEF__1__read__h8816;
  tUInt8 DEF__1__read__h8819;
  tUInt8 DEF__1__read__h8822;
  tUInt8 DEF__1__read__h8825;
  tUInt8 DEF__1__read__h8828;
  tUInt8 DEF__1__read__h8831;
  tUInt8 DEF__1__read__h8834;
  tUInt8 DEF__1__read__h8837;
  tUInt8 DEF__1__read__h8840;
  tUInt8 DEF__1__read__h8843;
  tUInt8 DEF__read__h473;
  tUInt8 DEF_x__h34721;
  tUInt8 DEF__read__h498;
  tUInt8 DEF_rg_nmi__h10118;
  tUWide DEF_csr_trap_actions_pcc_BITS_160_TO_10___d2005;
  tUWide DEF_rg_dpcc_02_BITS_81_TO_10___d1227;
  tUWide DEF_rg_mepcc_55_BITS_71_TO_0___d1141;
  tUWide DEF_rg_mtcc_25_BITS_71_TO_0___d1091;
  tUWide DEF_rg_sepcc_83_BITS_71_TO_0___d1017;
  tUWide DEF_rg_stcc_55_BITS_71_TO_0___d969;
  tUWide DEF_mav_scr_write_cap_BITS_71_TO_0___d1496;
  tUInt64 DEF_x__h10275;
  tUInt64 DEF__read_address__h9921;
  tUInt64 DEF__read_address__h9693;
  tUInt64 DEF__read_address__h9365;
  tUInt64 DEF__read_address__h9163;
  tUWide DEF_ret__h29292;
  tUInt64 DEF_x__h34816;
  tUInt64 DEF_SEXT__0b0_CONCAT_rg_mtcc_25_BITS_85_TO_72_26_2_ETC___d348;
  tUInt64 DEF_x__h34822;
  tUInt64 DEF_SEXT__0b0_CONCAT_rg_stcc_55_BITS_85_TO_72_56_5_ETC___d278;
  tUInt32 DEF__read_otype__h9926;
  tUInt32 DEF__read_otype__h9370;
  tUInt32 DEF__read_capFat_addrBits__h10175;
  tUInt32 DEF__read_capFat_bounds_baseBits__h10219;
  tUInt32 DEF__read_addrBits__h9922;
  tUInt32 DEF__read_bounds_baseBits__h9954;
  tUInt32 DEF__read_addrBits__h9694;
  tUInt32 DEF__read_bounds_baseBits__h9726;
  tUInt32 DEF__read_addrBits__h9366;
  tUInt32 DEF__read_bounds_baseBits__h9398;
  tUInt32 DEF__read_addrBits__h9164;
  tUInt32 DEF__read_bounds_baseBits__h9196;
  tUInt8 DEF_rg_dpcc_02_BITS_43_TO_38___d410;
  tUInt8 DEF_rg_mepcc_55_BITS_33_TO_28___d372;
  tUInt8 DEF_rg_mtcc_25_BITS_33_TO_28___d342;
  tUInt8 DEF_rg_sepcc_83_BITS_33_TO_28___d300;
  tUInt8 DEF_rg_stcc_55_BITS_33_TO_28___d272;
  tUInt8 DEF_csr_mstatus_rg_mstatus_39_BITS_22_TO_17___d868;
  tUInt8 DEF__read_exc_code__h9510;
  tUInt8 DEF__read_exc_code__h10066;
  tUInt8 DEF_ab__h9938;
  tUInt8 DEF_bb__h9937;
  tUInt8 DEF_ab__h9710;
  tUInt8 DEF_bb__h9709;
  tUInt8 DEF_ab__h9382;
  tUInt8 DEF_bb__h9381;
  tUInt8 DEF_ab__h9180;
  tUInt8 DEF_bb__h9179;
  tUInt8 DEF_rg_dcsr_BITS_2_TO_0___h12919;
  tUInt8 DEF_mpp__h31147;
  tUInt8 DEF_csr_mstatus_rg_mstatus_BITS_1_TO_0___h9075;
  tUInt8 DEF_rg_mepcc_55_BIT_150___d1125;
  tUInt8 DEF_rg_mtcc_25_BIT_150___d1075;
  tUInt8 DEF_rg_sepcc_83_BIT_150___d1001;
  tUInt8 DEF_rg_stcc_55_BIT_150___d953;
  tUInt8 DEF_SEXT__0b0_CONCAT_rg_mtcc_25_BITS_85_TO_72_26_2_ETC___d350;
  tUInt8 DEF_SEXT__0b0_CONCAT_rg_stcc_55_BITS_85_TO_72_56_5_ETC___d280;
  tUInt8 DEF_csr_mstatus_rg_mstatus_BIT_20___h53550;
  tUInt8 DEF_spp__h31145;
  tUInt8 DEF_csr_mstatus_rg_mstatus_BIT_0___h55849;
  tUInt8 DEF__read_interrupt__h9509;
  tUInt8 DEF__read_interrupt__h10065;
  tUInt8 DEF_rg_ctr_inhib_ir_cy_BIT_0___h5829;
  tUWide DEF_IF_read_scr_scr_addr_EQ_12_36_THEN_rg_stcc_55__ETC___d661;
  tUWide DEF_IF_IF_csr_trap_actions_nmi_THEN_0b11_ELSE_IF_c_ETC___d2229;
  tUWide DEF_IF_IF_csr_trap_actions_nmi_THEN_0b11_ELSE_IF_c_ETC___d2230;
  tUWide DEF_IF_mav_scr_write_scr_addr_EQ_13_499_OR_mav_scr_ETC___d1703;
  tUWide DEF_IF_IF_mav_scr_write_cap_BITS_33_TO_28_424_EQ_0_ETC___d1644;
  tUWide DEF_IF_mav_scr_write_scr_addr_EQ_29_523_OR_mav_scr_ETC___d1701;
  tUWide DEF_IF_csr_ret_actions_from_priv_EQ_0b11_234_THEN__ETC___d2316;
  tUWide DEF_csr_mstatus_rg_mstatus_39_AND_INV_1_SL_0_CONCA_ETC___d2312;
  tUWide DEF__0b0_CONCAT_csr_mstatus_rg_mstatus_39_AND_INV_1_ETC___d2315;
  tUWide DEF_IF_mav_scr_write_cap_BITS_33_TO_28_424_ULT_51__ETC___d1583;
  tUWide DEF_result__h29878;
  tUWide DEF_IF_mav_scr_write_cap_BITS_33_TO_28_424_ULT_52__ETC___d1588;
  tUWide DEF_length__h29937;
  tUInt64 DEF__0_CONCAT_rg_fflags_34___d235;
  tUInt64 DEF__0_CONCAT_rg_frm_36___d237;
  tUInt64 DEF__0_CONCAT_rg_frm_36_CONCAT_rg_fflags_34___d238;
  tUInt64 DEF_csr_mstatus_rg_mstatus_39_BIT_63_40_CONCAT_0_C_ETC___d252;
  tUInt64 DEF_SEXT__0b0_CONCAT_rg_stcc_55_BITS_85_TO_72_56_5_ETC___d281;
  tUInt64 DEF_SEXT__0b0_CONCAT_rg_sepcc_83_BITS_85_TO_72_84__ETC___d306;
  tUInt64 DEF_rg_scause_07_BIT_6_08_CONCAT_0_CONCAT_rg_scaus_ETC___d310;
  tUInt64 DEF__0_CONCAT_rg_sccsr_13_CONCAT_3_14___d315;
  tUInt64 DEF__0_CONCAT_rg_medeleg_17___d318;
  tUInt64 DEF__0_CONCAT_rg_mideleg_19___d320;
  tUInt64 DEF_SEXT__0b0_CONCAT_rg_mtcc_25_BITS_85_TO_72_26_2_ETC___d351;
  tUInt64 DEF__0_CONCAT_rg_mcounteren_52___d353;
  tUInt64 DEF_SEXT__0b0_CONCAT_rg_mepcc_55_BITS_85_TO_72_56__ETC___d378;
  tUInt64 DEF_rg_mcause_79_BIT_6_80_CONCAT_0_CONCAT_rg_mcaus_ETC___d382;
  tUInt64 DEF__0_CONCAT_rg_mccsr_85_CONCAT_3_86___d387;
  tUInt64 DEF__0_CONCAT_perf_counters_read_ctr_inhibit__read__ETC___d391;
  tUInt64 DEF__0_CONCAT_rg_dcsr_96_BITS_31_TO_4_97_CONCAT_rg__ETC___d401;
  tUInt64 DEF_SEXT__0b0_CONCAT_rg_dpcc_02_BITS_95_TO_82_03_0_ETC___d416;
  tUInt32 DEF_x__h16859;
  tUInt32 DEF_x__h20156;
  tUInt8 DEF_IF_csr_mstatus_rg_mstatus_39_BITS_12_TO_11_69__ETC___d871;
  tUInt8 DEF_IF_rg_mepcc_55_BITS_13_TO_11_58_ULT_rg_mepcc_5_ETC___d367;
  tUInt8 DEF_IF_rg_sepcc_83_BITS_13_TO_11_86_ULT_rg_sepcc_8_ETC___d295;
  tUInt8 DEF_rg_sepcc_83_BITS_85_TO_83_89_ULT_rg_sepcc_83_B_ETC___d290;
  tUInt8 DEF_rg_mepcc_55_BITS_85_TO_83_61_ULT_rg_mepcc_55_B_ETC___d362;
  tUInt8 DEF_rg_mepcc_55_BITS_13_TO_11_58_ULT_rg_mepcc_55_B_ETC___d360;
  tUInt8 DEF_rg_mtcc_25_BITS_13_TO_11_28_ULT_rg_mtcc_25_BIT_ETC___d330;
  tUInt8 DEF_rg_mtcc_25_BITS_85_TO_83_31_ULT_rg_mtcc_25_BIT_ETC___d332;
  tUInt8 DEF_rg_sepcc_83_BITS_13_TO_11_86_ULT_rg_sepcc_83_B_ETC___d288;
  tUInt8 DEF_rg_stcc_55_BITS_13_TO_11_58_ULT_rg_stcc_55_BIT_ETC___d260;
  tUInt8 DEF_rg_stcc_55_BITS_85_TO_83_61_ULT_rg_stcc_55_BIT_ETC___d262;
  tUInt8 DEF_NOT_csr_mstatus_rg_mstatus_39_BIT_20_430___d2431;
  tUInt8 DEF_NOT_rg_sepcc_83_BITS_85_TO_83_89_ULT_rg_sepcc__ETC___d292;
  tUInt8 DEF_NOT_rg_mepcc_55_BITS_85_TO_83_61_ULT_rg_mepcc__ETC___d364;
  tUInt8 DEF_NOT_cfg_verbosity_read__346_ULE_1_347___d1348;
  tUWide DEF_SEXT_IF_mav_scr_write_cap_BITS_27_TO_25_556_UL_ETC___d1563;
  tUInt64 DEF_x__h10935;
  tUInt32 DEF_offset__h10921;
  tUInt32 DEF_base__h10920;
  tUInt64 DEF_x__h9906;
  tUInt32 DEF_offset__h9892;
  tUInt32 DEF_x__h21190;
  tUInt64 DEF_x__h9678;
  tUInt32 DEF_offset__h9664;
  tUInt64 DEF_x__h9350;
  tUInt32 DEF_offset__h9336;
  tUInt32 DEF_x__h17821;
  tUInt64 DEF_x__h9148;
  tUInt32 DEF_offset__h9134;
  tUInt8 DEF_repBound__h9383;
  tUInt8 DEF_repBound__h9939;
  tUInt8 DEF_repBound__h9711;
  tUInt8 DEF_repBound__h9181;
  tUInt64 DEF_y__h10276;
  tUInt64 DEF_x__h10277;
  tUInt64 DEF_y__h10031;
  tUInt64 DEF_x__h10032;
  tUInt64 DEF_y__h9803;
  tUInt64 DEF_x__h9804;
  tUInt64 DEF_y__h9475;
  tUInt64 DEF_x__h9476;
  tUInt64 DEF_y__h9273;
  tUInt64 DEF_x__h9274;
  tUWide DEF__0_CONCAT_IF_mav_scr_write_cap_BITS_27_TO_25_55_ETC___d1586;
  tUWide DEF_addTop__h29290;
  tUInt64 DEF_x__h10933;
  tUInt64 DEF_x__h9904;
  tUInt64 DEF_x__h9676;
  tUInt64 DEF_x__h9348;
  tUInt64 DEF_x__h9146;
  tUInt64 DEF_addrLSB__h10922;
  tUInt64 DEF_addrLSB__h9893;
  tUInt64 DEF_addrLSB__h9665;
  tUInt64 DEF_addrLSB__h9337;
  tUInt64 DEF_addrLSB__h9135;
  tUWide DEF__0b0_CONCAT_mav_scr_write_cap_BITS_149_TO_100_4_ETC___d1555;
  tUWide DEF_soc_map_m_pcc_reset_value_CONCAT_soc_map_m_pcc_ETC___d24;
  tUWide DEF_mav_csr_write_word_BITS_63_TO_14_24_XOR_SEXT_m_ETC___d1247;
  tUWide DEF_rg_dpcc_02_BITS_159_TO_110_213_AND_11258999068_ETC___d1228;
  tUWide DEF_IF_csr_ret_actions_from_priv_EQ_0b11_234_THEN__ETC___d2291;
  tUWide DEF_IF_csr_ret_actions_from_priv_EQ_0b11_234_THEN__ETC___d2290;
  tUWide DEF_IF_mav_scr_write_scr_addr_EQ_13_499_THEN_mav_s_ETC___d1705;
  tUWide DEF_IF_mav_scr_write_scr_addr_EQ_13_499_THEN_mav_s_ETC___d1704;
  tUWide DEF_IF_mav_scr_write_cap_BITS_33_TO_28_424_EQ_0_42_ETC___d1646;
  tUWide DEF_IF_IF_mav_scr_write_cap_BITS_33_TO_28_424_EQ_0_ETC___d1645;
  tUWide DEF_SEXT__0b0_CONCAT_mav_scr_write_cap_BITS_85_TO__ETC___d1519;
  tUWide DEF_IF_mav_scr_write_cap_BITS_33_TO_28_424_EQ_52_4_ETC___d1518;
  tUWide DEF_SEXT__0b0_CONCAT_mav_scr_write_cap_BITS_85_TO__ETC___d1498;
  tUWide DEF_IF_mav_scr_write_cap_BITS_33_TO_28_424_EQ_52_4_ETC___d1497;
  tUWide DEF_mav_csr_write_word_BITS_63_TO_14_24_XOR_SEXT_m_ETC___d1143;
  tUWide DEF_IF_rg_mepcc_55_BITS_33_TO_28_72_EQ_52_134_THEN_ETC___d1142;
  tUWide DEF_mav_csr_write_word_BITS_63_TO_14_24_XOR_SEXT_m_ETC___d1093;
  tUWide DEF_IF_rg_mtcc_25_BITS_33_TO_28_42_EQ_52_084_THEN__ETC___d1092;
  tUWide DEF_mav_csr_write_word_BITS_63_TO_14_24_XOR_SEXT_m_ETC___d971;
  tUWide DEF_IF_rg_stcc_55_BITS_33_TO_28_72_EQ_52_62_THEN_0_ETC___d970;
  tUWide DEF_mav_csr_write_word_BITS_63_TO_14_24_XOR_SEXT_m_ETC___d1019;
  tUWide DEF_IF_rg_sepcc_83_BITS_33_TO_28_00_EQ_52_010_THEN_ETC___d1018;
  tUWide DEF_IF_csr_trap_actions_nmi_THEN_DONTCARE_ELSE_IF__ETC___d2231;
  tUWide DEF_NOT_csr_trap_actions_nmi_010_AND_csr_trap_acti_ETC___d2233;
  tUInt32 DEF_x__h10847;
  tUInt32 DEF_x__h10875;
  tUInt32 DEF_dcsr__h10614;
  tUInt32 DEF_x__h10096;
  tUInt32 DEF_IF_csr_mstatus_rg_mstatus_39_BITS_12_TO_11_69__ETC___d875;
 
 /* Rules */
 public:
  void RL_rl_reset_start();
  void RL_rl_mcycle_incr();
  void RL_rl_mtime_incr();
  void RL_rl_upd_minstret_csrrx();
  void RL_rl_upd_minstret_incr();
  void RL_rl_upd_ctr_inhib_csrrx();
 
 /* Methods */
 public:
  tUInt32 METH_read_misa();
  tUInt8 METH_RDY_read_misa();
  tUInt8 METH_access_permitted_scr(tUInt8 ARG_access_permitted_scr_priv,
				   tUInt8 ARG_access_permitted_scr_scr_addr,
				   tUInt8 ARG_access_permitted_scr_read_not_write);
  tUInt8 METH_RDY_access_permitted_scr();
  void METH_server_reset_request_put(tUInt8 ARG_server_reset_request_put);
  tUInt8 METH_RDY_server_reset_request_put();
  void METH_server_reset_response_get();
  tUInt8 METH_RDY_server_reset_response_get();
  tUWide METH_read_csr(tUInt32 ARG_read_csr_csr_addr);
  tUInt8 METH_RDY_read_csr();
  tUWide METH_read_csr_port2(tUInt32 ARG_read_csr_port2_csr_addr);
  tUInt8 METH_RDY_read_csr_port2();
  tUWide METH_read_scr(tUInt8 ARG_read_scr_scr_addr);
  tUInt8 METH_RDY_read_scr();
  tUWide METH_mav_read_csr(tUInt32 ARG_mav_read_csr_csr_addr);
  tUInt8 METH_RDY_mav_read_csr();
  tUWide METH_mav_csr_write(tUInt32 ARG_mav_csr_write_csr_addr, tUInt64 ARG_mav_csr_write_word);
  tUInt8 METH_RDY_mav_csr_write();
  tUWide METH_mav_scr_write(tUInt8 ARG_mav_scr_write_scr_addr, tUWide ARG_mav_scr_write_cap);
  tUInt8 METH_RDY_mav_scr_write();
  tUInt8 METH_read_frm();
  tUInt8 METH_RDY_read_frm();
  tUInt8 METH_read_fflags();
  tUInt8 METH_RDY_read_fflags();
  tUInt8 METH_mv_update_fcsr_fflags(tUInt8 ARG_mv_update_fcsr_fflags_flags);
  tUInt8 METH_RDY_mv_update_fcsr_fflags();
  void METH_ma_update_fcsr_fflags(tUInt8 ARG_ma_update_fcsr_fflags_flags);
  tUInt8 METH_RDY_ma_update_fcsr_fflags();
  tUInt64 METH_mv_update_mstatus_fs(tUInt8 ARG_mv_update_mstatus_fs_fs);
  tUInt8 METH_RDY_mv_update_mstatus_fs();
  void METH_ma_update_mstatus_fs(tUInt8 ARG_ma_update_mstatus_fs_fs);
  tUInt8 METH_RDY_ma_update_mstatus_fs();
  tUInt64 METH_read_mstatus();
  tUInt8 METH_RDY_read_mstatus();
  tUInt64 METH_read_sstatus();
  tUInt8 METH_RDY_read_sstatus();
  tUInt64 METH_read_ustatus();
  tUInt8 METH_RDY_read_ustatus();
  tUInt64 METH_read_satp();
  tUInt8 METH_RDY_read_satp();
  tUWide METH_csr_trap_actions(tUInt8 ARG_csr_trap_actions_from_priv,
			       tUWide ARG_csr_trap_actions_pcc,
			       tUInt8 ARG_csr_trap_actions_nmi,
			       tUInt8 ARG_csr_trap_actions_interrupt,
			       tUInt8 ARG_csr_trap_actions_cheri_exc_code,
			       tUInt8 ARG_csr_trap_actions_cheri_exc_reg,
			       tUInt8 ARG_csr_trap_actions_exc_code,
			       tUInt64 ARG_csr_trap_actions_xtval);
  tUInt8 METH_RDY_csr_trap_actions();
  tUWide METH_csr_ret_actions(tUInt8 ARG_csr_ret_actions_from_priv);
  tUInt8 METH_RDY_csr_ret_actions();
  tUInt64 METH_read_csr_minstret();
  tUInt8 METH_RDY_read_csr_minstret();
  void METH_csr_minstret_incr();
  tUInt8 METH_RDY_csr_minstret_incr();
  tUInt64 METH_read_csr_mcycle();
  tUInt8 METH_RDY_read_csr_mcycle();
  tUInt64 METH_read_csr_mtime();
  tUInt8 METH_RDY_read_csr_mtime();
  void METH_send_performance_events(tUWide ARG_send_performance_events_evts);
  tUInt8 METH_RDY_send_performance_events();
  tUInt8 METH_access_permitted_1(tUInt8 ARG_access_permitted_1_priv,
				 tUInt32 ARG_access_permitted_1_csr_addr,
				 tUInt8 ARG_access_permitted_1_read_not_write);
  tUInt8 METH_RDY_access_permitted_1();
  tUInt8 METH_access_permitted_2(tUInt8 ARG_access_permitted_2_priv,
				 tUInt32 ARG_access_permitted_2_csr_addr,
				 tUInt8 ARG_access_permitted_2_read_not_write);
  tUInt8 METH_RDY_access_permitted_2();
  tUInt8 METH_csr_counter_read_fault(tUInt8 ARG_csr_counter_read_fault_priv,
				     tUInt32 ARG_csr_counter_read_fault_csr_addr);
  tUInt8 METH_RDY_csr_counter_read_fault();
  tUInt64 METH_csr_mip_read();
  tUInt8 METH_RDY_csr_mip_read();
  void METH_m_external_interrupt_req(tUInt8 ARG_m_external_interrupt_req_set_not_clear);
  tUInt8 METH_RDY_m_external_interrupt_req();
  void METH_s_external_interrupt_req(tUInt8 ARG_s_external_interrupt_req_set_not_clear);
  tUInt8 METH_RDY_s_external_interrupt_req();
  void METH_timer_interrupt_req(tUInt8 ARG_timer_interrupt_req_set_not_clear);
  tUInt8 METH_RDY_timer_interrupt_req();
  void METH_software_interrupt_req(tUInt8 ARG_software_interrupt_req_set_not_clear);
  tUInt8 METH_RDY_software_interrupt_req();
  tUInt8 METH_interrupt_pending(tUInt8 ARG_interrupt_pending_cur_priv);
  tUInt8 METH_RDY_interrupt_pending();
  tUInt8 METH_wfi_resume();
  tUInt8 METH_RDY_wfi_resume();
  void METH_nmi_req(tUInt8 ARG_nmi_req_set_not_clear);
  tUInt8 METH_RDY_nmi_req();
  tUInt8 METH_nmi_pending();
  tUInt8 METH_RDY_nmi_pending();
  tUWide METH_read_dpcc();
  tUInt8 METH_RDY_read_dpcc();
  void METH_write_dpcc(tUWide ARG_write_dpcc_pcc);
  tUInt8 METH_RDY_write_dpcc();
  tUInt8 METH_dcsr_break_enters_debug(tUInt8 ARG_dcsr_break_enters_debug_cur_priv);
  tUInt8 METH_RDY_dcsr_break_enters_debug();
  tUInt8 METH_read_dcsr_step();
  tUInt8 METH_RDY_read_dcsr_step();
  void METH_write_dcsr_cause_priv(tUInt8 ARG_write_dcsr_cause_priv_cause,
				  tUInt8 ARG_write_dcsr_cause_priv_priv);
  tUInt8 METH_RDY_write_dcsr_cause_priv();
  void METH_debug();
  tUInt8 METH_RDY_debug();
 
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
  void dump_VCD(tVCDDumpType dt, unsigned int levels, MOD_mkCSR_RegFile &backing);
  void vcd_defs(tVCDDumpType dt, MOD_mkCSR_RegFile &backing);
  void vcd_prims(tVCDDumpType dt, MOD_mkCSR_RegFile &backing);
  void vcd_submodules(tVCDDumpType dt, unsigned int levels, MOD_mkCSR_RegFile &backing);
};

#endif /* ifndef __mkCSR_RegFile_h__ */
