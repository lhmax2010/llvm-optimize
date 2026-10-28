Name:       mmsvc-player
Summary:    A Media Player module for muse server
Version:    1.0.4
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	mmsvc-player.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(muse-server)
BuildRequires:  pkgconfig(mm-common)
BuildRequires:  pkgconfig(mm-display-interface)
BuildRequires:  pkgconfig(mm-player)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-media-sound-manager)
BuildRequires:  pkgconfig(capi-media-tool)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(ttrace)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(python)
%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A Media Player module for muse server and Tizen Native API.
%package devel
Summary:  A Media Player module for muse server.(Development)
Group:    Development/Multimedia
Requires: %{name} = %{version}-%{release}

%description devel
%devel_desc

%prep
%setup -q
cp %{SOURCE1001} .


%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
#export CFLAGS+=" -D_USE_X_DIRECT_"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_ASM"
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

%cmake . \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	-DBUILD_TESTS=%{?gtests:1}%{!?gtests:0}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest mmsvc-player.manifest
%license LICENSE.Apache-2.0
%{_libdir}/liblegacy-player.so
%{_libdir}/libmuse-player.so
%if 0%{?gtests:1}
%{_bindir}/gtest-mmsvc-player
%endif

%files devel
%{_includedir}/media/*.h
%{_includedir}/media/*.def
%{_libdir}/pkgconfig/*.pc
