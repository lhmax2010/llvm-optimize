Summary:        C library for prototyping and experimenting with quantum-resistant cryptography
Name:           liboqs
Version:        0.15.0
Release:        0
License:        MIT
Group:          Security/Crypto Libraries
Url:            https://openquantumsafe.org/
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
BuildRequires:  ninja
BuildRequires:  cmake

%description
liboqs is part of the Open Quantum Safe (OQS) project led by Douglas Stebila and Michele Mosca,
which aims to develop and integrate into applications quantum-safe cryptography to facilitate
deployment and testing in real world contexts. In particular, OQS provides prototype integrations
of liboqs into TLS and SSH, through OpenSSL and OpenSSH.

%prep
%setup -q

%build
cmake -GNinja \
      -DOQS_BUILD_ONLY_LIB=ON \
      -DOQS_USE_OPENSSL=OFF \
      -DOQS_ALGS_ENABLED=STD \
      -DOQS_ENABLE_SIG_FALCON=OFF \
      -DCMAKE_INSTALL_PREFIX=/usr/ .
ninja

%install
cp %{SOURCE1} .
DESTDIR=%{buildroot} ninja install

%files
%manifest %{name}.manifest
%license LICENSE.txt
%{_libdir}/%{name}.a
%{_libdir}/cmake/%{name}
%{_includedir}/oqs
%exclude %{_libdir}/pkgconfig/%{name}.pc
