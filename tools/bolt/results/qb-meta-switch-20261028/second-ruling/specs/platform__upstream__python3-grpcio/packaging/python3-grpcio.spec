Name:       python3-grpcio
Summary:    HTTP/2-based Remote Procedure Call implementation
Version:    1.76.0
Release:    0

# ==========================================================
License:    Apache-2.0
# ==========================================================

Group:      Development/Languages/Python
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

# ==========================================================
# BuildRequires
# specifies build-time dependencies for the package
# ==========================================================
BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools
BuildRequires:  python3-protobuf
BuildRequires:  python3-six

Requires:       python3-protobuf

%description
gRPC is a remote procedure call (RPC) framework. gRPC enables client
and server applications to communicate, and enables the building of
connected systems.


%prep
%setup -q
cp %{SOURCE1001} .

# ==========================================================
# build section
# how to actually build the software we are packaging
# ==========================================================
%build
%{_bindir}/python3 setup.py build


# ==========================================================
# install section
# how to actually build the software we are packaging
# ==========================================================
%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

# ==========================================================
# files section
# The list of files that will be installed in the end
# user’s system.
# ==========================================================
%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitearch}/grpc/*
%{python3_sitearch}/grpcio-%{version}-py%{python3_version}.egg-info/*

