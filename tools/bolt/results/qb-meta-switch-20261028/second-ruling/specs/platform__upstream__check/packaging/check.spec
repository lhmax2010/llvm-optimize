Name:           check
Version:        0.14.0
Release:        0
License:        LGPL-2.1+
Summary:        Unit Test Framework for C
Url:            http://check.sourceforge.net/
Group:          Development/Libraries/C and C++
Source:         %{name}-%{version}.tar.bz2
Source99:       baselibs.conf
Source1001: 	 check.manifest
BuildRequires:  pkg-config

%description
Check is a unit test framework for C. It features a simple interfacefor
defining unit tests, limitating the developer the less possible. Tests
are run in a separate address space, so Check cancatch both, assertion
failures and code errors that cause segmentationfaults or other
signals. The output of unit tests can be used within source code
editors and IDEs.

%package devel
License:        LGPL-2.1+
Summary:        Unit Test Framework for C
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}
Requires:       glibc-devel
Recommends:     pkg-config

%description devel
Check is a unit test framework for C. It features a simple interface
for defining unit tests, putting little in the way of the developer.
Tests are run in a separate address space, so Check can catch both
assertion failures and code errors that cause segmentation faults or
other signals. The output from unit tests can be used within source
code editors and IDEs.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="%{optflags} -std=gnu99"
export CXXFLAGS="%{optflags} -std=gnu99"
export FFLAGS="%{optflags} -std=gnu99"
autoreconf -ivf
%configure --disable-static --with-pic --disable-build-docs
make %{?_smp_mflags} 

%install
%make_install 

%remove_docs
%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%defattr (-, root, root)
%license COPYING.*
%exclude %{_bindir}/checkmk
%{_libdir}/*.so.*

%files devel
%manifest %{name}.manifest
%defattr (-, root, root)
%dir %{_datadir}/aclocal
%{_datadir}/aclocal/*.m4
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
