Name:       dali-application
Summary:    Tizen C++ Application Models Framework
Version:    1.2.1
Release:    1
Group:      Application Framework/Core
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dali2-core)
BuildRequires:  pkgconfig(dali2-ui-foundation)
BuildRequires:  pkgconfig(dali2-adaptor)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(app-core-cpp)
BuildRequires:  pkgconfig(app-core-tcore-cpp)
BuildRequires:  pkgconfig(dali2-adaptor-integration)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-core-wl)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(gtest)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(sensor)
BuildRequires:  gettext-devel

# The ui_app_main() reference application of the lifecycle integration test is
# built only on request: gbs build --define 'build_reference_app 1'
%{!?build_reference_app:%global build_reference_app 0}
%if %{build_reference_app}
BuildRequires:  pkgconfig(capi-appfw-application)
BuildRequires:  pkgconfig(elementary)
%endif

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Tizen C++ Application Models Framework library.

%package devel
Summary:    Tizen C++ Application Models Framework (Development)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development headers and package config for the Tizen C++ Application Models Framework.

%package -n app-core-dali-cpp
Summary:    Tizen C++ AppCore DALi Adaptor
Group:      Application Framework/Core

%description -n app-core-dali-cpp
Tizen C++ AppCore DALi Adaptor library.

%package -n app-core-dali-cpp-devel
Summary:    Tizen C++ AppCore DALi Adaptor (Development)
Group:      Development/Libraries
Requires:   app-core-dali-cpp = %{version}-%{release}

%description -n app-core-dali-cpp-devel
Development headers and package config for the Tizen C++ AppCore DALi Adaptor.

%package -n dali-gadget
Summary:    Tizen C++ DALi Gadget Framework
Group:      Application Framework/Core

%description -n dali-gadget
Tizen C++ DALi Gadget Framework library.

%package -n dali-gadget-devel
Summary:    Tizen C++ DALi Gadget Framework (Development)
Group:      Development/Libraries
Requires:   dali-gadget = %{version}-%{release}

%description -n dali-gadget-devel
Development headers and package config for the Tizen C++ DALi Gadget Framework.

%package unittests
Summary:    Tizen C++ Application Models Framework Unit Tests
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}

%description unittests
Unit tests for verifying Tizen C++ Application Models Framework.

%package integration-tests
Summary:    Tizen C++ Application Models Framework Integration Tests
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}
Requires:   dali-gadget = %{version}-%{release}
Requires:   app-core-dali-cpp = %{version}-%{release}

%description integration-tests
On-device integration tests: DaliApplication lifecycle and system events
compared with a ui_app_main() application, and DaliGadget behavior. They launch
real applications, so they are not run in the build. Register the packages with
"dali-integration-test setup", then run "dali-integration-test".

%if 0%{?gcov:1}
%package gcov
Summary:    Tizen C++ Application Models Framework (gcov)
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}

%description gcov
gcov coverage report for Tizen C++ Application Models Framework.
%endif

%prep
%setup -q
cp packaging/*.manifest .

%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
	-DENABLE_GTK=OFF \
	-DFULLVER=%{version} \
	-DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
%if %{build_reference_app}
	-DBUILD_REFERENCE_APP=ON \
%endif
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

mkdir -p %{buildroot}/usr/bin/tizen-unittests/dali-application
install -m 0755 unittest/dali-application-unittest %{buildroot}/usr/bin/tizen-unittests/dali-application/

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}/

%check
export LD_LIBRARY_PATH="$PWD/src/dali-application:$PWD/src/app-core-dali-cpp:$PWD/src/dali-gadget:$LD_LIBRARY_PATH"
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors graph,inconsistent,mismatch --no-external -b . -d . -o %{name}.info
genhtml --ignore-errors inconsistent,corrupt %{name}.info -o %{name}.out --legend --show-details
zip -r %{name}.zip %{name}.out
install -m 0644 %{name}.zip %{buildroot}%{_datadir}/gcov/
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n app-core-dali-cpp -p /sbin/ldconfig
%postun -n app-core-dali-cpp -p /sbin/ldconfig

%post -n dali-gadget -p /sbin/ldconfig
%postun -n dali-gadget -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libdali-application.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/appfw/dali_application.h
%{_libdir}/libdali-application.so
%{_libdir}/pkgconfig/dali-application.pc

%files -n app-core-dali-cpp
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libapp-core-dali-cpp.so.*

%files -n app-core-dali-cpp-devel
%defattr(-,root,root,-)
%{_includedir}/appcore_cpp/app_core_dali_base.hh
%{_libdir}/libapp-core-dali-cpp.so
%{_libdir}/pkgconfig/app-core-dali-cpp.pc

%files -n dali-gadget
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libdali-gadget.so.*

%files -n dali-gadget-devel
%defattr(-,root,root,-)
%{_includedir}/appfw/dali_gadget.h
%{_includedir}/appfw/dali_gadget_info.h
%{_includedir}/appfw/dali_gadget_manager.h
%{_libdir}/libdali-gadget.so
%{_libdir}/pkgconfig/dali-gadget.pc

%files unittests
%defattr(-,root,root,-)
%{_bindir}/tizen-unittests/dali-application/dali-application-unittest
%attr(0755,root,root) %{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%files integration-tests
%manifest packaging/%{name}-integration-tests.manifest
%defattr(-,root,root,-)
%{_bindir}/dali-integration-test
%{_datadir}/dali-application/integration-test/
/usr/apps/org.tizen.dali-lifecycle-test/*
/usr/apps/org.tizen.dali-gadget-test/*
/usr/apps/org.tizen.dali-gadget-test-*/*
%{_prefix}/share/packages/org.tizen.dali-lifecycle-test.xml
%{_prefix}/share/packages/org.tizen.dali-gadget-test.xml
%{_prefix}/share/packages/org.tizen.dali-gadget-test-*.xml
%if %{build_reference_app}
/usr/apps/org.tizen.dali-lifecycle-reference/*
%{_prefix}/share/packages/org.tizen.dali-lifecycle-reference.xml
%endif

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
