#!/usr/bin/env python

import argparse
import pathlib


def is_float(s):
    if s == 'inf' or s == 'INF':
        return False
    try:
        float(s)
    except ValueError:
        return False
    return True


def is_same_word(s1, s2):
    s1 = s1.rstrip('\r\n')
    s2 = s2.rstrip('\r\n')
    if is_float(s1) and is_float(s2):
        e, a = float(s1), float(s2)
        if e == 0:
            return a == 0
        else:
            return abs(e - a) < 1e-6 or abs(a / e - 1) < 1e-6
    return s1 == s2


def is_same_recursive(checker, delim):
    def wrapper(line1, line2):
        s1_list = line1.rstrip('\r\n').split(delim)
        s2_list = line2.rstrip('\r\n').split(delim)

        return len(s1_list) == len(s2_list) and \
            all(checker(s1, s2) for s1, s2 in zip(s1_list, s2_list))

    return wrapper


def read_file(path):
    with path.open() as f:
        s = '\n'.join(f.readlines())
    return s


def diff(path1, path2):
    s1 = read_file(path1)
    s2 = read_file(path2)
    is_same_line = is_same_recursive(is_same_word, ' ')
    is_same_lines = is_same_recursive(is_same_line, '\n')
    return is_same_lines(s1, s2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='diff')
    parser.add_argument('file1', type=str, nargs=1, help='Path to FILE')
    parser.add_argument('file2', type=str, nargs=1, help='Path to FILE')
    args = parser.parse_args()

    path1 = pathlib.Path(args.file1[0])
    path2 = pathlib.Path(args.file2[0])

    if diff(path1, path2):
        print('Correct')
    else:
        print('Incorrect')
