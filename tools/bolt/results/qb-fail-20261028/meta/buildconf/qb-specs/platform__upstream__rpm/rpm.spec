%define rpmlibdir %{_prefix}/lib
%define rpmhome %{rpmlibdir}/rpm

Name:           rpm
Summary:        The Package Manager
License:        LGPL-2.0+ and GPL-2.0+
Group:          Base/Package Management
Version:        4.14.1.1
Release:        1
Url:            http://www.rpm.org
BuildRequires:  binutils
BuildRequires:  bzip2
BuildRequires:  file-devel
BuildRequires:  findutils
BuildRequires:  gettext-tools
BuildRequires:  glibc-devel
BuildRequires:  gzip
BuildRequires:  libacl-devel
BuildRequires:  libattr-devel
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  libelf-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig(lua)
BuildRequires:  make
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  patch
BuildRequires:  pkgconfig(popt)
BuildRequires:  xz-devel
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  uthash-devel
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libsmack)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  fdupes
BuildRequires:  libdw-devel
BuildRequires:  libelf-devel
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(python2)
BuildRequires:  bash

Provides:       rpminst
Provides:       rpm-libs

Source1:        db-4.8.30.tar.bz2
Source2:        db-4.8.30-integration.dif
Source4:        rpm-tizen_macros
Source8:        rpmconfigcheck
Source13:       find-docs.sh
Source14:       find-isufiles.sh
Source22:       device-sec-policy
Source23:       find-provides.ksyms
Source24:       debug.manifest
Source1001:     rpm.manifest
Source0:        rpm-%{version}.tar.bz2
Source9:        libsymlink.attr

# avoid bootstrapping problem
%define _binary_payload w9.bzdio

%description
RPM Package Manager is the main tool for managing the software packages
of Tizen.

RPM can be used to install and remove software packages. With rpm, it
is easy to update packages.  RPM keeps track of all these manipulations
in a central database.	This way it is possible to get an overview of
all installed packages.  RPM also supports database queries.

%package devel
Summary:        Include Files and Libraries mandatory for Development
Requires:       rpm = %{version}
Requires:       pkgconfig(popt)

%description devel
This package contains the RPM C library and header files.  These
development files will simplify the process of writing programs which
manipulate RPM packages and databases and are intended to make it
easier to create graphical package managers or any other tools that
need an intimate knowledge of RPM packages in order to function.

%package build
Summary:        Tools and Scripts to create rpm packages
Requires:       rpm = %{version}
Provides:       rpmbuild rpm:%{_bindir}/rpmbuild
Requires:       bzip2
Requires:       xz
Requires:       gzip
Requires:       binutils
Requires:       make
Requires:       findutils
Requires:       patch
Requires:       glibc-devel

%description build
If you want to build a rpm, you need this package. It provides rpmbuild
and requires some packages that are usually required

%package security-plugin
Summary: MSM security plugin for rpm
Requires: rpm = %{version}-%{release}
Requires: smack
Requires: libopenssl3

%description security-plugin
This package contains the MSM security plugin for rpm that performs
security-related functionality.

%post security-plugin
echo "%__transaction_plugins     msm" >> %{rpmhome}/macros
echo "%__plugindir                           %{_libdir}/rpm-plugins" >> %{rpmhome}/macros
echo "%__transaction_msm                     %{__plugindir}/msm.so" >> %{rpmhome}/macros
echo "%__transaction_msm_default_policy      %{_libdir}/rpm-plugins/msm-device-sec-policy" >> %{rpmhome}/macros

%package -n python-rpm
Summary: Python 2 Bindings for Manipulating RPM Packages
Requires:       rpm = %{version}
BuildRequires:  pkgconfig(python2)

%description -n python-rpm
The python-rpm package contains a module that permits applications
written in the Python 2 programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python 2 programs
that will manipulate RPM packages and databases.

%package -n python3-rpm
Summary: Python 3 Bindings for Manipulating RPM Packages
Requires:       rpm = %{version}
BuildRequires:  pkgconfig(python3)

%description -n python3-rpm
The python3-rpm package contains a module that permits applications
written in the Python 3 programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python 3 programs
that will manipulate RPM packages and databases.

%prep
%setup -q -n rpm-%{version}
cp %{SOURCE1001} .
rm -rf sqlite
tar xjf %{S:1}
ln -sfn db-4.8.30 db
chmod -R u+w db/*
%ifarch riscv64
install -m0755 $(automake --print-libdir)/config.sub db/dist/config.sub
%endif
# will get linked from db3
rm -f rpmdb/db.h
patch -p0 < %{S:2}
if [ -s %{_sysconfdir}/rpm/tizen_macros ]; then
    cp -a %{_sysconfdir}/rpm/tizen_macros %{SOURCE4}
fi
cp -a %{SOURCE4} tizen_macros
rm -f m4/libtool.m4
rm -f m4/lt*.m4

# Change hard-coded paths in man pages and .rc files
#[[ x"/usr/lib/rpm" != x%{rpmhome} ]] && \
   /bin/bash -c '/usr/bin/find %{_builddir} -type f -exec sed -e "s|/usr/lib/rpm|%{rpmhome}|g" -i {} \;'

%build
CPPFLAGS="$CPPFLAGS `pkg-config --cflags openssl3`"
export CPPFLAGS
export CFLAGS="%{optflags} -ffunction-sections -fstack-protector-strong -Wl,-z,relro -D_FORTIFY_SOURCE=2 -fPIE"
export LDFLAGS="${LDFLAGS} -pie -Wl,-Bsymbolic-functions -ffunction-sections"
%ifarch armv5tel
export CFLAGS="-g -O0 -fno-strict-aliasing -ffunction-sections"
%endif

%{?hwasan_build:
export CPPFLAGS="$CPPFLAGS -DHWASAN_BUILD"
}

# Toybox mkdir is not in AC_PROG_MKDIR_P's whitelist (only GNU coreutils,
# BusyBox and fileutils are recognized via `mkdir --version`), so configure
# would fall back to the bundled mkinstalldirs script which rpm does not
# package. Predefine MKDIR_P so configure skips detection and uses
# toybox mkdir -p directly, keeping %__mkdir_p pointed at a real program.
export MKDIR_P="/bin/mkdir -p"

%reconfigure \
    --disable-dependency-tracking \
    --with-lua \
    --with-acl \
    --with-cap \
    --enable-shared \
    --enable-python \
    --with-vendor=tizen \
    --with-msm \
    --enable-zstd \
    --with-crypto=openssl \
    --with-rpmconfigdir=%{rpmhome}

make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{rpmlibdir}
mkdir -p %{buildroot}%{_datadir}/locale
ln -s ../share/locale %{buildroot}%{rpmlibdir}/locale
%make_install
install -m 644 db3/db.h %{buildroot}%{_includedir}/rpm
mkdir -p %{buildroot}%{_sysconfdir}/rpm
mkdir -p %{buildroot}%{rpmhome}/tizen
cp -a tizen_macros %{buildroot}%{rpmhome}
install -m 755 %{SOURCE13} %{buildroot}%{rpmhome}/tizen
install -m 755 %{SOURCE14} %{buildroot}%{rpmhome}/tizen
install -m 755 %{SOURCE23} %{buildroot}%{rpmhome}
install -m 644 %{SOURCE9} %{buildroot}%{rpmhome}/fileattrs/libsymlink.attr
install -m 644 %{SOURCE22} %{buildroot}%{_sysconfdir}/device-sec-policy
install -m 644 %{SOURCE22} %{buildroot}%{__plugindir}/msm-device-sec-policy
ln -s ../tizen_macros %{buildroot}%{rpmhome}/tizen/macros
for d in BUILD RPMS SOURCES SPECS SRPMS BUILDROOT ; do
  mkdir -p %{buildroot}%{_usrsrc}/packages/$d
  chmod 755 %{buildroot}%{_usrsrc}/packages/$d
done
for d in %{buildroot}%{rpmhome}/platform/*-linux/macros ; do
  dd=${d%%-linux/macros}
  dd=${dd##*/}
  mkdir -p %{buildroot}%{_usrsrc}/packages/RPMS/$dd
  chmod 755 %{buildroot}%{_usrsrc}/packages/RPMS/$dd
done
mkdir -p %{buildroot}%{_localstatedir}/lib/rpm
gzip -9 %{buildroot}%{_mandir}/man[18]/*.[18]
export RPM_BUILD_ROOT
chmod 755 doc/manual
rm -rf doc/manual/Makefile*
rm -f %{buildroot}%{rpmlibdir}/rpmpopt
for lang in fr ja ko pl ru sk; do
  rm -rf %{buildroot}%{_mandir}/$lang
done
rm -f %{buildroot}%{_datadir}/locale/de/LC_MESSAGES/rpm.mo
rm -f %{buildroot}%{rpmhome}/cpanflute %{buildroot}%{rpmhome}/cpanflute2
install -m 755 scripts/find-supplements %{buildroot}%{rpmhome}
install -m 755 scripts/find-supplements.ksyms %{buildroot}%{rpmhome}
install -m 755 scripts/firmware.prov %{buildroot}%{rpmhome}
install -m 755 scripts/debuginfo.prov %{buildroot}%{rpmhome}
install -m 644 %{SOURCE24} %{buildroot}%{rpmhome}
rm -f %{buildroot}%{rpmlibdir}/locale %{buildroot}%{rpmlibdir}/rpmrc
mkdir -p %{buildroot}%{_sysconfdir}/rpm
chmod 755 %{buildroot}%{_sysconfdir}/rpm
mkdir -p %{buildroot}%{rpmhome}/macros.d
# remove some nonsense or non-working scripts
for f in rpm2cpio.sh rpm.daily rpmdiff* rpm.log rpm.xinetd freshen.sh u_pkg.sh \
         magic magic.mgc magic.mime* rpmfile *.pl javadeps brp-redhat \
         vpkg-provides*.sh http.req sql.req tcl.req \
         rpmdb_* brp-sparc64-linux brp-java-gcjcompile
do
    rm -f %{buildroot}%{rpmhome}/$f
done
for i in %{_datadir}/automake-*/*; do
  if test -f "$i" && test -f %{buildroot}%{rpmhome}/"${i##*/}"; then
    rm -f %{buildroot}%{rpmhome}/"${i##*/}"
  fi
done
%ifarch aarch64 aarch64_ilp32 ppc64le riscv64
install -m 755 config.guess %{buildroot}%{rpmhome}
install -m 755 config.sub %{buildroot}%{rpmhome}
%endif
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{__plugindir}/*.la

%fdupes %{buildroot}%{rpmhome}/platform

sh %{buildroot}%{rpmhome}/find-lang.sh %{buildroot} rpm

%ifarch armv7hl armv7l
# rpm is using the host_cpu as default for the platform,
#but armv7hl is not known by the kernel.
# so we need to enforce the platform here.
echo -n %{_target_cpu}-tizen-linux-gnueabi > %{buildroot}%{_sysconfdir}/rpm/platform
%endif

grep -Rn '/usr/lib/rpm' %{_builddir} || echo "No hard-coded paths found"

%post
/sbin/ldconfig
test -f %{_dbpath}/Packages || rpm --initdb
rm -f %{_dbpath}/Filemd5s \
      %{_dbpath}/Filedigests \
      %{_dbpath}/Requireversion \
      %{_dbpath}/Provideversion

%postun
/sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/rpm
/bin/rpm
%{_bindir}/rpm2cpio
%{_bindir}/rpmdb
%{_bindir}/rpmkeys
%{_bindir}/rpmquery
%{_bindir}/rpmverify
%{_bindir}/rpmqpack
%{_bindir}/rpm2archive
%attr(0755, root, root) %dir %{rpmhome}
%{rpmhome}/macros
%{rpmhome}/macros.d
%{rpmhome}/rpmpopt*
%{rpmhome}/rpmrc
%attr(0755, root, root) %dir %{rpmhome}/tizen
%{rpmhome}/tizen/macros
%{rpmhome}/tizen_macros
%{rpmhome}/rpm.supp
%{rpmhome}/tgpg
%{rpmhome}/platform
%dir    %{__plugindir}
%{__plugindir}/ima.so
%{__plugindir}/prioreset.so
%{__plugindir}/syslog.so
%{_libdir}/librpm.so.*
%{_libdir}/librpmio.so.*
%{_libdir}/librpmbuild.so.*
%{_libdir}/librpmsign.so.*
%dir    %{_localstatedir}/lib/rpm
%dir    %attr(755,root,root) %{_usrsrc}/packages/BUILD
%dir    %attr(755,root,root) %{_usrsrc}/packages/SPECS
%dir    %attr(755,root,root) %{_usrsrc}/packages/SOURCES
%dir    %attr(755,root,root) %{_usrsrc}/packages/SRPMS
%dir    %attr(755,root,root) %{_usrsrc}/packages/RPMS
%dir    %attr(755,root,root) %{_usrsrc}/packages/BUILDROOT
%dir    %attr(755,root,root) %{_usrsrc}/packages/RPMS/*

%files build
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_bindir}/rpmbuild
%{_bindir}/gendiff
%{_bindir}/rpmspec
%{_bindir}/rpmsign
%attr(0755, root, root) %dir %{rpmhome}/tizen
%{rpmhome}/tizen/find-*
%{rpmhome}/brp-*
%{rpmhome}/find-supplements*
%{rpmhome}/check-*
%{rpmhome}/debugedit
%{rpmhome}/sepdebugcrcfix
%{rpmhome}/python-macro-helper
%{rpmhome}/find-debuginfo.sh
%{rpmhome}/find-lang.sh
%{rpmhome}/find-provides.ksyms
%{rpmhome}/*provides*
%{rpmhome}/*requires*
%{rpmhome}/*deps*
%{rpmhome}/*.prov
%{rpmhome}/*.req
%{rpmhome}/macros.*
%{rpmhome}/fileattrs
%{rpmhome}/debug.manifest
%ifarch aarch64 aarch64_ilp32 ppc64le riscv64
%{rpmhome}/config.*
%endif

%files devel
%manifest %{name}.manifest
%defattr(644,root,root,755)
%license COPYING
%attr(755,root,root) %{_bindir}/rpmgraph
%{_includedir}/rpm
%{_libdir}/librpm.so
%{_libdir}/librpmbuild.so
%{_libdir}/librpmio.so
%{_libdir}/librpmsign.so
%{_libdir}/pkgconfig/rpm.pc

%files security-plugin
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{__plugindir}/msm.so
%{__plugindir}/msm-device-sec-policy
%config(noreplace) %{_sysconfdir}/device-sec-policy

%files -n python-rpm
%defattr(-,root,root)
%license COPYING
%{python_sitearch}/rpm
%attr(755,root,root) %{python_sitearch}/rpm/transaction.py

%files -n python3-rpm
%defattr(-,root,root)
%license COPYING
%{python3_sitearch}/rpm
%attr(755,root,root) %{python3_sitearch}/rpm/transaction.py

%lang_package

%docs_package
%doc     GROUPS
