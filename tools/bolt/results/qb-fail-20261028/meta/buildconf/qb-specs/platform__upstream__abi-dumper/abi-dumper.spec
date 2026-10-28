Name:           abi-dumper
Version:        1.4
Release:        1
Summary:        Tool to dump ABI of an ELF object containing DWARF debug info
License:        LGPL-2.1-or-later
Group:          Development/Tools
URL:            https://github.com/lvc/abi-dumper
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source1000:     abi-dumper-ctags-detection.patch
Source1001:     abi-dumper-hex-overflow.patch
BuildRequires:  perl
BuildRequires:  make
Requires:       perl
Requires:       elfutils
Requires:       binutils
Requires:       ctags

%description
ABI Dumper is a tool to dump ABI of an ELF object containing DWARF
debug info. The tool is intended to be used with ABI Compliance
Checker to track ABI changes of a C/C++ library or a kernel module.

Runtime requirements of the tool (not needed at build time):
  - Elfutils (eu-readelf)
  - Binutils (objdump)
  - Universal Ctags
  - Vtable-Dumper (1.1 or newer) - needed only for C++ vtable info
  - GCC C++

%prep
%setup -q -n %{name}-%{version}
%{__patch} -p1 < %{SOURCE1000}
%{__patch} -p1 < %{SOURCE1001}
cp %{SOURCE1} .

%build
# Perl script package: nothing to compile

%install
mkdir -p %{buildroot}%{_prefix}
DESTDIR=%{buildroot} make install prefix=%{_prefix}
%{remove_docs}

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/%{name}
