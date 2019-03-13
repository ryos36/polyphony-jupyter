import io
import polyphony.version
import polyphony.compiler
import polyphony.compiler.__main__
import argparse
import polyphony.compiler.common
from polyphony.compiler.scope import Scope
from polyphony.compiler.env import env

class compile_result:
    map = {}

the_compile_result = compile_result()

def version():
    return polyphony.version.__version__

def build_result_map(compile_results):
    the_compile_result.map = {}
    scopes = Scope.get_scopes(with_class=True)
    scopes = [scope for scope in scopes
              if (scope.is_testbench() or (scope.is_module() and scope.is_instantiated()) or scope.is_function_module())]

    the_compile_result.map['scopes'] = scopes;

    with io.StringIO() as f:
        for scope in scopes:
            with io.StringIO() as f2:
                if scope not in compile_results:
                    continue
                code = compile_results[scope]
                if not code:
                    continue
                scope_name = scope.qualified_name()
                file_name = '{}.v'.format(scope_name)
                f2.write(code)
                if scope.is_testbench():
                    env.append_testbench(scope)
                else:
                    f.write('`include "./{}"\n'.format(file_name))

                the_compile_result.map[scope_name] = f2.getvalue()

            for lib in env.using_libs:
                f.write(lib)

        the_compile_result.map['__main__'] = f.getvalue()

class Usage:
    pass

#----------------------------------------------------------------
def compile(code_str, file_name='main.py'):
    #arg_parser = argparse.ArgumentParser(prog='polyphony')
    #options = arg_parser.parse_args()
    options = Usage()

    setattr(options, "debug_mode", False)
    setattr(options, "verbose_level", 0)
    setattr(options, "quiet_level", 1)
    setattr(options, "verilog_dump", False)
    setattr(options, "verilog_monitor", False)
    setattr(options, "config", False)

    polyphony.compiler.__main__.setup(file_name, options)
    plan = polyphony.compiler.__main__.compile_plan()
    polyphony.compiler.common.src_texts[file_name] = code_str
    compile_results = polyphony.compiler.__main__.compile(plan ,code_str, file_name)

    build_result_map(compile_results)

#----------------------------------------------------------------
def show_list():
    scopes = the_compile_result.map['scopes']
    for scope in scopes:
        scope_name = scope.qualified_name()
        print(scope_name)

#----------------------------------------------------------------
def show_testbench():
    scopes = the_compile_result.map['scopes']
    for scope in scopes:
        if scope.is_testbench() :
            scope_name = scope.qualified_name()
            print("############### {}.py #################".format(scope_name))
            print(the_compile_result.map[scope_name])

#----------------------------------------------------------------
def show_module():
    scopes = the_compile_result.map['scopes']
    for scope in scopes:
        if not scope.is_testbench() :
            scope_name = scope.qualified_name()
            print("############### {}.py #################".format(scope_name))
            print(the_compile_result.map[scope_name])

#----------------------------------------------------------------
def show_main():
    print("############### __main__ #################")
    print(the_compile_result.map['__main__'])
