#%%
import pexpect
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
    global child
    child.sendline('flags set -p '+folder_path+':+')
    s = child.read_nonblocking( size=10000,timeout=0.02)
    if s.find(b"Error"):
        print("Error:",s)

def load_package(package_name):
    global child
    child.sendline('bpackage load '+package_name)
    s = child.read_nonblocking( size=10000,timeout=0.02)
    if s.find(b"Error"):
        print("Error:",s)

def list_packages():
    global child
    child.sendline('bpackage list')
    s = child.read_nonblocking( size=10000,timeout=0.1)
    if s.find(b"Prelude")==-1:
        s = child.read_nonblocking( size=10000,timeout=1)
    s = s.replace(b"bpackage list\r\n",b"")
    TOREMOVE = [b"\r",b"\n",b"%"]
    for token in TOREMOVE:
        s = s.replace(token,b"")
    packages = s.split(b" ")
    print(s)
    return packages


# %%
