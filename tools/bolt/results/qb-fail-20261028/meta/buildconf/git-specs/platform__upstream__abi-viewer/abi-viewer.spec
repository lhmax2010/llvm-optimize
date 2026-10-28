Name:           abi-viewer
Version:        1.0
Release:        1
Summary:        Tool to visualize ABI structure of a C/C++ software library
License:        LGPL-2.1-or-later
Group:          Development/Tools
URL:            https://github.com/lvc/abi-viewer
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  make
# Runtime dependencies (README.md: Perl 5, ABI Dumper EE >= 1.4,
# Elfutils (eu-readelf), Vtable-Dumper >= 1.2)
Requires:       perl
Requires:       abi-dumper
# Source requires vtable-dumper >= 1.2; Tizen provides 1.2
Requires:       vtable-dumper >= 1.2
Requires:       elfutils


%description
ABI Viewer is a tool to visualize ABI structure of a C/C++ software
library. It is intended for developers of software libraries and Linux
maintainers who are interested in ensuring backward binary compatibility,
i.e. allow old applications to run with newer library versions.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} .

%build
# Pure Perl tool: no compilation required.
# Upstream install script (Makefile.pl) performs all installation work.

%install
# Makefile.pl requires that the destination directories exist beforehand
# and supports the DESTDIR convention for package building.
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_datadir}/%{name}
make install DESTDIR=%{buildroot} prefix=%{_prefix}

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/abi-viewer
%{_datadir}/%{name}/
