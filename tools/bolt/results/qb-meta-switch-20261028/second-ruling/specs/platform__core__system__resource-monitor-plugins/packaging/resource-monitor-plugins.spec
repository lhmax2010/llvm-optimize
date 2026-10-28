Name:           resource-monitor-plugins
Version:        1.0.0
Release:        1
Summary:        Example eBPF plugins for PASS Resource Monitor
Group:          System/Libraries
License:        Apache-2.0 and GPL-2.0
Source0:        %{name}-%{version}.tar.gz
Source1:        resource-monitor-plugins.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libbpf)
BuildRequires:  pkgconfig(libsyscommon)
BuildRequires:  pkgconfig(libsyscommon-plugin-api-common)
BuildRequires:  pkgconfig(libsyscommon-plugin-api-pass)
BuildRequires:  pkgconfig(libpass-resource-monitor)

BuildRequires:  libsyscommon-ebpf-devel

%description
Collection of reference implementation plugins for the Power Aware System Service (PASS)
using eBPF for deep kernel monitoring.

%package -n resource-monitor-plugin-network
Summary:        PASS Network Monitor Plugin (eBPF)
Group:          System/Libraries
Requires:       pass
Requires:       libpass-resource-monitor

%description -n resource-monitor-plugin-network
Network resource monitor plugin providing TCP retransmission and RX/TX stats via eBPF.

%package -n resource-monitor-plugin-network-devel
Summary:        Development headers for PASS Network Plugin
Group:          Development/Libraries
Requires:       resource-monitor-plugin-network = %{version}-%{release}

%description -n resource-monitor-plugin-network-devel
Headers defining eBPF attribute IDs for the network monitor plugin.

%prep
%setup -q

%build
%cmake . \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir}

%make_build

%install
%make_install
cp %{SOURCE1} .

%files -n resource-monitor-plugin-network
%manifest resource-monitor-plugins.manifest
%defattr(-,root,root,-)
%{_libdir}/resource-monitor/plugins/libresource-monitor-plugin-network.so

%files -n resource-monitor-plugin-network-devel
%defattr(-,root,root,-)
%{_includedir}/resource-monitor-plugins/network-attributes.h
