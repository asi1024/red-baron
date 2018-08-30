#!/usr/bin/env python

import argparse
import os
from pathlib import Path
import shutil
from string import Template
import sys
from termcolor import colored

import diff
import download


tests_dir = Path('tests')
tmp_dir = Path('tmp')
ignore_file = [
    'diff.py', 'download.py', 'test.py', str(tests_dir), str(tmp_dir)]


rule_from_language = {
    'cpp': ('g++ --std=c++14 -O2 -Werror ${source} -o ${exe}',
            '${exe}', 8),
    'py': (None, '/usr/bin/env python ${source}', 40),
}


def test_single(target):
    suffix = target.suffix[1:]
    source = tmp_dir / target.name
    out = tmp_dir / 'out'
    exe = tmp_dir / 'exec'

    if suffix not in rule_from_language:
        return

    print('>> {}'.format(target))

    # Download
    download.download_from_problem_id(source.stem)

    # Prepare
    if tmp_dir.exists() and tmp_dir.is_dir():
        shutil.rmtree(tmp_dir)

    tmp_dir.mkdir()

    shutil.copy(str(target), str(source))
    compile_rule, run_rule, time_duration = rule_from_language[suffix]
    kwargs = {'source': source, 'exe': exe, 'name': source.stem}

    # Compile
    if compile_rule is not None:
        compile_rule = Template(compile_rule).substitute(**kwargs)
        print('Compiling ...')
        os.system('{} &> /dev/null'.format(compile_rule))
    else:
        mode = source.stat().st_mode
        source.chmod((mode & 0o777) | 0o111)

    # Test
    run_rule = Template(run_rule).substitute(**kwargs)
    tests = tests_dir / source.stem

    for test_id in set(int(t.stem) for t in tests.iterdir()):
        testcase = (tests / str(test_id)).with_suffix('.in')
        answer = (tests / str(test_id)).with_suffix('.out')

        # Run
        result = os.system('timeout -s 9 {} {} < {} > {}'.format(
            time_duration, run_rule, testcase, out))

        if result == 137:
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
            exit(1)

    print('{}: {}'.format(target, colored('Passed', 'green')))
    print('')

    shutil.rmtree(str(tmp_dir))


def test_recursive(target):
    if str(target) in ignore_file:
        return

    if target.is_dir():
        listdir = [p for p in target.iterdir() if not str(p).startswith('.')]
        listdir.sort()
        for x in listdir:
            test_recursive(x)
    else:
        test_single(target)


if __name__ == '__main__':
    if sys.version_info[:3] < (3, 4, 0):
        Exception('Use Python 3.4 or later')

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'target', nargs='?', help='target directory', default='.')

    args = parser.parse_args()

    target = args.target

    test_recursive(Path(target))
