Name:       capi-network-inm
Summary:    An Intelligent Network Monitoring(INM) libraries in Native API
Version:    0.1.24
Release:    1
Group:      Network & Connectivity/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Intelligent Network Monitoring(INM) library in Tizen C API

%package devel
Summary:  Intelligent Network Monitoring(INM) in Native API (Development)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires: capi-base-common-devel

%description devel
An Intelligent Network Monitoring(INM) library in Tizen CAPI (Shared Library) (Development)

%package test
Summary:    INM - INM test binaries

%description test
Test Application for Intelligent Network Monitoring(INM)

%prep
%setup -q
chmod 644 %{SOURCE0}

%ifarch %{arm}
export ARCH=arm
%else
export ARCH=i586
%endif

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
        -DCMAKE_BUILD_TYPE=%{?build_type} \
        -DCMAKE_VERBOSE_MAKEFILE=ON \
        -DLIB_DIR:PATH=%{_libdir} \
        -DBIN_DIR:PATH=%{_bindir} \
        -DINCLUDE_DIR:PATH=%{_includedir} \
        -DLOCAL_STATE_DIR:PATH=%{_localstatedir} \
        -DDATA_ROOT_DIR:PATH=%{_datadir} \
        -DFULLVER=%{version} \
        -DMAJORVER=${MAJORVER}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest capi-network-inm.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/network/*.h
%{_libdir}/*.so

%files test
%manifest inm-test.manifest
%attr(755,root,root) %{_bindir}/inm-test

