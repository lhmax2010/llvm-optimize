Name:           attr
VCS:            platform/upstream/attr#3cccb9e2a2b96d7a45d20e84a2835a1c0d9a5f72
Summary:        Commands for Manipulating Extended Attributes
License:        GPL-2.0-or-later
Group:          Base/File Systems
Version:        2.5.1
Release:        1.14
Source:         %{name}-%{version}.src.tar.gz
Source2:        baselibs.conf
Source1001: 	attr.manifest
Url:            http://download.savannah.gnu.org/releases-noredirect/attr/
BuildRequires:  autoconf

%description
A set of tools for manipulating extended attributes on file system
objects, in particular getfattr(1) and setfattr(1). An attr(1) command
is also provided, which is largely compatible with the SGI IRIX tool of
the same name.

%package -n lib%{name}
Summary:        A dynamic library for filesystem extended attribute support
Group:          Base/File Systems
License:        LGPL-2.1-or-later

%description -n lib%{name}
This package contains the libattr.so dynamic library, which contains
the extended attribute library functions.

%package -n lib%{name}-devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries
License:        GPL-2.0-or-later
Provides:       attr-devel = %{version}
Obsoletes:      attr-devel <= %{version}
Requires:       lib%{name} = %{version}
Requires:       glibc-devel

%description -n lib%{name}-devel
This package contains the libraries and header files needed to develop
programs which make use of extended attributes. For Linux programs, the
documented system call API is the recommended interface, but an SGI
IRIX compatibility interface is also provided.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export OPTIMIZER="$RPM_OPT_FLAGS"
export DEBUG=-DNDEBUG
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
export LDFLAGS="${LDFLAGS} -Wl,-z,relro -pie"

%configure \
	--prefix=%{_prefix} \
	--enable-gettext=no \
	--exec-prefix=/ \
	--sbindir=%_sbindir \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--with-pic \
    --enable-static=no

%{__make} %{?_smp_mflags}

%install
%make_install
# remove libtool archives
find %{buildroot} -type f -name "*.la" -delete -print
# handle docs on our own
rm -rf %{buildroot}/%{_datadir}/doc/%{name}
%find_lang %{name}
%remove_docs

%post -n lib%{name} -p /sbin/ldconfig

%postun -n lib%{name} -p /sbin/ldconfig

%files -f %{name}.lang
%manifest %{name}.manifest
%license doc/COPYING
%{_bindir}/attr
%{_bindir}/getfattr
%{_bindir}/setfattr

%files -n libattr-devel
%manifest %{name}.manifest
%license doc/COPYING
%{_includedir}/attr/
%{_libdir}/pkgconfig/libattr.pc
%{_libdir}/libattr.so

%files -n lib%{name}
%manifest %{name}.manifest
%license doc/COPYING.LGPL
%{_libdir}/libattr.so.1*
%config %{_sysconfdir}/xattr.conf

%changelog
