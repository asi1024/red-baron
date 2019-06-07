import os
import string


class CompileRule(object):
    def __init__(self, compile_rule, exec_rule=None, time_limits=8):
        self._compile_rule = compile_rule
        self._exec_rule = './exec' if exec_rule is None else exec_rule
        self.time_limits = time_limits

    def compile(self, source):
        workspace = source.parent
        print('Compiling ...')
        print(source)
        com = string.Template(self._compile_rule).substitute(
            source=source.name)
        print('$', com)
        result = os.system('cd {} && {}'.format(workspace, com))
        return result

    def execute(self, source, testcase, output):
        workspace = source.parent
        com = string.Template(self._exec_rule).substitute(name=source.stem)
        if testcase is None:
            result = os.system('cd {} && timeout -s 9 {} {}'.format(
                workspace, self.time_limits, com))
        else:
            result = os.system('cd {} && timeout -s 9 {} {} < {} > {}'.format(
                workspace, self.time_limits, com, testcase, output.name))
        return result


class CompileRuleP(CompileRule):
    def __init__(self, compiler, flags, time_limits=8):
        self._compile_rule = '{} -o exec ${source} {}'.format(
            compiler, flags, source='{source}')
        self._exec_rule = './exec'
        self.time_limits = time_limits


class ScriptRule(CompileRule):
    def __init__(self, exec_rule, time_limits=40):
        self._exec_rule = exec_rule
        self.time_limits = time_limits

    def compile(self, source):
        return 0


rule_from_language = {
    'c': CompileRuleP(
        os.getenv('CC', 'gcc'),
        os.getenv('CCFLAGS', '-O2 -Wall')),
    'cpp': CompileRuleP(
        os.getenv('CXX', 'g++'),
        os.getenv('CXXFLAGS', '-O2 --std=c++14 -Wall')),
    'cs': CompileRule(
        'mcs -warn:0 -o+ -r:System.Numerics ${source}',
        'mono ${name}.exe', 16),
    'd': CompileRule(
        'dmd -m64 -w -O -release -inline ${source}',
        './${name}', 12),
    'go': ScriptRule(
        'go run ${name}.go', 20),
    'hs': CompileRuleP(
        os.getenv('GHC', 'ghc'),
        os.getenv('GHCFLAGS', '-O2'), 12),
    'java': CompileRule(
        'javac ${source}',
        'java -Xms512m ${name}', 16),
    'ml': CompileRuleP(
        os.getenv('OCAMLOPT', 'ocamlfind ocamlopt'),
        os.getenv('OCAMLOPTFLAGS',
                  '-linkpkg -thread -package str,num,threads,batteries'), 12),
    'rs': CompileRuleP('rustc', '-O'),
    'py': ScriptRule('/usr/bin/env python ${name}.py'),
    'rb': ScriptRule('ruby ${name}.rb'),
}
