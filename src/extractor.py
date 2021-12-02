from typing import Tuple
from lark import Lark, Transformer, v_args
import os



with open(os.path.join(os.path.join(os.path.dirname(__file__),"..","grammar","tests"), "testFunc.json")) as f:
    example_text = f.read()

# with open(os.path.join(os.path.join(os.path.dirname(__file__),"..","grammar","tests"), "funcs.json")) as f:
#     example_text = f.read()

#region class definitions
class Position:
    def __init__(self,file,line,column) -> None:
        self.file = file
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"{self.file}:{self.line}:{self.column}"

    def __repr__(self) -> str:
        return f"{self.file}:{self.line}:{self.column}"

class Alias:
    def __init__(self,name,type,position) -> None:
        self.name = name
        self.type = type
        self.position = position

    def __str__(self) -> str:
        return f"alias {self.name} {self.type}"

    def __repr__(self) -> str:
        return f"alias {self.name} {self.type}"
    
    @property
    def full_name(self) -> str:
        return f"Alias {self.name}"

class Type:
    def __init__(self,name,package=None,position=None,fields=None) -> None:
        self.name = name
        self.package = package
        self.fields = fields
        self.position = position
        self.primary = False
        self.width = None

    def __str__(self) -> str:
        return f"{self.package}.{self.name}"
    
    def __repr__(self) -> str:
        return f"{self.package}.{self.name}"

    @property
    def full_name(self) -> str:
        return f"{self.package}.{self.name}"

class Struct(Type):
    def __init__(self,name,members,package=None,position=None) -> None:
        super().__init__(name,package,position)
        self.members = members

class Interface(Type):
    def __init__(self,type_ide,members,position=None,attributes=None) -> None:
        super().__init__(type_ide.name,type_ide.package,position)
        self.type_ide = type_ide
        self.members = members
        self.attributes = attributes

    def __str__(self) -> str:
        return f"{self.type_ide}"
    
    def __repr__(self) -> str:
        return f"{self.type_ide}"

    @property
    def full_name(self) -> str:
        return f"{self.type_ide}"

class Interface_method:
    def __init__(self,name,type,input_types,ports) -> None:
        self.name = name
        self.type = type
        self.input_types = input_types
        self.ports = ports

class Enum(Type):
    def __init__(self,name,members,width=None,package=None,position=None) -> None:
        super().__init__(name,package,position)
        self.primary = True
        self.members = members
        self.width = width

class Type_ide:
    def __init__(self,name,package=None,formals=None,is_polymorphic=False,is_primary=False,used_name=None) -> None:
        self.name = name
        self.used_name = used_name
        self.package = package
        self.formals = formals
        self.is_polymorphic = is_polymorphic
        self.is_primary = is_primary

    def __str__(self) -> str:
        return f"{self.package}.{self.name}"# #({', '.join(self.formals)})"
    
    def __repr__(self) -> str:
        return self.__str__()

class Type_formal:
    def __init__(self,name,type_tag=False,numeric_tag=False) -> None:
        self.name = name
        self.type_tag = type_tag
        self.numeric_tag = numeric_tag
    
    def __str__(self) -> str:
        return f"""{"type" if self.type_tag else ""}
        {"numeric" if self.numeric_tag else ""} {self.name}"""

    def __repr__(self) -> str:
        return self.__string__()

class Module(Type):
    def __init__(self,name,package,interface,position,arguments=[],provisos=[]) -> None:
        Type.__init__(self,name=name,package=package,position=position)
        self.interface = interface
        self.arguments = arguments
        self.provisos = provisos
    
    def __str__(self) -> str:
        return super().__str__() +f""" {self.interface}"""
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def full_name(self) -> str:
        return f"{self.package}.{self.name}"

class Function(Type):
    def __init__(self,name,package=None,arguments=[],result=None,provisos=[],position=None,argument_names=None) -> None:
        Type.__init__(self,name=name,package=package,position=position)
        self.arguments = arguments
        self.result = result
        self.provisos = provisos
    
    def __str__(self) -> str:
        return super().__str__() + f""" ({"" if self.arguments is None else ", ".join(str(x) for x in self.arguments)}) out: {self.result}"""
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def full_name(self) -> str:
        return f"{self.package}.{self.name}"

class Typeclass():
    def __init__(self,type_ide,position=None,members=None,superclasses=None,dependencies=None,instances=None) -> None:
        self.type_ide = type_ide
        self.position = position
        self.members = members
        self.superclasses = superclasses
        self.dependencies = dependencies
        self.instances = instances
    
    def __str__(self) -> str:
        return f"{self.type_ide}"

    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def full_name(self) -> str:
        return f"{self.type_ide.package}.{self.type_ide.name}"



#endregion

#trnasforemr
class ModuleTransformer(Transformer):
    #region Typeclass workin progress

    def tcl_typeclass(self,args):
        type_ide = args[0]
        # find in args ("supercalsses",x)
        superclasses = None
        for i,arg in enumerate(args):
            if type(arg)==tuple and isinstance(arg[0],str) and arg[0] == "superclasses":
                superclasses = args[i][1]
                break
        # find in args ("dependencies",x)
        dependencies = None
        for i,arg in enumerate(args):
            if type(arg)==tuple and isinstance(arg[0],str) and arg[0] == "dependencies":
                dependencies = args[i][1]
                break
        # find in args ("members",x)
        members = None
        for i,arg in enumerate(args):
            if type(arg)==tuple and isinstance(arg[0],str) and arg[0] == "members":
                members = args[i][1]
                break
        # find in args ("instances",x)
        instances = None
        for i,arg in enumerate(args):
            if type(arg)==tuple and isinstance(arg[0],str) and arg[0] == "instances":
                instances = args[i][1]
                break
        return Typeclass(type_ide,members=members,superclasses=superclasses,dependencies=dependencies,instances=instances,position=args[-1])

    
    def tcl_tc_superclasses(self,args):
        return ("superclasses",args)

    def tcl_tc_dependencies(self,args):
        return ("dependencies",args)

    def tcl_tc_dependency(self,args):
        return (args[0],args[1])

    def tcl_tc_instances(self,args):
        return ("instances",args)
    
    def tcl_tc_i_instance(self,args):
        if len(args) == 1:
            return (args[0],None)
        return (args[0], args[1])
    
    def tcl_tc_members(self,args):
        return ("members",args)
    
    def tcl_tc_m_value(self,args):
        args[0].used_name = args[1]
        return ("value",args[0])

    def tcl_tc_m_function(self,args):
        if len(args) == 2:
            return ("function",args[0],args[1],None)
        return ("function",args[0],args[2],args[1])

    def tcl_tc_provisos(self,args):
        return ("provisos",args)

    def tcl_tc_m_f_function(self, args):
        return Function(name=args[1],result=args[0],arguments=args[2:])

    def tcl_tc_m_f_argument(self, args):
        if len(args) == 2:
            return ("argument",args[0],args[1]) 
        return ("function",args[0])
    #endregion
    
    #region func and module
    #new func
    

    def tcl_function(self, args):
        package = None
        arguments = []
        provisos = []
        result = None
        it = 0
        if type(args[it])==tuple and args[it][0] == "package":
            package = args[it][1]
            it+=1
        function_name = args[it]
        it+=1
        if type(args[it])==tuple and args[it][0] == "result":
            result = args[it][1]
            it+=1
        if type(args[it])==tuple and args[it][0] == "arguments":
            arguments = args[it][1]
            it+=1
        if type(args[it])==tuple and args[it][0] == "provisos":
            provisos = args[it][1]
            it+=1
        return Function(name=function_name,package=package,arguments=arguments,result=result,provisos=provisos,position=args[it])


    def package_name(self,args):
        return (args[0],args[1])

    def name_only(self,args):
        return (None,args[0])

    def tcl_f_result(self,args):
        if len(args) == 2:
            args[1].package = args[0]
            return args[1]       
        return ("result",args[0])

    def tcl_f_arguments(self,args):
        return ("arguments",args)

    def tcl_fa_argument(self, args):
        return args[0]

    # module

    def tcl_module(self, args):
        package = None
        interface = None
        arguments = []
        provisos = []
        position = None
        it = 0
        if type(args[it])==tuple and  args[it][0] == "package":
            package = args[it][1]
            it+=1
        module_name = args[it]
        it+=1
        interface = args[it][1]
        it+=1
        if type(args[it])==tuple and args[it][0] == "arguments":
            arguments = args[it][1]
            it+=1
        if type(args[it])==tuple and args[it][0] == "provisos":
            provisos = args[it][1]
            it+=1
        position = args[it]
        return Module(name=module_name,package=package,interface=interface,arguments=arguments,provisos=provisos,position=position)
    
    def tcl_m_interface(self, args):
        if len(args) == 2:
            args[1].package = args[0]
            return args[1]     
        return ("interface",args[0])

    #endregion

    #region types

    def tcl_primary(self,args):
        #TODO: check what to do
        args[0].is_primary = True
        if len(args) == 2:
            args[0].width = args[1][1]
        return args[0]

    def tcl_width(self, args):
        return ("width",args[0])

    def tcl_list(self, args):
        return ("list",args)

    def tcl_enum(self, args):
        if len(args) == 4:
            width = args[2][1]
            position = args[3]
        else:
            width = None
            position = args[2]
        return Enum(name=args[0],members=args[1],width=width,position=position)
        
    def tcl_alias(self, args):
        return Alias(name=args[0],type=args[1],position=args[2])

    def tcl_interface_dec(self, args):
        attributes = None
        if len(args)==4:
            attributes = args[3]
        return Interface(type_ide=args[0],members=args[1],position=args[2],attributes=attributes)


    def struct(self, args):
        return "Not Implemented"

    def tcl_tagged_union(self, args):
        return "Not Implemented"
    
    def poly_struct(self, args):
        return "Not Implemented"

    # type_def_type
    def type_ide(self, args):
        return ("type_ide",args[0])

    def type_ide_poly(self, args):
        return ("type_ide_poly",args[0])

    def type_def_type(self, args):
        poly = False
        package = None
        args_len = len(args)
        name_len = 1
        if type(args[0]) == tuple:
            if args[0][0] == "type_ide_poly":
                name = args[0][1]
                poly = True
            else:
                name = args[0][1]
                package = args[0][0]
        return Type_ide(name=name,package=package,formals=args[name_len:],is_polymorphic=poly)
        
    def type_formal(self, args):
        return Type_formal(name=args[0])

    def type_type_formal(self, args):
        return Type_formal(name=args[0],type_tag=True)

    def numeric_type_formal(self, args):
        return Type_formal(name=args[0],numeric_tag=True,type_tag=True)

    #endregion



    #utility

    def tcl_provisos(self,args):
        return ("provisos",args)

    def tcl_type_full(self,args):
        return args[0]

    def package_name_solo(self,args):
        return ("package",args[0])

    #region old crap
    
    # def tcl_module(self,args):
    #     return Module(package=args[0],name=args[1],interface=args[2],arguments=args[3],position=args[4])

    def tcl_position(self, args):
        return Position(args[0],args[1],args[2])

    def tcl_path(self, args):
        return os.path.join(*args)+".bsv"

    def tp_parametric(self, args):
        ct = 0
        package = None
        if type(args[0]) == tuple:
            package = args[0][1]
            ct = 1
        name = args[ct]
        return Type(fields=args[ct+1:],name=name,package=package)

    def t_single(self, args):
        return args[0]

    def tcl_arguments(self, args):
        return args

    def tcl_interface_use(self, args):
        return Type(name="Interface",fields=args[1])

    def identifier_u(self, name):
        return name[0].value
    
    def identifier_l(self, name):
        return name[0].value
    
    def string_placeholder(self, name):
        return name[0]

    def NUMBER(self, number):
        return int(number[0])

    def numeric_type_formal(self, args):
        return Type(name="numeric",fields=args)

    def type_formal(self, args):
        return Type(name="type_formal",fields=args)

    def list_of(self,args):
        return args

    # def type_def_type(self, args):
    #     return Type(name="type_def",fields=args)

    def tcl_polymorphic(self, args):
        return (args[0],"polyTAG")
    
    #endregion

parser = None

def initalize_parser(start="start"):
    global parser
    with open(os.path.join(os.path.join(os.path.dirname(__file__),"..","grammar"), "type.lark")) as f:
        lark_string = f.read()
    parser = Lark(lark_string, parser="earley",start=start)
    return parser

def parse_and_transform(tcl_string):
    if type(tcl_string) == bytes:
        tcl_string = tcl_string.decode("utf-8")
    global parser
    parsed = parser.parse(tcl_string)
    result = ModuleTransformer().transform(parsed)
    return result

if __name__ == "__main__":
    parser = initalize_parser(start="tcl_type_full")
    result = parse_and_transform(example_text)
    print(result)
