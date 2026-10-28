%define enable_libv4l2 0
%define build_test 0

Name:        vision-source-v4l2
Summary:     vision source-v4l2
Version:     1.2.0
Release:     0
Group:       Multimedia/Framework
License:     Apache-2.0
Source0:     %{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libtbm)
BuildRequires: pkgconfig(iniparser)
BuildRequires: pkgconfig(capi-media-tool)
%if 0%{?enable_libv4l2}
BuildRequires:  pkgconfig(libv4l2)
%endif
%if 0%{?build_test}
BuildRequires: gtest-devel
BuildRequires: vision-source-devel
%else
BuildRequires: pkgconfig(vision-source)
%endif # build_test

%description
Vision source v4l2

%prep
%setup -q

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

%cmake \
%if 0%{?enable_libv4l2}
	-DHAVE_LIBV4L2=ON \
%endif
%if 0%{?build_test}
	-DBUILD_TEST=ON \
%endif # build_test
.

make %{?jobs:-j%jobs}

%install

%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/*.so
%if 0%{?build_test}
%{_bindir}/*
%endif # build_test
%license LICENSE.APLv2
