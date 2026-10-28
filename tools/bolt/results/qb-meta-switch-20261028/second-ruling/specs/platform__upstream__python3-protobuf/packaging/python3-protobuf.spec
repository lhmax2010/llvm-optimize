Name:       python3-protobuf
Summary:    Protocol Buffers for Python
Version:    6.33.5
Release:    0
License:    BSD-3-Clause
Group:      Development/Languages/Python
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: LICENSE.BSD-3-Clause

BuildRequires:  pkgconfig(python3)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  python3-setuptools

%description
Protocol Buffers are Google's data interchange format.

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
export CFLAGS="$CFLAGS -Wno-error=int-conversion"
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
%license LICENSE.BSD-3-Clause
%{python3_sitearch}/google/*
%{python3_sitearch}/protobuf-%{version}-py%{python3_version}.egg-info/*
