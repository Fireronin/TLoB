import os
name_counter = 0
def get_name():
    global name_counter
    name_counter += 1
    return "__temp_" + str(name_counter)

class ModuleInstance():
    def __init__(self,creator_func,inteface_args=[],func_args=[],instance_name=None):
        self.creator_func = creator_func
        self.inteface_args = inteface_args
        self.func_args = func_args
        if(len(inteface_args) != len(creator_func.interface.fields)):
            raise Exception("Interface arguments do not match the interface")
        if(len(func_args) != len(creator_func.arguments)):
            raise Exception("Function arguments do not match the function")
        self.instance_name = instance_name
        if instance_name is None:
            self.instance_name = creator_func.name[:-2]+get_name()

class TopLevelModule():
    
    def __init__(self,name) -> None:
        self.modules = set()
        self.connections = set()
        self.name = name

    def add_module(self,creator_func,inteface_args=[],func_args=[],instance_name=None):
        self.modules.add(ModuleInstance(creator_func,inteface_args,func_args,instance_name))

    def add_connection(self,source,sink):
        self.connections.add((source,sink))

    def to_string(self):
        s = []
        s.append("package "+self.name + ";\n")
        packages = set()
        packages.add("Connectable")
        packages.add("GetPut")
        for m in self.modules:
            packages.add(m.creator_func.package)
        for p in packages:
            s.append("import "+p+"::*;\n")
        s.append("\n")
        s.append("module mk"+self.name+"();\n \n")
        for m in self.modules:
            if m.creator_func.interface.fields!=0:
                arguments = ""
                for i in range(len(m.inteface_args)):
                    stringified = str(m.inteface_args[i])
                    arguments += stringified
                    if i != len(m.inteface_args)-1:
                        arguments += ", "
                
            s.append("\t" + m.creator_func.interface.name + f"#({arguments})")
            s.append(" " + m.instance_name)
            s.append(" <- " + m.creator_func.name + "(")
            for i in range(len(m.func_args)):
                s.append(m.func_args[i])
                if i != len(m.func_args)-1:
                    s.append(", ")
            s.append(");\n")
        s.append("\n")
        for c in self.connections:
            s.append(f"\tmkConnection(toPut({c[0]}),toGet({c[1]}));\n")
        s.append("\n")
        s.append("endmodule\n")
        s.append("endpackage\n")
        s = "".join(s)
        return s
    
    def to_file(self,filename,folder="."):
        with open(os.path.join(folder,filename),'w') as f:
            f.write(self.to_string())


        
