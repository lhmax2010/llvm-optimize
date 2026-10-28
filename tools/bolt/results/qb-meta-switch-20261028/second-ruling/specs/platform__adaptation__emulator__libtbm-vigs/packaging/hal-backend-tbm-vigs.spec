Name:           hal-backend-tbm-vigs
Version:        3.1.2
Release:        1
License:        MIT
Summary:        hal tbm backend module for vigs
Group:          System/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(hal-rootstrap)

%description
description: hal tbm backend module for vigs

%package devel
Summary:        hal-backend-tbm library for vigs
Group:          System/Libraries
Requires:       hal-backend-tbm-vigs

%description devel
description: hal tbm backend library headers for vigs

%prep
%setup -q
cp %{SOURCE1001} .

%build
autoreconf -vfi
./configure --prefix=%{_prefix} --libdir=%{_libdir} \
            --with-hal-libdir=%{_hal_libdir} \
            CFLAGS="${CFLAGS} -Wall -Werror" LDFLAGS="${LDFLAGS} -Wl,--hash-style=both -Wl,--as-needed"

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

# make rule and license files
mkdir -p %{buildroot}%{_hal_licensedir}/libhal-backend-tbm-vigs
cp -af COPYING %{buildroot}%{_hal_licensedir}/libhal-backend-tbm-vigs

%post
if [ -f %{_hal_libdir}/libhal-backend-tbm.so ]; then
    rm -rf %{_hal_libdir}/libhal-backend-tbm.so
fi
ln -s libhal-backend-tbm-vigs.so %{_hal_libdir}/libhal-backend-tbm.so

%postun -n hal-backend-tbm-vigs -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_hal_licensedir}/libhal-backend-tbm-vigs/COPYING
%{_hal_libdir}/libhal-backend-*.so*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}
%{_includedir}/tbm-vigs/libhal_backend_tbm_vigs.h
%{_hal_libdir}/libhal-backend-tbm*.so
%{_libdir}/pkgconfig/hal-backend-tbm-vigs.pc
