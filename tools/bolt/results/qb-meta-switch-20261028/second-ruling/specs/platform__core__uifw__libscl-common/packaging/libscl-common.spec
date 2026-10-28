Name:       libscl-common
Summary:    A library for developing software keyboards
Version:    0.11.2
Release:    1
Group:      Graphics & UI Framework/Input
License:    Apache-2.0
Source0:    libscl-common-%{version}.tar.gz
BuildRequires:  cmake


%description
A library that helps developing S/W Keyboard

%package devel
Summary:    SCL-Common header file
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
A devel package of libscl-common library that helps developing S/W Keyboard

%prep
%setup -q


%build
rm -rf CMakeFiles
rm -rf CMakeCache.txt

%cmake .
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install



%post

%postun

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libscl-common.so
%license LICENSE

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/libscl-common.pc
