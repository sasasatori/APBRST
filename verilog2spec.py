from __future__ import absolute_import
from __future__ import print_function
import sys
import os
from optparse import OptionParser
from collections import defaultdict

import pyverilog
from pyverilog.vparser.parser import parse

def generate_module_tree(modules, top_module):
    """
    显示完整的实例化树，包含实例名和模块类型
    
     参数:
        modules: dict[str, dict[str, str]], 模块嵌套字典
        topmodules: str, 顶层模块名
    """
    module_counter = defaultdict(int)
    
    def recurse(parent, prefix=""):
        children = modules.get(parent, {})
        for i, (inst_name, mod_name) in enumerate(children.items()):
            is_last = i == len(children)-1
            
            # 显示格式：实例名: 模块类型
            node_label = f"{inst_name}: {mod_name}"
            
            # 如果是重复模块类型，添加标记
            mod_count = module_counter[mod_name]
            if mod_count > 0:
                node_label += f" (reused)"
            module_counter[mod_name] += 1
            
            # 打印当前节点
            print(prefix + ("└── " if is_last else "├── ") + node_label)
            
            # 递归子节点
            new_prefix = prefix + ("    " if is_last else "│   ")
            recurse(mod_name, new_prefix)
    
    # 打印顶层模块
    print(f"{top_module} (top)")
    recurse(top_module)

def generate_parameter_table(parameters, default_values, functions=None):
    """
    生成参数的 Markdown 表格
    
    参数:
        parameters: list[str], 参数名称列表
        default_values: list[any], 参数默认值列表
        functions: list[str], 可选, 参数功能描述列表
    """
    # 如果 functions 为空，初始化为空字符串列表
    if functions is None:
        functions = [""] * len(parameters)
    
    # 检查输入长度是否一致
    if not (len(parameters) == len(default_values) == len(functions)):
        raise ValueError("所有输入列表的长度必须相同")
    
    # 创建表头
    header = "| Parameter | Default Value | Function |\n"
    separator = "| :-------: | :-----------: | :------: |\n"
    
    # 生成表格行
    rows = []
    for param, default, func in zip(parameters, default_values, functions):
        # 将默认值转换为字符串，处理可能的非字符串类型
        default_str = str(default)
        rows.append(f"| {param.ljust(9)} | {default_str.center(13)} | {func.ljust(8)} |")
    
    # 组合所有部分
    table = header + separator + "\n".join(rows)
    print(table)

def generate_port_table(ports, widths, directions, functions=None):
    """
    生成端口的 Markdown 表格
    
    参数:
        ports: list[str], 端口名称列表
        widths: list[int/str], 端口位宽列表
        directions: list[str], 端口方向列表(input/output)
        functions: list[str], 可选, 端口功能描述列表
    """
    # 如果 functions 为空，初始化为空字符串列表
    if functions is None:
        functions = [""] * len(ports)
    
    # 检查输入长度是否一致
    if not (len(ports) == len(widths) == len(directions) == len(functions)):
        raise ValueError("所有输入列表的长度必须相同")
    
    # 创建表头
    header = "|     Port     | Width | Direction | Function |\n"
    separator = "| :----------: | :---: | :-------: | :------: |\n"
    
    # 生成表格行
    rows = []
    for port, width, direction, func in zip(ports, widths, directions, functions):
        rows.append(f"| {port.center(11)} | {str(width).center(5)} | {direction.center(9)} | {func.center(8)} |")
    
    # 组合所有部分
    table = header + separator + "\n".join(rows)
    print(table)

def verilog2spec():
    INFO = "Verilog code parser"
    VERSION = pyverilog.__version__
    USAGE = "Usage: python example_parser.py file ..."

    def showVersion():
        print(INFO)
        print(VERSION)
        print(USAGE)
        sys.exit()

    optparser = OptionParser()
    optparser.add_option("-v", "--version", action="store_true", dest="showversion",
                         default=False, help="Show the version")
    optparser.add_option("-I", "--include", dest="include", action="append",
                         default=[], help="Include path")
    optparser.add_option("-D", dest="define", action="append",
                         default=[], help="Macro Definition")
    (options, args) = optparser.parse_args()

    filelist = args
    if options.showversion:
        showVersion()

    for f in filelist:
        if not os.path.exists(f):
            raise IOError("file not found: " + f)

    if len(filelist) == 0:
        showVersion()

    ast, directives = parse(filelist,
                            preprocess_include=options.include,
                            preprocess_define=options.define)

    Description = ast.description
    ModuleDef = Description.definitions[0]
    Modulename = ModuleDef.name
    Paramlist = ModuleDef.paramlist.params
    Portlist = ModuleDef.portlist.ports

    print("\r\n-------------------------generate module tree-------------------------\r\n")

    modules = {Modulename: {}}
    for item in ModuleDef.children():
        if item.__class__.__name__ == 'InstanceList':
            modules[Modulename][item.instances[0].name] = item.instances[0].module

    generate_module_tree(modules, Modulename)

    print("\r\n-------------------------generate param table-------------------------\r\n")

    parameters = []
    default_values = []
    for item in Paramlist:
        parameters.append(item.list[0].name)
        default_values.append(item.list[0].value.var.value)

    generate_parameter_table(parameters,default_values)

    print("\r\n-------------------------generate port table-------------------------\r\n")

    ports = []
    widths = []
    directions = []
    for item in Portlist:
        ports.append(item.first.name)
        directions.append(item.first.__class__.__name__)
        if item.first.width.__class__.__name__ == 'Width': 
            widths.append(int(item.first.width.msb.value) - int(item.first.width.lsb.value) + 1)
        else:
            widths.append(1)

    generate_port_table(ports,widths,directions)

if __name__ == '__main__':
    verilog2spec()
