## 1日目 - Python演習 -

    「ls /etc/ の結果から特定の文字列（たとえば "net"）を含むファイル一覧を抽出する
    Pythonプログラム ls_etc.py を作ってください。」
    
    条件
    ・lsコマンドを subprocess.Popen を使って実行すること。
    ・スクリプトのコマンドライン引数は1つで、検索文字列（たとえば "net"）を取れること。
    ・grepコマンドを使うのは禁止です。
    
    以下のような実行結果になれば正解です。
    
    $ ./ls_etc.py net
    issue.net
    network
    networks

### ファイル内容
ls_etc.py : コードレビュー前の提出ファイル
ls_etc_rev2.py : コードレビュー後の修正ファイル
