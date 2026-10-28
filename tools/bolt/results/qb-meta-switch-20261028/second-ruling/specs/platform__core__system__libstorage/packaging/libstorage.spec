Name:       libstorage
Summary:    Library to get storage information
Version:    1.0.0
Release:    0
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(mount)
BuildRequires:  pkgconfig(blkid)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libsyscommon)
BuildRequires:  pkgconfig(cynara-uid)
%if 0%{?gcov:1}
BuildRequires: lcov
%endif

%description
development package of library to get storage

%package devel
Summary:	Get storage information (devel)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Library to get storage information (devel)

%if 0%{?gcov:1}
%package gcov
Summary:	Get storage information (gcov)
Group:		Development/Libraries
%description gcov
Library to get storage information (gcov)
%endif

%prep
%setup -q
cp %{SOURCE1} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

%cmake .
make %{?jobs:-j%jobs}

%install
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_libdir}/*.so.*
%{_sysconfdir}/storage/libstorage.conf

%files devel
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_includedir}/storage/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
