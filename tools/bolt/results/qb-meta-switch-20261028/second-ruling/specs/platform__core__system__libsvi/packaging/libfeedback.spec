Name:       libfeedback
Summary:    Feedback library
Version:    0.2.0
Release:    1
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
source1:	libfeedback.manifest
source2:	svi-data.manifest
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(mm-keysound)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-media-sound-manager)
BuildRequires:  pkgconfig(capi-media-wav-player)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libsyscommon)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-creds-self)
Requires: %{name}-isu

%if 0%{?gcov:1}
BuildRequires: lcov
%endif

Requires:	svi-data-compat = %{version}-%{release}
Recommends:	svi-data-profile_common = %{version}-%{release}

%description
Feedback library for playing sound and vibration


%package devel
Summary:    Feedback library for (devel)
Group:      Development/Libraries
Requires:   libfeedback = %{version}-%{release}

%description devel
Feedback library for playing sound and vibration (devel)

%package -n svi-data
Summary: 	svi resource package
Group:		Development/Libraries

%description -n svi-data
svi resource package

%package -n svi-data-profile_common
Summary:	svi resource package
Provides:	svi-data-compat = %{version}-%{release}
Provides:	svi-data-profile_tv = %{version}-%{release}
Provides:	svi-data-profile_ivi = %{version}-%{release}
%description -n svi-data-profile_common
default set for svi resource package.

%package test
Summary: Libfeedback test tool
Group: System/Utilities
Requires: libfeedback = %{version}-%{release}
%description test
Test-tool for libfeedback API.
This package can be installed optional for API test.

%if 0%{?gcov:1}
%package gcov
Summary:  Feedback library for (gcov)
Group:    Development/Libraries
%description gcov
Feedback library for playing sound and vibration (gcov)
%endif

%isu_package

%prep
%setup -q

%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

export CFLAGS="$CFLAGS -DTIZEN_ENGINEER_MODE"
cp %{SOURCE1} .
cp %{SOURCE2} .

%cmake . \
		-DCMAKE_INSTALL_PREFIX=%{_prefix} \
		-DTZ_SYS_RO_SHARE=%{_datadir} \
		-DTZ_SYS_SHARE=%{TZ_SYS_SHARE}
make

%install
rm -rf %{buildroot}

%make_install
cd %{buildroot}%{_datadir}
mv common feedback
cd -

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libfeedback.so.*
%license LICENSE
%manifest libfeedback.manifest

%files devel
%defattr(-,root,root,-)
%{_includedir}/feedback/*.h
%{_libdir}/libfeedback.so
%{_libdir}/pkgconfig/feedback.pc

%files -n svi-data
%defattr(666,app,app,-)
%license LICENSE
%manifest svi-data.manifest

%files -n svi-data-profile_common
%defattr(644,root,root,-)
%{_datadir}/feedback/*
%license LICENSE
%manifest svi-data.manifest

%files test
%manifest libfeedback.manifest
%license LICENSE
%{_bindir}/feedback-test

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
