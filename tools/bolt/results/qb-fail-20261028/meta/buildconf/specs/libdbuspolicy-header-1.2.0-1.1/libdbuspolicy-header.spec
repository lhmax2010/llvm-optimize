Name:           libdbuspolicy-header
VCS:            platform/core/system/libdbuspolicy-header#a4138557fa7a1bbcea2a845d1f38638b3305d21e
Summary:        Header-only package of libdbuspolicy
License:        MIT
Group:          Base/IPC
Version:        1.2.0
Release:        1.1
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

%global __provides_exclude_from %{_libdir}/pkgconfig/.*\\.pc$
%global __provides_exclude ^libdbuspolicy1\\.so\\.1.*$

# Conflict with the real libdbuspolicy to prevent OBS resolver from
# picking both packages when resolving libdbuspolicy1.so.1 dependency.
# Only one of them should be installed in the build environment.
Conflicts:      libdbuspolicy

%package devel
License:        MIT
Summary:        Development files for libdbuspolicy (header-only)
# devel subpackage requires the main package
Requires:       %{name} = %{version}

%description
Header-only stub package of libdbuspolicy.
This package is intended for build-time use only and should NOT be
included in the runtime image. The actual libdbuspolicy should be
used at runtime instead.

%description devel
This package contains the header files and stub .so for libdbuspolicy,
allowing compilation without a runtime dependency on the actual
libdbuspolicy library.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%reconfigure --libdir=%{_libdir}
make configure
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

# Remove libtool archive file
rm -f %{buildroot}%{_libdir}/libdbuspolicy1.la

# Remove the symlink created by libtool
rm -f %{buildroot}%{_libdir}/libdbuspolicy1.so

# Copy the real shared library from src/.libs directory
# libtool puts the actual library in src/.libs/
cp src/.libs/libdbuspolicy1.so %{buildroot}%{_libdir}/libdbuspolicy1.so

# Remove versioned .so files (we only need unversioned for build-time)
rm -f %{buildroot}%{_libdir}/libdbuspolicy1.so.*

# Install header files required for compilation
mkdir -p -m755 %{buildroot}%{_includedir}/dbuspolicy
install -m644 src/dbuspolicy1/libdbuspolicy1.h %{buildroot}%{_includedir}/dbuspolicy/
mkdir -p -m755 %{buildroot}%{_includedir}/linux/
install -m644 src/linux/kdbus.h %{buildroot}%{_includedir}/linux/

%files
%manifest %{name}.manifest
%license LICENSE.MIT
%defattr(-,root,root)
# Main package is empty - only devel package is needed for build-time

%files devel
%manifest %{name}.manifest
%license LICENSE.MIT
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/libdbuspolicy1.pc
%{_libdir}/libdbuspolicy1.so
