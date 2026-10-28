Name:           soundtouch
Version:        2.1.0
Release:        0
License:        LGPL-2.1
Summary:        Audio processing library
Url:            https://gitlab.com
Group:          Multimedia/Libraries
Source0:        %{name}-%{version}.tar.bz2
Source99:       baselibs.conf
Source1001:     soundtouch.manifest

%description
Soundtouch is an audio processing library that allows changing
the sound tempo, pitch and playback rate parameters independently from eash other.

%package devel
Summary:        Audio processing library
Group:      Multimedia/Libraries
Requires:       %{name} = %{version}

%description devel
Soundtouch is an audio processing library that allows changing
the sound tempo, pitch and playback rate parameters independently from eash other.

%prep
%setup -q
cp %{SOURCE1001} .

%build
chmod +x ./bootstrap
./bootstrap
chmod +x ./configure
%configure \
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
%defattr(-, root, root)
%license COPYING
%{_libdir}/*.so.*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/soundtouch/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
