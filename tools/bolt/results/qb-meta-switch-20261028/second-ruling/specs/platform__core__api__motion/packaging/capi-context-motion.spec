Name:       capi-context-motion
Summary:    Tizen Native Motion Recognition API
Version:    2.0.3
Release:    1
Group:      Service/Context
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

%{!?gcov: %global gcov 0}

BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(sensor)

Requires(post):  /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

# Backward compatibility
Provides: motion
Provides: libcore-context-manager.so.1

%description
Tizen Native Motion Recognition API

%prep
%setup -q

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%if 0%{gcov}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

export CXXFLAGS+=" -Wextra -Wcast-align -Wshadow -Wwrite-strings -Wswitch-default -Wno-unused-parameter"
export CXXFLAGS+=" -Wno-empty-body -fomit-frame-pointer -fno-optimize-sibling-calls"
export CXXFLAGS+=" -fno-strict-aliasing -fno-unroll-loops -fsigned-char -fstrict-overflow"
export CXXFLAGS+=" -Wnon-virtual-dtor"

%cmake . -DMAJORVER=${MAJORVER} -DFULLVER=%{version}
make %{?_smp_mflags}

%install
%make_install

# For backward compatibility
ln -s %{name}.pc %{buildroot}/%{_libdir}/pkgconfig/motion.pc
ln -s %{name}.pc %{buildroot}/%{_libdir}/pkgconfig/libcore-context-manager.pc
ln -s lib%{name}.so.%{version} %{buildroot}/%{_libdir}/libcore-context-manager.so.1

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest packaging/%{name}.manifest
%{_libdir}/*.so.*
%license LICENSE

%package devel
Summary:	Tizen Native Motion Recognition API (Development)
Group:		Framework/context
Requires:	%{name} = %{version}-%{release}

%description devel
Tizen Native Motion Recognition API (Development)

%files devel
%{_includedir}/*/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
