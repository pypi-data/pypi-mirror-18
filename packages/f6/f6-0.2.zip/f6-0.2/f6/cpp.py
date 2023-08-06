from f6 import bunch

import re
import os
import sys
import shutil
import subprocess
import ctypes

patterns = {
    'function_signature':
    r'(?P<restype>(\w|[ \*\&])+) +(?P<func_name>\w+)\((?P<args>.*)\)',
    'variable_decl':
    r'(?P<type>(\w|[ \*\&])+) +(?P<name>\w+)',
    'pointer_type':
    r'[^\*]+\*',
}
patterns = {k: re.compile(v) for k, v in patterns.items()}

export_mark = '// export'

class SourceCode(object):

    def __init__(self, text):
        self.text = text
        self.lines = []
        self.functions = []
        self.includes = []
        self.auto_export = True

        self.parse(text)

    def parse(self, text):
        self.lines = text.split('\n')
        for i_line, line in enumerate(self.lines):
            if line == export_mark:
                self.auto_export = False
                del self.functions[:]
            if line.startswith('#'):
                self.includes.append(line)
            if not line.startswith(' '):
                m = re.match(patterns['function_signature'], line)
                if m:
                    if (self.auto_export or
                            not self.auto_export
                            and self.lines[i_line - 1] == export_mark):
                        self.add_function(m)

    def add_function(self, m):
        self.functions.append(Function(
            name=m.group('func_name'),
            ret=m.group('restype').replace('inline', '').strip(),
            args=self.parse_args(m.group('args')),
        ))

    def parse_args(self, text):
        if not text:
            return []
        args = [self.parse_arg(t.strip()) for t in text.split(',')]
        return args

    def parse_arg(self, text):
        if '=' in text:
            text = text[:text.index('=')].strip()
        m = re.match(patterns['variable_decl'], text)
        return bunch(type=m.group('type'), name=m.group('name'))

class Function(object):

    def __init__(self, name, ret, args):
        self.name = name
        self.ret = ret
        self.args = args

    def __repr__(self):
        return 'Function({} | {} -> {})'.format(
            self.name, [t.type for t in self.args], self.ret
        )

    @property
    def argtypes(self):
        return [t.type for t in self.args]

def parse(text):
    return SourceCode(text)

def load(fpath):

    def compile():
        with open(header_fpath, 'w') as f:
            stdout = sys.stdout
            sys.stdout = f
            for include in src.includes:
                print include
            print 'extern "C" {'
            for func in src.functions:
                print '{} __declspec(dllexport) {}({});'.format(
                    func.ret,
                    func.name,
                    ', '.join(func.argtypes),
                )
            print '}'
            sys.stdout = stdout
        with open(source_fpath, 'w') as f:
            f.write('#include "{}"\n'.format(header_fname))
            f.write(text)
        cmd = 'g++ -std=c++11 -shared -o "{}" "{}"'.format(
            dll_fpath, source_fpath
        )
        out = subprocess.check_output(cmd, shell=True)
        if out:
            print out
            return None

    dir = os.path.dirname(fpath)
    fname = os.path.basename(fpath)
    name, ext = os.path.splitext(fname)

    header_fname = 'tmp-' + name + '.h'
    header_fpath = os.path.join(dir, header_fname)
    source_fpath = os.path.join(dir, 'tmp-' + name + '.cc')
    dll_fname = name + '.dll'
    dll_fpath = os.path.join(dir, dll_fname)

    need_compile = True
    if os.path.exists(dll_fpath):
        if os.stat(fpath).st_mtime < os.stat(dll_fpath).st_mtime:
            need_compile = False
    text = open(fpath).read()
    src = parse(text)
    if need_compile:
        compile()
    # load dll
    dll = ctypes.cdll.LoadLibrary(dll_fpath)
    py_funcs = {}
    for func in src.functions:
        py_func = dll[func.name]
        py_func.restype = to_py_type(func.ret)
        py_func.argtypes = map(to_py_type, func.argtypes)
        py_funcs[func.name] = py_func
    return bunch(**py_funcs)

def normalize_type(type):
    type = type.replace('const', '')
    type = type.replace(' *', '*')
    return type.strip()

cpptype_to_pytype = {
    'int': ctypes.c_int,
    'unsigned': ctypes.c_uint,
    'float': ctypes.c_float,
    'double': ctypes.c_double,
    'char*': ctypes.c_char_p,
    'void': None,
}

def to_py_type(type):
    type = normalize_type(type)
    try:
        type = cpptype_to_pytype[type]
        return type
    except KeyError:
        if re.match(patterns['pointer_type'], type):
            return ctypes.c_void_p
        raise

if __name__ == '__main__':
    funcs = load(r'D:\Source\C++\t.cpp')
    for name, f in funcs.items():
        print name
        print f.restype, f.argtypes
        print
