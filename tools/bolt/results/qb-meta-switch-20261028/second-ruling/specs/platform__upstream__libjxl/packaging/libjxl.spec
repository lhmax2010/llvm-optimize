## if you want to build tools, please enable after lodepng is added
%define enable_tools 0

Name:       libjxl
Summary:    JPEG XL encoder and decoder library
Version:    0.11.1
Release:    0
Group:      Multimedia/Libraries
URL:        https://github.com/libjxl/libjxl/
License:    BSD-3-Clause and Apache-2.0
Source0:    %{name}-%{version}.tar.gz
SOURCE1:    %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(libbrotlicommon)
BuildRequires:  pkgconfig(libbrotlidec)
BuildRequires:  pkgconfig(libbrotlienc)
BuildRequires:  pkgconfig(lcms2)

%description
Description: JPEG XL encoder and decoder library


%package devel
Summary:        JPEG XL encoder and decoder (development)
Requires:       %{name}  = %{version}-%{release}
Group:          Multimedia/Development

%description devel
Description: JPEG XL encoder and decoder library (development)

%if %{enable_tools}
%package tools
Summary:        JPEG XL encoder and decoder (tools)
Requires:       %{name}  = %{version}-%{release}
Group:          Multimedia/Development

%description tools
Description: JPEG XL encoder and decoder library (tools)
%endif

%prep
%setup -q
cp %{SOURCE1} .

%build
%{?_toolchain:
%if %{toolchain_is clang}
%ifarch armv7l armv7hl
CFLAGS+=" -fno-integrated-as"
CXXFLAGS+=" -fno-integrated-as"
%endif
%endif
}

%if "%{asan}" == "1"
sed -i 's/-fmerge-all-constants/-fno-merge-all-constants/g' lib/CMakeLists.txt
%endif
%cmake . -DCMAKE_BUILD_TYPE=Release \
         -DBUILD_TESTING=OFF \
%if %{enable_tools}
         -DJPEGXL_ENABLE_TOOLS=ON \
%else
         -DJPEGXL_ENABLE_TOOLS=OFF \
%endif
         -DJPEGXL_ENABLE_MANPAGES=OFF \
         -DJPEGXL_ENABLE_BENCHMARK=OFF \
         -DJPEGXL_ENABLE_EXAMPLES=OFF \
         -DJPEGXL_ENABLE_JNI=OFF \
         -DJPEGXL_ENABLE_SJPEG=OFF \
         -DJPEGXL_ENABLE_OPENEXR=OFF \
         -DJPEGXL_ENABLE_SKCMS=OFF \
         -DJPEGXL_BUNDLE_SKCMS=OFF \
         -DJPEGXL_STATIC=OFF \
         -DJPEGXL_FORCE_SYSTEM_BROTLI=ON \
         -DJPEGXL_FORCE_SYSTEM_LCMS2=ON \
         -D__TIZEN__=ON
make %{?jobs:-j%jobs}

%install
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%license LICENSE PATENTS LICENSE.APLv2.0

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}*.pc
%{_includedir}/jxl/*.h

%if %{enable_tools}
%files tools
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/*
%endif
