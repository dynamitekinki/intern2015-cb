#!/usr/bin/python

import sys
import argparse
import subprocess

def main():
    # 引数をチェック
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', metavar='PATTERN', help='print lines containing this pattern.')
    args = parser.parse_args()
    
    pattern = args.pattern
    
    # "ls /etc"を実行．標準出力をパイプへ
    proc = subprocess.Popen(['/bin/ls', '/etc'],
            stdout=subprocess.PIPE,
            )


    
    # 出力をいったん文字列へ
    ls_str = proc.communicate()[0]
    
    # 文字列を分割し，リストへ格納
    ls_list = ls_str.split()
    
    # リストでループ
    for element in ls_list:
        if pattern in element:  # 要素に検索パターンが含まれていれば出力
            print element
    
if __name__ == '__main__':
    main()
