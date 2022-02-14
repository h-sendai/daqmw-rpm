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

### tarballを展開してできるディレクトリと``{%name}-%{version}``の値が違う

setup -q -n other_name

### vim new.spec

CentOS上のvimでまだ存在しないファイル名 + .specを指定すると/usr/share/vim/vimfiles/template.spec
ファイルがバッファに入る。これをうめていけばspecファイルができる。
入る内容: [template/template.spec](template/template.spec)
