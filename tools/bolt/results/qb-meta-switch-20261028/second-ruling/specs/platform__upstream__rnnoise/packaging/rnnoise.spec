%global date 20210312
Name:       rnnoise
Version:    0
Release:    0.4
Summary:    Recurrent neural network for audio noise reduction
License:    BSD-3-Clause
URL:        https://gitlab.xiph.org/xiph/rnnoise
Source0:    %{name}-%{version}.%{date}.tar.gz
Source1:    %{name}.manifest

%description
RNNoise is a noise suppression library based on a recurrent neural network.

While it is meant to be used as a library, a simple command-line tool is
provided as an example. It operates on RAW 16-bit (machine endian) mono PCM
files sampled at 48 kHz. It can be used as:

./examples/rnnoise_demo <noisy speech> <output denoised>

The output is also a 16-bit raw PCM file.

%package    devel
Summary:    Devel files for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
Devel files for %{name}.

%prep
%setup -q
cp %{SOURCE1} .

cat > 'package_version' <<-EOF
    PACKAGE_VERSION=%{date}
EOF

%build
./autogen.sh
%configure \
    --disable-static
%make_build

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

rm -fv %{buildroot}%{_libdir}/lib*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/lib%{name}.so.0*
%exclude %{_datadir}/doc/%{name}/AUTHORS
%exclude /usr/share/doc/%{name}/COPYING
%exclude /usr/share/doc/%{name}/README

%files devel
%{_includedir}/*.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/*.pc
