Name:           acl
VCS:            platform/upstream/acl#67dd6e32146fce62b09124fb9ef88c157e6b1d0c
Summary:        Commands for Manipulating POSIX Access Control Lists
License:        LGPL-2.1+ and GPL-2.0+
Group:          Security/Access Control
Version:        2.3.2
Release:        1.13
Url:            http://download.savannah.gnu.org/releases/acl/
Source:         %{name}-%{version}.src.tar.gz
Source1001:     acl.manifest

BuildRequires:  libattr-devel

%description
getfacl and setfacl commands for retrieving and setting POSIX access
control lists.

%package -n libacl
Summary:        A dynamic library for accessing POSIX Access Control Lists
Group:          Security/Access Control

%description -n libacl
This package contains the libacl.so dynamic library which contains the
POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n libacl-devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries
Requires:       libacl = %{version}
Requires:       glibc-devel
# the .so file references libattr.so.x, so require libattr-devel
Requires:       libattr-devel

%description -n libacl-devel
This package contains all necessary include files and libraries needed
to develop applications that require libacl.

%prep
%setup -q -n acl-%version
cp %{SOURCE1001} .

%build
CFLAGS="$CFLAGS -fPIE"
LDFLAGS="$LDFLAGS -pie -Wl,-z,relro,-z,now"

%configure \
	--disable-nls \
	--disable-static \
	--docdir=%{_defaultdocdir}/%{name}

make %{?_smp_mflags} --output-sync=recurse

%install
%make_install
rm -rf %{buildroot}%{_defaultdocdir}/%{name}/COPYING*

%post -n libacl -p /sbin/ldconfig

%postun -n libacl -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license doc/COPYING doc/COPYING.LGPL
%{_bindir}/chacl
%{_bindir}/getfacl
%{_bindir}/setfacl

%files -n libacl-devel
%manifest %{name}.manifest
%{_includedir}/acl/libacl.h
%{_includedir}/sys/acl.h
%{_libdir}/libacl.so
%{_libdir}/pkgconfig/libacl.pc
%exclude %{_mandir}/
%exclude %{_defaultdocdir}/%{name}

%files -n libacl
%manifest %{name}.manifest
%license doc/COPYING doc/COPYING.LGPL
%{_libdir}/libacl.so.1*

