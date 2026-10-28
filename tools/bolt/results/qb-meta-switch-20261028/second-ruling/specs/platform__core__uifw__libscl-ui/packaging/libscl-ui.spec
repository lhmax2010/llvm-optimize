%bcond_with x
%bcond_with wayland

Name:       libscl-ui
Summary:    A library for developing XML-based software keyboards
Version:    0.11.13
Release:    1
Group:      Graphics & UI Framework/Input
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(gio-2.0)
%if %{with wayland}
BuildRequires:  pkgconfig(ecore-wl2)
%else
BuildRequires:  pkgconfig(ecore-x)
BuildRequires:  pkgconfig(x11)
%endif
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(feedback)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libscl-common)
BuildRequires:  pkgconfig(dali2-core)
BuildRequires:  pkgconfig(dali2-adaptor)
BuildRequires:  dali2-adaptor-integration-devel
BuildRequires:  pkgconfig(dali2-ui-foundation)
BuildRequires:  pkgconfig(dali2-ui-components)
BuildRequires:  pkgconfig(gtest)


%description
A library that helps developing S/W Keyboard

%package devel
Summary:    SCL-UI header file
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
A devel package of libscl-ui library that helps developing S/W Keyboard

%package -n libscl-ui-dali
Summary:    A library for developing XML-based software keyboards (DALi backend)
Group:      Graphics & UI Framework/Input
License:    Apache-2.0

%description -n libscl-ui-dali
A library that helps developing S/W Keyboard (DALi backend)

%package -n libscl-ui-dali-devel
Summary:    Development files for libscl-ui-dali
Group:      Development/Libraries
Requires:   %{name}-dali = %{version}-%{release}
Requires:   %{name}-devel = %{version}-%{release}

%description -n libscl-ui-dali-devel
Development files for libscl-ui-dali library (DALi backend)

%package -n libscl-ui-tests
Summary:    Test executables for libscl-ui
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-dali = %{version}-%{release}

%description -n libscl-ui-tests
Test executables for libscl-ui and libscl-ui-dali.

%prep
%setup -q


%build
export CFLAGS="$CFLAGS -fvisibility=hidden -DTIZEN_DEBUG_ENABLE -Werror"
export CXXFLAGS="$CXXFLAGS -fvisibility=hidden -fvisibility-inlines-hidden -DTIZEN_DEBUG_ENABLE -Werror"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

# The -fvisibility=hidden option disables a generation of the rtti information for
# some classes with hidden visibility, this information is critically needed for
# ubsan VPTR check. Since this library needed to ise-default package, we should
# just disable visibility option with ubsan to avoid situation with undefined
# refernce to typeinfo.
%{?ubsan:
export CFLAGS=$(echo $CFLAGS | sed -e "s/-fvisibility=hidden//g")
export CXXFLAGS=$(echo $CXXFLAGS | sed -e "s/-fvisibility=hidden//g" -e "s/-fvisibility-inlines-hidden//g")
}

rm -rf CMakeFiles
rm -rf CMakeCache.txt

%if %{with wayland}
%cmake . -Dwith_wayland=TRUE
%else
%cmake .
%endif
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
%license LICENSE

%files -n libscl-ui-dali
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/%{name}-dali.so
%license LICENSE

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc

%files -n libscl-ui-dali-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/%{name}-dali.pc

%files -n libscl-ui-tests
%defattr(-,root,root,-)
%{_bindir}/scl_test_dali
%{_bindir}/scl_test_efl
