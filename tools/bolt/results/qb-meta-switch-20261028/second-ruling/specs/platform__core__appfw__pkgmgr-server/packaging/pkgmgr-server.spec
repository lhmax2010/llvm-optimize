Name:       pkgmgr-server
Summary:    Packager Manager server package
Version:    1.1.4
Release:    1
Group:      Application Framework/Package Management
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
BuildRequires:  cmake
BuildRequires:  unzip
BuildRequires:  gettext-tools
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(pkgmgr-installer)
BuildRequires:  pkgconfig(pkgmgr-parser)
BuildRequires:  pkgconfig(libgum)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(minizip)
BuildRequires:  pkgconfig(rpc-port)
BuildRequires:  fdupes
BuildRequires:  tidl
BuildRequires:  rust
BuildRequires:  rust-libc
BuildRequires:  rust-glib-sys
BuildRequires:  rust-minizip-sys
BuildRequires:  rust-mockall
BuildRequires:  rust-mockall_double

%global real_crate_name rust_pkgmgr_server
%global rustc_edition 2021

%description
Packager Manager server package for packaging

%prep
%setup -q
cp %{SOURCE1001} .
tidlc -s -l C -e -i ./tidl_pkgmgr_server/PkgMgr.tidl -o tidl_pkgmgr_server
mv tidl_pkgmgr_server.* ./tidl_pkgmgr_server/

%define run_dir /run/user
%define backend_dir %{_sysconfdir}/package-manager/backend

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
  -DFULLVER=%{version} \
  -DMAJORVER=${MAJORVER} \
  -DUNITDIR=%{_unitdir} \
  %if 0%{?asan} != 1
    -DASAN_ENABLED=FALSE
  %else
    -DASAN_ENABLED=TRUE
  %endif

make %{?jobs:-j%jobs}

%{rustc_std_build} --crate-type=bin \
        --crate-name=%{real_crate_name} \
        -L native="./tidl_pkgmgr_server" \
        -L native="./util_pkgmgr_server" \
        -l "minizip" \
        %{?rustc_edition:--edition=%{rustc_edition}} \
        %rust_dylib_extern libc \
        ./src/main.rs
%{rustc_std_build} --test --crate-type=bin \
        --extern mockall=%{_rust_dylibdir}/libmockall.so \
        --extern mockall_double=%{_rust_dylibdir}/libmockall_double.so \
        --crate-name=unittests_%{real_crate_name} \
        -L native="./tidl_pkgmgr_server" \
        -L native="./util_pkgmgr_server" \
        -l "minizip" \
        %{?rustc_edition:--edition=%{rustc_edition}} \
        %rust_dylib_extern libc \
        ./src/main.rs

%check
export LD_LIBRARY_PATH=./util_pkgmgr_server/:./tidl_pkgmgr_server/:%{_rust_dylibdir}
RUST_BACKTRACE=1 RUST_TEST_THREADS=1 ./unittests_rust_pkgmgr_server

%install
%make_install

mkdir -p %{buildroot}%{_unitdir}/basic.target.wants
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
ln -sf ../package-manager.socket %{buildroot}%{_unitdir}/sockets.target.wants/package-manager.socket

install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 ./%{real_crate_name} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/package-manager/server

%fdupes %{buildroot}

%post
/sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_unitdir}/package-manager.service
%{_unitdir}/package-manager.socket
%{_unitdir}/sockets.target.wants/package-manager.socket
%{_sysconfdir}/package-manager/server
%attr(0644,root,root) %{_libdir}/libtidl_pkgmgr_server.so
%attr(0644,root,root) %{_libdir}/libutil_pkgmgr_server.so

%{_bindir}/%{name}
