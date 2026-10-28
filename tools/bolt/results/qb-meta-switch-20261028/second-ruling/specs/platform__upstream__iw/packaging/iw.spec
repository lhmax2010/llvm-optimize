Name:           iw
Summary:        Wireless configuration tool
License:        0BSD
Version:        5.9
Release:        0
Url:            https://git.kernel.org/pub/scm/linux/kernel/git/jberg/iw.git
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
BuildRequires: pkgconfig(libnl-3.0)

%description
Wireless configuration tool

%prep
%setup -q

%build
cp %{SOURCE1001} .
make %{?_smp_mflags}

%install
#rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp -f ./iw %{buildroot}%{_bindir}/iw

%files
%{_bindir}/iw
