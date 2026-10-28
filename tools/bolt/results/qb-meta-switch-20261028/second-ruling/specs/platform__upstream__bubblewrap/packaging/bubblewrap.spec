Summary: Core execution tool for unprivileged containers
Name: bubblewrap
Version: 0.7.0
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: LGPL-2.0+
URL: https://github.com/projectatomic/bubblewrap

# We always run autogen.sh
BuildRequires: autoconf automake libtool
BuildRequires: libcap-devel
BuildRequires: libxslt

%description
This project is based on bubblewrap but it was highly modified for Individual
Service Upgrade use case. It does not offer security of original bubblewrap
project, thus different name - isu-sandbox

%prep
%setup -q

%build
env NOCONFIGURE=1 ./autogen.sh
%configure --disable-silent-rules --with-priv-mode=none

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p -c"
find $RPM_BUILD_ROOT -name '*.la' -delete
rm -rf $RPM_BUILD_ROOT/usr/share/*
mv %{buildroot}/usr/bin/bwrap %{buildroot}/usr/bin/isu-sandbox

%files
%license COPYING
%doc README.md
%{_bindir}/isu-sandbox
