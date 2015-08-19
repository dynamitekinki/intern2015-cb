#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
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

def PutFileToContainer(name, src, dst):
    """
    name : コンテナ名
    src  : 送信元ファイル名
    dst  : 送信先ファイル名
    """
    dst_path = "/var/lib/lxc/" + name + "/rootfs/" + dst
    subprocess.check_call(["sudo", "cp", src, dst_path])
    

def ExecuteWebapp(name):
    """
    name : コンテナ名
    """
    
    '''
    UBUNTU_REPO = "archive.ubuntu.com"

    try:
        subprocess.check_call(["sudo", "lxc-attach",
                               "-n", name, "--",
                               "ping", "-c", "1", UBUNTU_REPO,])
    except:
    '''
    
    # コンテナ生成時はsocatが存在しないのでインストール
    subprocess.check_call(["sudo", "lxc-attach",
                           "-n", name, "--",
                           "sudo", "apt-get", "install", "-y", "socat",])
    subprocess.check_call(["sudo", "lxc-attach",
                           "-n", name, "--",
                           "sh", "-c",
                           "/usr/bin/socat TCP-LISTEN:8000,fork,reuseaddr EXEC:/usr/local/bin/webapp.py &",])

def main():
    EXECUTE_PATH = os.path.abspath(os.path.dirname(__file__))
    CreateContainer("ubuntu", "ubuntu-test")
    StartContainer("ubuntu-test")
    PutFileToContainer("ubuntu-test", EXECUTE_PATH + "/webapp.py", "/usr/local/bin/")
    ExecuteWebapp("ubuntu-test")

if __name__ == '__main__':
    main()
