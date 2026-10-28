Name:           alure
Version:        1.2
Release:        3
License:        MIT
Summary:        File-loading and utility functions for OpenAL
Group:          System Environment/Libraries
URL:            http://kcat.strangesoft.net/alure.html
Group:          System/Libraries
Source:         %{name}-%{version}.tar.bz2
Source1001:     alure.manifest
BuildRequires:  cmake, libsndfile-devel, openal-soft-devel

%description
ALURE is a utility library to help manage common tasks with OpenAL applications

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       pkgconfig

%description devel
ALURE is a utility library to help manage common tasks with OpenAL applications

%prep
%setup -q
cp %{SOURCE1001} .

%build

%cmake .
make %{?_smp_mflags}

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license COPYING
%{_libdir}/libalure.so.*
%exclude %{_bindir}/alure*

%files devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%exclude /usr/share/doc/alure/html/*
%{_includedir}/AL/alure.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
