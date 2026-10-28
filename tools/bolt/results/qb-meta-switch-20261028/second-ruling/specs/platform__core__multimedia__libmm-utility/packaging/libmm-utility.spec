Name:       libmm-utility
Summary:    Multimedia Framework Utility Library
Version:    0.5.6
Release:    0
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: libmm-utility.manifest
Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig
Requires: libmm-imgp-gstcs

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(opencv) >= 3.4.1
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libwebpmux)
BuildRequires:  giflib-devel
BuildRequires:  pkgconfig(GraphicsMagick)
BuildRequires:  pkgconfig(heif)
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(libjxl_threads)
%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif

%description
Multimedia Framework Utility Library - Main package.

%package devel
Summary:    Multimedia Framework Utility Library (DEV)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Multimedia Framework Utility Library - Development files.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -DGMAGICK_DEBUG=0 -D_FORTIFY_SOURCE=2 -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DBUILD_GTESTS=%{?gtests:1}%{!?gtests:0}
make %{?jobs:-j%jobs}

%install
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_libdir}/libmmutil_imgcv.so
%{_libdir}/libmmutil_gif.so
%{_libdir}/libmmutil_webp.so
%{_libdir}/libmmutil_common.so
%{_libdir}/libmmutil_imgp.so
%if 0%{?gtests:1}
%{_bindir}/gtest*
%{_bindir}/libmm*unittest*
%endif
%license LICENSE.APLv2.0

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
