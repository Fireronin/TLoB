/*-
 * Copyright (c) 2018-2019 Alexandre Joannou
 * All rights reserved.
 *
 * This software was developed by SRI International and the University of
 * Cambridge Computer Laboratory (Department of Computer Science and
 * Technology) under DARPA contract HR0011-18-C-0016 ("ECATS"), as part of the
 * DARPA SSITH research programme.
 *
 * @BERI_LICENSE_HEADER_START@
 *
 * Licensed to BERI Open Systems C.I.C. (BERI) under one or more contributor
 * license agreements.  See the NOTICE file distributed with this work for
 * additional information regarding copyright ownership.  BERI licenses this
 * file to you under the BERI Hardware-Software License, Version 1.0 (the
 * "License"); you may not use this file except in compliance with the
 * License.  You may obtain a copy of the License at:
 *
 *   http://www.beri-open-systems.org/legal/license-1-0.txt
 *
 * Unless required by applicable law or agreed to in writing, Work distributed
 * under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
 * CONDITIONS OF ANY KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations under the License.
 *
 * @BERI_LICENSE_HEADER_END@
 */

package ExampleAXI4;
import AXI4 :: *;

import Routable :: *;
import SourceSink :: *;
import ListExtra :: *;

import Connectable :: *;
import FIFOF :: *;
import SpecialFIFOs :: *;
import List :: *;
import Vector :: *;

typedef 2 NMASTERS;
typedef 2 NSLAVES;

typedef 4096 SlaveWidth;

typedef TLog#(NMASTERS) MID_sz;
typedef TAdd#(MID_sz, TLog#(NSLAVES)) SID_sz;
typedef TAdd#(1, TLog#(TMul#(NSLAVES, SlaveWidth))) ADDR_sz;
typedef 128 DATA_sz;
typedef   0 AWUSER_sz;
typedef   0 WUSER_sz;
typedef   0 BUSER_sz;
typedef   0 ARUSER_sz;
typedef   0 RUSER_sz;

`define PARAMS ADDR_sz, DATA_sz, AWUSER_sz, WUSER_sz, BUSER_sz, ARUSER_sz, RUSER_sz
`define MPARAMS MID_sz, `PARAMS
`define SPARAMS SID_sz, `PARAMS
`define MASTER_T AXI4_Master#(`MPARAMS)
`define SLAVE_T  AXI4_Slave#(`SPARAMS)

Integer nb_flit = 2;
Integer nb_rsp = 2;

module axiMaster#(Integer nr) (`MASTER_T);

  // AXI master shim
  AXI4_Shim#(`MPARAMS) shim <- mkAXI4Shim;
  // Req addr
  Reg#(Bit#(ADDR_sz)) nextWriteAddr <- mkReg(0);
  // book keep
  Reg#(Bool) awSent <- mkReg (False);
  Reg#(Bool) reqSent <- mkReg (False);
  Reg#(Bit#(32)) rspCnt <- mkReg (0);
  Reg#(Bit#(32)) cnt <- mkReg (0);

  // arbitrary work for each channel
  rule putAXI4_AWFlit (!awSent);
    AXI4_AWFlit#(MID_sz, ADDR_sz, AWUSER_sz) f = ?;
    f.awaddr  = nextWriteAddr;
    f.awburst = INCR;
    f.awlen   = 0;
    nextWriteAddr <= nextWriteAddr + 1;
    if (nextWriteAddr==1)
      awSent <= True;
    shim.slave.aw.put(f);
    
    
    AXI4_WFlit#(DATA_sz, WUSER_sz) wf = AXI4_WFlit{
      wdata: zeroExtend (cnt+1000*fromInteger(nr)), wstrb: -1, wlast: True, wuser: ?
    };
    shim.slave.w.put(wf);
    $display("%0t - MASTER %d - to %d - payload %d ", $time,nr,nextWriteAddr , cnt+1000*fromInteger(nr));
  endrule
  rule getAXI4_BFlit;
    let rsp <- get(shim.slave.b);
    //$display("%0t - MASTER - received ", $time, fshow(rsp));
    // reqSent <= False;
    // awSent <= False;
    if (rspCnt == fromInteger (2)) $finish(0);
    else rspCnt <= rspCnt + 1;
  endrule

  // return AXI interface
  return shim.master;

endmodule

module axiSlave#(Integer nr) (`SLAVE_T);

  // AXI slave shim
  AXI4_Shim#(`SPARAMS) shim <- mkAXI4Shim;

  // arbitrary work for each channel
  let awResp <- mkFIFOF;
  let wResp <- mkFIFOF;
  rule getAXI4_AWFlit;
    let req <- get(shim.master.aw);
    awResp.enq(AXI4_BFlit{
      bid: req.awid, bresp: OKAY, buser: ?
    });
    //$display("%0t ---- SLAVE %d - received ", $time,nr, fshow(req));
  endrule
  rule getAXI4_WFlit;
    let req <- get(shim.master.w);
    if (req.wlast) wResp.enq(True);
    let val = req.wdata*req.wdata * 1000*fromInteger(nr);
    $display("%0t - SLAVE %d - computed %d", $time,nr,val);
  endrule
  rule putAXI4_BFlit;
    awResp.deq;
    wResp.deq;
    shim.master.b.put(awResp.first);
    //$display("%0t ---- SLAVE - sending ", $time, fshow(awResp.first));
  endrule

  // return AXI interface
  return shim.slave;

endmodule

(* synthesize *)
module axiMaster1_synth  (AXI4_Master_Sig#(`MPARAMS));
  let master <- axiMaster(1);
  let axi_sig <- toAXI4_Master_Sig(master);
  return axi_sig;
endmodule

(* synthesize *)
module axiMaster2_synth  (AXI4_Master_Sig#(`MPARAMS));
  let master <- axiMaster(2);
  let axi_sig <- toAXI4_Master_Sig(master);
  return axi_sig;
endmodule

(* synthesize *)
module axiSlave5_synth  (AXI4_Slave_Sig#(`SPARAMS));
  let slave <- axiSlave(5);
  let axi_sig <- toAXI4_Slave_Sig(slave);
  return axi_sig;
endmodule

(* synthesize *)
module axiSlave7_synth  (AXI4_Slave_Sig#(`SPARAMS));
  let slave <- axiSlave(7);
  let axi_sig <- toAXI4_Slave_Sig(slave);
  return axi_sig;
endmodule

`undef PARAMS
`undef MPARAMS
`undef SPARAMS
`undef MASTER_T
`undef SLAVE_T
endpackage