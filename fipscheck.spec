Summary:	A library for integrity verification of FIPS validated modules
Name:		fipscheck
Version:	1.2.0
Release:	4.1%{?dist}
License:	BSD
Group:		System Environment/Libraries
# This is a Red Hat maintained package which is specific to
# our distribution.
URL:		http://fedorahosted.org/fipscheck/
Source0:	http://fedorahosted.org/releases/f/i/%{name}/%{name}-%{version}.tar.bz2

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: 	openssl-devel >= 0.9.8j

%description
FIPSCheck is a library for integrity verification of FIPS validated
modules. The package also provides helper binaries for creation and
verification of the HMAC-SHA256 checksum files.

%package lib
Summary:	Library files for %{name}
Group:		System Environment/Libraries

Requires:	%{_bindir}/fipscheck
Obsoletes:	%{name} < 1.2.0-1
Conflicts:	%{name} < 1.2.0-1

%description lib
This package contains the FIPSCheck library.

%package devel
Summary:	Development files for %{name}
Group:		System Environment/Libraries

Requires:	%{name}-lib = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%setup -q

%build
%configure --disable-static

make %{?_smp_mflags}

# Add generation of HMAC checksums of the final stripped binaries
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    $RPM_BUILD_ROOT%{_bindir}/fipshmac $RPM_BUILD_ROOT%{_bindir}/fipscheck \
    $RPM_BUILD_ROOT%{_bindir}/fipshmac $RPM_BUILD_ROOT%{_libdir}/libfipscheck.so.1.1.0 \
    ln -s .libfipscheck.so.1.1.0.hmac $RPM_BUILD_ROOT%{_libdir}/.libfipscheck.so.1.hmac \
%{nil}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -delete

%clean
rm -rf $RPM_BUILD_ROOT

%post lib -p /sbin/ldconfig

%postun lib -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README AUTHORS
%{_bindir}/fipscheck
%{_bindir}/.fipscheck.hmac
%{_bindir}/fipshmac

%files lib
%defattr(-,root,root,-)
%{_libdir}/libfipscheck.so.*
%{_libdir}/.libfipscheck.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/fipscheck.h
%{_libdir}/libfipscheck.so

%changelog
* Tue Nov 24 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.2.0-4.1
- Rebuilt for RHEL 6

* Tue Oct 27 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.0-4
- ldconfig must be in the lib subpackage post(un)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.0-3
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 26 2009 Tomas Mraz - 1.2.0-1
- add lib subpackage to avoid multilib on the base package
- add ability to compute hmacs on multiple files at once
- improved debugging with FIPSCHECK_DEBUG

* Thu Mar 19 2009 Tomas Mraz - 1.1.1-1
- move binaries and libraries to /usr

* Wed Mar 18 2009 Tomas Mraz - 1.1.0-1
- hmac check itself as required by FIPS

* Mon Feb  9 2009 Tomas Mraz - 1.0.4-1
- add some docs to the README, require current openssl in Fedora

* Fri Oct 24 2008 Tomas Mraz - 1.0.3-1
- use OpenSSL in FIPS mode to do the HMAC checksum instead of NSS

* Tue Sep  9 2008 Tomas Mraz - 1.0.2-1
- fix test for prelink

* Mon Sep  8 2008 Tomas Mraz - 1.0.1-1
- put binaries in /bin and libraries in /lib as fipscheck
  will be used by modules in /lib

* Mon Sep  8 2008 Tomas Mraz - 1.0.0-2
- minor fixes for package review

* Wed Sep  3 2008 Tomas Mraz - 1.0.0-1
- Initial spec file
