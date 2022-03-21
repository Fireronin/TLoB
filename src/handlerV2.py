#%%
import pexpect
import re

child = None

def create_bluetcl():
    global child
    child = pexpect.spawn('/opt/tools/bsc/latest/bin/bluetcl',cwd='/mnt/e/Mega/Documents/CS/TLoB')
    child.setecho(True)
    child.sendline(b'namespace import ::Bluetcl::*')
    child.expect(b'% ',timeout=5)
    return child

def add_folder(folder_path="tutorial"):
    fancy_call("flags set -p "+folder_path+":+")

def load_package(package_name="Polyfifo"):
    fancy_call("bpackage load "+package_name)

def clean_response(s):
    TOREMOVE = [b"\r",b"\n",b"%"]
    for token in TOREMOVE:
        s = s.replace(token,b"")
    s = s.strip()
    return s

def fancy_call(command,only_last_line=True):
    global child
    if type(command) == str:
        command = bytes(command, encoding= "raw_unicode_escape")
    child.sendline(command)
    child.expect(re.escape(command)+b"\r\n",timeout=5)
    full_text = b""
    try:
        if only_last_line:
            s = b""
            while child.buffer != b'% ':
                s = child.readline()
                full_text += s
        else:
            child.expect(b"\r\r\n",timeout=7)
            s = child.before
            full_text += s
    except pexpect.TIMEOUT:
        print("Warrning: TIMEOUT")
        s = b""
    if full_text.find(b"Error: ")!=-1:
        raise Exception("Error:",full_text)
    return s

def list_packages():
    s = fancy_call("bpackage list")
    packages = s.split()
    # covert from bytes to str
    packages = [str(p, encoding='utf-8') for p in packages]
    return packages

def list_types(package_name="Polyfifo"):
    s = fancy_call("defs type " + package_name )
    types = s.split()
    return types

def list_funcs(package_name="Polyfifo"):
    funcs = fancy_call("defs func " + package_name )
    return funcs

def read_type(type_string=b"Polyfifo::FIFOIfc"):
    type_name = type_string.split(b"::")[-1]
    print("Currently reading type: "+str(type_name, encoding='utf-8') )
    # if type_name in [b"Bits",b"SizedLiteral"]:
    #     return b""
    try:
        constr = fancy_call(b"type constr "+type_name,only_last_line=False)
    except Exception as e:
        print("Warrning:" + str(type_name, encoding='utf-8') + "is probably a keyword")
        return b""
    try:
        #remove spaces
        constr = constr.replace(b" ",b"")
        type_full = fancy_call(b"type full "+constr,only_last_line=False)
    except Exception as e:
        print(e)
        print("Warrning: Type "+ str(type_name, encoding='utf-8') + " failed to load")
        return b""
    return type_full

def read_all_types(package_name="Polyfifo"):
    print("Reading types in package: "+package_name)
    types = list_types(package_name)
    type_strings = []
    for type_name in types:
        type_strings.append(read_type(type_name))
    return type_strings



#%%
if __name__ == "__main__":
    create_bluetcl()
    add_folder("BlueStuff/build/bdir")
    add_folder("tutorial")
    add_folder("Flute/src_SSITH_P2/build_dir")
    load_package("AXI4_Types")
    load_package("Polyfifo")
    load_package("Core_IFC")
    print(list_funcs("Core_IFC"))
    print(list_packages())
    print(list_types(package_name="Polyfifo"))
    print(list_types(package_name="Core_IFC"))
    all_types = b""
    for type_name in list_types(package_name="Polyfifo"):
        all_types += read_type(type_name)
        all_types += b"\n"

# %%
