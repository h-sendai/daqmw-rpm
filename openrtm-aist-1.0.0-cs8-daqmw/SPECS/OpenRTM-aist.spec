%define majorver       1
%define minorver       0
%define revision       0
%define tinyver        r1971
%define pkgver         13
%define version        %{majorver}.%{minorver}.%{revision}
%define variant        %{version}-%{tinyver}
%define _distname      %{tinyver}%{?dist}
# %%define _distname     %%{tinyver}%%{?dist}

Summary: OpenRTM-aist: RTM/RTComponent development environment
Name: OpenRTM-aist
Version: %{version}
Release: %{pkgver}.%{_distname}
Group: Development/Libraries
License: Eclipse Public License
Buildroot: %{_tmppath}/%{name}-root
URL:    http://openrtp.jp/openrtm/svn/OpenRTM-aist/trunk/OpenRTM-aist/
Source0:	OpenRTM-aist-%{tinyver}.tar.gz
# Patch0: OpenRTM-aist-1.0.0-RingBuffer.h.patch
# Patch1: OpenRTM-aist-1.0.0-CorbaConsumer.h.patch
Patch0: OpenRTM-aist-r1971-InPort.h.patch
Patch1: OpenRTM-aist-r1971-RingBuffer.h.patch
Patch2: OpenRTM-aist-r1971-Makefile.am.2.patch
Patch3: OpenRTM-aist-r1971-SimpleService-Makefile.am.patch
Patch4: OpenRTM-aist-r1971-Routing.cpp.patch
patch5: OpenRTM-aist-r1971-coil-posix-Condition.h.patch
patch6: OpenRTM-aist-r1971-configure.ac.patch
patch7: OpenRTM-aist-r1971-coil-configure.ac.patch
patch8: OpenRTM-aist-r1971-coil-Timer.cpp.patch

BuildRequires: omniORB, omniORB-devel, python2
Requires: omniORB, omniORB-utils, omniORB-devel, omniORB-servers, omniORB-doc, python2
#Requires: omniORB, omniORB-utils, omniORB-devel, omniORB-servers, omniORB-bootscripts, omniORB-doc, python

Distribution: Scientific Linux
Vendor: KEK/IPNS

%undefine _hardened_build
# ../../../src/lib/coil/include/coil/File.h:140:60: error: ISO C++ forbids
# comparison between pointer and integer [-fpermissive]
#             for (size_t i(0); i < fname.size() && globc != '\0'; ++i, ++globc)
%define build_cflags -g -O2 -fpermissive
%define build_cxxflags -g -O2 -fpermissive

%description
OpenRTM is RTMiddleware and RTComponent development environment.

#------------------------------------------------------------
# prep section
%prep
#
# %%setup -n %%{name}-%%{version} -q
#
%setup -n %{name}-%{tinyver}
%patch0  -p1
%patch1  -p1
%patch2  -p1
%patch3  -p1
%patch4  -p1
%patch5  -p1
%patch6  -p1
%patch7  -p1
%patch8  -p1

/usr/bin/pathfix.py -i %{__python2} -n -p build/*
/usr/bin/pathfix.py -i %{__python2} -n -p utils/rtm-skelwrapper/*
/usr/bin/pathfix.py -i %{__python2} -n -p utils/rtc-template/*
/usr/bin/pathfix.py -i %{__python2} -n -p src/lib/coil/build/*

#------------------------------------------------------------
# build section
%build
sh build/autogen
%configure --prefix=/usr --enable-debug
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make

#------------------------------------------------------------
# install section
%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#------------------------------------------------------------
# clean section
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

#------------------------------------------------------------
# files section
%files
%defattr(-,root,root,-)
/etc/rtc.conf.sample
%{_bindir}/*
%{_includedir}/*
%{_libdir}/libRTC*
%{_libdir}/libcoil*
%{_libdir}/OpenRTM-aist/*
%{_libdir}/pkgconfig/*
# %%{_datadir}/OpenRTM-aist/*


#------------------------------------------------------------
# changelog section
%changelog
* Fri Feb 04 2022 Hiroshi Sendai
- Do not compile in examples directory becuase we cannot compile successfully (SimpleService)
* Fri May 07 2021 Hiroshi Sendai
- Re-apply Timer.cpp patch
- Rebuild normal rpm and debuginfo rpm
* Thu May 06 2021 Hiroshi Sendai
- Add patch to enable -g -O2 compile
- Disable Timer.cpp patch to test debuginfo
* Fri Apr 30 2021 Hiroshi Sendai
- Add patch for Timer.cpp
- --enable-debug build (will be removed)
* Fri Feb 22 2013 Hiroshi Sendai
- Add a patch to fix InPort read timeout. 
* Tue Jul 03 2012 Hiroshi Sendai
- Add a patch to fix missing pclose() in src/lib/coil/posix/coil/Routing.cpp
  for Linux ip(1) command.
* Fri Apr 13 2012 Hiroshi Sendai
- Remove omniORB-bootscripts from REQUIRES bacause EPEL project provides omniORB's rpm and it does not have omniORB-bootscripts.
* Mon Jan 24 2011 Hiroshi Sendai
- Add Makefile.am patch for SimpleService install error
  from upstream.
* Thu Jun 24 2010 Hiroshi Sendai
- Get source from http://openrtp.jp/openrtm/svn/OpenRTM-aist/trunk/OpenRTM-aist/
  using svn co
- Patch: InPort.h for getStatus() trial.
- Patch: RingBuffer mutex fix (will be fixed in the future release)
- Patch: Remove docs directory due to document processing failure
* Thu May 06 2010 Hiroshi Sendai
- Patch for src/lib/CorbaConsumer.h
- pkgver bump to 2
* Wed Apr 28 2010 Hiroshi Sendai
- Patch for src/lib/RingBuffer.h
- Remove ACE, ACE-devel from BuildRequires, Requires.
- pkgver bump to 1
* Fri Jan 29 2010 Hiroshi Sendai
- Create 1.0.0 RELEASE package
* Tue May 26 2009 Hiroshi Sendai
- Create 1.0.0 RC1 package.
- Add pkgconfig directory in files section.
* Wed Nov 05 2008 Hiroshi Sendai
- Reduce timeout.
* Sun Jun 08 2008 Hiroshi Sendai
- Add dist in _distname
- version bump 8.
* Thu Jan 10 2008 Hiroshi Sendai
- Add comment out std::cout in rtm/InPort.h, rtm/OutPort.h.
- bump version 7.
* Mon Jan 07 2008 Hiroshi Sendai
- Jumbo patch for KEK edition by Yasu.
- Do not compile in examples directory becuase we cannot compile successfully
  due to jumbo patch for KEK edition.
* Mon Nov 12 2007 Hiroshi Sendai
- Correct this spec file to apply rtm/idl/DataPort.idl patch.
- Correct patch to rtm/idl/DataPort.idl.  I mis-understood
  patch submitted by Yasu.
- pkgver version bump to 5.
* Sat Nov 10 2007 Hiroshi Sendai
- Apply patch to rtm/idl/DataPort.idl
- Dependencies ACE, ACE-devel version up to 5.6.
- pkgver version bump to 4.
* Mon Oct 29 2007 Hiroshi Sendai
- Dependencies ACE, ACE-devel version down from 5.6 to 5.5.
- pkgver version bump to 3.
* Fri Oct 26 2007 Hiroshi Sendai
- One more comment out in rtm/InPortTcpSockConsumer.h.
- pkgver verbion bump to 2.
* Fri Oct 26 2007 Hiroshi Sendai
- Create RPM for OpenRTM-aist-0.4.1-KEK.tar.gz
- Patch on rtm/InPortTcpSockConsumer.h, rtm/TcpSockServer.patch
  to comment out std::cout.  requested by Yasu.
- pkgver version bump to 1.
* Thu Sep 27 2007 Noriaki Ando <n-ando@aist.go.jp> - 0.4.1-1._distname
- The second public release version of OpenRTM-aist-0.4.1.
* Wed Jun 13 2007 Noriaki Ando <n-ando@aist.go.jp> - 0.4.0-1._distname
- The second public release version of OpenRTM-aist-0.4.0.
* Mon May 23 2005 Noriaki Ando <n-ando@aist.go.jp> - 0.2.0-0vl1
- The first public release version of OpenRTM-aist-0.2.0.
