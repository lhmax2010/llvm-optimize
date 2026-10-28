Name:       ise-engine-unikey
Version:    0.3.2
Release:    1
Summary:    Vietnamese Input Method Engine for SCIM using Unikey Engine
License:    GPL-2.0+
Group:      Graphics & UI Framework/Input
URL:        http://code.google.com/p/scim-unikey/
Source:     %{name}-%{version}.tar.gz
BuildRequires: pkgconfig(isf)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: gcc-c++

%description
SCIM (Smart Common Input Method) is an input method (IM) platform.
scim-unikey is a IME for scim. Use for type Vietnamese
Support via forum at: http://forum.ubuntu-vn.com/viewforum.php?f=85

%prep
%setup -q

%build
%configure --prefix=%{_prefix}
make %{?_smp_mflags}

%install
%make_install
%__rm -f %{buildroot}%{_libdir}/*.so
find $RPM_BUILD_ROOT -name *.la -exec rm '{}' +
%find_lang scim-unikey
mkdir -p %{buildroot}%{_datadir}/packages/
cp unikey.xml %{buildroot}%{_datadir}/packages/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f scim-unikey.lang
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_datadir}/locale/*
%{_libdir}/libunikey-scim.so*
%{_libdir}/scim-1.0/1.4.0/IMEngine/*.so
%{_datadir}/scim/icons/scim-unikey*.png
%{_datadir}/packages/*
%license COPYING
