Name:       context-common
Summary:    Tizen Context-Service Internal Shared Library
Version:    4.0.3
Release:    1
Group:      Service Framework/Context
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(alarm-service)
BuildRequires: pkgconfig(libtzplatform-config)

%description
Tizen Context-Service Internal Shared Library

%prep
%setup -q

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

export CXXFLAGS+=" -Wextra -Wcast-align -Wshadow -Wwrite-strings -Wswitch-default -Wno-unused-parameter"
export CXXFLAGS+=" -Wno-empty-body -fomit-frame-pointer -fno-optimize-sibling-calls"
export CXXFLAGS+=" -fno-strict-aliasing -fno-unroll-loops -fsigned-char -fstrict-overflow"
export CXXFLAGS+=" -Wnon-virtual-dtor -std=c++0x"

%cmake . -DMAJORVER=${MAJORVER} -DFULLVER=%{version}
make %{?_smp_mflags}

%install
%make_install

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest packaging/%{name}.manifest
%{_libdir}/*.so.*
%license LICENSE

%package devel
Summary:    Tizen Context-Service Internal Shared Library (Development)
Group:      Service Framework/Context
Requires:	%{name} = %{version}-%{release}

%description devel
Tizen Context-Service Internal Shared Library (Development)

%files devel
%{_includedir}/context-service/*/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
