# ecore is enabled by default; disable with: gbs build --define "ecore 0"
%{!?ecore:%define ecore 1}

Name:       libtrackrenderer
Summary:    new multimedia streaming player trackrenderer
Version:    0.2.14
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: libtrackrenderer.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(boost)
BuildRequires:  pkgconfig(mm-display-interface)
BuildRequires:  pkgconfig(resource-manager)
BuildRequires:  pkgconfig(resource-center-api)
BuildRequires:  pkgconfig(jsoncpp)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(capi-media-sound-manager)
BuildRequires:  pkgconfig(capi-media-tool)
BuildRequires:  gtest-devel
BuildRequires:  gtest

%description
new multimedia player, object-oriented model

%package devel
Summary:    Developement for multimedia player
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
%devel_desc

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if 0%{?ecore}
%define HAVE_ECORE ON
%else
%define HAVE_ECORE OFF
%endif

%ifarch aarch64
%cmake . -DHAVE_ECORE=%HAVE_ECORE -DCMAKE_C_FLAGS="${CFLAGS} -DDRM_MAPI_AARCH_64=1" -DCMAKE_CXX_FLAGS="${CXXFLAGS} -DDRM_MAPI_AARCH_64=1"
%else
%cmake . -DHAVE_ECORE=%HAVE_ECORE
%endif

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install

%files
%defattr(-,root,root,-)
%manifest libtrackrenderer.manifest
%license LICENSE.APLv2
%{_libdir}/libtrackrenderer.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/trackrenderer_capi/*.h
%{_libdir}/pkgconfig/libtrackrenderer.pc
