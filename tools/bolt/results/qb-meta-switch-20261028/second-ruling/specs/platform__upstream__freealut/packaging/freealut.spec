Name:       freealut
Summary:    OpenAL User Toolkit library
Version:    1.1.0
Release:    5
Group:		System/Libraries
URL:		http://openal.org/
License:	LGPL-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	freealut.manifest
BuildRequires:  pkgconfig(openal)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig


%description
OpenAL User Toolkit library development package


%package devel
Summary:    OpenAL User Toolkit library (devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
OpenAL User Toolkit library development package (devel)


%prep
%setup -q
cp %{SOURCE1001} .


%build
./autogen.sh
%configure --disable-static
%__make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root,-)
%exclude %{_bindir}/freealut-config
%{_libdir}/libalut.so.*


%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/AL/alut.h
%{_libdir}/libalut.so
%{_libdir}/pkgconfig/freealut.pc
