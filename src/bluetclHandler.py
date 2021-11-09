#%%
from pwn import *
import os

p = process("bluetcl",cwd="..")
# %%
p.newline =b'\n'
p.sendline(b"namespace import ::Bluetcl::*")

p.sendline(b"flags set -p ./tutorial:+ ")

# %%
p.sendline(b"bpackage load Polyfifo")
p.sendline(b"type full FIFOIfc#(8)")
p.recvline(timeout=1)
p.interactive()


# %%
