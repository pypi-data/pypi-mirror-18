#!/usr/local/bin/python3

import getopt
import json
import re
import subprocess
import sys


def main(argv):
    cmd = 'pdf2txt.py -F 1 %s ' % (argv[0], )
    run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = run.communicate()
    out = out.decode('utf-8')
    pat = re.compile("^(\f|)N° (?P<numero>\w+)", re.MULTILINE|re.DOTALL)
    m = pat.finditer(out)
    char_pos = [u.span()[0] for u in m]
    char_pos = [char_pos[i:i+1+1] for i in range(0,len(char_pos), 1)]
    char_pos[-1].append(len(out))
    pat2 = re.compile("^(\f|)N° (?P<numero>\w+)\n((.|\n)*)présenté par\n\n(?P<auteur>.*)\n\n----------\n\nARTICLE\s(?P<article>.*)(?P<texte>(.|\n)*)EXPOSÉ SOMMAIRE(?P<motif>(.|\n)*)")
    amds = []
    for a in char_pos:
        amd = out[a[0]:a[1]-1]
        for m in pat2.finditer(amd):
            obj = {
                'number': m.group('numero'),
                'authors':m.group('auteur'),
                'article':m.group('article'),
                'text':m.group('texte'),
                'reason':m.group('motif'),
            }
            amds.append(obj)

    sys.stdout.write(json.dumps(amds))

if __name__ == "__main__":
    main(sys.argv[1:])


