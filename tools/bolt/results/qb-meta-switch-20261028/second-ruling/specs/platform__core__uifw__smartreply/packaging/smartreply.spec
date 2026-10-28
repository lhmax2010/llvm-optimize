Name:       smartreply
Summary:    Tizen SmartReply Framework Native API
Version:    1.1.13
Release:    1
Group:      Framework/system
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(json-glib-1.0)

%description
Tizen SmartReply Framework Native API

%prep
%setup -q

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

export   CFLAGS="$CFLAGS -Wextra -Wcast-align -Wcast-qual -Wshadow -Wwrite-strings -Wswitch-default"
export CXXFLAGS="$CXXFLAGS -Wextra -Wcast-align -Wcast-qual -Wshadow -Wwrite-strings -Wswitch-default -Wnon-virtual-dtor -Wno-c++0x-compat"

export   CFLAGS="$CFLAGS -Wno-unused-parameter -Wno-empty-body"
export CXXFLAGS="$CXXFLAGS -Wno-unused-parameter -Wno-empty-body"

export   CFLAGS="$CFLAGS -fno-omit-frame-pointer -fno-optimize-sibling-calls -fno-strict-aliasing -fno-unroll-loops -fsigned-char -fstrict-overflow -fno-common"
export CXXFLAGS="$CXXFLAGS -fno-omit-frame-pointer -fno-optimize-sibling-calls -fno-strict-aliasing -fno-unroll-loops -fsigned-char -fstrict-overflow"

%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

install -D -m 0644 packaging/smartreply.service %{buildroot}%{_unitdir}/smartreply.service

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest packaging/%{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so*
%license LICENSE
/etc/dbus-1/system.d/*.conf
%{_unitdir}/smartreply.service
#%if %{BINTYPE} == "engineer"
%{_includedir}/smartreply/smartreply_service.h
#%endif

%package devel
Summary:    Tizen SmartReply Framework Native API (Development)
Group:      Framework/system
Requires:	%{name} = %{version}-%{release}

%description devel
Tizen SmartReply Framework Native API (Development)

%files devel
%defattr(-,root,root,-)
%{_includedir}/smartreply/*.h
%{_libdir}/pkgconfig/%{name}.pc
