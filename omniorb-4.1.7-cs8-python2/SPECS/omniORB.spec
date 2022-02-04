%global __python /usr/bin/python2
# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%global nameserver omniNames

%if 0%{?fedora} > 14 || 0%{?rhel} > 6
%global with_systemd 1
%endif

# openssl disabled by default, add conditional --with openssl
%bcond_with openssl

Name:           omniORB
Version:        4.1.7
Release:        4%{?dist}
Summary:        A robust high performance CORBA ORB for C++ and Python

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://omniorb.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/omniorb/%{name}/%{name}-%{version}/%{name}-%{version}.tar.bz2
Source1:        omniORB-nameserver.init
Source2:        omniORB-nameserver.logrotate
Source3:        omniORB.cfg
Source4:        omniNames.service
# fix incorrect fsf address
Patch0:         %{name}-4.1.6-fsf-address.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python2-devel
%{!?_without_openssl:BuildRequires:  openssl-devel}
%if 0%{?with_systemd}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%else
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(pre):  shadow-utils
# This is for /sbin/service
Requires(postun): initscripts
%endif
# needed for patch0
BuildRequires: byacc

# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}

%undefine _hardened_build
%define build_cflags -g -O2
%define build_cxxflags -g -O2

%description
omniORB is a robust high performance CORBA ORB for C++ and Python.
omniORB is a certified CORBA 2.1 implementation and largely CORBA 2.6
compliant.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
License:        LGPLv2+
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description    doc
The %{name}-doc package contains documentation files for
developing and administrating applications that use %{name}.

%package        servers
Summary:        OmniORB naming service
Group:          System Environment/Daemons
License:        GPLv2+
Requires:       %{name} = %{version}-%{release}

%description    servers
The %{name}-servers package contains omniNames naming server.

%package        utils
Summary:        Development files for %{name}
Group:          Development/Tools
License:        GPLv2+
Requires:       %{name} = %{version}-%{release}

%description    utils
The %{name}-utils package contains supplementary command line tools for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1

%build
%configure --disable-static %{?with_openssl:--with-openssl=%{_prefix}}
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
# fix rpmlint warnings: unstripped-binary-or-object
chmod 0755 %{buildroot}%{_libdir}/*.so.*
chmod 0755 %{buildroot}%{python_sitearch}/_omniidlmodule.so.*
# fix rpmlint errors: non-standard-dir-perm
chmod 0755 %{buildroot}%{_includedir}/{omnithread,COS}
chmod 0755 %{buildroot}%{_includedir}/omniORB4/{,internal}
chmod 0755 %{buildroot}%{_datadir}/idl/%{name}/COS
chmod 0755 %{buildroot}%{python_sitelib}/omniidl
chmod 0755 %{buildroot}%{python_sitelib}/omniidl_be
chmod 0755 %{buildroot}%{python_sitelib}/omniidl_be/cxx/{,skel,impl,dynskel,header}
# fix rpmlint error: non-executable-script
chmod +x %{buildroot}%{python_sitelib}/omniidl/main.py
%if 0%{?with_systemd}
# install systemd unit
mkdir -p %{buildroot}/lib/systemd/system/
install -m 0644 %{SOURCE4} %{buildroot}/lib/systemd/system/
%else
# install service init script
mkdir -p %{buildroot}%{_initddir}
install -m 0755 %{SOURCE1} %{buildroot}%{_initddir}/%{nameserver}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_localstatedir}/run/%{name}
%endif
# install server configuration stuff
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{nameserver}
mkdir -p %{buildroot}%{_sysconfdir}/
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}.cfg
pathfix.py -pni "%{__python2} %{py2_shbang_opts}" %{buildroot}%{python_sitelib}/omniidl/* %{buildroot}%{_bindir}/*
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
# install man pages
pushd man
mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 man1/* %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_mandir}/man8
install -m 0644 man8/* %{buildroot}%{_mandir}/man8/
popd


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%pre servers
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
-c "OmniNames Naming Service" %{name}
exit 0

%if 0%{?with_systemd}
%post servers
%systemd_post omniNames.service

%preun servers
%systemd_preun omniNames.service

%postun servers
%systemd_postun omniNames.service

%else
%post servers
/sbin/chkconfig --add %{nameserver}

%preun servers
if [ $1 = 0 ] ; then
  /sbin/service  stop >/dev/null 2>&1
  /sbin/chkconfig --del  %{nameserver}
fi

%postun servers
if [ $1 -ge 1 ] ; then
    /sbin/service  %{nameserver} condrestart >/dev/null 2>&1 || :
fi
%endif

%files
%defattr(-,root,root,-)
%doc COPYING.LIB README.FIRST.txt README.unix
%{_libdir}/*.so.*

%files servers
%defattr(-,root,root,-)
%if 0%{?fedora} > 14 || 0%{?rhel} > 6
/lib/systemd/system/omniNames.service
%else
%{_initddir}/%{nameserver}
%dir %attr(0755, %{name}, root) %{_sharedstatedir}/%{name}
%dir %attr(0755, %{name}, root) %{_localstatedir}/run/%{name}
%endif
%config(noreplace) %{_sysconfdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{nameserver}
%dir %attr(0755, %{name}, root) %{_localstatedir}/log/%{name}
%{_bindir}/omniMapper
%{_bindir}/%{nameserver}
%{_mandir}/man8/*

%files devel
%defattr(-,root,root,-)
%doc doc/
%{_bindir}/omniidl
%{_bindir}/omniidlrun.py
%{_bindir}/omnicpp
%{_bindir}/omkdepend
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/idl/%{name}/*
# For noarch packages: sitelib
%{python_sitelib}/*
# For arch-specific packages: sitearch
%{python_sitearch}/*
%{_mandir}/man1/omniidl.1.gz
%{_mandir}/man1/omnicpp.1.gz

%files doc
%defattr(-,root,root,-)
%doc doc/

%files utils
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/catior
%{_bindir}/convertior
%{_bindir}/genior
%{_bindir}/nameclt
%{_mandir}/man1/catior.1.gz
%{_mandir}/man1/convertior.1.gz
%{_mandir}/man1/genior.1.gz
%{_mandir}/man1/nameclt.1.gz


%changelog
* Thu Feb 03 2022 Hiroshi Sendai <hiroshi.sendai@kek.jp> - 4.1.7-4
- Recompile on CentOS Stream 8 with python2 (not python3)
- Disable openssl support by default

* Mon May 10 2021 Hiroshi Sendai <hiroshi.sendai@kek.jp> - 4.1.7-3
- Recompile with debuginfo package

* Tue Apr 27 2021 Hiroshi Sendai <hiroshi.sendai@kek.jp> - 4.1.7-2
- Recompile
- Fix systemd on EL 7

* Tue Sep 10 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 4.1.7-1
- upstream 4.1.7 (RHBZ #1005607)
- macroized systemd scriptlets (RHBZ #850239)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 20 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 4.1.6-2
- enable openssl support
- fix typo in omniNames.service

* Wed Jul 13 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 4.1.6-1
- upstream 4.1.6
- use systemd for fedora >= 15

* Sun May 08 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 4.1.5-2
- spec cleanup

* Sun Jan 09 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 4.1.5-1
- upstream 4.1.5

* Wed Nov 24 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 4.1.4-1
- initial packaging
