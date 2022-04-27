#%%
import pexpect
import re


def clean_response(s):
    TOREMOVE = [b"\r",b"\n",b"%"]
    for token in TOREMOVE:
        s = s.replace(token,b"")
    s = s.strip()
    return s

class Handler():
    child = None

    def __init__(self,cwd='/mnt/e/Mega/Documents/CS/TLoB'):
        self.child = pexpect.spawn('/opt/tools/bsc/latest/bin/bluetcl',cwd=cwd)
        self.child.setecho(True)
        self.child.sendline(b'namespace import ::Bluetcl::*')
        self.child.expect(b'% ',timeout=5)

    def call(self,command,only_last_line=True):
        if type(command) == str:
            command = bytes(command, encoding= "raw_unicode_escape")
        self.child.sendline(command)
        self.child.expect(re.escape(command)+b"\r\n",timeout=5)
        full_text = b""
        try:
            if only_last_line:
                s = b""
                while self.child.buffer != b'% ':
                    s = self.child.readline()
                    full_text += s
            else:
                self.child.expect(b"\r\r\n",timeout=7)
                s = self.child.before
                full_text += s
        except pexpect.TIMEOUT:
            #decode bytes to string
            strCommand = str(command, encoding='utf-8')
            print("Warrning: TIMEOUT, whem calling "+strCommand)
            s = b""
        if full_text.find(b"Error: ")!=-1:
            raise Exception("Error:",full_text)
        return s

    def add_folder(self,folder_path="tutorial"):
        self.call("flags set -p "+folder_path+":+")

    def load_package(self,package_name="Polyfifo"):
        self.call("bpackage load "+package_name)

    def list_packages(self):
        s = self.call("bpackage list")
        packages = s.split()
        # covert from bytes to str
        packages = [str(p, encoding='utf-8') for p in packages]
        return packages

    def list_types(self,package_name="Polyfifo"):
        s = self.call("defs type " + package_name )
        types = s.split()
        return types

    def list_funcs(self,package_name="Polyfifo"):
        try:
            funcs = self.call("defs func " + package_name )
        except Exception as e:
            print("Warrning:" + package_name + " failed to load")
            return b""   
        return funcs

    def read_type(self,type_string=b"Polyfifo::FIFOIfc"):
        type_name = type_string.split(b"::")[-1]
        if type_name == "Generic":
            return ""
        #print("Currently reading type: "+str(type_name, encoding='utf-8') )
        # if type_name in [b"Bits",b"SizedLiteral"]:
        #     return b""
        try:
            constr = self.call(b"type constr "+type_name,only_last_line=False)
        except Exception as e:
            print("Warrning:" + str(type_name, encoding='utf-8') + " is probably a keyword")
            return b""
        try:
            #remove spaces
            constr = constr.replace(b" ",b"")
            type_full = self.call(b"type full "+constr,only_last_line=False)
        except Exception as e:
            print(e)
            print("Warrning: Type "+ str(type_name, encoding='utf-8') + " failed to load")
            return b""
        return type_full

    def read_all_types(self,package_name="Polyfifo"):
        #print("Reading types in package: "+package_name)
        types = self.list_types(package_name)
        type_strings = []
        for type_name in types:
            type_strings.append(self.read_type(type_name))
        return type_strings


#%%
#tests
if __name__ == "__main__":
    h = Handler()
    h.add_folder("BlueStuff/build/bdir")
    h.add_folder("tutorial")
    h.add_folder("Flute/src_SSITH_P2/build_dir")
    h.load_package("AXI4_Types")
    h.load_package("Polyfifo")
    h.load_package("Core_IFC")
    print(h.list_funcs("Core_IFC"))
    print(h.list_packages())
    print(h.list_types(package_name="Polyfifo"))
    print(h.list_types(package_name="Core_IFC"))
    all_types = b""
    for type_name in h.list_types(package_name="Polyfifo"):
        all_types += h.read_type(type_name)
        all_types += b"\n"

# %%
