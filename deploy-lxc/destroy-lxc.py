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

    subprocess.check_call(["sudo", "lxc-stop",
                           "-n", name,])
    subprocess.check_call(["sudo", "lxc-destroy",
                           "-n", name,])

if __name__ == '__main__':
    main()
