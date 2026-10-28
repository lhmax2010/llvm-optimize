Name:       libheif
Summary:    Multimedia Framework Library for HEIF(ISO/IEC 23008-12) image
Version:    0.1.1
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: libheif.manifest
Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(libswscale)
BuildRequires:  pkgconfig(mm-common)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(GraphicsMagick)
BuildRoot:  %{_tmppath}/%{name}-%{version}-build

%description
Multimedia Framework Library for HEIF(ISO/IEC 23008-12) image - Main package.

%package devel
Summary:    Multimedia Framework Utility Library (DEV)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Multimedia Framework Utility for HEIF(ISO/IEC 23008-12) image - Development files.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -D_FORTIFY_SOURCE=2"
# enable debug options if you need
#export CFLAGS+=" -D__ENABLE_DEBUG_MODE -D__DEBUG_SOURCE -D__DEBUG_CODEC_CONFIG"

%cmake .
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%license LICENSE.APLv2.0

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
