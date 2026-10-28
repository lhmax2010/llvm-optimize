Name:    fluoride
Summary: Fluoride Bluetooth Stack
Version: 0.0.1
Release: 1
Group:   Network & Connectivity/Bluetooth
License: Apache-2.0
URL:     https://android.googlesource.com/platform/packages/modules/Bluetooth/
Source0: %{name}-%{version}.tar.gz

BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libevent)
BuildRequires: pkgconfig(gtest)
#BuildRequires: pkgconfig(chromium-efl)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(protobuf-lite)
BuildRequires: pkgconfig(flatbuffers)
BuildRequires: pkgconfig(re2)
BuildRequires: pkgconfig(openssl1.1)
#BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(dlog)
#BuildRequires: pkgconfig(liblc3)
#BuildRequires: pkgconfig(bluetooth-host)
#BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(libtzplatform-config)

BuildRequires: cmake
BuildRequires: python3
BuildRequires: python3-six
BuildRequires: bison
BuildRequires: flex
BuildRequires: clang
BuildRequires: gn
BuildRequires: ninja
BuildRequires: abseil-cpp-devel
BuildRequires: llvm
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Fluoride is the Bluetooth stack implementation used in Android. It provides
a comprehensive Bluetooth protocol stack supporting various Bluetooth profiles
including A2DP, AVRCP, HFP, GATT, and more. This package contains the core
Bluetooth libraries and components for building Bluetooth-enabled applications
on Tizen and other Linux-based systems.

%package devel
Summary: Development files for Fluoride Bluetooth Stack
Requires: %{name} = %{version}-%{release}

%description devel
This package contains header files and development libraries needed to
develop applications that use the Fluoride Bluetooth stack. It includes
the necessary API headers, pkg-config files, and static libraries for
software development.

%prep
%setup -q
chmod 644 %{SOURCE0}
mkdir -p .floss/staging/external
mkdir -p .floss/output
%define config_dir %{TZ_SYS_RW_APP}/bluetooth-config
%define config_data_dir %{config_dir}/data/

%build
%define _arch "arm"

# build stack
%if 0%{?skip_stack_build:1}
%else
ln -sf $PWD .floss/staging/bt
ln -sf $PWD/.floss/repos/platform2/common-mk .floss/staging/common-mk
ln -sf $PWD/.floss/repos/platform2/.gn .floss/staging/.gn
ln -sf $PWD/.floss/repos/platform2/system_api .floss/staging/system_api
ln -sf $PWD/.floss/repos/proto_logging .floss/staging/external/proto_logging 
gn gen --root=$PWD/.floss/staging '--args=platform_subdir="bt" cc="gcc" cxx="g++" ar="llvm-ar" pkg_config="pkg-config" clang_cc=false clang_cxx=false OS="tizen" sysroot="/" libdir="/usr/lib" build_root="\$PWD/.floss/output" platform2_root="\$PWD/.floss/staging" libbase_ver="NOT-INSTALLED" enable_exceptions=false external_cflags=["-fPIC", "-O2"] external_cxxflags=["-DNDEBUG","-I/usr/include/", "-fPIC", "-O2", "-Wno-attributes", "-DTIZEN_FEATURE_AURACAST", "-DTIZEN_FEATURE_EXCLUDE_AOSP_FLAGS"] enable_werror=false use={bt_dynlib=true dbus=false crypto=false mojo=false asan=false coverage=false cros_host=false cros_debug=false floss_rootcanal=false function_elimination_experiment=false fuzzer=false lto_experiment=false msan=false profiling=false proto_force_optimize_speed=false tcmalloc=false test=false ubsan=false android=false bt_nonstandard_codecs=false clang=false dualaudio_mtk=true dualaudio_rtk=false}' $PWD/.floss/output/out/Default
ninja -C $PWD/.floss/output/out/Default -j 12 bt:tools
ninja -C $PWD/.floss/output/out/Default -j 12 bt:all
%endif

%install
# install stack libraries
mkdir -p %{buildroot}/prd/%{_libdir}
mkdir -p %{buildroot}%{_libdir}
%if 0%{?skip_stack_build:1}
install -D -m 0644 packaging/libbluetooth.so %{buildroot}%{_libdir}/libbluetooth.so
install -D -m 0644 packaging/libbase.so %{buildroot}%{_libdir}/libbase.so
install -D -m 0644 packaging/libbase-core.so %{buildroot}%{_libdir}/libbase-core.so
install -D -m 0644 packaging/libbase-policy.so %{buildroot}%{_libdir}/libbase-policy.so
%else
cd .floss/output/out/Default
install -D -m 0644 lib/libbluetooth.so %{buildroot}%{_libdir}/libbluetooth.so
install -D -m 0644 libbase-core.a %{buildroot}%{_libdir}/libbase-core.a
cd -
%endif
install -D -m 0644 liblc3/%{_target_cpu}/liblc3.so %{buildroot}%{_libdir}/liblc3.so
install -D -m 0644 system/conf/sysprops.conf %{buildroot}%{config_data_dir}/sysprops.conf

# install header files
mkdir -p %{buildroot}%{_includedir}/btif
mkdir -p %{buildroot}%{_includedir}/build
mkdir -p %{buildroot}%{_includedir}/hardware
mkdir -p %{buildroot}%{_includedir}/hardware/bluetooth
mkdir -p %{buildroot}%{_includedir}/audio_hal_interface
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cd system/include/
find hardware/ -type f -name '*.h' -exec cp --parents {} %{buildroot}%{_includedir}/ \;
cp macros.h %{buildroot}%{_includedir}/
cd -
cd system
# bluetooth/log.h is required from hardware/ headers
cp log/include/bluetooth/log.h %{buildroot}%{_includedir}/hardware/bluetooth/log.h
find btcore/ -type f -name '*.h' -exec cp --parents {} %{buildroot}%{_includedir}/ \;
# av functions are provided via btif
install -D -m 0644 btif/include/btif_av.h %{buildroot}%{_includedir}/btif/btif_av.h
# audio hal interface for start/stop/suspend stream
install -D -m 0644 audio_hal_interface/a2dp_encoding_host.h %{buildroot}%{_includedir}/audio_hal_interface/a2dp_encoding_host.h
find types/ -type f -name '*.h' -exec cp --parents {} %{buildroot}%{_includedir}/ \;
cd -

cd third_party/libchrome/
find base/ -type f -name '*.h' -exec cp --parents {} %{buildroot}%{_includedir}/ \;
find components/ -type f -name '*.h' -exec cp --parents {} %{buildroot}%{_includedir}/ \;
find testing/gmock/include/gmock/ -type f -name '*.h' -exec cp --parents {} %{buildroot}%{_includedir}/ \;
find testing/gtest/include/gtest/ -type f -name '*.h' -exec cp --parents {} %{buildroot}%{_includedir}/ \;
find third_party/abseil-cpp/ -type f -name '*.h' -exec cp --parents {} %{buildroot}%{_includedir}/ \;
cd -
cp -r third_party/libchrome/build/*.h %{buildroot}%{_includedir}/build
install -D -m 0644 system/libbluetooth.pc %{buildroot}%{_libdir}/pkgconfig/libbluetooth.pc

# install examples
mkdir -p %{buildroot}%{_bindir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
#%manifest %{name}.manifest
#%license LICENSE
%{_libdir}/libbluetooth.so
%{_libdir}/liblc3.so
%{config_data_dir}/sysprops.conf

%files devel
#%manifest %{name}-devel.manifest
%{_includedir}/
%{_includedir}/audio_hal_interface/
%{_includedir}/btcore/
%{_includedir}/btif/
%{_includedir}/hardware/
%{_includedir}/types/
%{_libdir}/libbase-core.a
%{_libdir}/pkgconfig/libbluetooth.pc
