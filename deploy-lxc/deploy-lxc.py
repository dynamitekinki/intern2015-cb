#!/usr/bin/python

import time
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
    # 起動後ネットワークにつながるまで待つ
    # テスト時では3秒ほど待つと安定します
    time.sleep(3.0)

def ExecuteSocat(name):
    """
    name : コンテナ名
    """

    # コンテナ生成時はsocatが存在しないのでインストール
    subprocess.check_call(["sudo", "lxc-attach",
                           "-n", name, "--",
                           "sudo", "apt-get", "install", "-y", "socat",])
    subprocess.check_call(["sudo", "lxc-attach",
                           "-n", name, "--",
                           "sh", "-c",
                           "/usr/bin/socat TCP4-LISTEN:8000,fork,reuseaddr EXEC:\"hostname\" &",])

def main():
    CreateContainer("ubuntu", "ubuntu-ap1")
    CreateContainer("ubuntu", "ubuntu-ap2")
    CreateContainer("ubuntu", "ubuntu-nginx")

    StartContainer("ubuntu-ap1")
    StartContainer("ubuntu-ap2")
    StartContainer("ubuntu-nginx")
    
    ExecuteSocat("ubuntu-ap1")
    ExecuteSocat("ubuntu-ap2")

if __name__ == '__main__':
    main()
