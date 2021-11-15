from typing import Tuple
from lark import Lark, Transformer, v_args
import os

#region lark grammar
lark_string = r"""

BITS: "bit"
INT: "int"

int: NUMBER

start: tcl_type_full_list

tcl_type_full_list: tcl_type_full*
//tcl_func_list: tcl_func*

//tcl_func: tcl_module
   // | tcl_function

type: typeprimary -> t_single
    | typeprimary "(" type ("," type)*  ")" -> t_parametric

typeprimary: (identifier_u | identifier_l)["#(" type  ("," type)* ")"] -> tp_parametric
    | "bit" "[" typenat ":" typenat "]" -> bit
    | "int" -> int
    //| identifier_l -> string_placeholder
    | typenat -> int_value

// typeide: WORD
typenat: NUMBER

identifier_l: /[a-z_$][\w$_']*/ 
identifier_u: /[A-Z][\w$_]*/ 
type_ide: identifier_u -> string_placeholder
type_ide_poly: identifier_l -> string_placeholder



interface_decl: [atribute_instances] "interface" type_def_type ";" (interface_member_decl)* "endinterface" (":" type_ide)*

type_def_type: [identifier_u":"":"] type_ide (type_formals)* 
            | type_ide_poly (type_formals)*

type_formals: "#(" type_formal ("," type_formal)* ")" -> list_of

type_formal: "numeric" "type" identifier_l -> numeric_type_formal
            | "type" identifier_l
            | identifier_l

interface_member_decl: method_proto

method_proto: [atribute_instances] "method" type identifier_l ((("(" method_proto_formals ")")*) | "()") ";"

method_proto_formals: (method_proto_formal ("," method_proto_formal)*)

method_proto_formal: [atribute_instances] type identifier_l


tcl_position: "{" "position" "{" tcl_path NUMBER NUMBER ["{" "Library" identifier_u "}"] "}" "}"
// todo check paths with spaces
tcl_path: ["%/"] /\w+/ ["/" /\w+/ ]*  "." /\w+/

tcl_type_full: tcl_interface_dec
            | tcl_typeclass
            | tcl_struct
            | tcl_enum
            | tcl_tagged_union
            | tcl_primary
            | tcl_alias
            | tcl_list
            | tcl_function
            | tcl_module

tcl_width: "{" "width" NUMBER "}"

// Typeclass grammar
tcl_typeclass: "Typeclass" "{" type_def_type "}" [tcl_tc_superclasses] ["coherent"] tcl_tc_members tcl_tc_instances tcl_position

tcl_tc_superclasses: "{" "superclasses" type_def_type* "}"

tcl_tc_instances: "{" "instances" "{" (tcl_tc_i_instance)*  "}" "}"
               |  "{" "instances" tcl_tc_i_instance "}"
               
tcl_tc_i_instance: type
                | "{" type [tcl_tc_provisos] "}"

tcl_tc_provisos: "provisos" "(" type ("," type)* ")"

tcl_tc_members: "{" "members" "{" (tcl_tc_m_value | tcl_tc_m_function)* "}" "}"

tcl_tc_m_value: "{" type_def_type identifier_l "}"

tcl_tc_m_function: "{" "{" tcl_tc_m_f_function [tcl_tc_provisos] "}" (identifier_l | /\S/ | /\S\S/ ) "}"

tcl_tc_m_f_function: "function" type identifier_l "("  tcl_tc_m_f_argument ("," tcl_tc_m_f_argument )* ")"

tcl_tc_m_f_argument: type_def_type identifier_l
                | tcl_tc_m_f_function
// Primary 
tcl_primary: "Primary" type [tcl_width]
    | "Primary" "{" type_def_type "}" "polymorphic" [tcl_width]

// Enum
tcl_enum: "Enum" identifier_u tcl_e_members [tcl_width] tcl_position
tcl_e_members: "{" "members" "{" identifier_u* "}" "}"
            | "{" "members" identifier_u "}"
// Alias
tcl_alias: "Alias" identifier_u type tcl_position
        | "Alias" "{" type_def_type "}" type tcl_position

// List this is type on it's own weird ??
tcl_list: "List" "{" type_def_type "}" "polymorphic" "{" type identifier_l "}" 
// Struct and TaggedUnion
tcl_struct: "Struct" identifier_u tcl_stu_members tcl_position
        | "Struct" "{" type_def_type "}" "polymorphic" tcl_stu_members tcl_position

tcl_tagged_union: "TaggedUnion" identifier_u tcl_stu_members [tcl_width] tcl_position
        | "TaggedUnion" "{" type_def_type "}" "polymorphic"  tcl_stu_members  [tcl_width] tcl_position

tcl_stu_members: "{" "members" "{" tcl_stu_member* "}" "}"

tcl_stu_member: "{" (type |"void") (identifier_u|identifier_l) [tcl_width] "}"

// Interface
atribute_instances: "ATRIBUTE INSTANCES TODO"

tcl_interface_dec: "Interface" "{" type_def_type "}" tcl_i_members tcl_position 
        | "Interface" "{" type_def_type "}" "polymorphic"  tcl_i_members  tcl_position
        | "Interface" type_def_type tcl_i_members tcl_position
   // | "Interface"  identifier_u ":"":" type_def_type  tcl_members tcl_position

tcl_i_members:  "{" "members" "{" ( "{" tcl_im_method "}"  )* "}" "}" -> list_of

tcl_im_method: "method" "{" type identifier_l tcl_imm_input_types tcl_imm_ports "}"

tcl_imm_input_types: (type | "{" type* "}" ) -> list_of

tcl_imm_ports: "{" "{" "(*" "ports =" "[" [tcl_immp_name ( "," tcl_immp_name )* ] "]" "*)" "}" "}" -> list_of
            | "{" "}"

tcl_immp_name: "\""  identifier_l "\"" -> string_placeholder

// Functions via defs func package_name

tcl_function: "{" "function" [identifier_u ":" ":"] tcl_f_identifier [tcl_f_result] [tcl_f_arguments] [tcl_provisos] tcl_position "}"


tcl_f_identifier: "{" identifier_l "}" ->string_placeholder
            | identifier_l ->string_placeholder
            | /\S{1,3}/ -> string_placeholder



tcl_f_result: "{" "result" [identifier_u ":"":"] type "}" -> complex_result
            | "{" "result" "{" "{" [identifier_u ":"":"] type "}" "}" "}" -> simple_result

tcl_f_arguments: "{" "arguments" tcl_fa_argument  "}"
            | "{" "arguments" "{" tcl_fa_argument* "}"  "}"

tcl_fa_argument: "{" tcl_tc_m_f_function "}" 
            | type
            | "{" type "}"

//// module
tcl_module: "{" "module" [identifier_u ":" ":"] identifier_l  tcl_m_interface [tcl_f_arguments] [tcl_provisos] tcl_position "}"

tcl_m_interface: "{" "interface" [identifier_u ":"":"] type "}"

//////// Other crap


//tcl_arguments: "{" "arguments" "{" type type* "}" "}"

//tcl_module: "{" "module" identifier_u ":" ":" identifier_l tcl_interface_use [tcl_func_arguments] [tcl_provisos] tcl_position "}"






 

tcl_provisos: "{" "provisos" "{" ("{" type "}")* "}" "}"
            | "{" "provisos" type "}"

//// flags imports
%import common.CNAME -> NAME
%import common.NUMBER
%import common.WS_INLINE
%import common.WORD

%import common.WS
%ignore WS

%ignore WS_INLINE
"""
#endregion

with open(os.path.join(os.path.join(os.path.dirname(__file__),"..","grammar"), "type.lark")) as f:
    lark_string = f.read()

with open(os.path.join(os.path.join(os.path.dirname(__file__),"..","grammar","tests"), "testFunc.json")) as f:
    example_text = f.read()

# with open(os.path.join(os.path.join(os.path.dirname(__file__),"..","grammar","tests"), "funcs.json")) as f:
#     example_text = f.read()

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

class Type:
    def __init__(self,name,package=None,position=None,fields=None) -> None:
        self.name = name
        self.package = package
        self.fields = []
        self.position = position
        self.primary = False
        self.width = None

    def __str__(self) -> str:
        return f"{self.package}.{self.name}"
    
    def __repr__(self) -> str:
        return f"{self.package}.{self.name}"

class Struct(Type):
    def __init__(self,name,members,package=None,position=None) -> None:
        super().__init__(name,package,position)
        self.members = members


class Interface(Type):
    def __init__(self,type_ide,members,position=None) -> None:
        super().__init__(type_ide.name,type_ide.package,position)
        self.type_ide = type_ide
        self.members = members

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
    def __init__(self,name,package=None,formals=None,is_polymorphic=False,is_primary=False) -> None:
        self.name = name
        self.package = package
        self.formals = formals
        self.is_polymorphic = is_polymorphic
        self.is_primary = is_primary



class Type_formal:
    def __init__(self,name,type_tag=False,numeric_tag=False) -> None:
        self.name = name
        self.type_tag = type_tag
        self.numeric_tag = numeric_tag

class Module(Type):
    def __init__(self,name,package,interface,arguments,provisos,position) -> None:
        Type.__init__(self,name=name,package=package,position=position)
        self.interface = interface
        self.arguments = arguments
        self.provisos = provisos

class Function(Type):
    def __init__(self,name,package=None,arguments=None,result=None,provisos=None,position=None) -> None:
        Type.__init__(self,name=name,package=package,position=position)
        self.arguments = arguments
        self.result = result
        self.provisos = provisos


# trnasforemr
class ModuleTransformer(Transformer):
    #region func and module
    #new func
    

    def tcl_function(self, args):
        package = None
        arguments = None
        provisos = None
        result = None
        it = 0
        if type(args[it])==tuple and args[it][0] == "package name":
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
        arguments = None
        provisos = None
        position = None
        it = 0
        if type(args[it])==tuple and  args[it][0] == "package name":
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
        return Alias(name=args[0],package=args[1],position=args[2])

    def tcl_interface_dec(self, args):
        return Interface(type_ide=args[0],members=args[1],position=args[2])


    def tcl_struct(self, args):
        return "Not Implemented"

    def tcl_tagged_union(self, args):
        return "Not Implemented"

    def tcl_typeclass(self, args):
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
            if args[0][0] == "type_ide":
                name = args[0][1]
            else:
                name = args[0][1]
                poly = True
        else:
            name_len = 2
            package = args[0]
            name = args[1][1]
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



    #region old crap
    
    # def tcl_module(self,args):
    #     return Module(package=args[0],name=args[1],interface=args[2],arguments=args[3],position=args[4])

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

    def list_of(self,args):
        return args

    def type_def_type(self, args):
        return Type(name="type_def",fields=args)

    def tcl_polymorphic(self, args):
        return (args[0],"polyTAG")
    
    #endregion


parser = Lark(lark_string, parser="earley")
parsed = parser.parse(example_text)

result = ModuleTransformer().transform(parsed)
print(result)