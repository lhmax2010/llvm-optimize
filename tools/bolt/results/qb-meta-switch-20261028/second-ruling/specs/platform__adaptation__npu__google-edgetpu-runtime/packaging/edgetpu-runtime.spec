Name:		edgetpu-runtime
Summary:	Support library for Edge TPU
Version:	12.1
Release:	0
Group:		Development/Libraries
Packager:	MyungJoo Ham <myungjoo.ham@samsung.com>
License:	Apache-2.0
Source0:	edgetpu-runtime-%{version}.tar.gz
Source1001:	edgetpu-runtime.manifest
Source1002:	edgetpu.pc.in
ExclusiveArch:	aarch64 x86_64

%description
This is repackaging of libedgetpu1-*.deb of Ubuntu at
https://packages.cloud.google.com/apt

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
sed -i 's|@PREFIX@|%{_prefix}|' edgetpu.pc.in
sed -i 's|@EXEC_PREFIX@|%{_exec_prefix}|' edgetpu.pc.in
sed -i 's|@LIB_INSTALL_DIR@|%{_libdir}|' edgetpu.pc.in
sed -i 's|@INCLUDE_INSTALL_DIR@|%{_includedir}|' edgetpu.pc.in
sed -i 's|@VERSION@|%{version}|' edgetpu.pc.in
mv edgetpu.pc.in edgetpu.pc

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_includedir}/edgetpu
%ifarch aarch64
install -p -m 0755 libedgetpu/direct/aarch64/libedgetpu.so.1.0 %{buildroot}%{_libdir}/libedgetpu-max.so.1.0
install -p -m 0755 libedgetpu/throttled/aarch64/libedgetpu.so.1.0 %{buildroot}%{_libdir}/libedgetpu-std.so.1.0
%endif
%ifarch x86_64
install -p -m 0755 libedgetpu/direct/k8/libedgetpu.so.1.0 %{buildroot}%{_libdir}/libedgetpu-max.so.1.0
install -p -m 0755 libedgetpu/throttled/k8/libedgetpu.so.1.0 %{buildroot}%{_libdir}/libedgetpu-std.so.1.0
%endif
install -p -m 0644 libedgetpu/*.h %{buildroot}%{_includedir}/

pushd %{buildroot}%{_libdir}
ln -sf libedgetpu-max.so.1.0 libedgetpu-max.so.1
ln -sf libedgetpu-std.so.1.0 libedgetpu-std.so.1
ln -sf libedgetpu.so.1 libedgetpu.so
popd
install -p -m 0644 edgetpu.pc %{buildroot}%{_libdir}/pkgconfig/

%package -n libedgetpu1
Summary:	Metapackage for edgetpu-runtime library
Requires:	libedgetpu1-driver = %{version}-%{release}
Recommends:	libedgetpu1-std = %{version}-%{release}
%description -n libedgetpu1
Metapacakge for edgetpu-runtime library.
By default it uses "std" library instead of "max" library.
%files -n libedgetpu1

%package -n libedgetpu1-std
Summary:	Standard throttling version of edgetpu-runtime library
Provides:	libedgetpu1-driver = %{version}-%{release}
Conflicts:	libedgetpu1-max
%description -n libedgetpu1-std
Standard throttled edgetpu-runtime library

%files -n libedgetpu1-std
%manifest edgetpu-runtime.manifest
%license LICENSE
%{_libdir}/libedgetpu-std.so.1
%{_libdir}/libedgetpu-std.so.1.0

%post -n libedgetpu1-std
pushd %{_libdir}
ln -sf libedgetpu-std.so.1 libedgetpu.so.1
ln -sf libedgetpu-std.so.1.0 libedgetpu.so.1.0
popd
/sbin/ldconfig
%postun -n libedgetpu1-std
# If it's uninstall
if [ "$1" == "0" ]; then
rm %{_libdir}/libedgetpu.so.1
rm %{_libdir}/libedgetpu.so.1.0
fi
/sbin/ldconfig

%package -n libedgetpu1-max
Summary:	Max-performance version of edgetpu-runtime library
Provides:	libedgetpu1-driver = %{version}-%{release}
Conflicts:	libedgetpu1-std
%description -n libedgetpu1-max
Non-throttled, max-performance edgetpu-runtime library

%files -n libedgetpu1-max
%manifest edgetpu-runtime.manifest
%license LICENSE
%{_libdir}/libedgetpu-max.so.1
%{_libdir}/libedgetpu-max.so.1.0

%post -n libedgetpu1-max
pushd %{_libdir}
ln -sf libedgetpu-max.so.1 libedgetpu.so.1
ln -sf libedgetpu-max.so.1.0 libedgetpu.so.1.0
popd
/sbin/ldconfig
%postun -n libedgetpu1-max
# If it's uninstall
if [ "$1" == "0" ]; then
rm %{_libdir}/libedgetpu.so.1
rm %{_libdir}/libedgetpu.so.1.0
fi
/sbin/ldconfig

%package -n libedgetpu-dev
Summary:	Developmental support for libedgetpu
Requires:	libedgetpu1 = %{version}-%{release}
%description -n libedgetpu-dev
Developmental support for libedgetpu

%files -n libedgetpu-dev
%{_libdir}/libedgetpu.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
