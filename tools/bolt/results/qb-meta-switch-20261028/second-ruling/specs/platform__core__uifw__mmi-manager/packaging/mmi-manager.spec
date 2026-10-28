%define USE_GCOV 0

Name:		mmi-manager
Version:	1.0.3
Release:	0
Summary:	Multi-modal Interaction Manager
License:	MIT
URL:		http://www.tizen.org
Source:		%{name}-%{version}.tar.xz
Source1004:	%{name}.manifest

BuildRequires:	meson
BuildRequires:	tidl
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(dlog)
BuildRequires:	pkgconfig(rpc-port)
BuildRequires:	pkgconfig(ecore)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(tizen-extension-client)
BuildRequires:	pkgconfig(capi-media-vision)
BuildRequires:	pkgconfig(opencv)
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(gstreamer-base-1.0)
BuildRequires: pkgconfig(gstreamer-app-1.0)
BuildRequires: pkgconfig(libaurum)
BuildRequires: pkgconfig(capi-system-info)

#Build dependencies for tests
BuildRequires:	pkgconfig(gmock)

%description
MMI(Multi-modal Interaction) Manager

%package devel
Summary:	Development package for MMI Manager Module
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%description devel
Development package for MMI Manager Module

#%package tests
#Summary:	Testcases for MMI Manager APIs
#Group:		System/Libraries
#%description tests
#Testcases for testing MMI Manager APIs

%prep
%setup -q
cp %{SOURCE1004} .

#generate mmi-stub using TIDL Compiler
tidlc -s -l C -i tidl/mmi.tidl -o mmi_stub
mv mmi_stub.* src/mmimgr

%build
%if "%{USE_GCOV}" == "1"
CFLAGS+=" -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV"
CXXFLAGS+=" -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV"
LDFLAGS+=" -lgcov"
%endif
meson setup --prefix=/usr \
	--bindir %{_bindir} \
	--libdir %{_libdir} \
	builddir
ninja -C builddir all

%install
DESTDIR=%{buildroot} ninja -C builddir install

mkdir -p %{buildroot}%{_libdir}/provider

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/mmi-manager
%{_libdir}/libmmi*.so*
%{_datadir}/iu/*
#%{_datadir}/mmi-provider/*
#%{_libdir}/provider/libmmi*.so
%{_datadir}/packages/%{name}.xml

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_includedir}/mmi-*.h
%{_libdir}/pkgconfig/*

#%files tests
#%defattr(-,root,root,-)
#%license COPYING
#%{_bindir}/mmi-manager-tests
#%{_bindir}/modality_keyboard-tests
#%{_bindir}/modality_vision-tests
