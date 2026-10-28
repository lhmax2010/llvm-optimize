Name:       dynpart-tools
Summary:    Host tools for managing dynamic partitions for Tizen
Version:    1.0
Release:    1
Group:      Development/Tools
License:    Apache-2.0
URL:        https://github.com/LonelyFool/lpunpack_and_lpmake
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

BuildRequires:	cmake
BuildRequires:	zlib-devel
BuildRequires:	clang

ExclusiveArch:	x86_64 %ix86

%description
Host tools for managing dynamic partitions for Tizen

%prep
%setup -q

%build
%cmake \
	-DCMAKE_C_COMPILER=clang \
	-DCMAKE_CXX_COMPILER=clang++ \
	.

make

cp %{SOURCE1} .

%install
mkdir -p %{buildroot}%{_bindir}
cp lpadd %{buildroot}%{_bindir}
cp lpdump %{buildroot}%{_bindir}
cp lpflash %{buildroot}%{_bindir}
cp lpmake %{buildroot}%{_bindir}
cp lpunpack %{buildroot}%{_bindir}

%files
%manifest dynpart-tools.manifest
%license LICENSE.Apache-2.0
%{_bindir}/lpadd
%{_bindir}/lpdump
%{_bindir}/lpflash
%{_bindir}/lpmake
%{_bindir}/lpunpack
