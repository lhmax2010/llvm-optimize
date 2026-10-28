%if "%{_with_da_profile}" == "1"
%define WITH_DA 1
%else
%define WITH_DA 0
%endif

%define plt_ext_support_dir %{_libexecdir}/platform-extension-support
Name:           platform-extension
Version:        1.0.0
Release:        0
License:        Apache-2.0
Group:          System/Base
Summary:        Platform extension script for RW data migrations
Requires:       sqlite3
Source0:        %{name}-%{version}.tar.gz
Source1:        210.%{name}-migration.sh
Source2:        platform-extension-post-backup.sh
Source1001:     %{name}.manifest
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  sqlite-devel
BuildRequires:  cmake

%description
Platform extension script for RW data migrations.

%package proxy
Summary:    hal access limitter

%description proxy
This package provides a prelodable library to check if hal modules don't
access file system resources outside the /hal directory (and a few
others).

%prep
%setup -q
cp %{SOURCE1001} .

%build
cd src
mkdir -p build
cd build
%cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix}
make
cd ../..

cd proxy
%ifarch armv7l aarch64
export CFLAGS="$CFLAGS -U_FILE_OFFSET_BITS"
%endif
# Disable warning and errors due to invalid signatures of some wrappers.
# libc header files define some arguments as arrays, but it's impossible
# to generate wrappers with such signatures with macros.
CFLAGS="$CFLAGS -Wno-error=array-parameter"
%autogen \
    --docdir=%_defaultdocdir/platform-extension-proxy/
%__make %{?_smp_mflags}
cd ..

%install
cd src/build
%make_install DESTDIR=%{buildroot}
cd ../..
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_datadir}/platform-extension
mkdir -p %{buildroot}%{_sysconfdir}/platform-extension
mkdir -p %{buildroot}%{plt_ext_support_dir}

cp %{SOURCE1} %{buildroot}%{_datadir}/platform-extension/210.%{name}-migration.sh

install -m 755 src/platform-extension-migration.sh %{buildroot}%{_bindir}/platform-extension-migration.sh
install -m 755 src/platform-extension-run-with-timeout.sh %{buildroot}%{_bindir}/platform-extension-run-with-timeout.sh
mkdir -p %{buildroot}%{_unitdir}/local-fs.target.wants
%if "%{WITH_DA}" == "1"
cp service/platform-extension-migration-da.service %{buildroot}%{_unitdir}/platform-extension-migration.service
mkdir -p %{buildroot}%{_unitdir}/security-manager.socket.d
cat <<EOF > %{buildroot}%{_unitdir}/security-manager.socket.d/platform-extension-migration-deps.conf
[Unit]
DefaultDependencies=no
EOF
cp service/platform-extension-migration-da.service %{buildroot}%{_unitdir}/platform-extension-migration.service
%else
cp service/platform-extension-migration.service %{buildroot}%{_unitdir}/platform-extension-migration.service
%endif
ln -s ../platform-extension-migration.service %{buildroot}%{_unitdir}/local-fs.target.wants/platform-extension-migration.service
install -m 644 src/timeout.conf %{buildroot}%{_sysconfdir}/platform-extension/timeout.conf

install -m 755 src/platform-extension-config.sh %{buildroot}%{_bindir}/platform-extension-config.sh
mkdir -p %{buildroot}%{_unitdir}/sysinit.target.wants
cp service/platform-extension-config.service %{buildroot}%{_unitdir}/platform-extension-config.service
ln -s ../platform-extension-config.service %{buildroot}%{_unitdir}/local-fs.target.wants/platform-extension-config.service
ln -s ../platform-extension-config.service %{buildroot}%{_unitdir}/sysinit.target.wants/platform-extension-config.service

install -m 755 src/platform-extension-common.inc %{buildroot}%{plt_ext_support_dir}/platform-extension-common.inc
install -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}

cd proxy
%make_install DESTDIR=%{buildroot}
cd ..
mkdir -p %{buildroot}/%{_sysconfdir}
echo "%{_libdir}/libplatform-extension-proxy.so.0.0.0" > %{buildroot}/%{_sysconfdir}/ld.so.preload

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/platform-extension-migration.sh
%{_bindir}/platform-extension-run-with-timeout.sh
%attr(0755,-,-) %{_bindir}/platform-extension-merge-generic-db
%{_unitdir}/platform-extension-migration.service
%{_unitdir}/local-fs.target.wants/platform-extension-migration.service
%dir %{_datadir}/platform-extension
%attr(0755,-,-) %{_datadir}/platform-extension/210.platform-extension-migration.sh
%config %{_sysconfdir}/platform-extension/timeout.conf
%{_bindir}/platform-extension-config.sh
%{_unitdir}/platform-extension-config.service
%{_unitdir}/local-fs.target.wants/platform-extension-config.service
%{_unitdir}/sysinit.target.wants/platform-extension-config.service
%{plt_ext_support_dir}/platform-extension-common.inc
%if "%{WITH_DA}" == "1"
%{_unitdir}/security-manager.socket.d/platform-extension-migration-deps.conf
%endif
%attr(0755,-,-) %{_sysconfdir}/platform-extension-post-backup.sh

%files proxy
%manifest %{name}.manifest
%exclude %{_libdir}/libplatform-extension-proxy.so
%exclude %{_libdir}/libplatform-extension-proxy.so.0
%{_libdir}/libplatform-extension-proxy.so.0.0.0
%{_sysconfdir}/ld.so.preload
%config(noreplace) %{_sysconfdir}/platform-extension-proxy.policy
%config(noreplace) %{_sysconfdir}/platform-extension-proxy.enforce
%doc %_defaultdocdir/platform-extension-proxy/README
