#!/usr/bin/python

import sys
import argparse
import subprocess

def main():
    # $B0z?t$r%A%'%C%/(B
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', metavar='PATTERN', help='print lines containing this pattern.')
    args = parser.parse_args()
    
    pattern = args.pattern
    
    # "ls /etc"$B$r<B9T!%I8=`=PNO$r%Q%$%W$X(B
    proc = subprocess.Popen(['/bin/ls', '/etc'],
            stdout=subprocess.PIPE,
            )


    
    # $B=PNO$r$$$C$?$sJ8;zNs$X(B
    ls_str = proc.communicate()[0]
    
    # $BJ8;zNs$rJ,3d$7!$%j%9%H$X3JG<(B
    ls_list = ls_str.split()
    
    # $B%j%9%H$G%k!<%W(B
    for element in ls_list:
        if pattern in element:  # $BMWAG$K8!:w%Q%?!<%s$,4^$^$l$F$$$l$P=PNO(B
            print element
    
if __name__ == '__main__':
    main()
