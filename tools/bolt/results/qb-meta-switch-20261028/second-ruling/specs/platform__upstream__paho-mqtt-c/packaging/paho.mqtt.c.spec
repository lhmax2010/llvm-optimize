Name:           paho-mqtt-c
Version:        1.3.15
Release:        0
Summary:        MQTT C Client
License:        EPL-2.0
Group:          Productivity/Networking/Other
URL:            https://www.eclipse.org/paho/clients/c/
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
Source1002:     %{name}.pc

BuildRequires:  pkgconfig(openssl3)
BuildRequires:  cmake

%description
The Paho MQTT C Client is a fully featured MQTT client written in ANSI standard
C. C was chosen rather than C++ to maximize portability. A C++ API over this
library is also available in Paho.

In fact there are two C APIs. "Synchronous" and "asynchronous" for which the
API calls start with MQTTClient and MQTTAsync respectively. The synchronous API
is intended to be simpler and more helpful. To this end, some of the calls will
block until the operation has completed, which makes programming easier. In
contrast, only one call blocks in the asynchronous API - waitForCompletion.
Notifications of results are made by callbacks which makes the API suitable for
use in environments where the application is not the main thread of control.

%package devel
Summary:        MQTT C Client development files
Requires:       lib%{name}

%description devel
The Paho MQTT C Client is a fully featured MQTT client written in ANSI standard
C. C was chosen rather than C++ to maximize portability. A C++ API over this
library is also available in Paho.

In fact there are two C APIs. "Synchronous" and "asynchronous" for which the
API calls start with MQTTClient and MQTTAsync respectively. The synchronous API
is intended to be simpler and more helpful. To this end, some of the calls will
block until the operation has completed, which makes programming easier. In
contrast, only one call blocks in the asynchronous API - waitForCompletion.
Notifications of results are made by callbacks which makes the API suitable for
use in environments where the application is not the main thread of control.

This package contains development files.

%package -n lib%{name}
Summary:        MQTT C Client libraries

%description -n lib%{name}
The Paho MQTT C Client is a fully featured MQTT client written in ANSI standard
C. C was chosen rather than C++ to maximize portability. A C++ API over this
library is also available in Paho.

In fact there are two C APIs. "Synchronous" and "asynchronous" for which the
API calls start with MQTTClient and MQTTAsync respectively. The synchronous API
is intended to be simpler and more helpful. To this end, some of the calls will
block until the operation has completed, which makes programming easier. In
contrast, only one call blocks in the asynchronous API - waitForCompletion.
Notifications of results are made by callbacks which makes the API suitable for
use in environments where the application is not the main thread of control.

This package contains libraries only.

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
%{__make} -j1 build LDCONFIG=echo

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}
%{__make} prefix=%{?buildroot:%{buildroot}}%{_prefix} \
          libdir=%{?buildroot:%{buildroot}}%{_libdir} \
          LDCONFIG=echo \
          install

rm -rf %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp %{SOURCE1002} %{buildroot}%{_libdir}/pkgconfig

%post -n lib%{name} -p /sbin/ldconfig

%postun -n lib%{name} -p /sbin/ldconfig

%files
%license LICENSE
%doc README.md

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}

%files -n lib%{name}
%{_libdir}/lib*.so.*


