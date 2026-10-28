Name:           srt
Version:        1.5.0
Release:        1
License:        MPL-2.0
Summary:        SRT (Secure Reliable Transport) library
Url:            https://github.com/Haivision/srt
Group:          Multimedia/Libraries
Source0:        %{name}-%{version}.tar.gz
Source99:       baselibs.conf
Source1001:     srt.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  pkgconfig(tcl)

%description
SRT allows users to deliver high-quality,
low-latency video streams across the public internet.

%package devel
Summary:    SRT (Secure Reliable Transport) library
Group:      Multimedia/Libraries
Requires:       %{name} = %{version}

%description devel
SRT allows users to deliver high-quality,
low-latency video streams across the public internet.

%prep
%setup -q -n %{name}-%{version}

cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -Wall -g -fPIC"
export LDFLAGS="$LDFLAGS -pthread "

chmod +x ./configure
%configure \
  --disable-static \
  --prefix=/usr/ \
  --with-pic

make

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/srt/*.h
%{_libdir}/pkgconfig/*.pc
