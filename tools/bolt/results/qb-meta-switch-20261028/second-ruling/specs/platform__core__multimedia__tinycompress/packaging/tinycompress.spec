Name:       tinycompress
Summary:    userspace library for alsa compressed API
Version:    1.1.8
Release:    1
Group:      System/Libraries
License:    LGPL-2.1 or BSD-3-Clause
Source0:    tinycompress-%{version}.tar.gz
Source1001: %{name}.manifest
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: pkgconfig(alsa)

%description
userspace library for alsa compressed API

%package devel
Summary:    tinycompress headers and libraries for development.
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
tinycompress headers and libraries for development.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
chmod +x autogen.sh
%autogen.sh
%configure
make %{?jobs:-j%jobs}


%install
rm -rf %{buildroot}
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/cplay
%{_bindir}/crecord
%{_libdir}/libtinycompress.so.*
%license COPYING

%files devel
%manifest %{name}.manifest
%{_libdir}/libtinycompress.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/tinycompress/tinycompress.h
#%{_includedir}/tinycompress/tinymp3.h
#%{_includedir}/tinycompress/version.h
#%{_includedir}/sound/compress_offload.h
#%{_includedir}/sound/compress_params.h
