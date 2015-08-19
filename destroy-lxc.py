#!/usr/bin/python

import sys
import argparse
import subprocess

def main():
    # 引数をチェック
    parser = argparse.ArgumentParser()
    parser.add_argument('name', metavar='CONTEINER_NAME', help='stop and destroy conteiner.')
    args = parser.parse_args()

    name = args.name
    
    try:
        subprocess.check_call(["sudo", "lxc-stop",
                               "-n", name,])
    except:
        print "lxc-stop failed!"
    
    try:
        subprocess.check_call(["sudo", "lxc-destroy",
                               "-n", name,])
    except:
        print "lxc-destroy failed!"

if __name__ == '__main__':
    main()
