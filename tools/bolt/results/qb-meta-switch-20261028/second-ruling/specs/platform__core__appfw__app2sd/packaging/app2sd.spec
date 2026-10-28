Name:       app2sd
Summary:    Application installation on external memory
Version:    0.8.2
Release:    1
Group:      Application Framework/Package Management
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source2:    %{name}-test.manifest
Source3:    %{name}-plugin.manifest

BuildRequires:  pkgconfig(db-util)
BuildRequires:  pkgconfig(minizip)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(storage)
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  cmake
Requires:       cryptsetup

%description
Tizen application installation on external memory

%package devel
Summary:    Application install on external memory (devel)
Group:      Development/Libraries
Requires:   app2sd = %{version}-%{release}

%description devel
Tizen application installation on external memory (devel)

%package test
Summary:    Application install on external memory (test)
Group:      Development/Libraries
Requires:   app2sd = %{version}-%{release}

%description test
Tizen application installation on external memory (test)

%package plugin
Summary:    app2sd server and plugin library
Group:      Application Framework/Package Management

%description plugin
app2sd server and plugin library

%prep
%setup -q

cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DUNITDIR=%{_unitdir} -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DARCH=%{_arch} \
%if 0%{?asan} != 1
  -DASAN_ENABLED=FALSE
%else
  -DASAN_ENABLED=TRUE
%endif

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%check
cd unit-tests
LD_LIBRARY_PATH=../:../plugin/app2sd/ ctest -V

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libapp2ext.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/pkgconfig/app2sd.pc
%{_libdir}/libapp2ext.so

%files test
%manifest %{name}-test.manifest
%defattr(-,root,root,-)
%{_bindir}/test_app2ext

%files plugin
%manifest %{name}-plugin.manifest
%{_libdir}/libapp2sd.so*
%{_bindir}/app2sd-server
%{_unitdir}/app2sd-server.service
%{_datadir}/dbus-1/system-services/org.tizen.app2sd.service
%config %{_sysconfdir}/dbus-1/system.d/org.tizen.app2sd.conf
%{_bindir}/app2sd-mount-helper
