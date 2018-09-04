#!/usr/bin/env python

import argparse
import os
from pathlib import Path
import shutil
from string import Template
import sys
from termcolor import colored

from scripts import diff
from scripts import download


tests_dir = download.tests_dir
workspace_dir = download.cache_dir / 'workspace'
ignore_file = ['diff.py', 'download.py', 'test.py']


rule_from_language = {
    'c': ('gcc -O2 -o exec ${name}.c'
          ' -Werror -Wextra -Wshadow -Wno-unused-result',
          './exec', 8),
    'cpp': ('g++ --std=c++14 -O2 -o exec ${name}.cpp'
            ' -Werror -Wextra -Wshadow -Wno-unused-result',
            './exec', 8),
    'cs': ('mcs -warn:0 -o+ -r:System.Numerics ${name}.cs',
           'mono ${name}.exe', 16),
    'd': ('dmd -m64 -w -O -release -inline ${name}.d', './${name}', 12),
    # 'go': ('go build -o ${name} ${name}.go', './${name}', 12),
    'go': (None, 'go run ${name}.go', 12),
    'hs': ('ghc -O2 ${name}.hs -o exec', './exec', 12),
    'java': ('javac ${name}.java', 'java -Xms512m ${name}', 16),
    'ml': ('ocamlfind ocamlopt ${name}.ml'
           ' -linkpkg -thread -package str,num,threads,batteries -o exec',
           './exec', 12),
    'py': (None, '/usr/bin/env python ${name}.py', 40),
    'rb': (None, 'ruby ${name}.rb', 40),
    'rs': ('rustc -O ${name}.rs -o exec', './exec', 8),
}


def test_single(target, redownload=False):
    suffix = target.suffix[1:]
    source = workspace_dir / target.name
    out = workspace_dir / 'out'

    if suffix not in rule_from_language:
        return

    print('>> {}'.format(target))

    # Download
    download.download_from_problem_id(source.stem, redownload)

    # Prepare
    if workspace_dir.exists() and workspace_dir.is_dir():
        shutil.rmtree(workspace_dir)

    workspace_dir.mkdir(parents=True)

    shutil.copy(src=str(target), dst=str(source))
    compile_rule, run_rule, time_duration = rule_from_language[suffix]

    # Compile
    if compile_rule is not None:
        compile_rule = Template(compile_rule).substitute(name=source.stem)
        print('Compiling ...')
        result = os.system('cd {} && {}'.format(workspace_dir, compile_rule))

        if result != 0:
            msg = colored('Compile Error', 'cyan')
            print('{}: {}'.format(target, msg))
            exit(1)

    else:
        mode = source.stat().st_mode
        source.chmod((mode & 0o777) | 0o111)

    # Test
    run_rule = Template(run_rule).substitute(name=source.stem)
    tests = tests_dir / source.stem

    for test_id in set(int(t.stem) for t in tests.iterdir()):
        testcase = (tests / str(test_id)).with_suffix('.in')
        answer = (tests / str(test_id)).with_suffix('.out')

        # Run
        result = os.system('cd {} && timeout -s 9 {} {} < {} > {}'.format(
            workspace_dir, time_duration, run_rule, testcase, out.name))

        if result in [137, 35072]:
            msg = colored('Time Limit Exceeded', 'yellow')
        elif result != 0:
            msg = colored('Runtime Error', 'magenta')
        elif not diff.diff(answer, out):
            msg = colored('Wrong Answer', 'red')
        else:
            msg = 'Correct'

        print('{}: {}'.format(testcase, msg))

        if msg != 'Correct':
            print('=== {} ==='.format(testcase))
            with testcase.open() as f:
                print('\n'.join(f.readlines()))
            print('=== Expected ===')
            with answer.open() as f:
                print('\n'.join(f.readlines()))
            print('=== Output ===')
            with out.open() as f:
                print('\n'.join(f.readlines()))
            exit(1)

    print('{}: {}'.format(target, colored('Passed', 'green')))
    print('')

    shutil.rmtree(str(workspace_dir))


def test_recursive(target, redownload=False):
    if str(target.name) in ignore_file:
        return

    if target.is_dir():
        listdir = [p for p in target.iterdir()
                   if not str(p.name).startswith('.')]
        listdir.sort()
        for x in listdir:
            test_recursive(x, redownload)
    else:
        test_single(target, redownload)


if __name__ == '__main__':
    if sys.version_info[:3] < (3, 4, 0):
        Exception('Use Python 3.4 or later')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'target', nargs='?', help='target directory', default='.')
    args = parser.parse_args()
    target = Path.cwd() / args.target

    test_recursive(target)
