Name:       setup-adaptor
Summary:    Provide network and system data setting daemon
Version:    0.3.1
Release:    0
Group:      System & System Tools
ExclusiveArch: %{arm} aarch64 riscv64
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source2:    %{name}.service
BuildRequires:  awk
BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-network-wifi-manager)
BuildRequires:  pkgconfig(capi-network-connection)
BuildRequires:  pkgconfig(json-c)


Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
provide setting for network and system data based on config

%prep
%setup -q
cp %{SOURCE1} ./
cp %{SOURCE2} ./

%build
export LDFLAGS+=" -Wl,--as-needed,-z,noexecstack"
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%cmake . \
		-DBUILD_TESTS=OFF\
		-DMAJORVER=${MAJORVER}\
		-DFULLVER=%{version}\
		-DBIN_INSTALL_DIR:PATH=%{_bindir}

%install
%make_install
mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
install -m 0644 %SOURCE2 %{buildroot}%{_unitdir}/%{name}.service
%install_service multi-user.target.wants %{name}.service
mkdir -p %{buildroot}/opt/etc/setup-adaptor

%post

%preun

%postun

%files
%attr(0755,system_fw,system_fw) %dir /opt/etc/setup-adaptor
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE.Apache-2.0
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/multi-user.target.wants/%{name}.service
