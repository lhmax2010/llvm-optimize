%define SYSTEM_PLUGIN_LIBDIR %{_libdir}/system/plugin

Name:       system-plugin-backend-deviced-headed
Summary:    System plugin backend for deviced and headed profile
Version:    0.1.0
Release:    0
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libsyscommon)
BuildRequires:  pkgconfig(libsyscommon-plugin-api-deviced)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(vconf)

%description
System plugin backend for deviced and headed profile

%prep
%setup -q
cp %{SOURCE1} .

%build
%cmake . -DPLUGIN_BACKEND_NAME=%{name} \
	-DPLUGIN_LIB_DIR=%{SYSTEM_PLUGIN_LIBDIR} \
	-DPLUGIN_DEVICED_INPUT_ENABLE_DLOG=1

make %{?jobs:-j%jobs}

%install
%make_install

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{SYSTEM_PLUGIN_LIBDIR}/libplugin-backend-deviced-display.so
%{SYSTEM_PLUGIN_LIBDIR}/libplugin-backend-deviced-input.so
%config %{_sysconfdir}/deviced/conf.d/display.conf
%{_unitdir}/rndis.service
%{_bindir}/rndis.sh
