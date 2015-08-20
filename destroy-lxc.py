#!/usr/bin/python

import sys
import argparse
import subprocess

def main():
    # $B0z?t$r%A%'%C%/(B
    parser = argparse.ArgumentParser()
    parser.add_argument('names', metavar='CONTEINER_NAME', nargs='+', help='stop and destroy conteiners.')
    args = parser.parse_args()

    conteiners = args.names

    flag = true
    
    # $B0z?t$KF~$C$?$9$Y$F$N%3%s%F%J$r:o=|(B
    # $B0l2s$G$bNc30$,H/@8$7$?>l9g0[>o=*N;$H$9$k!%(B
    for name in conteiners:
        try:
            subprocess.check_call(["sudo", "lxc-stop",
                                   "-n", name,])
        except Exception as e:
            print '=== $B%(%i!<FbMF(B ==='
            print 'type:' + str(type(e))
            print 'args:' + str(e.args)
            print 'message:' + e.message
            flag = false
    
        try:
            subprocess.check_call(["sudo", "lxc-destroy",
                                   "-n", name,])
        except Exception as e:
            print '=== $B%(%i!<FbMF(B ==='
            print 'type:' + str(type(e))
            print 'args:' + str(e.args)
            print 'message:' + e.message
            flag = false

    if !flag:
        sys.exit(1)

if __name__ == '__main__':
    main()
