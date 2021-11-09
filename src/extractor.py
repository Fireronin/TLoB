from lark import Lark, Transformer, v_args
import os

with open(os.path.join(os.path.join(os.path.dirname(__file__),"..","grammar"), "type.lark")) as f:
    lark_string = f.read()

with open(os.path.join(os.path.join(os.path.dirname(__file__),"..","grammar","tests"), "Polyfifo2.json")) as f:
    example_text = f.read()

parser = Lark(lark_string, parser="earley")

parsed = parser.parse(example_text)

class Type:
    def __init__(self,fields,name="name") -> None:
        if type(fields) == Type:
            self.fields = fields.fields
            self.name = fields.name
            return
        if len(fields) == 1 and type(fields[0])==str:
            self.fields = fields[0]
            self.name = name
            return

        self.name = name
        self.fields = fields


    def __repr__(self) -> str:
        return f"Type({self.name},{self.fields})"

class Module:
    def __init__(self,package,name,interface,arguments,position) -> None:
        self.package = package
        self.name = name
        self.interface = interface
        self.arguments = arguments
        self.position = position

class Position:
    def __init__(self,file,line,column) -> None:
        self.file = file
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"{self.file}:{self.line}:{self.column}"

    def __repr__(self) -> str:
        return f"{self.file}:{self.line}:{self.column}"

class Interface:
    def __init__(self,name,type_def,members,position) -> None:
        self.name = name
        self.type_def = type_def
        self.is_poly = False
        if type(members) == tuple:
            self.members = members[0]
            self.is_poly = True
        else:
            self.memers = members
        self.position = position
    

class Method:
    def __init__(self,kind,name,input_types,port_names):
        self.kind = kind
        self.name = name
        self.input_types = input_types
        self.port_names = port_names

    def __repr__(self) -> str:
        return f"Method({self.kind},{self.name},{self.input_types},{self.port_names})"

class ModuleTransformer(Transformer):
    def tcl_module(self,args):
        return Module(package=args[0],name=args[1],interface=args[2],arguments=args[3],position=args[4])

    def tcl_position(self, args):
        return Position(args[0],args[1],args[2])

    def tcl_path(self, args):
        return os.path.join(*args)+".bsv"

    def tp_parametric(self, args):
        print(args)
        return Type(fields=args[1:],name=args[0])

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

    def tcl_interface_dec(self, args):
        return Interface(name=args[0],type_def=args[1],members=args[2],position=args[3])

    def list_of(self,args):
        return args

    def type_def_type(self, args):
        return Type(name="type_def",fields=args)

    def tcl_polymorphic(self, args):
        return (args[0],"polyTAG")
    
    def tcl_method(self, args):
        return Method(kind=args[0],name=args[1],input_types=args[2],port_names=args[3])



parser = Lark(lark_string, parser="lalr",transformer=ModuleTransformer())
parsed = parser.parse(example_text)
