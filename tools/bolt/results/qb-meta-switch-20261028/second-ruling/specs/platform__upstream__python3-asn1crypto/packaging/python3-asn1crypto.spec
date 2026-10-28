Name:       python3-asn1crypto 
Summary:    %{name}
Version:    1.5.1 
Release:    0
License:    MIT
Group:      Development/Testing
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest


BuildRequires: pkgconfig(python3)
BuildRequires: python3-setuptools 

%description
ASN.1 parser and serializer with definitions for private keys, public keys,
certificates, CRL, OCSP, CMS, PKCS#3, PKCS#7, PKCS#8, PKCS#12, PKCS#5, X509 and TSP


%prep
%setup -q
cp %{SOURCE1001} .

%build
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean  

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/asn1crypto-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/asn1crypto/*
