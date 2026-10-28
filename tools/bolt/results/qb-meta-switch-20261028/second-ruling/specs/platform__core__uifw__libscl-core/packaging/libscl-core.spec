Name:       libscl-core
Summary:    A library for developing software keyboards
Version:    0.11.3
Release:    1
Group:      Graphics & UI Framework/Input
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(isf)
BuildRequires:  pkgconfig(ecore-wl2)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(input-method-client)
BuildRequires:  pkgconfig(libscl-common)
BuildRequires:  pkgconfig(appcore-efl)
BuildRequires:  pkgconfig(capi-appfw-app-common)

Provides:	%{name}-profile_common = %{version}-%{release}
Provides:	%{name}-profile_mobile = %{version}-%{release}
Provides:	%{name}-profile_tv = %{version}-%{release}
Provides:	%{name}-profile_ivi = %{version}-%{release}

%define PURE_NAME libscl-core-pure

%description
A library that helps developing S/W Keyboard

%package pure-devel
Summary:    SCL-Core-Pure header file
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description pure-devel
A devel package of libscl-core-pure library that helps developing S/W Keyboard

%package devel
Summary:    SCL-Core header file
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description devel
A devel package of libscl-core library that helps developing EFL S/W Keyboard

%prep
%setup -q

%build
export CFLAGS="${CFLAGS} -fvisibility=hidden -DTIZEN_DEBUG_ENABLE -Werror"
export CXXFLAGS="${CXXFLAGS}  -fvisibility=hidden -fvisibility-inlines-hidden -DTIZEN_DEBUG_ENABLE -Werror"
export FFLAGS="${FFLAGS} -DTIZEN_DEBUG_ENABLE"

rm -rf CMakeFiles
rm -rf CMakeCache.txt

# common
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIB_INSTALL_DIR:PATH=%{_libdir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/%{name}.so
%{_libdir}/%{PURE_NAME}.so
%license LICENSE

%files pure-devel
%defattr(-,root,root,-)
%{_includedir}/%{PURE_NAME}/*
%{_libdir}/pkgconfig/%{PURE_NAME}.pc

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/%{name}.pc
