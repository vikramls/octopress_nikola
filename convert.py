#!/usr/bin/env python
"""
Converts markdown files written for octopress in markdown format to Restructured Text format suitable for use in nikola.
"""

import os
import sys
import glob
import re
from subprocess import check_output
from datetime import datetime


PANDOC_TOOL = '/usr/bin/pandoc' # Tested with 1.12.2.1

def get_rst(octo_file):
    args = []
    args.append(PANDOC_TOOL)
    args.append('-f')
    args.append('markdown')
    args.append('-t')
    args.append('rst')
    args.append(octo_file)
    output = check_output(args)
    return output.split('\n')

def cleanup_rst(rst):
    """Remove octopress extensions to markdown. 
    Matches: {% img /path/to/image %}
    """
    lines = []
    for line in rst:
#        m = re.match(r'.*?\{\%\s+img\s+([a-zA-Z0-9\\_\/.]+)\s+(.*?)\%\}', line)
#        if m:
#        img_path = m.group(1).replace('\\', '')
        lines.append(re.sub(r'.*?\{\%\s+img\s+([a-zA-Z0-9\\_\/.]+)\s+(.*?)\%\}', r'\n.. figure:: \1\n:alt: \2\n', line))
            
    return lines

def get_meta(octo_file):
    meta = {}
    octo_meta = open(octo_file).read().split('---\n')[1]
    
    for m in octo_meta.split('\n'):
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

def get_rst_file(octo_file):
    """Converts octopress file name (YYYY-MM-DD-slug.markdown) into the rst file (slug.rst)
    """
    d, l = os.path.split(octo_file)
    tmp = octo_file.split('.markdown')[0]
    rst_file = '-'.join(tmp.split('-')[3:])
    rst_file += '.rst'
    return os.path.join(d, rst_file)

def main():
    octo_dir = sys.argv[1]
    niko_dir = sys.argv[2]

    for octo_file in glob.glob('%s/*.markdown' % octo_dir):
        lines = []
        meta = get_meta(octo_file)
        lines.append('.. title: %s' % meta.get('title', ''))
        lines.append('.. slug: %s' % meta.get('slug', ''))
        lines.append('.. date: %s' % meta.get('date', ''))
        lines.append('.. tags: %s' % meta.get('tags', ''))
        lines.append('.. link: %s' % meta.get('link', ''))
        lines.append('.. description: %s' % meta.get('description', ''))
        lines.append('.. type: %s' % meta.get('type', 'text'))
        lines.append('')
        rst_file = get_rst_file(octo_file)
        f = open(rst_file, 'w')
        f.write('\n'.join(lines))

        rst = get_rst(octo_file)
        f.write('\n'.join(cleanup_rst(rst)))
        f.close()
        print 'INFO: Processed (%s) -- (%s)' % (octo_file, rst_file)
        
    return


if __name__ == '__main__':
    main()
