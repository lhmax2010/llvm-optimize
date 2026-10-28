Name:       capi-media-sound-pool
Version:    0.0.28
Summary:    Tizen Sound Pool module
Release:    0
Group:      Multimedia/Framework
License:    Apache-2.0
URL:        http://source.tizen.org
Source0:    %{name}-%{version}.tar.gz
Source1001:    %{name}.manifest
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(openal)
#BuildRequires: pkgconfig(freealut)
BuildRequires: pkgconfig(alure)

%description
Tizen Sound Pool Module allowing sounds playing for audio resources.

%package tools
Summary:    Tizen Sound Pool tools
Group:      Multimedia/Framework
Requires:   %{name} = %{version}-%{release}

%description tools
Tools for Tizen Sound Pool module.

%package devel
Summary:    Tizen Module allowing sounds playing for audio resources (Development)
Group:      Multimedia/Framework
Requires:   %{name} = %{version}-%{release}

%description devel
SoundPool Library in Tizen Native API (DEV).

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage files
Group: Development/Multimedia

%description gcov
Collection of files related to line coverage using gcov.
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build
export ENABLE_ALURE=1

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

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
%license LICENSE.APLv2
%{_libdir}/lib%{name}.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib%{name}.so

%files tools
%manifest %{name}.manifest
%{_bindir}/*

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
