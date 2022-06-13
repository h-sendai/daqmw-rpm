# RPM specファイルメモ

解説: https://rpm-packaging-guide.github.io/

## RPMビルド環境整備

ビルド環境インストール

```
yum install rpmdevtools
yum install rpmlint
```

ディレクトリ構成

```
# $HOME/.rpmmacors
%_topdir /home/sendai/rpm
```

と書いて``rpmdev-setuptree``で``/home/sendai/rpm``以下に
次のディレクトリができる:

```
BUILD
RPMS
SOURCES
SPECS:
SRPMS
```

## RPM specファイル構造

- preamble
  - Name
  - Version
  - Release
  - Summary
  - License
  - URL
  - Source0, Source1, ...
  - Patch0, Patch1, ...
  - BuildRequires
  - Requires
- %description
- %prep (prepare)
- %build
- %install
- %check
- %files
- %changelog

## 色々

rpmマクロの定義は/usr/lib/rpm/ディレクトリ以下にある。

### rpm specファイル中のマクロの展開

``rpm --eval '%make_build'``のように``rpm --eval``でマクロを展開した
値を調べることができる。

### %make_build

CentOS 7: ``%make_build %{__make} %{?_smp_mflags}``

CentOS 8: ``%{__make} %{_make_output_sync} %{?_smp_mflags}``

複数CPUがあるマシンではCentOS 7では``make -j 4``となる。
CentOS 8では``%{_make_output_sync}``が``-O``に展開され、
``%make_build``を使うとコンパイルコマンドが表示されなくなる。
``%make_build``のかわりに
``%{__make} %{?_smp_mflags}``を使うと表示されるようになる。

### tarballを展開してできるディレクトリと``{%name}-%{version}``の値が違う

setup -q -n other_name

### vim new.spec

CentOS上のvimでまだ存在しないファイル名 + .specを指定すると/usr/share/vim/vimfiles/template.spec
ファイルがバッファに入る。これをうめていけばspecファイルができる。
入る内容: [template/template.spec](template/template.spec)
