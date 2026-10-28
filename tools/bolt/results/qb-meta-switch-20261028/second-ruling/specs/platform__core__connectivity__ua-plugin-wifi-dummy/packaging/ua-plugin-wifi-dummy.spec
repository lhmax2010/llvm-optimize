# Do not create provides from emulator .so files because the main package
# should anchor any reverse-dependencies

Name:       ua-plugin-wifi-dummy
Summary:    Wi-Fi User awareness plugin
Version:    0.14.0
Release:    1
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(ua-plugins)
BuildRequires:  pkgconfig(capi-network-connection)

%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Wi-Fi User awareness plugin

%prep
%setup -q
cp %{SOURCE1001} .

%build
CFLAGS=$(echo $CFLAGS | sed 's/-O2/-O0/' | sed 's/-O1/-O0/' | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')
CXXFLAGS=$(echo $CXXFLAGS | sed 's/-O2/-O0/' | sed 's/-O1/-O0/' | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%if 0%{?gcov:1}
export LDFLAGS+=" -lgcov"
%endif

%define NETWORK_FW_DATADIR %{TZ_SYS_RO_SHARE}/network
%define DBDIR %{TZ_SYS_GLOBALUSER_DATA}/

cmake . -DCMAKE_INSTALL_PREFIX=/usr \
		-DCMAKE_LIB_DIR=%{_libdir} \
		-DBIN_DIR=%{_bindir} \
		-DSBIN_DIR=%{_sbindir} \
		-DNETWORK_FW_DATADIR=%{NETWORK_FW_DATADIR} \
		-DDBDIR=%{DBDIR} \
		-DBUILD_GTESTS=%{?gtests:1}%{!?gtests:0} \
		-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}
make %{?jobs:-j%jobs}

%cmake

%install
mkdir -p %{buildroot}/usr/share/network/ua/lib/sensor
cp -af *.so %{buildroot}/usr/share/network/ua/lib/sensor
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-, root, root)
%attr(640,network_fw,network_fw) %{NETWORK_FW_DATADIR}/ua/lib/sensor/wifi-plugin.so*
