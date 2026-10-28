%define enable_tools 1

Name:       capi-media-radio
Summary:    A Radio library in Tizen Native API
Version:    0.1.21
Release:    0
Group:      API/C API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	capi-media-radio.manifest
Source1002: 	capi-media-radio-tools.manifest
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(mm-radio)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
%if "%{enable_tools}" == "1"
BuildRequires:  pkgconfig(glib-2.0)
%endif
BuildRequires:  cmake

%description
A Radio library in Tizen Native API.

%package devel
Summary:    A Radio library in Tizen Native API (Development)
Group:      Development/API
Requires:   %{name} = %{version}-%{release}

%description devel
A Radio library in Tizen Native API (Development).


%if "%{enable_tools}" == "1"
%package tools
Summary:    A test app for Radio library in Tizen Native API
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}

%description tools
A test app for Radio library in Tizen Native API
%endif

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Radio library in Tizen C API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is tested as gcov for a radio library in Tizen native API
%endif

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
%if "%{enable_tools}" == "1"
	-DENABLE_TOOLS=YES\
%endif
	-DFULLVER=%{version}\
	-DMAJORVER=${MAJORVER}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install
%if "%{enable_tools}" == "1"
mkdir -p %{buildroot}%{_bindir}
cp test/radio_test %{buildroot}%{_bindir}
%endif
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
%defattr(-,root,root,-)
%{_libdir}/libcapi-media-radio.so.*
%license LICENSE.Apache-2.0

%files devel
%defattr(-,root,root,-)
/usr/include/media/radio.h
%{_libdir}/pkgconfig/capi-media-radio.pc
%{_libdir}/libcapi-media-radio.so

%if "%{enable_tools}" == "1"
%files tools
%manifest %{name}-tools.manifest
%defattr(-,root,root,-)
%license LICENSE.Apache-2.0
%{_bindir}/*
%endif

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
