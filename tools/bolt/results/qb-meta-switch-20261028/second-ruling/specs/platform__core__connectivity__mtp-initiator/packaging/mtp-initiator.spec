Name:       mtp-initiator
Summary:    mtp(media transfer protocol) initiator
Version:    1.4.39
Release:    0
Group:      Network & Connectivity/Other
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(libmtp)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(capi-base-common)
Buildrequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  python
BuildRequires:  python-xml
BuildRequires:  python3-setuptools
Requires:  security-config

%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif

%define upgrade_script_path /usr/share/upgrade/scripts

%description
A mtp-initiator

%package haltests
Summary: mtp-initiator extension for HAL test
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(libusb-1.0)
BuildRequires: pkgconfig(libmtp)
BuildRequires: pkgconfig(capi-system-info)
Requires: %{name} = %{version}-%{release}
## Remove libmtp dependency because haltest include lipmtp package.
#Requires: libmtp
%description haltests
TIZEN MTP Initiator extension for HAL test.

%prep
%setup -q
cp %{SOURCE1} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov "
%endif

CFLAGS+=" -DTIZEN_EXT"
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DMAJORVER=${MAJORVER} -DFULLVER=%{version} %{?ARM_DEF} \
		    -DBUILD_GTESTS=%{?gtests:1}%{!?gtests:0} \
		    -DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}


make %{?jobs:-j%jobs}

%post
mkdir -p %TZ_SYS_DB/mtp
chown network_fw:network_fw %TZ_SYS_DB/mtp
chsmack -a "System::Shared" --transmute %TZ_SYS_DB/mtp

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_prefix}/lib/udev/rules.d
cp packaging/99-mtp.rules %{buildroot}/%{_prefix}/lib/udev/rules.d/99-mtp.rules

mkdir -p %{buildroot}/etc/dbus-1/system.d/
cp -af %{_builddir}/%{name}-%{version}/packaging/org.tizen.mtp.conf %{buildroot}/etc/dbus-1/system.d/

mkdir -p %{buildroot}/opt/usr/data/network/lib
%ifarch aarch64
unrpm %{_builddir}/%{name}-%{version}/res/libmtp-1.1.11-5.5.aarch64.rpm
cp -af ./usr/lib64/* %{buildroot}/opt/usr/data/network/lib/
cp -af ./lib/udev/rules.d/*.rules  %{buildroot}/%{_prefix}/lib/udev/rules.d/
%endif
%ifarch armv7l armv7hl armv7nhl armv7tnhl armv7thl
unrpm %{_builddir}/%{name}-%{version}/res/libmtp-1.1.11-5.5.armv7l.rpm
cp -af ./usr/lib/* %{buildroot}/opt/usr/data/network/lib/
cp -af ./lib/udev/rules.d/*.rules  %{buildroot}/%{_prefix}/lib/udev/rules.d/
%endif

%make_install

install -D -m 0644 packaging/mtp-initiator.service %{buildroot}/%{_unitdir}/mtp-initiator.service

%files
%manifest %{name}.manifest
%license LICENSE.APLv2
%defattr(-,root,root,-)
%{_bindir}/mtp-initiator
%{_unitdir}/mtp-initiator.service
%{_prefix}/lib/udev/rules.d/99-mtp.rules
%config %{_sysconfdir}/dbus-1/system.d/org.tizen.mtp.conf
%if 0%{?gtests:1}
%{_bindir}/gtest*
%endif

%files haltests
%manifest %{name}.manifest
%{_bindir}/hal/*haltests
%ifarch aarch64 armv7l armv7hl armv7nhl armv7tnhl armv7thl
%{_prefix}/lib/udev/rules.d/69-libmtp.rules
/opt/usr/data/network/lib/*
%endif
