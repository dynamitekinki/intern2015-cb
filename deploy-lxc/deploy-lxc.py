#!/usr/bin/python

import sys
import subprocess

def CreateContainer(dist, name):
    """
    dist : $B%G%#%9%H%j%S%e!<%7%g%sL>(B
    name : $B%3%s%F%JL>(B
    """
    subprocess.check_call(["sudo", "lxc-create",
                           "-t", dist,
                           "-n", name,])


def StartContainer(name):
    """
    name : $B%3%s%F%JL>(B
    """
    subprocess.check_call(["sudo", "lxc-start",
                           "-n", name, "-d",])

def ExecuteSocat(name):
    """
    name : $B%3%s%F%JL>(B
    """

    # $B%3%s%F%J@8@.;~$O(Bsocat$B$,B8:_$7$J$$$N$G%$%s%9%H!<%k(B
    subprocess.check_call(["sudo", "apt-get", "-y",
                           "install", "socat",])

    subprocess.check_call(["sudo", "lxc-attach",
                           "-n", name, "--", #$B$3$N8e!$%3%s%F%J$G$N<B9T%3%^%s%I(B
                           "sh", "-c",
                           "'socat TCP4-LISTEN:8000,fork,reuseaddr EXEC:\"hostname\" &'",])

def main():
    CreateContainer("ubuntu", "ubuntu-test")
    StartContainer("ubuntu-test")
    ExecuteSocat("ubuntu-test")

if __name__ == '__main__':
    main()
