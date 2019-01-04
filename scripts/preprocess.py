#!/usr/bin/env python

import argparse
from datetime import datetime
from pathlib import Path


def preprocess(path):
    includes_set = set()
    result_lines = []

    def recursive(path):
        if str(path) in includes_set:
            return
        includes_set.add(str(path))

        result = []
        for line in path.open():
            line = line.rstrip()
            if line.startswith('#include') and len(line.split('"')) >= 3:
                relpath = path.parent / ''.join(line.split('"')[1:-1])
                recursive(relpath)
            elif (line.startswith('//') or
                  line.split(' ') == ['#pragma', 'once']):
                continue
            else:
                result.append(line)

        result_lines.append('')
        result_lines.append('// {}'.format(path))
        result_lines.append('')
        result_lines.extend(result)
        result_lines.append('')

    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    result_lines.append('// ===== {} ====='.format(time))
    recursive(path)
    result_lines.append('// ===== {} ====='.format(time))

    lines = []
    for line in result_lines:
        if not(line == '' and (len(lines) == 0 or lines[-1] == '')):
            lines.append(line)
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs=1, help='source')
    args = parser.parse_args()
    filepath = Path(args.filepath[0])
    result = preprocess(filepath)
    print(result)
