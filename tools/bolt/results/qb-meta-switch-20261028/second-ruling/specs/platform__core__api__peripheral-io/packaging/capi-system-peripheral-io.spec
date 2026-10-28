Name:       capi-system-peripheral-io
Summary:    Tizen Peripheral Input & Output library
Version:    0.4.3
Release:    0
Group:      System & System Tools
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source10:   peripheral-io.udev.rules
Source11:   peripheral-io.tmpfiles.conf
Source12:   apply-peripheral-io-perms
#Conflicts:  peripheral-bus
BuildRequires:  awk
BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libudev)
%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Tizen Peripheral Input & Output library

%package devel
Summary:    Tizen Peripheral Input & Output library (devel)
Group:      System & System Tools/Development
Requires:   %{name} = %{version}-%{release}

%description devel
Tizen Peripheral Input & Output library (devel)

%package test
Summary:    Tizen Peripheral Input & Output Test Programs (test)
Group:      System & System Tools/Testing
Requires:   %{name} = %{version}-%{release}

%description test
Tizen Peripheral Input & Output Test Programs (test)

%prep
%setup -q
cp %{SOURCE1} ./%{name}.manifest
cp %{SOURCE10} .
cp %{SOURCE11} .
cp %{SOURCE12} .

%build
%{?asan:
export CFLAGS+=" -Wno-format-truncation "
export CXXFLAGS+=" -Wno-format-truncation "
}
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DMAJORVER=${MAJORVER} -DFULLVER=%{version} -DGCOV=%{gcov}

%install
%make_install
mkdir -p %{buildroot}/usr/lib/tmpfiles.d
install -m0644 peripheral-io.tmpfiles.conf %{buildroot}/usr/lib/tmpfiles.d/peripheral-io.conf
mkdir -p %{buildroot}/usr/lib/udev/rules.d
install -m0644 peripheral-io.udev.rules %{buildroot}/usr/lib/udev/rules.d/90-peripheral-io.rules
mkdir -p %{buildroot}/%{_libexecdir}/peripheral-io
install -m0755 apply-peripheral-io-perms %{buildroot}/%{_libexecdir}/peripheral-io/apply-peripheral-io-perms

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so*
/usr/lib/tmpfiles.d/peripheral-io.conf
/usr/lib/udev/rules.d/90-peripheral-io.rules
%{_libexecdir}/peripheral-io/apply-peripheral-io-perms
%license LICENSE.APLv2

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files test
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/peripheral-io-test
%license LICENSE.APLv2
