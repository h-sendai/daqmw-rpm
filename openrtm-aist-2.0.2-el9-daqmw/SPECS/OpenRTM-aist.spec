Name:           OpenRTM-aist
Version:        2.0.2
Release:        5%{?dist}
Summary:        RT-Component development environment

License:        LGPL
URL:            https://www.openrtm.org/
#Source0:       https://github.com/OpenRTM/OpenRTM-aist/archive/refs/tags/v2.0.2.tar.gz
Source0:        OpenRTM-aist-2.0.2.tar.gz
Patch0:         OpenRTM-aist-2.0.2-utils-skelwrapper-shebang.patch
Patch1:         OpenRTM-aist-2.0.2-utils-skelwrapper-regex.patch
Patch2:         OpenRTM-aist-2.0.2-utils-rtm-config-CMakeLists.txt.patch
Patch3:         OpenRTM-aist-2.0.2-src-lib-coil-posix-coil-affinity.patch

BuildRequires: omniORB-devel >= 4.3
# BuildRequires: doxygen
BuildRequires: libuuid-devel
BuildRequires: boost-devel
BuildRequires: cmake

# need OpenRTM-aist 1.2.1 build
#BuildRequires: /usr/bin/pathfix.py
# need OpenRTM-aist 1.2.1 build end

Requires:      omniORB >= 4.3
Requires:      omniORB-servers >= 4.3
Requires:      omniORB-devel >= 4.3
Requires:      omniORB-utils >= 4.3
Requires:      libuuid-devel
Requires:      boost-devel

%undefine _hardened_build
%define build_cflags -g -O2
%define build_cxxflags -g -O2

%description
OpenRTM-aist is a reference implementation of RTC (Robotic Technology
Component Version 1.1, formal/12-09-01) specification which is OMG
standard (http://www.omg.org/spec/RTC/). OpenRTM-aist includes
RT-Middleware runtime environment and RTC framework. The OMG standard
defines a component model and certain important infrastructure
services applicable to the domain of robotics software
development. OpenRTM-aist is being developed and distributed by
National Institute of Advanced Industrial Science and Technology
(AIST), Japan. Please see http://www.openrtm.org/ for more detail.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
# %%autosetup
# %%patch0 -p1
# need 1.2.1 rpmbuild
# /usr/bin/pathfix.py -i %%{__python2} -n -p build/*
# /usr/bin/pathfix.py -i %%{__python2} -n -p utils/rtm-skelwrapper/*
# /usr/bin/pathfix.py -i %%{__python2} -n -p utils/rtc-template/*
# /usr/bin/pathfix.py -i %%{__python2} -n -p src/lib/coil/build/*
# need 1.2.1 rpmbuild end

%build
%cmake -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir}
%cmake_build

%install
rm -rf $RPM_BUILD_ROOT
%cmake_install

%files
%defattr(-,root,root,-)
# /etc/rtc.conf.sample
/etc/*
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*
%{_datadir}/*

%license COPYRIGHT

%changelog
* Thu Sep 25 2025 Hiroshi Sendai <hiroshi.sendai@kek.jp> 2.0.2-4
- Update patch filename

* Fri Sep 12 2025 Hiroshi Sendai <hiroshi.sendai@kek.jp> 2.0.2-2
- Add patch1 and patch2

* Fri Sep 12 2025 Hiroshi Sendai <hiroshi.sendai@kek.jp> 2.0.2-1
- Build on AlmaLinux 9

* Mon Feb 07 2022 Hiroshi Sendai <hiroshi.sendai@kek.jp> 1.2.2-4
- Add support to compile CentOS Stream 9

* Thu May 13 2021 Hiroshi Sendai <hiroshi.sendai@kek.jp> 1.2.2-3
- add BuildRequires: libuuid-devel boost-devel
- remove doxygen BuildRequires (configure --without-doxygen)

* Wed May 12 2021 Hiroshi Sendai <hiroshi.sendai@kek.jp> 1.2.2-2
- add patch for configure.ac, src/lib/coil/configure.ac to build with -g -O2

* Wed Apr 28 2021 Hiroshi Sendai <hiroshi.sendai@kek.jp> 1.2.2-1
- OpenRTM-aist 1.2.2 build

* Fri May 01 2020 Hiroshi Sendai <hiroshi.sendai@kek.jp>
- add omniORB-devel and omniORB-utils in Requires:

* Fri Dec 06 2019 Hiroshi Sendai <hiroshi.sendai@kek.jp>
- add --without-doxygen in configure section
- undefine _hardened_build
- add cflags and cxxflags

* Wed Dec 04 2019 Hiroshi Sendai <hiroshi.sendai@kek.jp>
- OpenRTM-aist 1.2.1 build
- add --enable-fluentd=no in configure
- use pathfix.py before configure and build

* Tue Nov 26 2019 Hiroshi Sendai <hiroshi.sendai@kek.jp>
- OpenRTM-aist 1.2.0
