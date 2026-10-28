Name:       ise-engine-thai
Summary:    Thai Input Method Engine for ISF
Version:    1.0.1
Release:    1
Group:      Graphics & UI Framework/Input
License:    GPL-2.0+
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  gettext-tools
BuildRequires:  pkgconfig(isf)
BuildRequires:  pkgconfig(libthai)

%description
SCIM (Smart Common Input Method) is an input method (IM) platform.
This package provides Thai input method engine for SCIM.  Currently, it
supports Ketmanee, TIS-820.2538 and Pattachote keyboards; three levels
of strictness for input sequence check.

%prep
%setup -q

%build
export CFLAGS="$CFLAGS -fvisibility=hidden -fPIC"
export CXXFLAGS="$CXXFLAGS -fvisibility=hidden -fPIC"
export CPPFLAGS="$CPPFLAGS -DEXPORTED=__attribute__\(\(visibility\(\\\"default\\\"\)\)\)"

%configure --prefix=%{_prefix} --disable-static

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}%{_datadir}/packages/
cp %{name}.xml %{buildroot}%{_datadir}/packages/

%post

%postun

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_datadir}/scim/icons/*
%{_datadir}/locale/*
%{_datadir}/packages/*
%{_libdir}/scim-1.0/1.4.0/IMEngine/*.so
