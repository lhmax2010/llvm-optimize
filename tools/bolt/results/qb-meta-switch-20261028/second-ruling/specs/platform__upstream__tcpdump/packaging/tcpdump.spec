Name:           tcpdump
Version:        4.9.3
Release:        1
License:        BSD-3-Clause
Summary:        A Packet Sniffer
Url:            http://www.tcpdump.org/
Group:          Productivity/Networking/Diagnostic
Source:         http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
Source1001: 	tcpdump.manifest
BuildRequires:  libpcap-devel
BuildRequires:  pkgconfig(openssl3)
Requires: 		security-config

%description
This program can "read" all or only certain packets going over the
ethernet. It can be used to debug specific network problems.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="%{optflags} -Wall -DGUESS_TSO -fstack-protector -fno-strict-aliasing -fPIE"
export LDFLAGS="-pie"

%configure \
  --enable-ipv6
make

%install
%make_install

%files
%manifest %{name}.manifest
%defattr(-,network_fw,network_fw)
%doc LICENSE README *.awk
%doc %{_mandir}/man?/*
%{_sbindir}/*

%changelog
