%define major 0
%define minor 6
%define patchlevel 0

Name:           libtcore
Version:        %{major}.%{minor}.%{patchlevel}
Release:        2
License:        Apache-2.0
Summary:        Telephony-core library
Group:          System/Libraries
Source0:        libtcore-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(dlog)
%if 0%{?gcov:1}
BuildRequires:  gtest-devel
BuildRequires:  lcov
%endif
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Telephony-core library

%package devel
Summary:        Telephony-core library (Development)
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
Telephony-core library (Development)

%prep
%setup -q

%build

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DVERSION=%{version} \
%ifarch %{arm}
%else
	-DARCH_EMUL=1 \
%endif
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}

make %{?_smp_mflags}

%if 0%{?gcov:1}
mkdir -p gcov-obj
find . -name '*.gcno' -exec cp '{}' gcov-obj ';'
%endif

%if 0%{?gcov:1}
%check
LD_LIBRARY_PATH=. gtest/gtest-libtcore
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info --exclude "*/gtest/*"
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%install
%make_install

%if 0%{?gcov:1}
mkdir -p %{buildroot}%{_datadir}/gcov/obj
install -m 0644 gcov-obj/* %{buildroot}%{_datadir}/gcov/obj
%endif

%files
%manifest libtcore.manifest
%defattr(644,root,root,-)
%{_libdir}/*.so.*
%license LICENSE
%exclude %{_datadir}/gcov/obj/*
%exclude %{_bindir}/gtest-libtcore
%exclude %{_libdir}/debug/bin/gtest-libtcore.debug

%files devel
%defattr(644,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/tcore.pc
%{_libdir}/*.so
