typedef struct {
  Bit#(d) data;
  Bit#(o) dest;
} AFlit#(numeric type d, numeric type o) deriving (Bits);
instance FShow#(AFlit#(a,b));
  function fshow(x) =
    $format("[data = %b, dest = %b]", x.data, x.dest);
endinstance
instance Has_routingField #(Flit#(i,o), Bit#(o));
  function routingField (x) = x.dest;
endinstance
instance Has_isLast #(Flit#(i,o));
  function isLast = constFn(True);
endinstance