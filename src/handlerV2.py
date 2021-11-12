#%%
import pexpect
import re
child = pexpect.spawn('bluetcl',cwd='..')
child.sendline('namespace import ::Bluetcl::*')
child.sendline('flags set -p ./tutorial:+')
child.sendline('bpackage load Polyfifo')
s = child.read_nonblocking( size=10000,timeout=1)
lines = s.split(b"\r\n")
lines = list(filter( lambda x: not x.startswith(b"%"),lines))
# %%



def create_bluetcl():
    global child
    child = pexpect.spawn('bluetcl',cwd='..')
    child.sendline('namespace import ::Bluetcl::*')
    return child

def add_folder(folder_path="./tutorial"):
    fancy_call("flags set -p "+folder_path+":+")

def load_package(package_name):
    fancy_call("bpackage load "+package_name)

def clean_response(s):
    TOREMOVE = [b"\r",b"\n",b"%"]
    for token in TOREMOVE:
        s = s.replace(token,b"")
    s = s.strip()
    return s

def fancy_call(command):
    global child
    if type(command) == str:
        command = bytes(command, encoding= "raw_unicode_escape")
    child.sendline(command)
    child.expect(re.escape(command)+b"\r\n",timeout=2)
    child.expect(b"\r\r\n%",timeout=5)
    s = child.before
    if s.find(b"Error")!=-1:
        raise Exception("Error:",s)
    #s = s.replace(command,b"")
    #s = clean_response(s)
    return s

def list_packages():
    s = fancy_call("bpackage list")
    packages = s.split()
    return packages

def list_types(package_name="Polyfifo"):
    s = fancy_call("defs type " + package_name )
    print(s)
    types = s.split()
    return types

def read_type(type_string=b"Polyfifo::FIFOIfc"):
    type_name = type_string.split(b"::")[-1]
    print(b"type constr "+type_name)
    if type_name in [b"Bits",b"SizedLiteral"]:
        return b""
    try:
        constr = fancy_call(b"type constr "+type_name)
    except Exception as e:
        print(b"Warrning:" + type_name + b"is probably a keyword")
        return b""
    #print(b"Constructor extracted: "+ constr)
    try:
        type_full = fancy_call(b"type full "+constr)
    except Exception as e:
        print(b"Warrning: Type "+ type_name + b" failed to load")
        return b""
    #print(b"Type full extracted: " + type_full)
    return type_full
#%%
print(list_packages())
print(list_types(package_name="Polyfifo"))
all_types = b""
for type_name in list_types(package_name="Polyfifo"):
    all_types += read_type(type_name)
    all_types += b"\n"

"""samve all_types to json file"""
with open("../src/types2.json","w") as f:
    f.write(all_types.decode("utf-8"))
# %%
