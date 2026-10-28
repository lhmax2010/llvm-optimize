%bcond_with x
%bcond_with wayland

Name: e-mod-tizen-gesture
Version: 0.3.17
Release: 1
Summary: The Enlightenment Gesture Module for Tizen
URL: http://www.enlightenment.org
Group: Graphics & UI Framework/Other
Source0: %{name}-%{version}.tar.gz
License: BSD-2-Clause
BuildRequires:  pkgconfig(enlightenment)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(tizen-extension-server)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(tzsh-server)
BuildRequires:  pkgconfig(gtest)

%global TZ_SYS_RO_SHARE  %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:/usr/share}

%description
This package is a the Enlightenment Gesture Module for Tizen.

%if "%{disable_tests}" != "1"
%package test
Summary: Test executables for %{name}
Group: Development/Testing
Requires: %{name} = %{version}-%{release}

%description test
This package contains test executables for %{name}.
%endif

%prep
%setup -q

%build

export GC_SECTIONS_FLAGS="-fdata-sections -ffunction-sections -Wl,--gc-sections"
export CFLAGS="${CFLAGS} -Wall -Werror -g -fPIC -rdynamic ${GC_SECTIONS_FLAGS} -DE_LOGGING=1 "
export LDFLAGS="${LDFLAGS} -Wl,--hash-style=both -Wl,--as-needed -Wl,--rpath=/usr/lib"

%autogen
%configure --prefix=/usr \
           --enable-wayland-only \
           %{?disable_tests:--disable-tests}
make

%if "%{disable_tests}" != "1"
%check
make check VERBOSE=1
%endif

%install
rm -rf %{buildroot}

# install
make install DESTDIR=%{buildroot}

# clear useless textual files
find  %{buildroot}%{_libdir}/enlightenment/modules/%{name} -name *.la | xargs rm

%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/enlightenment/modules/e-mod-tizen-gesture

%if "%{disable_tests}" != "1"
%files test
%defattr(-,root,root,-)
%{_bindir}/test_gesture_integration
%endif
