Name:       dotnet-launcher
Summary:    Launchpad plugin for dotnet apps
Version:    10.0.10
Release:    1
Group:      Application Framework/Application State Management
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
AutoReqProv: no
Source1: %{name}.conf

BuildRequires: cmake
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(liblaunchpad)
BuildRequires: pkgconfig(liblaunchpad-hydra)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(pkgmgr-installer)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libsmack)
BuildRequires: pkgconfig(jsoncpp)
BuildRequires: pkgconfig(yaca)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: sqlite-devel
BuildRequires: boost-devel
BuildRequires: aul-devel
BuildRequires: dotnet-build-tools
BuildRequires: unzip
BuildRequires: coreclr-devel

%if 0%{?asan_enabled}
BuildRequires: clang >= 3.8
BuildRequires: compiler-rt
%endif

Requires: aul
Requires: liblaunchpad
Requires: coreclr
Requires: mscorlib
Requires: corefx-native
Requires: corefx-managed
Requires: jsoncpp

Requires(post): /sbin/ldconfig
Requires(post): /usr/bin/systemctl
Requires(post): /usr/bin/chsmack
Requires(postun): /sbin/ldconfig
Requires(postun): /usr/bin/systemctl
Requires(preun): /usr/bin/systemctl

%define _loaderdir %{_prefix}/share/aul
%define _device_api_dir %{dotnet_assembly_path}
%define _runtime_dir /usr/share/dotnet.tizen/netcoreapp
%define _framework_dir /usr/share/dotnet.tizen/framework
%define _install_mdplugin_dir /etc/package-manager/parserlib/metadata
%define _install_plugin_dir /etc/package-manager/parserlib
%define _native_lib_dir /usr/share/dotnet.tizen/lib
%define _dotnet_dir /opt/dotnet
%define _dotnet_tac_dir /opt/dotnet/tac
%define _dotnet_mic_dir /opt/usr/dotnet/mic
%define _readonly_app_update_dir /opt/dotnet/apps
%define _readonly_tac_dir /usr/share/dotnet.tizen/tac
%define _system_base_addr_file /opt/dotnet.system.base.addr
%define _tizen_preload_dir /usr/share/dotnet.tizen/preload

%ifarch x86_64 aarch64
%define _default_base_addr_start 0x6000000000
%endif

%ifarch %{arm}
%define _default_base_addr_start 0x30000000
%endif

%define _rw_update_scripts_dir /usr/share/upgrade/scripts
%define _rw_dotnet_update_script 715.dotnet_regen_app_ni.patch.sh

%define _build_dotnet_plugin 0

%description
Launchpad plugin for launching dotnet apps

%package gbs-support
Summary: dotnet corerun for gbs environment
Requires: coreclr
Requires: mscorlib
Requires: corefx-native
Requires: corefx-managed

%description gbs-support
This package contains only dotnet-corerun executable to run dotnet processes in gbs build environment

%package devel
Summary: Libraries and Header Files for dotnet-launcher plugins and AOTC tools

%description devel
This package contains library and header files needed to develop plugins for dotnet-launcher
and AOTC tools.

%prep
%setup -q
cp %{SOURCE1} .

%build

%if 0%{?asan_enabled}
%define _dotnet_build_conf Debug
export CFLAGS=" --target=%{_host} "
export CXXFLAGS=" --target=%{_host} "
%ifarch %{ix86}
export CFLAGS=$(echo $CFLAGS | sed -e 's/--target=i686/--target=i586/')
export CXXFLAGS=$(echo $CXXFLAGS | sed -e 's/--target=i686/--target=i586/')
%endif
%endif

%ifarch x86_64 aarch64 riscv64
export CFLAGS+=" -DBIT64 -DHOST_64BIT "
export CXXFLAGS+=" -DBIT64 -DHOST_64BIT "
%endif

# add define HOST_XXX to support pal.h becuase processor-specifc glue code is removed from latest code
%ifarch %{arm}
export CFLAGS+=" -DHOST_ARM "
export CXXFLAGS+=" -DHOST_ARM "
%endif
%ifarch aarch64
export CFLAGS+=" -DHOST_ARM64 "
export CXXFLAGS+=" -DHOST_ARM64 "
%endif
%ifarch %{ix86}
export CFLAGS+=" -DHOST_X86 "
export CXXFLAGS+=" -DHOST_X86 "
%endif
%ifarch x86_64
export CFLAGS+=" -DHOST_AMD64"
export CXXFLAGS+=" -DHOST_AMD64 "
%endif
%ifarch riscv64
export CFLAGS+=" -DHOST_RISCV64 "
export CXXFLAGS+=" -DHOST_RISCV64 "
%endif

dotnet msbuild Managed /t:clean
dotnet msbuild Managed /t:restore /p:RestoreSources=/nuget
dotnet msbuild Managed /p:Configuration=Release

mkdir -p artifacts
cd artifacts

cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
%if 0%{?asan_enabled}
	-DCMAKE_C_COMPILER=clang \
	-DCMAKE_CXX_COMPILER=clang++ \
	-DASAN_ENABLED=TRUE \
%endif
	-DLIBDIR=%{_libdir} \
	-DBINDIR=%{_bindir} \
	-DINCLUDEDIR=%{_includedir} \
	-DLOADERDIR=%{_loaderdir} \
	-DCMAKE_BUILD_TYPE=%{_dotnet_build_conf} \
	-DDEVICE_API_DIR=%{_device_api_dir} \
	-DRUNTIME_DIR=%{_runtime_dir} \
	-DFRAMEWORK_DIR=%{_framework_dir} \
	-DCROSSGEN_PATH=%{_runtime_dir}/crossgen \
	-DINSTALL_MDPLUGIN_DIR=%{_install_mdplugin_dir} \
	-DINSTALL_PLUGIN_DIR=%{_install_plugin_dir} \
	-DDOTNET_DIR=%{_dotnet_dir} \
	-DDOTNET_TAC_DIR=%{_dotnet_tac_dir} \
	-DDOTNET_MIC_DIR=%{_dotnet_mic_dir} \
	-DREAD_ONLY_APP_UPDATE_DIR=%{_readonly_app_update_dir} \
	-DREAD_ONLY_TAC_DIR=%{_readonly_tac_dir} \
	-DVERSION=%{version} \
	-DNATIVE_LIB_DIR=%{_native_lib_dir} \
%ifarch %{arm} aarch64
%if 0%{?use_default_base_addr}
	-DUSE_DEFAULT_BASE_ADDR="" \
%endif
	-DUNIQUE_DEFAULT_BASE_ADDR_SUPPORT="" \
	-DSYSTEM_BASE_FILE=%{_system_base_addr_file} \
	-DDEFAULT_BASE_ADDR_START=%{_default_base_addr_start} \
%endif
%if 0%{_build_dotnet_plugin}
	-DBUILD_DOTNET_PLUGIN="" \
%endif
	../NativeLauncher

make %{?jobs:-j%jobs} VERBOSE=1
cd ..

%install
rm -rf %{buildroot}
cd artifacts
%make_install
cd ..
mkdir -p %{buildroot}%{_framework_dir}
mv Managed/Tizen.Runtime/bin/Release/Tizen.Runtime.dll %{buildroot}%{_framework_dir}
mv Managed/Tizen.Runtime/bin/Release/Tizen.Runtime.pdb %{buildroot}%{_framework_dir}

mkdir -p %{buildroot}%{_dotnet_dir}
mkdir -p %{buildroot}%{_dotnet_tac_dir}
mkdir -p %{buildroot}%{_dotnet_tac_dir}/Libraries
mkdir -p %{buildroot}%{_readonly_app_update_dir}
mkdir -p %{buildroot}%{_readonly_tac_dir}/Libraries
mkdir -p %{buildroot}%{_native_lib_dir}
ln -sf %{_libdir}/libsqlite3.so.0 %{buildroot}%{_native_lib_dir}/libsqlite3.so

mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_tmpfilesdir}/%{name}.conf

mkdir -p %{buildroot}%{_tizen_preload_dir}
cp packaging/10.Dotnet.Launcher.preload %{buildroot}%{_tizen_preload_dir}
cp packaging/Hydra.Exclude.Preload.list %{buildroot}%{_tizen_preload_dir}

# for gbs-support
cp -a %{buildroot}%{_bindir}/dotnet %{buildroot}%{_bindir}/dotnet-corerun

# for crossgen2-support
cp -a %{buildroot}%{_bindir}/dotnet %{buildroot}%{_bindir}/dotnet-inhouse

# to support fota upgrade
mkdir -p %{buildroot}/%{_rw_update_scripts_dir}
install -m 0755 packaging/%{_rw_dotnet_update_script} %{buildroot}/%{_rw_update_scripts_dir}/%{_rw_dotnet_update_script}

# bash completion for dotnettool
# Install as a profile.d script so it is auto-loaded by /etc/bashrc
# (Tizen does not ship bash-completion framework)
mkdir -p %{buildroot}/etc/profile.d
install -m 0644 packaging/dotnettool.bash_completion %{buildroot}/etc/profile.d/dotnettool-completion.sh

%post
mkdir -p /opt/etc/skel/.dotnet
chsmack -t -a User::App::Shared /opt/etc/skel/.dotnet
ln -sf /usr/bin/dotnet-loader /usr/bin/dotnet-uts-loader
chsmack -a User /usr/bin/dotnet-uts-loader

%files
%manifest dotnet-launcher.manifest
%{_loaderdir}/dotnet.loader
%{_loaderdir}/dotnet.launcher
%{_loaderdir}/dotnet.debugger
%{_native_lib_dir}/libsqlite3.so
%{_bindir}/tpatool
%{_bindir}/dotnettool
%{_install_mdplugin_dir}/libprefer_nuget_cache_plugin.so
%{_install_mdplugin_dir}/libprefer_dotnet_aot_plugin.so
%{_install_mdplugin_dir}/libmulticorejit_plugin.so
%{_install_plugin_dir}/libdotnet_apptype_plugin.so
%{_bindir}/dotnet-launcher
%{_bindir}/dotnet-loader
%{_bindir}/dotnet
%{_bindir}/dotnet-inhouse
%{_bindir}/dotnet-hydra-loader
%{_libdir}/libdotnet_launcher_util.so
%{_libdir}/libdotnet_launcher_core.so
%{_libdir}/libni_common.so
%{_libdir}/libtac_common.so
%{_libdir}/libprofile_common.so
%{_libdir}/libprivilege_common.so
%{_libdir}/libmulti_target_resolver.so
%{_tmpfilesdir}/%{name}.conf
/usr/share/parser-plugins/dotnet-launcher.info
%{_framework_dir}/Tizen.Runtime.dll
%{_dotnet_dir}
%{_dotnet_tac_dir}
%{_dotnet_tac_dir}/Libraries
%{_readonly_app_update_dir}
%{_readonly_tac_dir}
%{_readonly_tac_dir}/Libraries
%{_tizen_preload_dir}
%{_rw_update_scripts_dir}/%{_rw_dotnet_update_script}
/etc/profile.d/dotnettool-completion.sh
%if 0%{_build_dotnet_plugin}
%{_native_lib_dir}/libdotnet_plugin.so
%endif

%files devel
%manifest dotnet-launcher.manifest
%defattr(-,root,root,-)
%{_includedir}/ni_common.h
%{_includedir}/tac_common.h
%{_includedir}/tac_installer.h
%{_includedir}/tac_db.h
%{_includedir}/profile_common.h
%{_includedir}/privilege_common.h
%{_includedir}/dotnet_launcher_plugin.h
%{_includedir}/coreclr_host.h
%{_includedir}/r2r_checker.h
%{_includedir}/utils.h
%{_includedir}/launcher_env.h
%{_libdir}/libdotnet_launcher_util.so
%{_libdir}/libni_common.so
%{_libdir}/libtac_common.so
%{_libdir}/libprofile_common.so
%{_libdir}/libprivilege_common.so
%{_libdir}/pkgconfig/dotnet-launcher.pc
%{_framework_dir}/Tizen.Runtime.pdb

%files gbs-support
%{_bindir}/dotnet-corerun
