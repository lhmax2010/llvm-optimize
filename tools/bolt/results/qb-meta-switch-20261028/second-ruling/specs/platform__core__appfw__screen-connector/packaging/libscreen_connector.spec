Name: libscreen_connector
Summary: Library for developing the application
Version: 1.9.14
Release: 1
Group: Applications/Core Applications
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1001: %{name}_watcher.manifest
Source1002: %{name}_watcher_evas.manifest
Source1003: %{name}_provider.manifest
Source1004: %{name}_remote_surface.manifest
Source1005: %{name}_remote_surface_evas.manifest
Source1006: %{name}_launcher_service.manifest
Source1007: %{name}_launcher_service_evas.manifest
Source1008: %{name}_shared_widget_launch.manifest
Source1009: %{name}_input.manifest
Source1010: %{name}_provider_tcore.manifest
Source1011: %{name}_remote_surface_tcore.manifest
Source1012: %{name}_watcher_tcore.manifest
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(wayland-tbm-client)
BuildRequires: pkgconfig(elementary)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(ecore-wl2)
BuildRequires: pkgconfig(tizen-core)
BuildRequires: pkgconfig(tizen-core-wl)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(tzsh-launcher-service)
BuildRequires: pkgconfig(libtbm)
BuildRequires: pkgconfig(rpc-port)
BuildRequires: tidl

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
API for creating a new instance of the widget and managing its life-cycle.

%package devel
Summary: Development Library for widget Viewer Application (dev)
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Header and package configuration files for the widget viewer development

%package unittests
Summary:    %{name} unittests binary

%description unittests
unittests binary

%if 0%{?gcov:1}
%package gcov
Summary:  Screen Connector(gcov)
Group:    Application Framework/Libraries

%description gcov
gcov objects of a screen-connector library
%endif

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .
cp %{SOURCE1003} .
cp %{SOURCE1004} .
cp %{SOURCE1005} .
cp %{SOURCE1006} .
cp %{SOURCE1007} .
cp %{SOURCE1008} .
cp %{SOURCE1009} .
cp %{SOURCE1010} .
cp %{SOURCE1011} .
cp %{SOURCE1012} .

tidlc -p -l C++ -i tidl/screen_connector_input.tidl -o screen_connector_input_proxy
tidlc -s -l C++ -i tidl/screen_connector_input.tidl -o screen_connector_input_stub
mv screen_connector_input_* screen_connector_input/

%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

export CFLAGS="$CFLAGS -DEFL_BETA_API_SUPPORT"
export CXXFLAGS="$CXXFLAGS -DEFL_BETA_API_SUPPORT"
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DTZ_SYS_SHARE=/usr/share -DMAJORVER=${MAJORVER} -DFULLVER=%{version} -DBIN_INSTALL_DIR:PATH=%{_bindir} -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
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

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/%{name}-unittest
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
export LD_LIBRARY_PATH=../../screen_connector_remote_surface_tcore:../../screen_connector_remote_surface:../../screen_connector_input
ctest -V

%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o screen-connector.info
genhtml screen-connector.info -o screen-connector.out
zip -r screen-connector.zip screen-connector.out
install -m 0644 screen-connector.zip %{buildroot}%{_datadir}/gcov/obj/
%endif

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

#################################################
# libscreen_connector_watcher
#################################################
%package -n %{name}_watcher
Summary: Library for developing the screen connector watcher
Group: Applications/Core Applications
License: Apache-2.0

%description -n %{name}_watcher
Provider APIs to develop the screen connector watcher application.

%package -n %{name}_watcher-devel
Summary: Screen connector watcher application development library (dev)
Group: Development/Libraries
Requires: %{name}_watcher

%description -n %{name}_watcher-devel
Header & package configuration files to support development of the widget viewer applications.

%post -n %{name}_watcher -p /sbin/ldconfig
%postun -n %{name}_watcher -p /sbin/ldconfig

%files -n %{name}_watcher
%manifest %{name}_watcher.manifest
%attr(0644,root,root) %{_libdir}/%{name}_watcher.so.*
%license LICENSE

%files -n %{name}_watcher-devel
%{_includedir}/screen_connector_watcher/*.h
%{_libdir}/pkgconfig/screen_connector_watcher.pc
%{_libdir}/%{name}_watcher.so

#################################################
# libscreen_connector_watcher_tcore
#################################################
%package -n %{name}_watcher_tcore
Summary: Library for developing the screen connector watcher
Group: Applications/Core Applications
License: Apache-2.0

%description -n %{name}_watcher_tcore
Provider APIs to develop the screen connector watcher application.

%package -n %{name}_watcher_tcore-devel
Summary: Screen connector watcher application development library (dev)
Group: Development/Libraries
Requires: %{name}_watcher_tcore

%description -n %{name}_watcher_tcore-devel
Header & package configuration files to support development of the widget viewer applications.

%post -n %{name}_watcher_tcore -p /sbin/ldconfig
%postun -n %{name}_watcher_tcore -p /sbin/ldconfig

%files -n %{name}_watcher_tcore
%manifest %{name}_watcher_tcore.manifest
%attr(0644,root,root) %{_libdir}/%{name}_watcher_tcore.so.*
%license LICENSE

%files -n %{name}_watcher_tcore-devel
%{_includedir}/screen_connector_watcher_tcore/*.h
%{_libdir}/pkgconfig/screen_connector_watcher_tcore.pc
%{_libdir}/%{name}_watcher_tcore.so

#################################################
# libscreen_connector_provider
#################################################
%package -n %{name}_provider
Summary: Library for developing the screen connector provider
Group: Applications/Core Applications
License: Apache-2.0

%description -n %{name}_provider
Provider APIs to develop the screen connector provider application.

%package -n %{name}_provider-devel
Summary: Screen connector provider application development library (dev)
Group: Development/Libraries
Requires: %{name}_provider

%description -n %{name}_provider-devel
Header & package configuration files to support development of the widget viewer applications.

%post -n %{name}_provider -p /sbin/ldconfig
%postun -n %{name}_provider -p /sbin/ldconfig

%files -n %{name}_provider
%manifest %{name}_provider.manifest
%attr(0644,root,root) %{_libdir}/%{name}_provider.so.*
%license LICENSE

%files -n %{name}_provider-devel
%{_includedir}/screen_connector_provider/*.h
%{_libdir}/pkgconfig/screen_connector_provider.pc
%{_libdir}/%{name}_provider.so

#################################################
# libscreen_connector_provider_tcore
#################################################
%package -n %{name}_provider_tcore
Summary: Library for developing the screen connector provider using tizen-core-wayland
Group: Applications/Core Applications
License: Apache-2.0

%description -n %{name}_provider_tcore
Provider APIs to develop the screen connector provider application.

%package -n %{name}_provider_tcore-devel
Summary: Screen connector provider application development library (dev)
Group: Development/Libraries
Requires: %{name}_provider

%description -n %{name}_provider_tcore-devel
Header & package configuration files to support development of the widget viewer applications.

%post -n %{name}_provider_tcore -p /sbin/ldconfig
%postun -n %{name}_provider_tcore -p /sbin/ldconfig

%files -n %{name}_provider_tcore
%manifest %{name}_provider_tcore.manifest
%attr(0644,root,root) %{_libdir}/%{name}_provider_tcore.so.*
%license LICENSE

%files -n %{name}_provider_tcore-devel
%{_includedir}/screen_connector_provider_tcore/*.h
%{_libdir}/pkgconfig/screen_connector_provider_tcore.pc
%{_libdir}/%{name}_provider_tcore.so

#################################################
# libscreen_connector_watcher_evas
#################################################
%package -n %{name}_watcher_evas
Summary: Library for developing the screen connector watcher evas
Group: Applications/Core Applications
License: Apache-2.0

%description -n %{name}_watcher_evas
Provider APIs to develop the widget viewer EFL application.

%package -n %{name}_watcher_evas-devel
Summary: Screen connector watcher evas application development library (dev)
Group: Development/Libraries
Requires: %{name}_watcher_evas

%description -n %{name}_watcher_evas-devel
Header & package configuration files to support development of the widget viewer applications.

%post -n %{name}_watcher_evas -p /sbin/ldconfig
%postun -n %{name}_watcher_evas -p /sbin/ldconfig

%files -n %{name}_watcher_evas
%manifest %{name}_watcher_evas.manifest
%attr(0644,root,root) %{_libdir}/%{name}_watcher_evas.so.*
%license LICENSE

%files -n %{name}_watcher_evas-devel
%{_includedir}/screen_connector_watcher_evas/*.h
%{_libdir}/pkgconfig/screen_connector_watcher_evas.pc
%{_libdir}/%{name}_watcher_evas.so

#################################################
# libscreen_connector_remote_surface
#################################################
%package -n %{name}_remote_surface
Summary: Library for developing the screen connector remote surface
Group: Applications/Core Applications
License: Apache-2.0

%description -n %{name}_remote_surface
Provider APIs to develop the screen connector viewer application.

%package -n %{name}_remote_surface-devel
Summary: Screen connector watcher application development library (dev)
Group: Development/Libraries
Requires: %{name}_remote_surface

%description -n %{name}_remote_surface-devel
Header & package files to support development of the widget viewer applications.

%post -n %{name}_remote_surface -p /sbin/ldconfig
%postun -n %{name}_remote_surface -p /sbin/ldconfig

%files -n %{name}_remote_surface
%manifest %{name}_remote_surface.manifest
%attr(0644,root,root) %{_libdir}/%{name}_remote_surface.so.*
%license LICENSE

%files -n %{name}_remote_surface-devel
%{_includedir}/screen_connector_remote_surface/*.h
%{_libdir}/pkgconfig/screen_connector_remote_surface.pc
%{_libdir}/%{name}_remote_surface.so

#################################################
# libscreen_connector_remote_surface_tcore
#################################################
%package -n %{name}_remote_surface_tcore
Summary: Library for developing the screen connector remote surface
Group: Applications/Core Applications
License: Apache-2.0

%description -n %{name}_remote_surface_tcore
Provider APIs to develop the screen connector viewer application.

%package -n %{name}_remote_surface_tcore-devel
Summary: Screen connector watcher application development library (dev)
Group: Development/Libraries
Requires: %{name}_remote_surface

%description -n %{name}_remote_surface_tcore-devel
Header & package files to support development of the widget viewer applications.

%post -n %{name}_remote_surface_tcore -p /sbin/ldconfig
%postun -n %{name}_remote_surface_tcore -p /sbin/ldconfig

%files -n %{name}_remote_surface_tcore
%manifest %{name}_remote_surface_tcore.manifest
%attr(0644,root,root) %{_libdir}/%{name}_remote_surface_tcore.so.*
%license LICENSE

%files -n %{name}_remote_surface_tcore-devel
%{_includedir}/screen_connector_remote_surface_tcore/*.h
%{_libdir}/pkgconfig/screen_connector_remote_surface_tcore.pc
%{_libdir}/%{name}_remote_surface_tcore.so

#################################################
# libscreen_connector_remote_surface_mock
#################################################
%package -n %{name}_remote_surface_mock
Summary: Mockup header for developing the screen connector remote surface
Group: Applications/Core Applications
License: Apache-2.0

%description -n %{name}_remote_surface_mock
Provider APIs to develop unittests.

%license LICENSE

%files -n %{name}_remote_surface_mock
%{_includedir}/screen_connector_remote_surface_mock/*.h
%{_libdir}/pkgconfig/screen_connector_remote_surface_mock.pc

#################################################
# libscreen_connector_remote_surface_evas
#################################################
%package -n %{name}_remote_surface_evas
Summary: Library for developing the screen connector remote surface evas
Group: Applications/Core Applications
Requires: %{name}_remote_surface
License: Apache-2.0

%description -n %{name}_remote_surface_evas
Provider APIs to develop the screen connector viewer application.

%package -n %{name}_remote_surface_evas-devel
Summary: Screen connector watcher application development library (dev)
Group: Development/Libraries
Requires: %{name}_remote_surface_evas

%description -n %{name}_remote_surface_evas-devel
Header & package files to support development of the widget viewer applications.

%post -n %{name}_remote_surface_evas -p /sbin/ldconfig
%postun -n %{name}_remote_surface_evas -p /sbin/ldconfig

%files -n %{name}_remote_surface_evas
%manifest %{name}_remote_surface_evas.manifest
%attr(0644,root,root) %{_libdir}/%{name}_remote_surface_evas.so.*
%license LICENSE

%files -n %{name}_remote_surface_evas-devel
%{_includedir}/screen_connector_remote_surface_evas/*.h
%{_libdir}/pkgconfig/screen_connector_remote_surface_evas.pc
%{_libdir}/%{name}_remote_surface_evas.so

#################################################
# libscreen_connector_remote_surface_evas_mock
#################################################
%package -n %{name}_remote_surface_evas_mock
Summary: Mockup header for developing the screen connector remote surface evas
Group: Applications/Core Applications
Requires: %{name}_remote_surface_mock
License: Apache-2.0

%description -n %{name}_remote_surface_evas_mock
Provider APIs to develop unittests.

%license LICENSE

%files -n %{name}_remote_surface_evas_mock
%{_includedir}/screen_connector_remote_surface_evas_mock/*.h
%{_libdir}/pkgconfig/screen_connector_remote_surface_evas_mock.pc

#################################################
# libscreen_connector-unittest
#################################################
%package    unittest
Summary:    libscreen-connector unittests
Group:      Development/Libraries
Requires:   %{name}_watcher_evas

%description unittest
libscreen-connector unittests

%files unittest
%{_bindir}/%{name}-unittest
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# libscreen_connector_launcher_service
#################################################
%package -n %{name}_launcher_service
Summary: Library for developing the screen connector launcher service
Group: Applications/Core Applications
License: Apache-2.0

%description -n %{name}_launcher_service
Launcher Service APIs to develop the screen connector launcher application.

%package -n %{name}_launcher_service-devel
Summary: Screen connector launcher application development library (dev)
Group: Development/Libraries
Requires: %{name}_launcher_service

%description -n %{name}_launcher_service-devel
Header & package files to support development of the launcher applications.

%post -n %{name}_launcher_service -p /sbin/ldconfig

%postun -n %{name}_launcher_service -p /sbin/ldconfig

%files -n %{name}_launcher_service
%manifest %{name}_launcher_service.manifest
%attr(0644,root,root) %{_libdir}/%{name}_launcher_service.so.*
%license LICENSE

%files -n %{name}_launcher_service-devel
%{_includedir}/screen_connector_launcher_service/*
%{_libdir}/pkgconfig/screen_connector_launcher_service.pc
%{_libdir}/%{name}_launcher_service.so

#################################################
# libscreen_connector_launcher_service_evas
#################################################
%package -n %{name}_launcher_service_evas
Summary: Library for developing the screen connector launcher service evas
Group: Applications/Core Applications
License: Apache-2.0

%description -n %{name}_launcher_service_evas
Launcher Service Evas APIs to develop the screen connector launcher application.

%package -n %{name}_launcher_service_evas-devel
Summary: Screen connector launcher service evas application development library (dev)
Group: Development/Libraries
Requires: %{name}_launcher_service_evas

%description -n %{name}_launcher_service_evas-devel
Header & package files to support development of the launcher service evas applications.

%post -n %{name}_launcher_service_evas -p /sbin/ldconfig

%postun -n %{name}_launcher_service_evas -p /sbin/ldconfig

%files -n %{name}_launcher_service_evas
%manifest %{name}_launcher_service_evas.manifest
%attr(0644,root,root) %{_libdir}/%{name}_launcher_service_evas.so.*
%license LICENSE

%files -n %{name}_launcher_service_evas-devel
%{_includedir}/screen_connector_launcher_service_evas/*
%{_libdir}/pkgconfig/screen_connector_launcher_service_evas.pc
%{_libdir}/%{name}_launcher_service_evas.so

#################################################
# libscreen_connector_shared_widget_launch
#################################################
%package -n %{name}_shared_widget_launch
Summary: Library for developing the screen connector shared launch widget
Group: Applications/Core Applications
License: Apache-2.0

%description -n %{name}_shared_widget_launch
Shared Widget Launch APIs to develop the screen connector launcher application.

%package -n %{name}_shared_widget_launch-devel
Summary: Screen connector shared widget launch application development library (dev)
Group: Development/Libraries
Requires: %{name}_launcher_service_evas

%description -n %{name}_shared_widget_launch-devel
Header & package files to support development of the shared widget launch applications.

%post -n %{name}_shared_widget_launch -p /sbin/ldconfig

%postun -n %{name}_shared_widget_launch -p /sbin/ldconfig

%files -n %{name}_shared_widget_launch
%manifest %{name}_shared_widget_launch.manifest
%attr(0644,root,root) %{_libdir}/%{name}_shared_widget_launch.so.*
%license LICENSE

%files -n %{name}_shared_widget_launch-devel
%{_includedir}/screen_connector_shared_widget_launch/*
%{_libdir}/pkgconfig/screen_connector_shared_widget_launch.pc
%{_libdir}/%{name}_shared_widget_launch.so

#################################################
# libscreen_connector_input
#################################################
%package -n %{name}_input
Summary: Library for developing the screen connector input
Group: Applications/Core Applications
License: Apache-2.0

%description -n %{name}_input
Input APIs to develop the screen connector provider and watcher applications.

%package -n %{name}_input-devel
Summary: Screen connector input application development library (dev)
Group: Development/Libraries

%description -n %{name}_input-devel
Header & package files to support development of the screen connector applications.

%post -n %{name}_input -p /sbin/ldconfig

%postun -n %{name}_input -p /sbin/ldconfig

%files -n %{name}_input
%manifest %{name}_input.manifest
%attr(0644,root,root) %{_libdir}/%{name}_input.so.*
%license LICENSE

%files -n %{name}_input-devel
%{_includedir}/screen_connector_input/*
%{_libdir}/pkgconfig/screen_connector_input.pc
%{_libdir}/%{name}_input.so


# End of a file
