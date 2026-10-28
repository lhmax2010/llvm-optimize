Name:       libmm-common
Summary:    Multimedia Framework Common Lib
Version:    0.2.132
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  sed
BuildRequires:  pkgconfig(dlog)

%description
Multimedia Framework Common Library

%package devel
Summary:    Multimedia Framework Common Lib (devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Multimedia Framework Common Library (devel)

%prep
%setup -q


%build
CFLAGS="%{optflags} -DEXPORT_API=\"__attribute__((visibility(\\\"default\\\")))\" -Werror"
export CFLAGS="$CFLAGS -Wall -Wcast-align -Wcast-qual -Wextra -Wno-array-bounds -Wno-empty-body -Wno-ignored-qualifiers -Wno-unused-parameter -Wshadow -Wwrite-strings -Wswitch-default -Wno-unused-but-set-parameter -Wno-unused-but-set-variable"
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif
%reconfigure
make %{?jobs:-j%jobs}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}
sed -i -e 's|@HAL_LIBDIR@|%{_hal_libdir}|g' script/%{_sysconfdir}/profile.d/mmf.sh
cp -arf script/%{_sysconfdir}/* %{buildroot}/%{_sysconfdir}
%make_install


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%manifest libmm-common.manifest
%license LICENSE.APLv2
%defattr(-,root,root,-)
%{_libdir}/libmmfcommon.so.*
%{_sysconfdir}/profile.d/mmf.sh

%files devel
%defattr(-,root,root,-)
%{_includedir}/mmf/mm_types.h
%{_includedir}/mmf/mm_error.h
%{_includedir}/mmf/mm_message.h
%{_includedir}/mmf/mm_attrs.h
%{_includedir}/mmf/mm_debug.h
%{_includedir}/mmf/mm_log.h
%{_includedir}/mmf/mm.h
%{_libdir}/pkgconfig/mm-common.pc
%{_libdir}/libmmfcommon.so
