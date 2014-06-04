#!/usr/bin/env python
"""
Converts markdown files written for octopress in markdown format to Restructured Text format suitable for use in nikola.
"""

import sys
import glob
from subprocess import check_output
from datetime import datetime


PANDOC_TOOL = '/usr/bin/pandoc'

def get_pandoc_output(octo_file):
    args = []
    args.append(PANDOC_TOOL)
    args.append('-f')
    args.append('markdown')
    args.append('-t')
    args.append('rst')
    args.append(octo_file)
    output = check_output(args)
    return output

def get_meta(octo_file):
    meta = {}
    old_meta = open(octo_file).read().split('---\n')[1]
    
    for m in old_meta.split('\n'):
        if 'title' in m:
            k,v = m.split(':')
            meta['title'] = v.strip()
            meta['slug'] = meta['title'].replace(' ', '-').lower()
        elif 'date' in m:
            fields = m.split('date: ')
            dt = datetime.strptime(' '.join(fields[1].split()[:-1]), '%Y-%m-%d %H:%M:%S')
            meta['date'] = dt.strftime('%m/%d/%Y %I:%M:%S %p %Z')
        elif 'categories' in m:
            k,v = m.split(':')
            v = v.strip().strip('[]')
            meta['tags'] = v
    return meta

def main():
    octo_dir = sys.argv[1]
    niko_dir = sys.argv[2]

    for octo_file in glob.glob('%s/*.markdown' % octo_dir):
        meta = get_meta(octo_file)
        rst = get_pandoc_output(octo_file)
        print meta



if __name__ == '__main__':
    main()
