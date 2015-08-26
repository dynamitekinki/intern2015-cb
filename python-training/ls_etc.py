#!/usr/bin/python

import sys
import subprocess

# 引数をチェック
param = sys.argv
if len(param) == 2: # 引数は(スクリプトを除いて)1つとる
    pattern = param[1]
else:
    sys.exit("Usage: python ls_etc.py PATTERN")

# "ls /etc"を実行．標準出力をパイプへ
proc = subprocess.Popen(['ls', '/etc'],
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


