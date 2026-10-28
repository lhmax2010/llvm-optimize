%define keepstatic 1
Name:           libtool
Summary:        A Tool to Build Shared Libraries
License:        GPL-2.0-or-later
Group:          Development/Tools
Version:        2.5.4
Release:        1
Url:            http://www.gnu.org/software/libtool/
Source:         http://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.gz
Source2:        baselibs.conf
Source3:        libtool-rpmlintrc
Source1001:     libtool.manifest
Source1002:     Change_order_of_deplib_and_compiler_flags.patch

BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  texinfo
BuildRequires:  makeinfo
BuildRequires:  help2man

Requires:       automake > 1.4
Requires:       libltdl = %{version}

Provides:       libltdl-devel
# fedora name
Provides:       libtool-ltdl-devel

%description
GNU libtool is a set of shell scripts to automatically configure UNIX
architectures to build shared libraries in a generic fashion.

%package -n libltdl
Summary:        Libtool Runtime Library
Group:          System/Libraries
License:        LGPL-2.1-or-later

%description -n libltdl
Library needed by programs that use the ltdl interface of GNU libtool.

%prep
%setup -q -n libtool-%{version}
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE1002}

%build
# force regeneration of ltmain.sh from ltmain.in
touch -r build-aux/ltmain.in build-aux/ltmain.sh
touch build-aux/ltmain.in

%configure CFLAGS="$RPM_OPT_FLAGS" \
   --prefix=%{_prefix} --infodir=%{_infodir} --libdir=%{_libdir}

# force rebuild with non-broken makeinfo
rm -f doc/libtool.info
%__make %{?_smp_mflags}

%install
%make_install DESTDIR=%{buildroot}
%remove_docs

%post -n libltdl -p /sbin/ldconfig

%postun -n libltdl -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%{_bindir}/libtool
%{_bindir}/libtoolize
%{_includedir}/libltdl
%{_includedir}/ltdl.h
%{_libdir}/libltdl.so
%{_libdir}/libltdl.a

%{_datadir}/aclocal/*.m4
%{_datadir}/libtool

%files -n libltdl
%manifest %{name}.manifest
%license COPYING libltdl/COPYING.LIB
%{_libdir}/libltdl.so.*

