Name:          opus
VCS:           platform/upstream/opus#fc25c776d00208a7a0d3caf4d37711fd8bf7a141
Version:       1.3.1
Release:       2.1
Summary:       An audio codec for use in low-delay speech and audio communication
Group:         System Environment/Libraries
License:       BSD-3-Clause
URL:           http://www.opus-codec.org/
Source0:       %{name}-%{version}.tar.gz
Source1001:    %{name}.manifest
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Opus codec is designed for interactive speech and audio transmission over
the Internet. It is designed by the IETF Codec Working Group and incorporates
technology from Skype's SILK codec and Xiph.Org's CELT codec.

%package devel
Summary: Development package for opus
Group: Development/Libraries
Requires: libogg-devel
Requires: opus = %{version}-%{release}

%description devel
Files for development with opus.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
%configure --enable-custom-modes --disable-static
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Remove libtool archives and static libs

find %{buildroot} -type f -name "*.la" -delete
rm -rf %{buildroot}%{_datadir}/doc/opus/html

#%check
#make check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libopus.so.*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/opus/*.h
%{_libdir}/libopus.so
%{_libdir}/pkgconfig/opus.pc
%{_datadir}/aclocal/opus.m4

%changelog

