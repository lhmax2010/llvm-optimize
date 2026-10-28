%global rustlibdir %{_libdir}/rustlib
%global rustdocdir %{_datadir}/doc/%{name}

# rpm strip disable
%global _rpm_strip_disable 1

# Disables debug packages and stripping of binaries:
%global debug_package %{nil}
%global __debug_package %{nil}
%global __debug_install_post %{nil}

Name:           rust
Version:        1.90.0
Release:        1
Summary:        The Rust Programming Language
License:        Apache-2.0 or MIT
URL:            https://www.rust-lang.org
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  x86_64 armv7l aarch64

Source11:       rust-%{version}-x86_64-unknown-linux-gnu.tar.xz
Source12:       rust-%{version}-arm-unknown-linux-gnueabi.tar.xz
Source13:       rust-%{version}-aarch64-unknown-linux-gnu.tar.xz

Source100:      macros.rust-toolset
Source1001:     rust.manifest

Provides:       rustc = %{version}-%{release}
Requires:       %{name}-std-static
Requires:       %{name}-std-shared

%description
Rust is a systems programming language that runs blazingly fast, prevents
segfaults, and guarantees thread safety.

This package includes the Rust compiler and documentation generator.

%package std-shared
Summary:        Shared libraries for Rust

%description std-shared
This package includes the shared libraries for building applications written in Rust.

%package devel
Summary:        Libraries for Development and Test

%description devel
This package includes libraries for development and test.

%package std-static
Summary:        Standard library for Rust

%description std-static
This package includes the standard libraries for building applications
written in Rust.

%package -n cargo
Summary:        Rust's package manager and build tool
Requires:       %{name}
Obsoletes:      cargo-vendor <= 0.1.23
Provides:       cargo-vendor = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}

%description -n cargo
Cargo is a tool that allows Rust projects to declare their various dependencies
and ensure that you'll always get a repeatable build.

%prep
%setup -q
cp %{SOURCE1001} .

%build
# skip build

%install

%ifarch x86_64
xz -d < %{SOURCE11} | tar x
dir_name=$(basename %{SOURCE11} .tar.xz)
%endif

%ifarch armv7l
xz -d < %{SOURCE12} | tar x
dir_name=$(basename %{SOURCE12} .tar.xz)
%endif

%ifarch aarch64
xz -d < %{SOURCE13} | tar x
dir_name=$(basename %{SOURCE13} .tar.xz)
%endif

cd ${dir_name}
components=$(cat components | grep -E  "rust-std|cargo|rustc|clippy-preview" | tr '\n' ',' | sed 's/,$//g')
./install.sh --components=${components} \
             --prefix=%{buildroot}%{_prefix} \
             --sysconfdir=%{buildroot}%{_sysconfdir} \
             --bindir=%{buildroot}%{_bindir} \
             --libdir=%{buildroot}%{_libdir} \
             --datadir=%{buildroot}%{_datadir} \
             --docdir=%{buildroot}%{rustdocdir} \
             --disable-ldconfig

cd -

mkdir -p %{buildroot}%{_sysconfdir}/rpm
cp -av %{SOURCE100} %{buildroot}%{_sysconfdir}/rpm/macros.rust-toolset
cp %{buildroot}%{rustlibdir}/*/lib/libstd-*.so %{buildroot}%{_libdir}
rm -f %{buildroot}%{rustlibdir}/install.log
rm -f %{buildroot}%{rustlibdir}/manifest-*
rm -f %{buildroot}%{rustlibdir}/components
rm -f %{buildroot}%{rustlibdir}/rust-installer-version
rm -f %{buildroot}%{rustlibdir}/uninstall.sh
rm -rf %{buildroot}%{rustdocdir}

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo %{_libdir}/rustlib/dylib > %{buildroot}%{_sysconfdir}/ld.so.conf.d/rustlib-dylib.conf

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post std-shared -p /sbin/ldconfig

%postun std-shared -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYRIGHT LICENSE-APACHE LICENSE-MIT
%{_bindir}/rustc
%{_bindir}/rustdoc
%{_bindir}/rust-gdb
%{_bindir}/rust-gdbgui
%{_bindir}/rust-lldb
%{_bindir}/clippy-driver
%{_libexecdir}/rust-analyzer-proc-macro-srv
%{_mandir}/man1/rustc.1*
%{_mandir}/man1/rustdoc.1*
%dir %{rustlibdir}
%{rustlibdir}/*/bin/gcc-ld/*
%{rustlibdir}/*/bin/rust-lld
%{rustlibdir}/*/bin/rust-objcopy
%{rustlibdir}/*/bin/wasm-component-ld
%{_sysconfdir}/rpm/macros.rust-toolset
%{rustlibdir}/etc/*.py
%{rustlibdir}/etc/lldb_commands
%{rustlibdir}/*/lib/*.so

%files std-shared
%manifest %{name}.manifest
%license COPYRIGHT LICENSE-APACHE LICENSE-MIT
%{_libdir}/libstd-*.so
%{_sysconfdir}/ld.so.conf.d/rustlib-dylib.conf

%files devel
%manifest %{name}.manifest
%{_libdir}/librustc_driver-*.so
%ifnarch x86_64 aarch64
%{_libdir}/libdarling_macro-*.so
%{_libdir}/libderive_setters-*.so
%{_libdir}/libdisplaydoc-*.so
%{_libdir}/libderive_where-*.so
%{_libdir}/libicu_provider_macros-*.so
%{_libdir}/libproc_macro_hack-*.so
%{_libdir}/librustc_fluent_macro-*.so
%{_libdir}/librustc_index_macros-*.so
%{_libdir}/librustc_macros-*.so
%{_libdir}/librustc_type_ir_macros-*.so
%{_libdir}/libserde_derive-*.so
%{_libdir}/libthiserror_impl-*.so
%{_libdir}/libtracing_attributes-*.so
%{_libdir}/libunic_langid_macros_impl-*.so
%{_libdir}/libyoke_derive-*.so
%{_libdir}/libzerofrom_derive-*.so
%{_libdir}/libzerovec_derive-*.so
%endif
%ifarch x86_64 aarch64
%{_libdir}/libLLVM*
%endif

%files std-static
%manifest %{name}.manifest
%license COPYRIGHT LICENSE-APACHE LICENSE-MIT
%dir %{rustlibdir}
%{rustlibdir}/*/lib/*.rlib
%ifarch aarch64 x86_64
%{rustlibdir}/*/lib/*.a
%endif

%files -n cargo
%manifest %{name}.manifest
%license COPYRIGHT LICENSE-APACHE LICENSE-MIT
%{_bindir}/cargo
%{_bindir}/cargo-clippy
%{_mandir}/man1/cargo*.1*
%{_datadir}/zsh/site-functions/_cargo
/etc/bash_completion.d/cargo
