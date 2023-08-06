Name: libpff
Version: 20161119
Release: 1
Summary: Library to to access the Personal Folder File (PFF) and the Offline Folder File (OFF) format. PFF is used in PAB (Personal Address Book), PST (Personal Storage Table) and OST (Offline Storage Table) files.
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libpff/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:                 zlib
BuildRequires:                 zlib-devel

%description
libpff is a library to access the Personal Folder File (PFF) and the Offline Folder File (OFF) format. PFF is used in PAB (Personal Address Book), PST (Personal Storage Table) and OST (Offline Storage Table) files.

%package devel
Summary: Header files and libraries for developing applications for libpff
Group: Development/Libraries
Requires: libpff = %{version}-%{release}

%description devel
Header files and libraries for developing applications for libpff.

%package tools
Summary: Several tools for reading Personal Folder Files (OST, PAB and PST)
Group: Applications/System
Requires: libpff = %{version}-%{release} 
 

%description tools
Several tools for reading Personal Folder Files (OST, PAB and PST)

%package python
Summary: Python 2 bindings for libpff
Group: System Environment/Libraries
Requires: libpff = %{version}-%{release} python
BuildRequires: python-devel

%description python
Python 2 bindings for libpff

%package python3
Summary: Python 3 bindings for libpff
Group: System Environment/Libraries
Requires: libpff = %{version}-%{release} python3
BuildRequires: python3-devel

%description python3
Python 3 bindings for libpff

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README ChangeLog
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libpff.pc
%{_includedir}/*
%{_mandir}/man3/*

%files tools
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_bindir}/pffexport
%attr(755,root,root) %{_bindir}/pffinfo
%{_mandir}/man1/*

%files python
%defattr(644,root,root,755)
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files python3
%defattr(644,root,root,755)
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%changelog
* Mon Nov 21 2016 Joachim Metz <joachim.metz@gmail.com> 20161119-1
- Auto-generated

