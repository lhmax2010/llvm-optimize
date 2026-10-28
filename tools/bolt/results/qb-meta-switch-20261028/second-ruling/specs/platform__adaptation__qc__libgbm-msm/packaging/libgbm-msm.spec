Summary:        QC contributed GBM
Name:           libgbm-msm
Version:        1.0.0
Release:        0
Group:          System/Libraries
License:        BSD-3-Clause and BSD-3-Clause-Clear and MIT and Apache-2.0
Source:	        %{name}-%{version}.tar.gz
ExclusiveArch:  aarch64

BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  linux-qc-kernel-headers
BuildConflicts: linux-glibc-devel

%description
Provide QC contributed GBM (Generic Buffer Management) Library

%package devel
Summary:    Development header files for QC contributed GBM
Group:      System/Libraries
Requires:   %{name}

%description devel
Development header files for QC contributed GBM

%package vendor
summary: Vendor cfgs for for QC contributed GBM

%description vendor
Vendor cfgs for QC contributed GBM

%prep
%setup -q -n %{name}

%build
export CFLAGS+=" -fPIC -I/usr/include/glib-2.0/ -DUSE-GLIB"
export LDFLAGS+=" -lglib-2.0"
%reconfigure --disable-static --enable-compilewithdrm --with-glib --enable-wayland-support\
            CFLAGS="${CFLAGS} -Wall"

make libdir=%{_hal_libdir}

%install
mkdir -p %{buildroot}/%{_hal_libdir}
%makeinstall libdir=%{buildroot}/%{_hal_libdir}
rm -f %{buildroot}/%{_hal_libdir}/*.la

ln -sf libgbm.so %{buildroot}/%{_hal_libdir}/libgbm.so.1
ln -sf libgbm.so.1 %{buildroot}/%{_hal_libdir}/libgbm.so.1.0.0

# Replace name to avoid conflict with public libgbm
mv %{buildroot}/%{_hal_libdir}/pkgconfig/gbm.pc %{buildroot}/%{_hal_libdir}/pkgconfig/gbm-msm.pc

mkdir -p %{buildroot}/etc/vendor/platform
cp tizen.vendor/vendor-%{name}.cfg %{buildroot}/etc/vendor/platform

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
mv %{_hal_libdir}/pkgconfig/gbm-msm.pc %{_hal_libdir}/pkgconfig/gbm.pc

%postun devel
mv %{_hal_libdir}/pkgconfig/gbm.pc %{_hal_libdir}/pkgconfig/gbm-msm.pc

%files
%manifest packaging/%{name}.manifest
%license BSD-3-Clause BSD-3-Clause-Clear NOTICE
%defattr(-,root,root,-)
%{_hal_libdir}/libgbm.so*

%files devel
%defattr(-,root,root,-)
%{_includedir}/gbm_priv.h
%{_includedir}/gbm.h
%{_hal_libdir}/pkgconfig/gbm-msm.pc

%files vendor
/etc/vendor/platform/vendor-%{name}.cfg
