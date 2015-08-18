#!/usr/bin/python

import sys
import subprocess

# $B0z?t$r%A%'%C%/(B
param = sys.argv
if len(param) == 2: # $B0z?t$O(B($B%9%/%j%W%H$r=|$$$F(B)1$B$D$H$k(B
    pattern = param[1]
else:
    sys.exit("Usage: python ls_etc.py PATTERN")

# "ls /etc"$B$r<B9T!%I8=`=PNO$r%Q%$%W$X(B
proc = subprocess.Popen(['ls', '/etc'],
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


