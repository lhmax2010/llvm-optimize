Name:       ui-gadget-1
Summary:    UI Gadget Library
Version:    0.2.14
Release:    1
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	ui-gadget-1.manifest
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(appcore-efl)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(appsvc)
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(capi-appfw-application)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  cmake
BuildRequires:  edje-bin
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(ecore-wl2)

%description
UI gadget library (development headers)

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for %{name}

%if 0%{?gcov:1}
%package gcov
Summary:  UI Gadget Library(gcov)
Group:    System/API

%description gcov
gcov objects of UI Gadget Library
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

export CFLAGS="$CFLAGS -DEFL_BETA_API_SUPPORT "
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake -DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	-DTZ_SYS_ETC=%TZ_SYS_ETC \
	.

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

%post
/sbin/ldconfig
ln -sf %{TZ_SYS_BIN}/ug-client %{TZ_SYS_BIN}/ug-launcher

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_libdir}/lib%{name}-efl-engine.so
/usr/share/edje/ug_effect.edj
%{_bindir}/ug-client
/usr/share/edje/ug-client/*.edj
%license LICENSE

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/ug-1/*.h
%{_libdir}/libui-gadget-1.so
%{_libdir}/pkgconfig/%{name}.pc

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
