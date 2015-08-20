## 4日目 - LXCを用いたロードバランサ -
### 内容
生成したコンテナ上で，PythonスクリプトをWebアプリとして動かす．
さらにnginx(リバースプロキシ)を立ち上げたコンテナでロードバランサを動かす

### ファイル構成
- deploy.py : LXCコンテナを生成し，Webアプリの立ち上げからnginxの設定・立ち上げまで行う．
- webapp.py : コンテナ内で実行するWebアプリ
- 