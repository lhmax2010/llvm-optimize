Name:       activationd-plugin
Version:    0.1.1
Release:    0
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.xz
Source1001: %{name}.manifest
Summary:    Event-based activation daemon rules
Group:      System/Monitoring

%description
Rules for activationd

%prep

%setup -q
cp %{SOURCE1001} .

%build

%install
%define cdir %{_libdir}/actd/modules.conf.d
%define bcdir %{buildroot}/%{cdir}
%define fname 70-activationd-plugin.conf

mkdir -p %{bcdir}/unit_control_eh.conf.d
mkdir -p %{bcdir}/vconf_listener.conf.d
mkdir -p %{bcdir}/dbus_listener.conf.d
mkdir -p %{bcdir}/activation_eh.conf.d
install -m644 unit_control_whitelist.conf %{bcdir}/unit_control_eh.conf.d/%{fname}
install -m644 vconf_listener.conf %{bcdir}/vconf_listener.conf.d/%{fname}
install -m644 dbus_listener.conf  %{bcdir}/dbus_listener.conf.d/%{fname}
install -m644 activation.conf     %{bcdir}/activation_eh.conf.d/%{fname}

%files
%license COPYING
%{cdir}/unit_control_eh.conf.d/%{fname}
%{cdir}/vconf_listener.conf.d/%{fname}
%{cdir}/activation_eh.conf.d/%{fname}
%{cdir}/dbus_listener.conf.d/%{fname}
