#!/usr/bin/python

import sys
import subprocess

def CreateContainer(dist, name):
    """
    dist : ディストリビューション名
    name : コンテナ名
    """
    subprocess.check_call(["sudo", "lxc-create",
                           "-t", dist,
                           "-n", name,])


def StartContainer(name):
    """
    name : コンテナ名
    """
    subprocess.check_call(["sudo", "lxc-start",
                           "-n", name, "-d",])

def ExecuteSocat(name):
    """
    name : コンテナ名
    """

    # コンテナ生成時はsocatが存在しないのでインストール
    subprocess.check_call(["sudo", "apt-get", "-y",
                           "install", "socat",])

    subprocess.check_call(["sudo", "lxc-attach",
                           "-n", name, "--", #この後，コンテナでの実行コマンド
                           "sh", "-c",
                           "'socat TCP4-LISTEN:8000,fork,reuseaddr EXEC:\"hostname\" &'",])

def main():
    CreateContainer("ubuntu", "ubuntu-test")
    StartContainer("ubuntu-test")
    ExecuteSocat("ubuntu-test")

if __name__ == '__main__':
    main()
