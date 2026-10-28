Name:           vtable-dumper
Version:        1.2
Release:        1
Summary:        A tool to list content of virtual tables in a C++ shared library
License:        GPL-2.0-or-later or LGPL-2.0-or-later
URL:            https://github.com/lvc/vtable-dumper
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
BuildRequires:  gcc-c++
BuildRequires:  libelf-devel

%description
Vtable-Dumper is a tool to list content of virtual tables in a C++ shared
library. It is intended for developers of software libraries and maintainers
of Linux distributions who are interested in ensuring backward binary
compatibility.

%prep
%setup -q
cp %{SOURCE1} .

%build
%__make %{?_smp_mflags} CC="gcc"

%install
%make_install
%{remove_docs}

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/vtable-dumper
