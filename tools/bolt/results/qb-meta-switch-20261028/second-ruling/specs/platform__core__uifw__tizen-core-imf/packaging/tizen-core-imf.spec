Name:       tizen-core-imf
Summary:    Tizen core Input Method Framework
Version:    0.2.25
Release:    0
Group:      UI Framework / Text Input
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-core-wl)

%description
Tizen core Input Method Framework (Development) package.

%package devel
Summary:  Tizen core Input Method Framework
Group:    Graphics System/Display Management

%description devel
Tizen core Input Method Framework package.

%if 0%{?gcov:1}
%package gcov
Summary:  Tizen core Input Method Framework (gcov)
Group:    UI Framework / Text Input

%description gcov
tizen-core-imf gcov objects
%endif

%package unittests
Summary:    GTest for tizen core imf API
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for tizen core imf API

%package sample
Summary:    Sample for tizen core imf API
Group:      Development/Libraries
Requires:   %{name}

%description sample
Sample for tizen core imf API

%prep
%setup -q

%build
rm -rf CMakeFiles
rm -rf CMakeCache.txt
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
         -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
         -DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}
%__make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%check
# Coverage data (.gcda) is generated on the target device, not at build time.
# This package only ships the .gcno files (packaged by the install section)
# needed to produce the coverage report after running tests on the target.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%attr(0644,root,root) %{_libdir}/libtizen-core-imf.so.*
%license LICENSE

%files devel
%{_includedir}/tizen-core-imf/*.h
%{_libdir}/pkgconfig/tizen-core-imf.pc
%{_libdir}/libtizen-core-imf.so

%files unittests
%{_bindir}/tizen-core-imf_unittests

%files sample
%{_bindir}/tizen-core-imf_sample

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
