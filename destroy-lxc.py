#!/usr/bin/python

import sys
import argparse
import subprocess

def main():
    # 引数をチェック
    parser = argparse.ArgumentParser()
    parser.add_argument('names', metavar='CONTEINER_NAME', nargs='+', help='stop and destroy conteiners.')
    args = parser.parse_args()

    conteiners = args.names

    flag = true
    
    # 引数に入ったすべてのコンテナを削除
    # 一回でも例外が発生した場合異常終了とする．
    for name in conteiners:
        try:
            subprocess.check_call(["sudo", "lxc-stop",
                                   "-n", name,])
        except Exception as e:
            print '=== エラー内容 ==='
            print 'type:' + str(type(e))
            print 'args:' + str(e.args)
            print 'message:' + e.message
            flag = false
    
        try:
            subprocess.check_call(["sudo", "lxc-destroy",
                                   "-n", name,])
        except Exception as e:
            print '=== エラー内容 ==='
            print 'type:' + str(type(e))
            print 'args:' + str(e.args)
            print 'message:' + e.message
            flag = false

    if !flag:
        sys.exit(1)

if __name__ == '__main__':
    main()
