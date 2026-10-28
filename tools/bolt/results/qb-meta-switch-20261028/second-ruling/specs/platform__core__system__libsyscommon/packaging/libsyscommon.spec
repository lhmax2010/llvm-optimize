%define libsyscommon_version 5.0.0
%define libsyscommon_plugin_api_common_version 0.1.0
%define libsyscommon_plugin_api_resourced_version 0.1.0
%define libsyscommon_plugin_api_deviced_version 0.1.0
%define libsyscommon_plugin_api_update_control_version 0.1.0
%define libsyscommon_plugin_api_sessiond_version 0.1.0
%define libsyscommon_plugin_api_pass_version 0.1.0
%if "%{?_with_emulator}" == "1"
%define emulator_mode 1
%else
%define emulator_mode 0
%endif

%define WITH_EBPF 1

# Disable for VD and DA
%if "%{tizen_profile_name}" == "tv"
%define WITH_EBPF 0
%endif

%if "%{_with_da_profile}" == "1"
%define WITH_EBPF 0
%endif

Name:           libsyscommon
Summary:        System Libraries
Version:        %{libsyscommon_version}
Release:        0%{?release_flags}
License:        MIT
Group:          System/Libraries
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(cmocka)
BuildRequires:  pkgconfig(glib-2.0) >= 2.44
BuildRequires:  pkgconfig(gio-2.0) >= 2.44
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(capi-system-resource)

Requires:         /bin/cp
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
System common utility libraries.

%package -n libsyscommon-devel
Summary:        Header files for system common library
License:        MIT
Requires:       libsyscommon = %{version}

%description -n libsyscommon-devel
Development header files for system common library.

%if %{WITH_EBPF}
%package -n libsyscommon-ebpf-devel
Summary:        Shared CMake macros for building eBPF programs
License:        MIT
Requires:       clang >= 10
Requires:       llvm >= 10
Requires:       bpftool
Requires:       libbpf-devel
Requires:       kernel-btf-devel

%description -n libsyscommon-ebpf-devel
This package provides shared CMake macros for building eBPF programs on Tizen.
It includes helper functions for architecture detection and eBPF program compilation.
Consumer projects can use find_package(TizenBpfHelpers) to access these macros.
Installing this package automatically pulls in all required eBPF build tools
(clang, llvm, bpftool, libbpf-devel, kernel-btf-devel).
%endif

# Packages for system plugin api
%package -n libsyscommon-plugin-api-common
Summary:	Common system plugin APIs
Version:	%{libsyscommon_plugin_api_common_version}
License:	MIT

%package -n libsyscommon-plugin-api-common-devel
Summary:	Header files for common system plugin APIs
Version:	%{libsyscommon_plugin_api_common_version}
License:	MIT

%description -n libsyscommon-plugin-api-common-devel
Development header files for common system plugin APIs.

%package -n libsyscommon-plugin-api-resourced
Summary:	System plugin APIs for the resourced
Version:	%{libsyscommon_plugin_api_resourced_version}
License:	MIT

%description -n libsyscommon-plugin-api-resourced
System plugin APIs for the resourced.

%package -n libsyscommon-plugin-api-resourced-devel
Summary:	Header files for system plugin APIs for the resourced
Version:	%{libsyscommon_plugin_api_resourced_version}
License:	MIT

%description -n libsyscommon-plugin-api-resourced-devel
Development header files for system plugin APIs for the resourced.

%package -n libsyscommon-plugin-api-deviced
Summary:	System plugin APIs for the deviced
Version:	%{libsyscommon_plugin_api_deviced_version}
License:	MIT

%description -n libsyscommon-plugin-api-deviced
System plugin APIs for the deviced.

%package -n libsyscommon-plugin-api-deviced-devel
Summary:	Header files for system plugin APIs for the deviced
Version:	%{libsyscommon_plugin_api_deviced_version}
License:	MIT

%description -n libsyscommon-plugin-api-deviced-devel
Development header files for system plugin APIs for the deviced.

%package -n libsyscommon-plugin-api-update-control
Summary:	System plugin API for the update-control
Version:	%{libsyscommon_plugin_api_update_control_version}
License:	MIT

%description -n libsyscommon-plugin-api-update-control
System plugin API for update-control.

%package -n libsyscommon-plugin-api-update-control-devel
Summary:	Header files for system plugin API for update-control
Version:	%{libsyscommon_plugin_api_update_control_version}
License:	MIT

%description -n libsyscommon-plugin-api-update-control-devel
Development header files for system plugin API for update-control.


%package -n libsyscommon-plugin-api-sessiond
Summary:	System plugin API for the sessiond
Version:	%{libsyscommon_plugin_api_sessiond_version}
License:	MIT

%description -n libsyscommon-plugin-api-sessiond
System plugin API for sessiond.

%package -n libsyscommon-plugin-api-sessiond-devel
Summary:	Header files for system plugin API for sessiond
Version:	%{libsyscommon_plugin_api_sessiond_version}
License:	MIT

%description -n libsyscommon-plugin-api-sessiond-devel
Development header files for system plugin API for sessiond.


%package -n libsyscommon-plugin-api-pass-devel
Summary:	Header-only plugin API for PASS (Power Aware System Service)
Version:	%{libsyscommon_plugin_api_pass_version}
License:	MIT

%description -n libsyscommon-plugin-api-pass-devel
Header-only plugin API for PASS (Power Aware System Service).
This package contains only header files - no runtime library is needed.


######


%prep
%setup -q
cp %{SOURCE1001} .

%build
# Tizen uses -D_FORTIFY_SOURCE option, which makes "open" inline,
# preventing the use of __wrap_open in testing.
CFLAGS="$CFLAGS -Wp,-U_FORTIFY_SOURCE"

PLUGIN_API_COMMON_MAJORVER=$(echo %{libsyscommon_plugin_api_common_version} | cut -d'.' -f1)
PLUGIN_API_RESOURCED_MAJORVER=$(echo %{libsyscommon_plugin_api_resourced_version} | cut -d'.' -f1)
PLUGIN_API_DEVICED_MAJORVER=$(echo %{libsyscommon_plugin_api_deviced_version} | cut -d'.' -f1)
PLUGIN_API_UPDATE_CONTROL_MAJORVER=$(echo %{libsyscommon_plugin_api_update_control_version} | cut -d'.' -f1)
PLUGIN_API_SESSIOND_MAJORVER=$(echo %{libsyscommon_plugin_api_sessiond_version} | cut -d'.' -f1)
PLUGIN_API_PASS_MAJORVER=$(echo %{libsyscommon_plugin_api_pass_version} | cut -d'.' -f1)
%cmake . -DFULLVER=%{libsyscommon_version} \
	-DPLUGIN_API_COMMON_VERSION=%{libsyscommon_plugin_api_common_version} \
	-DPLUGIN_API_COMMON_MAJORVER=${PLUGIN_API_COMMON_MAJORVER} \
	-DPLUGIN_API_RESOURCED_VERSION=%{libsyscommon_plugin_api_resourced_version} \
	-DPLUGIN_API_RESOURCED_MAJORVER=${PLUGIN_API_RESOURCED_MAJORVER} \
	-DPLUGIN_API_DEVICED_VERSION=%{libsyscommon_plugin_api_deviced_version} \
	-DPLUGIN_API_DEVICED_MAJORVER=${PLUGIN_API_DEVICED_MAJORVER} \
	-DPLUGIN_API_UPDATE_CONTROL_VERSION=%{libsyscommon_plugin_api_update_control_version} \
	-DPLUGIN_API_UPDATE_CONTROL_MAJORVER=${PLUGIN_API_UPDATE_CONTROL_MAJORVER} \
	-DPLUGIN_API_SESSIOND_VERSION=%{libsyscommon_plugin_api_sessiond_version} \
	-DPLUGIN_API_SESSIOND_MAJORVER=${PLUGIN_API_SESSIOND_MAJORVER} \
	-DPLUGIN_API_PASS_VERSION=%{libsyscommon_plugin_api_pass_version} \
	-DPLUGIN_API_PASS_MAJORVER=${PLUGIN_API_PASS_MAJORVER} \
	-DPLUGIN_API_COMMON_ENABLE_DLOG=1 \
	-DPLUGIN_API_RESOURCED_ENABLE_DLOG=1 \
	-DPLUGIN_API_DEVICED_ENABLE_DLOG=1 \
	-DPLUGIN_API_UPDATE_CONTROL_ENABLE_DLOG=1 \
	-DPLUGIN_API_SESSIOND_ENABLE_DLOG=1 \
	-DPLUGIN_API_PASS_ENABLE_DLOG=1 \
	-DEMULATOR_MODE=%{emulator_mode}
make %{?_smp_mflags}

%install
%make_install

%if %{WITH_EBPF}
# Install eBPF helper CMake files
install -d -m 755 %{buildroot}%{_libdir}/cmake/TizenBpfHelpers
install -m 644 cmake/TizenBpfHelpers.cmake %{buildroot}%{_libdir}/cmake/TizenBpfHelpers/
install -m 644 cmake/TizenBpfHelpersConfig.cmake %{buildroot}%{_libdir}/cmake/TizenBpfHelpers/TizenBpfHelpersConfig.cmake
%endif

# make sure debugsources.list exist, it used by rpm macro in %file
# section.
touch debugsources.list

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.MIT
%{_libdir}/libsyscommon.so.*

%files -n libsyscommon-devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.MIT
%{_libdir}/libsyscommon.so
%{_includedir}/libsyscommon/*.h
%{_libdir}/pkgconfig/libsyscommon.pc

%description -n libsyscommon-plugin-api-common
Common system plugin APIs to load another APIs from backend.

%files -n libsyscommon-plugin-api-common
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.MIT
%{_libdir}/libsyscommon-plugin-api-common.so.*

%post -n libsyscommon-plugin-api-common
/sbin/ldconfig

%files -n libsyscommon-plugin-api-common-devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.MIT
%{_includedir}/system/syscommon-plugin-common*.h
%{_libdir}/pkgconfig/libsyscommon-plugin-api-common.pc
%{_libdir}/libsyscommon-plugin-api-common.so

%files -n libsyscommon-plugin-api-resourced
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.MIT
%{_libdir}/libsyscommon-plugin-api-resourced.so.*

%post -n libsyscommon-plugin-api-resourced
/sbin/ldconfig

%files -n libsyscommon-plugin-api-resourced-devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.MIT
%{_includedir}/system/syscommon-plugin-resourced*.h
%{_libdir}/pkgconfig/libsyscommon-plugin-api-resourced.pc
%{_libdir}/libsyscommon-plugin-api-resourced.so

%files -n libsyscommon-plugin-api-deviced
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.MIT
%{_libdir}/libsyscommon-plugin-api-deviced.so.*

%files -n libsyscommon-plugin-api-deviced-devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.MIT
%{_includedir}/system/syscommon-plugin-deviced*.h
%{_libdir}/pkgconfig/libsyscommon-plugin-api-deviced.pc
%{_libdir}/libsyscommon-plugin-api-deviced.so

%files -n libsyscommon-plugin-api-update-control
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.MIT
%{_libdir}/libsyscommon-plugin-api-update-control.so.*

%files -n libsyscommon-plugin-api-update-control-devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.MIT
%{_includedir}/system/syscommon-plugin-update-control*.h
%{_libdir}/pkgconfig/libsyscommon-plugin-api-update-control.pc
%{_libdir}/libsyscommon-plugin-api-update-control.so

%files -n libsyscommon-plugin-api-sessiond
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.MIT
%{_libdir}/libsyscommon-plugin-api-sessiond.so.*

%files -n libsyscommon-plugin-api-sessiond-devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.MIT
%{_includedir}/system/syscommon-plugin-sessiond*.h
%{_libdir}/pkgconfig/libsyscommon-plugin-api-sessiond.pc
%{_libdir}/libsyscommon-plugin-api-sessiond.so

%files -n libsyscommon-plugin-api-pass-devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.MIT
%{_includedir}/system/syscommon-plugin-pass*.h
%{_libdir}/pkgconfig/libsyscommon-plugin-api-pass.pc

%if %{WITH_EBPF}
%files -n libsyscommon-ebpf-devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.MIT
%{_libdir}/cmake/TizenBpfHelpers
%endif
