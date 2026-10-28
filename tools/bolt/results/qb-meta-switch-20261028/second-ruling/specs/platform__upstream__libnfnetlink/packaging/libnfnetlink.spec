Name:           libnfnetlink
%define libsoname	%{name}
Version:        1.0.1
Release:        2
License:        GPL-2.0
Url:            http://netfilter.org/projects/libnfnetlink/
Group:          Productivity/Networking/Security

Summary:        Low-level library for Netfilter-related kernel/userspace communication
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
Source1001: 	libnfnetlink.manifest
BuildRequires:  autoconf
BuildRequires:  automake >= 1.6
BuildRequires:  libtool
BuildRequires:  pkgconfig >= 0.23
BuildRequires:  xz

%description
libnfnetlink is the low-level library for netfilter related
kernel/userspace communication. It provides a generic messaging
infrastructure for in-kernel netfilter subsystems (such as
nfnetlink_log, nfnetlink_queue, nfnetlink_conntrack) and their
respective users and/or management tools in userspace.

This library is not meant as a public API for application developers.
It is only used by other netfilter.org projects, such as
libnetfilter_log, libnetfilter_queue or libnetfilter_conntrack.

%package devel
Summary:        Low-level library for Netfilter-related kernel/userspace communication
Group:          Development/Libraries/C and C++
Requires:       %libsoname = %{version}

%description devel
libnfnetlink is the low-level library for netfilter related
kernel/userspace communication. It provides a generic messaging
infrastructure for in-kernel netfilter subsystems (such as
nfnetlink_log, nfnetlink_queue, nfnetlink_conntrack) and their
respective users and/or management tools in userspace.

This library is not meant as a public API for application developers.
It is only used by other netfilter.org projects, such as
libnetfilter_log, libnetfilter_queue or libnetfilter_conntrack.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure --disable-static --includedir=%{_includedir}/%{name}-%{version}
make %{?_smp_mflags}

%install
%make_install

%post  -p /sbin/ldconfig

%postun  -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libnfnetlink.so.*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/libnfnetlink*
%{_libdir}/libnfnetlink.so
%{_libdir}/pkgconfig/libnfnetlink.pc

%changelog
