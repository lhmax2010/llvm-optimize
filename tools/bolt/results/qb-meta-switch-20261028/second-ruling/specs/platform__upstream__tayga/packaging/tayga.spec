Name:       tayga
Summary:    Simple, no-fuss NAT64 for Linux
Version:    0.9.2
Release:    1
Group:      System/Tools
License:    GPL-2.0+
URL:        http://www.litech.org/tayga/
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  pkgconfig(libtzplatform-config)
Requires:       security-config

%description
TAYGA is an out-of-kernel stateless NAT64 implementation for Linux that uses
the TUN driver to exchange IPv4 and IPv6 packets with the kernel.
It is intended to provide production-quality NAT64 service for networks
where dedicated NAT64 hardware would be overkill.

%prep
%setup -q

%build
export CFLAGS="$CFLAGS -Wno-implicit-function-declaration"
aclocal && \
     autoheader && \
         libtoolize --automake --copy --force && \
         automake --add-missing --copy && \
         autoconf
%configure
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_sbindir}
cp tayga %{buildroot}%{_sbindir}/tayga

mkdir -p %{buildroot}%{TZ_SYS_ETC}/tayga/
cp tayga.conf %{buildroot}%{TZ_SYS_ETC}/tayga/tayga.conf

%post
chown -R network_fw:network_fw %{TZ_SYS_ETC}/tayga

%files
%manifest tayga.manifest
%defattr(-,root,root,-)
%license COPYING
%{_sbindir}/tayga
%attr(644,network_fw,network_fw) %{TZ_SYS_ETC}/tayga/tayga.conf
