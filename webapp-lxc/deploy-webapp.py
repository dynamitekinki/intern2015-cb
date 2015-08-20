#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import subprocess


def CreateContainer(dist, name):
    """
    コンテナを生成する
    dist : ディストリビューション名
    name : コンテナ名
    """
    subprocess.check_call(["sudo", "lxc-create",
                           "-t", dist,
                           "-n", name,])

def StartContainer(name):
    """
    コンテナを立ち上げる
    name : コンテナ名
    """
    subprocess.check_call(["sudo", "lxc-start",
                           "-n", name, "-d",])

def PutFileToContainer(name, src, dst):
    """
    指定したコンテナにファイルをコピーする
    name : コンテナ名
    src  : 送信元ファイル名
    dst  : 送信先ファイル名
    """
    dst_path = "/var/lib/lxc/" + name + "/rootfs/" + dst
    subprocess.check_call(["sudo", "cp", src, dst_path])
    

def ExecuteWebapp(name):
    """
    Webアプリをsocatで起動する
    name : コンテナ名
    """
    
    TTL = 60 # ネットワーク接続がエラー時，タイムアウトするまでの時間
    
    # ネットワークに接続可能かの確認をTTLまでの間実行
    UBUNTU_REPO = "archive.ubuntu.com"
    for num in range(0, TTL):
        try:
            subprocess.check_call(["sudo", "lxc-attach",
                                   "-n", name, "--",
                                   "ping", "-c", "1", UBUNTU_REPO,])
        except:
            print "Bad network connection. (" + str(num + 1) + ")" 
            time.sleep(1.0)
        else:
            break
    
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

    CreateContainer("ubuntu", "ubuntu-ap1")
    CreateContainer("ubuntu", "ubuntu-ap2")
    CreateContainer("ubuntu", "ubuntu-nginx")

    StartContainer("ubuntu-ap1")
    StartContainer("ubuntu-ap2")
    StartContainer("ubuntu-nginx")

    PutFileToContainer("ubuntu-ap1", EXECUTE_PATH + "/webapp.py", "/usr/local/bin/")
    PutFileToContainer("ubuntu-ap2", EXECUTE_PATH + "/webapp.py", "/usr/local/bin/")

    ExecuteWebapp("ubuntu-ap1")
    ExecuteWebapp("ubuntu-ap2")

if __name__ == '__main__':
    main()
