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
    subprocess.check_call(["sudo", "cp", "-ar", src, dst_path])

def CheckNetworkConnection(name):
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
            return
    
    raise

def CheckIpAddress(name):
    '''
    コンテナのIPアドレスを得る
    name : コンテナ名
    '''
    containers = subprocess.check_output(["sudo", "lxc-ls", "--fancy", "-F", "name,ipv4",])
    
    for container in containers.splitlines():
        element = container.split()
        if element[0] == name:
            return element[1]

    return None

def ExecuteNginx(name):
    """
    Nginxを起動する
    name : コンテナ名
    """
    CheckNetworkConnection(name)
    
    # コンテナ生成時はnginxが存在しないのでインストール
    subprocess.check_call(["sudo", "lxc-attach",
                           "-n", name, "--",
                           "sudo", "apt-get", "install", "-y", "nginx",])

    subprocess.check_call(["sudo", "lxc-attach",
                           "-n", name, "--",
                           "sudo", "service", "nginx", "start",])


def RestartNginx(name):
    """
    Nginxをリスタートする
    name : コンテナ名
    """
    subprocess.check_call(["sudo", "lxc-attach",
                           "-n", name, "--",
                           "sudo", "service", "nginx", "restart",])


def ExecuteWebapp(name):
    """
    Webアプリをsocatで起動する
    name : コンテナ名
    """
    CheckNetworkConnection(name)

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

    PutFileToContainer("ubuntu-ap1", EXECUTE_PATH + "/webapp.py", "/usr/local/bin/webapp.py")
    PutFileToContainer("ubuntu-ap2", EXECUTE_PATH + "/webapp.py", "/usr/local/bin/webapp.py")

    PutFileToContainer("ubuntu-ap1", EXECUTE_PATH + "/conf.d/ubuntu-ap1.conf", "/etc/network/interfaces")
    PutFileToContainer("ubuntu-ap2", EXECUTE_PATH + "/conf.d/ubuntu-ap2.conf", "/etc/network/interfaces")
    PutFileToContainer("ubuntu-nginx", EXECUTE_PATH + "/conf.d/ubuntu-nginx.conf", "/etc/network/interfaces")


    StartContainer("ubuntu-ap1")
    StartContainer("ubuntu-ap2")
    StartContainer("ubuntu-nginx")

    ExecuteWebapp("ubuntu-ap1")
    ExecuteWebapp("ubuntu-ap2")
    
    # 一旦，Nginxを起動して設定ファイル群を生成しておく
    ExecuteNginx("ubuntu-nginx")
    PutFileToContainer("ubuntu-nginx", EXECUTE_PATH + "/conf.d/default.conf", "/etc/nginx/sites-available/default")
    RestartNginx("ubuntu-nginx")

    CheckNetworkConnection("ubuntu-nginx")
    print '{0} is Web-server address.'.format(CheckIpAddress("ubuntu-nginx"))

if __name__ == '__main__':
    main()
