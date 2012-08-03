#!/usr/bin/env python

import sys, os
import subprocess
import urllib

def main():
    if len(sys.argv) != 3:
        print "\nUsage: %s (alchemy|starter|zodb) [NAME]\nInitialize your Pyramid project\n" % sys.argv[0]
        return 1
    scaffold = sys.argv[1]
    name = sys.argv[2]
    major_version = '.'.join([str(x) for x in sys.version_info[:2]])
    if major_version not in ['2.6', '2.7']:
        print "Need Python 2.6 or 2.7"
        return 1
    dirname = os.path.dirname(__file__)
    script = '''
%(python)s virtualenv.py virtualenv
./virtualenv/bin/python bootstrap.py -c base.cfg
./bin/buildout -vvv -c base.cfg install pyramid
./bin/pcreate -s %(scaffold)s %(name)s
rm -rf bin/ develop-eggs/ parts/ virtualenv/
echo -e "[buildout]\\nextends = base.cfg\\nappname = %(name)s" > buildout.cfg 
git add buildout.cfg %(name)s
    ''' % {'name': name, 'scaffold': scaffold, 'python': sys.executable}

    for line in script.split('\n'):
        if not line.strip():
            continue
        print '+', line
        if os.system(line):
            print "+ Aborted"
            return 1


if __name__ == '__main__':
    main()
