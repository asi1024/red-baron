#!/usr/bin/env python

import argparse
from pathlib import Path
import shutil
import sys
from termcolor import colored
import time

from scripts import diff
from scripts import download
from scripts import language


tests_dir = download.tests_dir
workspace_dir = download.cache_dir / 'workspace'
ignore_file = ['diff.py', 'download.py', 'test.py']


def print_lines(lines, max_lines):
    count = 0
    for line in lines:
        if count >= max_lines:
            print('...')
            return
        print(line)
        count += 1


def test_single(target, redownload, max_lines):
    suffix = target.suffix[1:]
    source = workspace_dir / target.name
    out = workspace_dir / 'out'

    if suffix not in language.rule_from_language:
        return

    print('>> {}'.format(target))

    # Download
    problem_id = source.stem.split('.')[0]
    download.download_from_problem_id(problem_id, redownload)

    # Prepare
    if workspace_dir.exists() and workspace_dir.is_dir():
        shutil.rmtree(workspace_dir)

    workspace_dir.mkdir(parents=True)

    shutil.copy(src=str(target), dst=str(source))
    rule = language.rule_from_language[suffix]

    # Compile
    if rule.compile(source) != 0:
        msg = colored('Compile Error', 'cyan')
        print('{}: {}'.format(target, msg))
        exit(1)

    # Test
    tests = tests_dir / source.stem
    max_time = 0

    for test_id in set(int(t.stem) for t in tests.iterdir()):
        testcase = (tests / str(test_id)).with_suffix('.in')
        answer = (tests / str(test_id)).with_suffix('.out')

        # Run
        start_time = time.time()
        result = rule.execute(source, testcase, out)
        time_duration = int((time.time() - start_time) * 1000)
        max_time = max(max_time, time_duration)

        if result in [137, 35072]:
            msg = colored('Time Limit Exceeded', 'yellow')
        elif result != 0:
            msg = colored('Runtime Error', 'magenta')
        elif not diff.diff(answer, out):
            msg = colored('Wrong Answer', 'red')
        else:
            msg = 'Correct'

        print('{}: {} ({} ms)'.format(testcase, msg, time_duration))

        if msg != 'Correct':
            print('=== {} ==='.format(testcase))
            with testcase.open() as f:
                print_lines(f.readlines(), max_lines)
            print('=== Expected ===')
            with answer.open() as f:
                print_lines(f.readlines(), max_lines)
            print('=== Output ===')
            with out.open() as f:
                print_lines(f.readlines(), max_lines)
            exit(1)

    result_msg = 'Passed ({} ms)'.format(max_time)
    print('{}: {}'.format(target, colored(result_msg, 'green')))
    print('')

    shutil.rmtree(str(workspace_dir))


def test_recursive(target, redownload, max_lines):
    if str(target.name) in ignore_file:
        return

    if target.is_dir():
        listdir = [p for p in target.iterdir()
                   if not str(p.name).startswith('.')]
        listdir.sort()
        for x in listdir:
            test_recursive(x, redownload, max_lines)
    else:
        test_single(target, redownload, max_lines)


if __name__ == '__main__':
    if sys.version_info[:3] < (3, 4, 0):
        Exception('Use Python 3.4 or later')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'target', nargs='?', help='target directory', default='.')
    parser.add_argument(
        '--redownload', help='Redownload testcase', action='store_true')
    parser.add_argument(
        '--lines', '-n', nargs='?', help='Output first N lines', default=10)
    args = parser.parse_args()
    target = Path.cwd() / args.target
    redownload = args.redownload
    max_lines = int(args.lines)

    test_recursive(target, redownload, max_lines)
