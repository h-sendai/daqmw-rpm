Name:           kek-daqmiddleware-testing-repo       
Version:        8 
Release:        0%{?dist}
Summary:        KEK DAQMiddleware Repository Configuration File.

Group:          System Environment/Base 
License:        XXX
URL:            http://daqmw.kek.jp/

Source0:        kek-daqmiddleware-testing.repo	

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch

%description
This package contains the KEK DAQ Middleware TESTING repostiry configuration file.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE0} .

%build

%install
rm -rf $RPM_BUILD_ROOT

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%post

%postun 

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*

%changelog
* Wed Aug 11 2010 Hiroshi Sendai
- Create Testing RPM repository.

* Tue Jun 10 2008 Hiroshi Sendai
- Use basearch.

* Wed Jan 30 2008 Hiroshi Sendai <hiroshi.sendai@kek.jp>
- baseurl's ~ should be ~ itself.  We should not write ~ as %7E.

* Mon Jan 28 2008 Hiroshi Sendai <hiroshi.sendai@kek.jp>
- Initial revision.
