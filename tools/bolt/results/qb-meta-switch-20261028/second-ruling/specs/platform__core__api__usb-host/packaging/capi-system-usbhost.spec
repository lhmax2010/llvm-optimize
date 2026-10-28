Name:           capi-system-usbhost
Version:        0.0.2
Release:        1
License:        Apache-2.0
Summary:        RAW USB host API
Group:          Base/Device Management

Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
BuildRequires:  pkg-config
BuildRequires:  cmake
BuildRequires:  libattr-devel
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(capi-base-common)
%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%description
Usb-host is a librarary for raw communication with USB devices.

%package devel
Summary:    RAW USB host API
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development package for capi-system-usbhost. Contains headers and binaries required for
compilation of applications which use capi-system-usbhost.

%if 0%{?gcov:1}
%package gcov
Summary:    A USB-Host library in TIZEN C API (gcov)
Group:      System/Libraries

%description gcov
A USB-Host library in TIZEN C API (gcov)
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

export LDFLAGS="${LDFLAGS} -Wl,--rpath=%{_libdir}"

%cmake . -DVERSION=%{version} \
         -DCMAKE_BUILD_TYPE=%{?build_type:%build_type}%{!?build_type:RELEASE} \
         -DCMAKE_VERBOSE_MAKEFILE=ON \
         --no-warn-unused-cli

%__make %{?_smp_mflags}

ctest -V

%install
rm -rf %{buildroot}
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%defattr(-,root,root)
%{_libdir}/lib%{name}.so.*
/usr/lib/udev/rules.d/40-usb.rules

%files devel
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%defattr(-,root,root)
%{_includedir}/usb_host.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif

%changelog
