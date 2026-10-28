%define server wayland

Name:       efl-extension
Summary:    EFL extension library
Version:    0.1.8
Release:    1
Group:      System/Libraries
License:    Flora-1.1
URL:        http://www.tizen.org/
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(eina)
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(eldbus)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(libsystemd)

BuildRequires:  cmake
BuildRequires:  gettext
BuildRequires:  eolian-devel
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
%if "%{?server}" == "x"
BuildRequires:  pkgconfig(ecore-x)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(inputproto)
%else if "%{?server}" == "wayland"
BuildRequires:  pkgconfig(ecore-wl2)
BuildRequires:  pkgconfig(ecore-input)
BuildRequires:  eolian-devel
BuildRequires:  pkgconfig(glib-2.0)
%endif

#TIZEN_ONLY(20191212): adding internal interface for rotary event type
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(capi-ui-efl-util)
#

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig


%description
EFL extension library


%package devel
Summary:    EFL extensiona library (devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}


%description devel
EFL extension library providing small utility functions (devel)

%prep
%setup -q


%build
export CFLAGS+=" -fvisibility=hidden -fPIC -Wall -Wno-implicit-function-declaration"
export LDFLAGS+=" -fvisibility=hidden -Wl,-z,defs -Wl,--hash-style=both -Wl,--as-needed"

cmake . -DLIB_INSTALL_DIR:PATH=%{_libdir} \
	-DBIN_INSTALL_DIR:PATH=%{_bindir} \
%if "%{?server}" == "x"
	-DCMAKE_INSTALL_PREFIX=/usr -DWITH_X=1
%else if "%{?server}" == "wayland"
	-DCMAKE_INSTALL_PREFIX=/usr -DWITH_WAYLAND=1
%else
	-DCMAKE_INSTALL_PREFIX=/usr
%endif

make clean
make %{?jobs:-j%jobs}

%install
%make_install


# Use -s not -sf for ln to ensure that there is no duplicates.
pushd %{buildroot}%{_includedir}/efl-extension
pushd mobile
for FILE in *.h; do ln -s mobile/${FILE} ../${FILE}; done
popd
popd

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libefl-extension.so.*

%{_datadir}/locale/*

%manifest %{name}.manifest
%license LICENSE


%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/efl-extension.pc
%{_includedir}/efl-extension/*.h
%{_includedir}/efl-extension/mobile/*.h

