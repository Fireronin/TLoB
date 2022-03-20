from ast import arguments
from dataclasses import dataclass
import enum
from turtle import position
from typing import Dict, List, Tuple, Union
from lark import Lark, Transformer, v_args
import os

from sympy import EX, arg



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



class Type:
    position: Position

    def __init__(self,name,package=None,position=None,fields=None) -> None:
        self.name = name
        self.package = package
        self.fields = fields
        self.position = position
        self.primary = False
        self.width = None

    def __eq__(self, other) -> bool:
        if self.name != other.name:
            return False
        if self.package != other.package:
            return False
        if self.fields != other.fields:
            return False
        return True

    def __str__(self) -> str:
        return f"{self.package}::{self.name}"
    
    def __repr__(self) -> str:
        return f"{self.package}::{self.name} ({','.join([str(f) for f in  self.fields])})"

    @property
    def full_name(self) -> str:
        return f"{self.package}::{self.name}"

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



class Type_ide:
    name: str

    def __init__(self,name,package=None,formals=None,is_polymorphic=False,is_primary=False,used_name=None) -> None:
        self.name = name
        self.used_name = used_name
        self.package = package
        self.formals = formals
        self.is_polymorphic = is_polymorphic
        self.is_primary = is_primary

    def __getitem__(self,key):
        for i in range(len(self.formals)):
            if self.formals[i].name == key:
                return self.fields[i]

    def __str__(self) -> str:
        return f"{self.package}::{self.name}"
    
    def __repr__(self) -> str:
        return self.__str__()

    @property
    def full_name(self) -> str:
        return f"{self.package}::{self.name}"


class Value:
    is_string: bool

    def __init__(self,value) -> None:
        self.value = value        
        if type(value) == str:
            self.is_string = True

    def __str__(self) -> str:
        return f"{self.value}"
    
    def __repr__(self) -> str:
        return f"{self.value}"

class Enum(Type):
    def __init__(self,type_ide,members,width=None,position=None) -> None:
        super().__init__(type_ide.name,type_ide.package,position)
        self.primary = True
        self.members = members
        self.width = width
        self.type_ide = type_ide

    def __str__(self) -> str:
        return f"{self.type_ide}"
    
    def __repr__(self) -> str:
        return f"{self.type_ide}"

    @property
    def full_name(self) -> str:
        return f"{self.type_ide}"

class Struct(Type):
    is_tagged_union = False
    is_polymorphic: bool
    type_ide: Type_ide
    members: Dict[str,Type]
    position: Position


    def __init__(self,type_ide: Type_ide,members,position=None,is_polymorphic=False,width=None,widths={},is_tagged_union=False) -> None:
        super().__init__(type_ide.name,type_ide.package,position)
        self.type_ide = type_ide
        self.members = members
        self.is_polymorphic = is_polymorphic
        self.widths = widths
        self.width = width 
        self.is_tagged_union = is_tagged_union
    
    def __str__(self) -> str:
        return f"{self.type_ide}"
    
    def __repr__(self) -> str:
        return f"{self.type_ide}"

    @property
    def full_name(self) -> str:
        return f"{self.type_ide}"



#list or vector
class GetItemTypes(Type):
    type_ide: Type_ide

    def __init__(self,type_ide: Type_ide,elem,length =None) -> None:
        super().__init__(type_ide.name,type_ide.package)
        self.type_ide = type_ide
        self.elem = elem
        self.length = length
    
    def __str__(self) -> str:
        return f"{self.type_ide}"

    def __repr__(self) -> str:
        return f"{self.type_ide}"

    @property
    def full_name(self) -> str:
        return f"{self.type_ide}"


class Alias:
    type_ide: Type_ide
    type: Type
    position: Position

    def __init__(self,type_ide:Type_ide,type,position:Position) -> None:
        self.name = type_ide
        self.type_ide = type_ide
        self.type = type
        self.position = position

    def __str__(self) -> str:
        return f"{self.name.__str__()}"

    def __repr__(self) -> str:
        return f"alias {self.name} {self.type}"
    
    @property
    def full_name(self) -> str:
        return self.__str__()

class Type_formal:
    is_module: bool = False

    def __init__(self,name,type_tag=False,numeric_tag=False) -> None:
        self.name = name
        self.type_tag = type_tag
        self.numeric_tag = numeric_tag
    
    def __str__(self) -> str:
        return f"""{self.name}"""

    def __repr__(self) -> str:
        return self.__str__()

class Module(Type):
    type_ide: Type_ide

    def __init__(self,name,interface,package=None,position=None,arguments=[],provisos=[]) -> None:
        Type.__init__(self,name=name,package=package,position=position)
        self.interface = interface
        self.arguments = arguments
        self.provisos = provisos
        self.type_ide = interface
    
    def __str__(self) -> str:
        return super().__str__() +f""" {self.interface}"""
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def full_name(self) -> str:
        return f"{self.package}::{self.name}"

class Function(Type):
    type_ide: Type_ide #result
    arguments: Dict[str,Type]

    def __init__(self,name,package=None,arguments={},result=None,provisos=[],position=None,argument_names=None) -> None:
        Type.__init__(self,name=name,package=package,position=position)
        self.arguments = arguments
        self.result = result
        self.type_ide = result
        self.provisos = provisos
    
    def __str__(self) -> str:
        return f"{self.type_ide} ({','.join([str(aa) for aa in self.arguments.values()])})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def full_name(self) -> str:
        return f"{self.package}::{self.name}"

class Proviso(Type):
    type_ide: Type_ide

    def __init__(self,type_ide: Type_ide,position=None) -> None:
        Type.__init__(self,type_ide.name,type_ide.package,position)
        self.type_ide = type_ide

    def __str__(self) -> str:
        return f"{self.type_ide}"
    
    def __repr__(self) -> str:
        return f"{self.type_ide}"
    
    @property
    def full_name(self) -> str:
        return f"{self.type_ide}"

class Typeclass_instance():
    type_ide: Type_ide

    def __init__(self,t_type,provisos=None) -> None:
        self.t_type = t_type
        self.provisos = provisos
        self.type_ide = t_type
        self.inputs = t_type.formals

    # add [] operator to allow for typeclass instances to be subscripted
    def __getitem__(self,index):
        if index == 0:
            return self.t_type
        if index == 1:
            return self.provisos
        raise IndexError(f"Typeclass instance index out of range: {index}")

    def __str__(self) -> str:
        return f"{self.inputs} {self.provisos}"

    def __repr__(self) -> str:
        return self.__str__()


class Typeclass():
    type_ide: Type_ide
    position: Position
    instances: List[Typeclass_instance]

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
        return f"{self.type_ide.package}::{self.type_ide.name}"




#endregion

#trnasforemr
class ModuleTransformer(Transformer):
    #region Typeclass workin progress

    def tcl_typeclass(self,args):
        args = [x for x in args if x is not None]
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

    def tcl_tc_d_dependency(self,args):
        return (args[0],args[1])

    def tcl_tc_instances(self,args):
        return ("instances",args)
    
    def tcl_tc_i_instance(self,args):
        args = [x for x in args if x is not None]
        if len(args) == 1:
            return Typeclass_instance(args[0],None)
        return Typeclass_instance(args[0], args[1])
    
    def tcl_tc_members(self,args):
        members = {}
        for arg in args:
            if type(arg)==tuple:
                members[arg[1]] = arg[2]
            else:
                members[arg] = None
        return ("members",members)
    
    def tcl_tc_m_value(self,args):
        # name value
        return ("memberValue",args[1],args[0])

    def tcl_tc_m_module(self,args):
        name = args[-1]
        provisos = None
        if len(args) == 3:
            provisos = args[1]
        module = args[0]
        module.provisos = provisos
        return ("module",name,module)

    def tcl_tc_m_function(self,args):
        name = args[-1]
        provisos = None
        if len(args) == 3:
            provisos = args[1]
        func = args[0]
        func.provisos = provisos
        return ("function",name,func)

    def tcl_provisos(self,args):
        provisos = [ Proviso(x) for x in args ]
        return ("provisos",provisos)

    def tcl_tc_m_f_function(self, args):
        try:
            arguments = {}
            for argument in args[2:]:
                if argument[0] =="TypeIdeAndName":
                    arguments[argument[2]] = argument[1]
                else:
                    arguments[argument[1].name] = argument[1]

            return Function(name=args[1],result=args[0],arguments=arguments)
        except Exception as e:
            print(e)
            return None

    def tcl_tc_m_f_module(self, args):
        arguments = {}
        for argument in args[2:]:
            if issubclass(type(argument),Type):
                arguments[argument.name] = argument
            else:
                arguments[argument[1]] = argument[0]
        return Module(name=args[0],arguments=args[1:-1],interface=args[-1])

    def tcl_tc_m_f_argument(self, args):
        args = [x for x in args if x is not None]
        if len(args) == 2:
            return ("TypeIdeAndName",args[0],args[1]) 
        return ("functionOrModule",args[0])
    #endregion
    
    #region func and module
    #new func
    
    def string_input(self,args):
        return args[0][1:-1]

    def tcl_function(self, args):
        try:
            args = [x for x in args if x is not None]
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
        except Exception as e:
            print(e)
            print(args)
            raise e

    def package_name(self,args):
        return (args[0],args[1])

    def name_only(self,args):
        return (None,args[0])

    def tcl_f_result(self,args):
        args = [x for x in args if x is not None]
        if len(args) == 2:
            args[1].package = args[0]
            return args[1]       
        return ("result",args[0])

    def tcl_f_arguments(self,args):
        arguments = {}
        for i,argument in enumerate(args):
            arguments[str(i)] = argument
        return ("arguments",arguments)

    def tcl_fa_argument(self, args):
        return args[0]

    # module

    def tcl_module(self, args):
        try:
            args = [x for x in args if x is not None]
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
        except Exception as e:
            print(e)
            print(args)
            raise e

    def tcl_m_interface(self, args):
        args = [x for x in args if x is not None]
        if len(args) == 2:
            args[1].package = args[0]
            return args[1]     
        return ("interface",args[0])

    #endregion

    #region types

    def typeprimary(self,args):
        return args[0]

    def tcl_primary(self,args):
        args = [x for x in args if x is not None]
        #TODO: check what to do
        args[0].is_primary = True
        if len(args) == 2:
            args[0].width = args[1][1]
        return args[0]

    def tcl_width(self, args):
        return ("width",args[0])

    def tcl_enum(self, args):
        try:
            args = [x for x in args if x is not None]
            width = None
            if len(args) == 4:
                width = args[2][1]
                
            position = args[-1]
            return Enum(type_ide=args[0],members=args[1],width=width,position=position)
        except Exception as e:
            print(e)
            return None
        
    def tcl_alias(self, args):
        return Alias(type_ide=args[0],type=args[1],position=args[2])

    def tcl_interface_dec(self, args):
        args = [x for x in args if x is not None]
        attributes = None
        if len(args)==4:
            attributes = args[3]
        members_set = {args[1][x][0]:args[1][x][1] for x in range(len(args[1]))}
        return Interface(type_ide=args[0],members=members_set,position=args[2],attributes=attributes)

    def tcl_im_subinterface(self, args):
        return (args[1],Interface(type_ide=args[0],members=None))

    def tcl_im_method(self,args):
        return (args[1],Interface_method(name=args[1],type=args[0],input_types=None,ports=None))

    def struct(self, args):
        type_ide = args[0]
        members = args[1][1]
        widths = args[1][2]
        if len(args) == 4:
            width = args[2]
        else:
            width = None
        position = args[-1]
        return Struct(type_ide=type_ide,members=members,width=width,position=position,widths=widths)

    def tcl_tagged_union(self, args):
        type_ide = args[0]
        members = args[1][1]
        widths = args[1][2]
        if len(args) == 4:
            width = args[2]
        else:
            width = None
        position = args[-1]
        return Struct(type_ide=type_ide,members=members,width=width,position=position,widths=widths,is_tagged_union=True)
    
    def poly_struct(self, args):
        struct = self.struct(args)
        struct.is_polymorphic = True
        return struct
    
    def tcl_stu_members(self, args):
        #dict of members
        members = {}
        widths = {}
        for x in range(len(args)):
            members[args[x][2]] = args[x][1]
            widths[args[x][2]] = args[x][3]

        return ("members_widths",members,widths)

    def tcl_stu_member(self,args):
        width = None
        if type(args[-1]) == tuple and args[-1][0] == "width":
            width = args[-1][1]
        
        return ("member",args[0],args[1],width)

    def tcl_v_elem(self, args):
        return args[0]

    def tcl_v_length(self, args):
        return args[0]

    def tcl_vector(self, args):
        return GetItemTypes(type_ide=args[0],elem = args[2],length =args[1])

    def tcl_list(self, args):
        return GetItemTypes(type_ide=args[0],elem = args[1])

    # type_def_type
    def type_ide(self, args):
        return ("type_ide",args[0])

    def type_ide_poly(self, args):
        return ("type_ide_poly",args[0])

    def type_def_type_value(self, args):
        return Value(args[0])

    def type_def_type(self, args):
        if type(args[0]) == Value:
            return args[0]
        args = [x for x in args if x is not None]
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
        return Type_ide(name=name,package=package,formals=(None if len(args)==1 else args[name_len]),is_polymorphic=poly)
        
    def type_formal(self, args):
        return Type_formal(name=args[0])

    def module_type_formal(self, args):
        args[0].is_module = True
        return args[0]

    def type_type_formal(self, args):
        return Type_formal(name=args[0],type_tag=True)

    def numeric_type_formal(self, args):
        return Type_formal(name=args[0],numeric_tag=True,type_tag=True)

    #endregion


    #utility

    def tcl_type_full(self,args):
        return args[0]

    def package_name_solo(self,args):
        return ("package",args[0])

    #region old crap

    def tcl_position(self, args):
        return Position(args[0],args[1],args[2])

    def tcl_path(self, args):
        # remove None from args, this is to avoid bugs comming from parser
        args = [x for x in args if x is not None]
        return os.path.join(*args)#+".bsv"

    def tp_parametric(self, args):
        # remove None from args, this is to avoid bugs comming from parser
        args = [x for x in args if x is not None]
        if len(args)==1 and type(args[0]) == str and (args[0][0].islower() or args[0][0] == "_" or args[0][0] == "$"):
            return args[0]
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

    def int_value(self,number):
        return int(number[0])

    def NUMBER(self, number):
        return int(number.value)

    def list_of(self,args):
        return args

    def tcl_polymorphic(self, args):
        return (args[0],"polyTAG")
    
    #endregion

parser: Lark = None
typeParser: Lark = None

def initalize_parser(start: str="start"):
    global parser
    global typeParser
    with open(os.path.join(os.path.join(os.path.dirname(__file__),"..","grammar"), "type.lark")) as f:
        lark_string = f.read()
    parser = Lark(lark_string, parser="earley",start=start)
    typeParser = Lark(lark_string, parser="earley",start="type")
    return parser

def parse_and_transform(tcl_string: Union[str,bytes]):
    if type(tcl_string) == bytes:
        tcl_string = tcl_string.decode("utf-8")
    global parser
    try:
        parsed = parser.parse(tcl_string)
    except Exception as e:
        if tcl_string == 'can\'t read "Cons": no such variable':
            raise Exception("Failed to parse: \n")
        raise Exception("Failed to parse: \n")
    result = ModuleTransformer().transform(parsed)
    return result

def evaluateType(type_string: Union[str,bytes]):
    if type(type_string) == bytes:
        type_string = type_string.decode("utf-8")
    global typeParser
    parsed = typeParser.parse(type_string)
    result = ModuleTransformer().transform(parsed)
    return result

if __name__ == "__main__":
    parser = initalize_parser(start="tcl_type_full")
    result = parse_and_transform(example_text)
    print(result)
