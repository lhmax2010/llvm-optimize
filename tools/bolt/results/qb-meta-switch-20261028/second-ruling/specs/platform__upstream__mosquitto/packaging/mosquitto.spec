%define home    %{_localstatedir}/lib/%{name}
%define c_lib   libmosquitto1
%define cpp_lib libmosquittopp1
Name:           mosquitto
Version:        2.0.22
Release:        0
Summary:        A MQTT v3.1/v3.1.1 Broker
License:        EPL-1.0 and BSD-3-Clause
Group:          Network & Connectivity/Other
URL:            https://mosquitto.org/
Source:         https://mosquitto.org/files/source/mosquitto-%{version}.tar.gz
Source1:        mosquitto.service
Source1001:     %{name}.manifest
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libcares)
BuildRequires:  pkgconfig(libwebsockets)
BuildRequires: systemd-devel
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig


%description
Mosquitto is a message broker that implements the
MQ Telemetry Transport protocol versions 3.1 and 3.1.1. MQTT provides a
lightweight method of carrying out messaging using a publish/subscribe model.
This makes it suitable for "machine to machine" messaging such as with low
power sensors or mobile devices such as phones, embedded computers or
microcontrollers like the Arduino. A good example of this is all of the work
that Andy Stanford-Clark (one of the originators of MQTT) has done in home
monitoring and automation with his twittering house and twittering ferry.

%package -n %{c_lib}
Summary:        Shared C Library for %{name}
Group:          Development/Libraries/C and C++

%description -n %{c_lib}
Mosquitto is a message broker that implements the
MQ Telemetry Transport protocol versions 3.1 and 3.1.1. MQTT provides a
lightweight method of carrying out messaging using a publish/subscribe model.

This package holds the shared C library.

%package -n %{cpp_lib}
Summary:        Shared C++ Library for %{name}
Group:          Development/Libraries/C and C++

%description -n %{cpp_lib}
Mosquitto is a message broker that implements the
MQ Telemetry Transport protocol versions 3.1 and 3.1.1. MQTT provides a
lightweight method of carrying out messaging using a publish/subscribe model.

This package holds the shared C++ library.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries/C and C++
Requires:       %{c_lib} = %{version}
Requires:       %{cpp_lib} = %{version}
Provides:       libmosquitto-devel = %{version}-%{release}
Provides:       libmosquittopp-devel = %{version}-%{release}

%description devel
Mosquitto is a message broker that implements the
MQ Telemetry Transport protocol versions 3.1 and 3.1.1. MQTT provides a
lightweight method of carrying out messaging using a publish/subscribe model.

This package holds the development files.

%package clients
Summary:        Client for Mosquitto
Group:          Productivity/Networking/Other

%description clients
Mosquitto is a message broker that implements the
MQ Telemetry Transport protocol versions 3.1 and 3.1.1. MQTT provides a
lightweight method of carrying out messaging using a publish/subscribe model.
This makes it suitable for "machine to machine" messaging such as with low
power sensors or mobile devices such as phones, embedded computers or
microcontrollers like the Arduino. A good example of this is all of the work
that Andy Stanford-Clark (one of the originators of MQTT) has done in home
monitoring and automation with his twittering house and twittering ferry.

Client for Mosquitto.

%prep
%setup -q
cp %{SOURCE1001} ./%{name}.manifest

%build
export CFLAGS="$CFLAGS -Wno-error=shadow -Wno-error=sign-compare -Wno-error=format="
make all %{?_smp_mflags}

%install
%if "%{_lib}" == "lib64"
export LIB_SUFFIX=64
%endif
%make_install
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%install_service multi-user.target.wants %{name}.service


%post -n %{c_lib} -p /sbin/ldconfig
%postun -n %{c_lib} -p /sbin/ldconfig
%post -n %{cpp_lib} -p /sbin/ldconfig
%postun -n %{cpp_lib} -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license edl-v10 epl-v20 LICENSE.txt
%config(noreplace) %attr(-,root,%{name}) %{_sysconfdir}/mosquitto/
%{_bindir}/mosquitto_passwd
%{_sbindir}/mosquitto
%{_unitdir}/%{name}.service
%{_unitdir}/multi-user.target.wants/%{name}.service

%files clients
%manifest %{name}.manifest
%license edl-v10 epl-v20 LICENSE.txt
%{_bindir}/mosquitto_pub
%{_bindir}/mosquitto_sub
%{_bindir}/mosquitto_rr

%files -n %{c_lib}
%manifest %{name}.manifest
%license edl-v10 epl-v20 LICENSE.txt
%{_libdir}/libmosquitto.so.*

%files -n %{cpp_lib}
%manifest %{name}.manifest
%license edl-v10 epl-v20 LICENSE.txt
%{_libdir}/libmosquittopp.so.*

%files devel
%{_libdir}/libmosquitto.so
%{_libdir}/libmosquittopp.so
%{_includedir}/mosquitto.h
%{_includedir}/mosquitto_*.h
%{_includedir}/mosquittopp.h
%{_includedir}/mqtt_protocol.h
%{_libdir}/pkgconfig/libmosquitto.pc
%{_libdir}/pkgconfig/libmosquittopp.pc

%changelog
