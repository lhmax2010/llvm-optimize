Name:       newfs-msdos
Summary:    Newfs-msdos
Version:    1.0.0
Release:    1
Group:      System/Utilities
License:    BSD-2-Clause
Source0:    %{name}-%{version}.tar.gz
Source1:    newfs-msdos.manifest

BuildRequires:  cmake

%description
Newfs-msdos tool

%prep
%setup -q

%build
%cmake .

cp %{SOURCE1} .
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/newfs_msdos
