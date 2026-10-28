Name: boot-animation-dali
Version: 1.0.0
Release: 1
Summary: Boot animation
URL: http://slp-source.sec.samsung.net
Source: %{name}-%{version}.tar.gz
Source1: boot-animation.service
Source2: shutdown-animation.service
Source5: boot-animation.path
License: Apache-2.0
Group: Samsung/Application
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: cmake
BuildRequires: pkgconfig(dali2-core)
BuildRequires: pkgconfig(dali2-toolkit)
BuildRequires: pkgconfig(dali2-adaptor)
BuildRequires: dali2-integration-devel
BuildRequires: dali2-adaptor-integration-devel
BuildRequires: dali2-toolkit-integration-devel
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(vconf)
Requires(post): /usr/bin/vconftool

%description
Shows an animation when the device is booted or shutdown.


%prep
%setup -q

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}/usr/lib/systemd/system/multi-user.target.wants
install -m 0644 %SOURCE1 %{buildroot}/usr/lib/systemd/system/boot-animation.service
install -m 0644 %SOURCE2 %{buildroot}/usr/lib/systemd/system/shutdown-animation.service
install -m 0644 %SOURCE5 %{buildroot}/usr/lib/systemd/system/boot-animation.path
ln -s ../boot-animation.path %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/

%clean
make clean

%docs_package

%post


%files
%manifest boot-animation.manifest
/usr/share/lottie/power_on.json
/usr/share/lottie/power_off.json
%license LICENSE
%{_bindir}/boot-animation-dali
/usr/lib/systemd/system/boot-animation.service
/usr/lib/systemd/system/shutdown-animation.service
/usr/lib/systemd/system/boot-animation.path
/usr/lib/systemd/system/multi-user.target.wants/boot-animation.path


