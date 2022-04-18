package AddressFlit;

import Routable :: *;

typedef struct {
  Bit#(d) data;
  Bit#(o) dest;
} AFlit#(numeric type d, numeric type o) deriving (Bits);
instance FShow#(AFlit#(a,b));
  function fshow(x) =
    $format("[data = %b, dest = %b]", x.data, x.dest);
endinstance
instance Has_routingField #(AFlit#(i,o), Bit#(o));
  function routingField (x) = x.dest;
endinstance
instance Has_isLast #(AFlit#(i,o));
  function isLast = constFn(True);
endinstance
instance Bits#(AFlit#(d,o),d);
  function pack = constFn(d);
  function unPack = constFn(d.data);
endinstance

endpackage