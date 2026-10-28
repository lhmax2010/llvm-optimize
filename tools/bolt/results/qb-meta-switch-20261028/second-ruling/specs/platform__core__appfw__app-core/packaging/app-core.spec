Name:           app-core
Summary:        Application basic
Version:        1.28.10
Release:        0
Group:          Application Framework/Libraries
License:        Apache-2.0
Source0:        app-core-%{version}.tar.gz
Source1001:     app-core.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(ecore-wl2)
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(libsessiond)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(sensor)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-core-wl)
BuildRequires:  pkgconfig(tizen-extension-client)
BuildRequires:  pkgconfig(tizen-shared-queue)
BuildRequires:  pkgconfig(tizen-launch-client)
BuildRequires:  pkgconfig(ttrace)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-tbm-client)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
SLP common application basic


%package efl
Summary:    App basic EFL
Group:      Development/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description efl
Application basic EFL


%package efl-devel
Summary:    App basic EFL (devel)
Group:      Development/Libraries
Requires:   %{name}-efl = %{version}-%{release}
Requires:   %{name}-ui-devel = %{version}-%{release}

%description efl-devel
Application basic EFL (devel)

%package multicontext
Summary:    Application core for multi-context
Group:      Development/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description multicontext
Application core for multi-context

%package multicontext-devel
Summary:    Application core for multi-context (devel)
Group:      Development/Libraries
Requires:   %{name}-multicontext = %{version}-%{release}
Requires:   %{name}-common-devel = %{version}-%{release}

%description multicontext-devel
Application core for multi-context (devel)

%package multiwindow
Summary:    Application core for multiwindow
Group:      Development/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description multiwindow
Application core for multiwindow

%package multiwindow-devel
Summary:    Application core for multiwindow (devel)
Group:      Development/Libraries
Requires:   %{name}-multiwindow = %{version}-%{release}
Requires:   %{name}-common-devel = %{version}-%{release}
Requires:   %{name}-multicontext-devel = %{version}-%{release}

%description multiwindow-devel
Application core for multiwindow (devel)

%package multiwindow-tcore
Summary:    Application core for multiwindow
Group:      Development/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description multiwindow-tcore
Application core for multiwindow

%package multiwindow-tcore-devel
Summary:    Application core for multiwindow (devel)
Group:      Development/Libraries
Requires:   %{name}-multiwindow = %{version}-%{release}
Requires:   %{name}-common-devel = %{version}-%{release}
Requires:   %{name}-multicontext-devel = %{version}-%{release}

%description multiwindow-tcore-devel
Application core for multiwindow (devel)

%package common
Summary:    App basics common
Group:      Development/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description common
Application basics common


%package common-devel
Summary:    App basics common (devel)
Group:      Development/Libraries
Requires:   %{name}-common = %{version}-%{release}
Requires:   pkgconfig(sensor)
Requires:   pkgconfig(vconf)
Requires:   pkgconfig(elementary)
Requires:   pkgconfig(aul)

%description common-devel
Application basics common (devel)

%package ui
Summary:    App basic UI
Group:      Development/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description ui
Application basic UI

%package ui-devel
Summary:    App basic UI (devel)
Group:      Development/Libraries
Requires:   %{name}-ui = %{version}-%{release}
Requires:   %{name}-common-devel = %{version}-%{release}

%description ui-devel
Application basic EFL (devel)

%package tcore
Summary:    App basic UI using Tizen core
Group:      Development/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description tcore
Application basic UI using Tizen core

%package tcore-devel
Summary:    App basic UI using Tizen core(devel)
Group:      Development/Libraries
Requires:   %{name}-tcore = %{version}-%{release}
Requires:   %{name}-common-devel = %{version}-%{release}

%description tcore-devel
Application App basic UI using Tizen core(devel)

%package template
Summary:    App basics template
Group:      Development/Libraries

%description template
Application basics template


%if 0%{?gcov:1}
%package gcov
Summary:  Application Core API(gcov)
Group:    Application Framework/Libraries

%description gcov
gcov objects of a widget application library
%endif

%package unittests
Summary:    %{name} unittests binary

%description unittests
unittests binary

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

%{?_toolchain:
%if %{toolchain_is clang}
export CFLAGS="$CFLAGS -Wno-error=inconsistent-missing-override "
%endif
}

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
	-DENABLE_GTK=OFF \
	-DFULLVER=%{version} \
	-DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
	-DMAJORVER=${MAJORVER}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/app-core_unittests
}

teardown() {
    echo "teardown start"
}

main() {
    setup
    test_main
    teardown
}

main "\$*"
EOF

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}/

%check
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o %{name}.out --legend --show-details
zip -r %{name}.zip %{name}.out
install -m 0644 %{name}.zip %{buildroot}%{_datadir}/gcov/
%endif


%post -n app-core-efl -p /sbin/ldconfig

%postun -n app-core-efl -p /sbin/ldconfig

%post -n app-core-multicontext -p /sbin/ldconfig

%postun -n app-core-multicontext -p /sbin/ldconfig

%post -n app-core-multiwindow -p /sbin/ldconfig

%postun -n app-core-multiwindow -p /sbin/ldconfig

%post -n app-core-common -p /sbin/ldconfig

%postun -n app-core-common -p /sbin/ldconfig

%post -n app-core-ui -p /sbin/ldconfig

%postun -n app-core-ui -p /sbin/ldconfig

%files efl
%manifest %{name}.manifest
%{_libdir}/libappcore-efl.so.*

%{_libdir}/libapp-core-efl-cpp.so.*
%license LICENSE

%files efl-devel
%manifest %{name}.manifest
%{_includedir}/appcore/appcore-efl.h
%{_includedir}/appcore/appcore_efl_base.h
%{_libdir}/libappcore-efl.so
%{_libdir}/pkgconfig/appcore-efl.pc

%{_includedir}/appcore_cpp/app_core_efl_base.hh
%{_libdir}/libapp-core-efl-cpp.so
%{_libdir}/pkgconfig/app-core-efl-cpp.pc

%files multicontext
%manifest %{name}.manifest
%{_libdir}/libapp-core-multi-context-cpp.so.*
%license LICENSE

%files multicontext-devel
%manifest %{name}.manifest
%{_includedir}/appcore_cpp/app_core_multi_context_base.hh
%{_includedir}/appcore_cpp/api/app_core_multi_context_plugin.h
%{_libdir}/libapp-core-multi-context-cpp.so
%{_libdir}/pkgconfig/app-core-multi-context-cpp.pc

%files multiwindow
%manifest %{name}.manifest
%{_libdir}/libappcore-multiwindow.so.*

%{_libdir}/libapp-core-multi-window-cpp.so.*
%license LICENSE

%files multiwindow-devel
%manifest %{name}.manifest
%{_includedir}/appcore/appcore_multiwindow_base.h
%{_libdir}/libappcore-multiwindow.so
%{_libdir}/pkgconfig/appcore-multiwindow.pc

%{_includedir}/appcore_cpp/app_core_multi_window_base.hh
%{_includedir}/appcore_cpp/api/app_core_multi_window_plugin.h
%{_libdir}/libapp-core-multi-window-cpp.so
%{_libdir}/pkgconfig/app-core-multi-window-cpp.pc

%files multiwindow-tcore
%manifest %{name}.manifest
%{_libdir}/libapp-core-multi-window-tcore-cpp.so.*
%license LICENSE

%files multiwindow-tcore-devel
%manifest %{name}.manifest
%{_includedir}/appcore_cpp/app_core_multi_window_base.hh
%{_libdir}/libapp-core-multi-window-tcore-cpp.so
%{_libdir}/pkgconfig/app-core-multi-window-tcore-cpp.pc

%files common
%manifest %{name}.manifest
%{_libdir}/libappcore-common.so.*

%{_libdir}/libapp-core-cpp.so.*
%{_libdir}/libapp-core-rotation-cpp.so.*
%license LICENSE

%files common-devel
%manifest %{name}.manifest
%{_libdir}/libappcore-common.so
%{_libdir}/pkgconfig/appcore-common.pc
%{_includedir}/appcore/appcore-common.h
%{_includedir}/appcore/appcore_base.h
%{_includedir}/appcore/appcore_watchdog.h
%{_includedir}/appcore/appcore_base_control.h

%{_includedir}/appcore_cpp/app_core_base.hh
%{_includedir}/appcore_cpp/interface_app_core.hh
%{_includedir}/appcore_cpp/interface_app_core_ui.hh
%{_includedir}/appcore_cpp/interface_app_core_ui_event.hh
%{_includedir}/appcore_cpp/interface_main_loop.hh
%{_includedir}/appcore_cpp/interface_window.hh
%{_includedir}/appcore_cpp/api/app_core_base_control.h
%{_includedir}/appcore_cpp/api/app_core_base.h
%{_libdir}/libapp-core-cpp.so
%{_libdir}/pkgconfig/app-core-cpp.pc

%{_includedir}/appcore_cpp/app_core_rotation.hh
%{_libdir}/libapp-core-rotation-cpp.so
%{_libdir}/pkgconfig/app-core-rotation-cpp.pc

%files ui
%manifest %{name}.manifest
%{_libdir}/libappcore-ui.so.*

%{_libdir}/libapp-core-ui-cpp.so.*
%license LICENSE

%files ui-devel
%manifest %{name}.manifest
%{_includedir}/appcore/appcore_ui_base.h
%{_libdir}/libappcore-ui.so
%{_libdir}/pkgconfig/appcore-ui.pc

%{_includedir}/appcore_cpp/ecore/include/app_core_task_base.hh
%{_includedir}/appcore_cpp/ecore/include/app_core_ui_base.hh
%{_includedir}/appcore_cpp/ecore/include/app_core_ui_thread_base.hh
%{_includedir}/appcore_cpp/api/app_core_ui_base.h
%{_libdir}/libapp-core-ui-cpp.so
%{_libdir}/pkgconfig/app-core-ui-cpp.pc

%files tcore
%manifest %{name}.manifest
%{_libdir}/libapp-core-tcore-cpp.so.*
%license LICENSE

%files tcore-devel
%manifest %{name}.manifest
%{_includedir}/appcore_cpp/tcore/include/app_core_task_base.hh
%{_includedir}/appcore_cpp/tcore/include/app_core_tcore_base.hh
%{_includedir}/appcore_cpp/tcore/include/app_core_ui_base.hh
%{_includedir}/appcore_cpp/tcore/include/app_core_ui_thread_base.hh
%{_libdir}/libapp-core-tcore-cpp.so
%{_libdir}/pkgconfig/app-core-tcore-cpp.pc

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif

%files unittests
%attr(0755,root,root) %{_bindir}/app-core_unittests
%attr(0755,root,root) %{_bindir}/tizen-unittests/%{name}/run-unittest.sh
