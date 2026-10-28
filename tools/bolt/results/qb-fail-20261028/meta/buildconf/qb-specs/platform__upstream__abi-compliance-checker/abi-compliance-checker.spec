Name:           abi-compliance-checker
Version:        2.3
Release:        1
Summary:        ABI Compliance Checker - a tool for checking ABI compatibility of C/C++ libraries
License:        LGPL-2.1-or-later
URL:            https://github.com/lvc/abi-compliance-checker
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  coreutils
Requires:       perl
Requires:       ctags

%description
ABI Compliance Checker is a tool for checking backward binary and source-level
compatibility of a C/C++ software library. It analyzes two versions of a
library (headers and shared objects) and detects incompatible ABI changes,
including removed symbols, changed virtual-table layouts and other binary
incompatibilities that can break applications built against the old version.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} .

%build
# Pure Perl application: nothing to compile.

%install
# Makefile.pl requires the destination prefix directory to exist beforehand
mkdir -p %{buildroot}%{_prefix}
perl Makefile.pl -install -prefix %{_prefix} -destdir %{buildroot}

# Remove unnecessary files
%{remove_docs}

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/
