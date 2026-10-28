#
# emuld package spec file
#

%define emuld_major_version 0
%define emuld_minor_version 11
%define emuld_release_number 3

Name: emuld
Version: %{emuld_major_version}.%{emuld_minor_version}.%{emuld_release_number}
Release: 0
Summary: Emulator daemon
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Group: SDK/Other

BuildRequires: cmake
BuildRequires: libxml2-devel
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(deviced)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(tizen-core)
BuildRequires: pkgconfig(capi-network-connection)
BuildRequires: pkgconfig(eventsystem)

ExclusiveArch: %{ix86} x86_64

%description
A emulator daemon is used for communication between guest and host

%package emuld
Summary:    Emulator daemon
Requires:   libemuld = %{version}-%{release}

%description emuld
Emulator daemon

%package -n libemuld
Summary:    Emulator daemon library
Requires:   vconf

%description -n libemuld
Emulator daemon library for emuld and plugins

%package -n libemuld-devel
Summary:    Emulator daemon library for (devel)
Requires:   libemuld = %{version}-%{release}

%description -n libemuld-devel
Emulator daemon library for emuld plugins

%package -n yagl_virgl_switcher
Summary:    YAGL/Virgl switcher service

%description -n yagl_virgl_switcher
YAGL/Virgl switcher service for emulator

%prep
chmod 644 %{SOURCE0}
%setup -q

# Add gcc version check as stringop-overflow stringop-truncation warnings are not introduced by GCC-6
%define gccversion %(gcc -dumpversion | cut -f1 -d.)

%if %{gccversion} >= 9
	%define extraflags "-Wno-error=stringop-overflow -Wno-error=sizeof-pointer-memaccess -Wno-error=array-bounds -Wno-error=stringop-truncation -std=gnu++14"
%else
	%define extraflags "-Wno-error=sizeof-pointer-memaccess -Wno-error=array-bounds"
%endif

echo %{extraflags}

cmake . \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DLIB_INSTALL_DIR=%{_libdir} \
    -DEMULD_MAJOR_VERSION=%{emuld_major_version} \
    -DEMULD_MINOR_VERSION=%{emuld_minor_version} \
    -DEMULD_RELEASE_NUMBER=%{emuld_release_number} \
    -DEXTRA_CFLAGS=%{extraflags}

%build

make

%install
rm -rf %{buildroot}

# for systemd
if [ ! -d %{buildroot}/usr/lib/systemd/system/emulator.target.wants ]; then
    mkdir -p %{buildroot}/usr/lib/systemd/system/emulator.target.wants
fi

cp emuld.service %{buildroot}/usr/lib/systemd/system/.
ln -s ../emuld.service %{buildroot}/usr/lib/systemd/system/emulator.target.wants/emuld.service

# for yagl_virgl_switcher
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_unitdir}/graphical.target.wants
cp script/yagl_virgl_switcher.sh %{buildroot}/%{_bindir}/yagl_virgl_switcher
cp yagl_virgl_switcher.service %{buildroot}/%{_unitdir}/yagl_virgl_switcher.service
ln -s ../yagl_virgl_switcher.service %{buildroot}/%{_unitdir}/graphical.target.wants/yagl_virgl_switcher.service

%make_install

%clean
make clean
rm -rf CMakeCache.txt
rm -rf CMakeFiles
rm -rf cmake_install.cmake
rm -rf Makefile
rm -rf install_manifest.txt

%post
chmod 770 %{_prefix}/bin/emuld

%post -n libemuld -p /sbin/ldconfig
%post -n libemuld-devel -p /sbin/ldconfig
%postun -n libemuld -p /sbin/ldconfig
%postun -n libemuld-devel -p /sbin/ldconfig

%files -n emuld
%defattr(-,root,root,-)
%manifest emuld.manifest
%{_prefix}/bin/emuld
%license LICENSE
/usr/lib/systemd/system/emuld.service
/usr/lib/systemd/system/emulator.target.wants/emuld.service

%files -n libemuld
%defattr(-,root,root,-)
%manifest libemuld.manifest
%license LICENSE
%{_libdir}/libemuld.so*

%files -n libemuld-devel
%defattr(-,root,root,-)
%{_includedir}/libemuld/*.h
%{_libdir}/libemuld.so*
%{_libdir}/pkgconfig/libemuld.pc

%files -n yagl_virgl_switcher
%manifest yagl_virgl_switcher.manifest
%{_bindir}/yagl_virgl_switcher
%{_unitdir}/yagl_virgl_switcher.service
%{_unitdir}/graphical.target.wants/yagl_virgl_switcher.service

%changelog
