Name:           xdgmime
VCS:            platform/upstream/xdgmime#9ee107f4bd57eb84dac44cc31f852927dd5bd974
Version:        0.0.20
Release:        2.1
License:        LGPL-2.1+ and AFL-2.0
Summary:        Querying information about file type
Group:          Applications/Other
Source0:        xdgmime-%{version}.tar.gz
Source1001:     xdgmime.manifest
BuildRequires:  cmake

%description
Querying information about file type package.

%package devel
Summary:        Querying information about file type (devel)
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
Querying information about file type (devel) package.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -Wno-error=implicit-function-declaration "
%cmake . 
%__make %{?_smp_mflags}

%check
ctest -V

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libxdgmime.so.*
%license COPYING

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/xdgmime.h
%{_libdir}/libxdgmime.so
%{_libdir}/pkgconfig/xdgmime.pc
%changelog
* Fri May 31 2013 Baptiste DURAND <baptiste.durand@eurogiciel.fr> accepted/tizen/20130520.100945@a4ba312
- Fix library path in pc file
