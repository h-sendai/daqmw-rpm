# omniORB 4.1.7 on CentOS Stream 8 python2

CentOS Stream 8上でpython2を使うomniORB 4.1.7 RPMパッケージ作成用ファイル。

rpmbuildコマンドは

```
rpmbuild -bb --without openssl omniORB.spec
```

と``--without openssl``を付けて行う。たぶんOpenSSL 1.1系ではコンパイルできない。
SOURCESにはomniORB-4.1.7.tar.bz2をダウンロードして入れておく（gitリポジトリに
バイナリをあまりいれたくないのでここではいれてない）。

