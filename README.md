# Scientific Linux, CentOSにDAQ-Middlewareをセットするスクリプト

1. yumリポジトリファイルをダウンロードしインストールする。
2. DAQ-Middleware RPMパッケージ、および依存パッケージをダウンロード、インストールする。
3. EPELにあるomniORB 4.2.0は今はDAQ-Middlewareでは使えないので/etc/yum.conf、/etc/yum/yum-cron.confに
   ``exclude=omniORB*``を追加する。すでに``exclude=``があればその行に追加する。
