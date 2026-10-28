Name:       context-service
Summary:    Tizen Contextual Service Framework
Version:    4.0.3
Release:    1
Group:      Service/Context
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:	contextd.service
Source2:	org.tizen.context.conf
Source3:	contextd-agent.service
Source4:	contextd-agent.socket
Source5:	contextd.asan.conf

BuildRequires: cmake
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gmodule-2.0)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(alarm-service)
BuildRequires: pkgconfig(cynara-creds-gdbus)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-session)

BuildRequires: pkgconfig(context-common-server)
BuildRequires: pkgconfig(context-app-history-server)
BuildRequires: pkgconfig(context-sensor-recorder-server)
BuildRequires: pkgconfig(context-job-scheduler-server)


%description
This is a systemd service that contains all features provided by the Tizen Contextual Service Framework.


%package -n context-agent
Summary:	User-level agent service of the Tizen Contextual Service Framework

%description -n context-agent
This is a systemd service that runs in the user session to assist the main service daemon of the Contextual Service Framework.


%prep
%setup -q

%build
export CXXFLAGS+=" -Wall -Wextra -Wcast-align -Wshadow -Wwrite-strings -Wswitch-default -Wno-unused-parameter"
export CXXFLAGS+=" -Wformat=2 -Wno-empty-body -fomit-frame-pointer -fno-optimize-sibling-calls"
export CXXFLAGS+=" -fno-strict-aliasing -fno-unroll-loops -fsigned-char -fstrict-overflow"
export CXXFLAGS+=" -Wnon-virtual-dtor -std=c++0x"

%cmake . -DLIBDIR=%{_libdir}
make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}
ln -s ../contextd.service %{buildroot}%{_unitdir}/multi-user.target.wants/contextd.service

mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/dbus-1/system.d/

mkdir -p %{buildroot}%{_unitdir_user}/sockets.target.wants
install -m 0644 %{SOURCE3} %{buildroot}%{_unitdir_user}
install -m 0644 %{SOURCE4} %{buildroot}%{_unitdir_user}
ln -s ../contextd-agent.socket %{buildroot}%{_unitdir_user}/sockets.target.wants/contextd-agent.socket

%if "%{asan}" == "1"
mkdir -p %{buildroot}%{_unitdir}/contextd.service.d
install -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/contextd.service.d
%endif

%files
%manifest packaging/%{name}.manifest
%config %{_sysconfdir}/dbus-1/system.d/*
%{_bindir}/contextd
%{_unitdir}/contextd.service
%{_unitdir}/*/contextd.service
%license LICENSE
%if "%{asan}" == "1"
%{_unitdir}/contextd.service.d/contextd.asan.conf
%endif

%files -n context-agent
%manifest packaging/%{name}.manifest
%{_bindir}/contextd-agent
%{_unitdir_user}/contextd-agent.service
%{_unitdir_user}/contextd-agent.socket
%{_unitdir_user}/*/contextd-agent.socket
%license LICENSE
