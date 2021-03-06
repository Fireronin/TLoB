/*
 * Generated by Bluespec Compiler, version 2021.07 (build 4cac6eb)
 * 
 * On Tue Mar  8 15:41:57 GMT 2022
 * 
 */

/* Generation options: */
#ifndef __mkSoC_Map_h__
#define __mkSoC_Map_h__

#include "bluesim_types.h"
#include "bs_module.h"
#include "bluesim_primitives.h"
#include "bs_vcd.h"


/* Class declaration for the mkSoC_Map module */
class MOD_mkSoC_Map : public Module {
 
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
 
 /* Constructor */
 public:
  MOD_mkSoC_Map(tSimStateHdl simHdl, char const *name, Module *parent);
 
 /* Symbol init methods */
 private:
  void init_symbols_0();
 
 /* Reset signal definitions */
 private:
  tUInt8 PORT_RST_N;
 
 /* Port definitions */
 public:
  tUWide PORT_m_plic_addr_range;
  tUWide PORT_m_near_mem_io_addr_range;
  tUWide PORT_m_ethernet_0_addr_range;
  tUWide PORT_m_dma_0_addr_range;
  tUWide PORT_m_uart16550_0_addr_range;
  tUWide PORT_m_uart16550_1_addr_range;
  tUWide PORT_m_iic_0_addr_range;
  tUWide PORT_m_axi_quad_spi_0_full_addr_range;
  tUWide PORT_m_axi_quad_spi_0_lite_addr_range;
  tUWide PORT_m_axi_quad_spi_1_addr_range;
  tUWide PORT_m_gpio_0_addr_range;
  tUWide PORT_m_gpio_1_addr_range;
  tUWide PORT_m_boot_rom_addr_range;
  tUWide PORT_m_ddr4_0_uncached_addr_range;
  tUWide PORT_m_ddr4_0_cached_addr_range;
  tUWide PORT_m_pcc_reset_value;
  tUWide PORT_m_ddc_reset_value;
  tUWide PORT_m_mtcc_reset_value;
  tUWide PORT_m_mepcc_reset_value;
 
 /* Publicly accessible definitions */
 public:
 
 /* Local definitions */
 private:
 
 /* Rules */
 public:
 
 /* Methods */
 public:
  tUWide METH_m_plic_addr_range();
  tUInt8 METH_RDY_m_plic_addr_range();
  tUWide METH_m_near_mem_io_addr_range();
  tUInt8 METH_RDY_m_near_mem_io_addr_range();
  tUWide METH_m_ethernet_0_addr_range();
  tUInt8 METH_RDY_m_ethernet_0_addr_range();
  tUWide METH_m_dma_0_addr_range();
  tUInt8 METH_RDY_m_dma_0_addr_range();
  tUWide METH_m_uart16550_0_addr_range();
  tUInt8 METH_RDY_m_uart16550_0_addr_range();
  tUWide METH_m_uart16550_1_addr_range();
  tUInt8 METH_RDY_m_uart16550_1_addr_range();
  tUWide METH_m_iic_0_addr_range();
  tUInt8 METH_RDY_m_iic_0_addr_range();
  tUWide METH_m_axi_quad_spi_0_full_addr_range();
  tUInt8 METH_RDY_m_axi_quad_spi_0_full_addr_range();
  tUWide METH_m_axi_quad_spi_0_lite_addr_range();
  tUInt8 METH_RDY_m_axi_quad_spi_0_lite_addr_range();
  tUWide METH_m_axi_quad_spi_1_addr_range();
  tUInt8 METH_RDY_m_axi_quad_spi_1_addr_range();
  tUWide METH_m_gpio_0_addr_range();
  tUInt8 METH_RDY_m_gpio_0_addr_range();
  tUWide METH_m_gpio_1_addr_range();
  tUInt8 METH_RDY_m_gpio_1_addr_range();
  tUWide METH_m_boot_rom_addr_range();
  tUInt8 METH_RDY_m_boot_rom_addr_range();
  tUWide METH_m_ddr4_0_uncached_addr_range();
  tUInt8 METH_RDY_m_ddr4_0_uncached_addr_range();
  tUWide METH_m_ddr4_0_cached_addr_range();
  tUInt8 METH_RDY_m_ddr4_0_cached_addr_range();
  tUInt8 METH_m_is_mem_addr(tUInt64 ARG_m_is_mem_addr_addr);
  tUInt8 METH_RDY_m_is_mem_addr();
  tUInt8 METH_m_is_IO_addr(tUInt64 ARG_m_is_IO_addr_addr);
  tUInt8 METH_RDY_m_is_IO_addr();
  tUInt8 METH_m_is_near_mem_IO_addr(tUInt64 ARG_m_is_near_mem_IO_addr_addr);
  tUInt8 METH_RDY_m_is_near_mem_IO_addr();
  tUInt64 METH_m_pc_reset_value();
  tUInt8 METH_RDY_m_pc_reset_value();
  tUWide METH_m_pcc_reset_value();
  tUInt8 METH_RDY_m_pcc_reset_value();
  tUWide METH_m_ddc_reset_value();
  tUInt8 METH_RDY_m_ddc_reset_value();
  tUWide METH_m_mtcc_reset_value();
  tUInt8 METH_RDY_m_mtcc_reset_value();
  tUWide METH_m_mepcc_reset_value();
  tUInt8 METH_RDY_m_mepcc_reset_value();
  tUInt64 METH_m_mtvec_reset_value();
  tUInt8 METH_RDY_m_mtvec_reset_value();
  tUInt64 METH_m_nmivec_reset_value();
  tUInt8 METH_RDY_m_nmivec_reset_value();
 
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
  void dump_VCD(tVCDDumpType dt, unsigned int levels, MOD_mkSoC_Map &backing);
  void vcd_defs(tVCDDumpType dt, MOD_mkSoC_Map &backing);
};

#endif /* ifndef __mkSoC_Map_h__ */
