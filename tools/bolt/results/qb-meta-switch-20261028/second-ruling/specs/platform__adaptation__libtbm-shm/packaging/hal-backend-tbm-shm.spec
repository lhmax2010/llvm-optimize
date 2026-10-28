Name:           hal-backend-tbm-shm
Version:        3.1.1
Release:        1
License:        MIT
Summary:        hal-backend-tbm module for shm
Group:          System/Libraries
ExcludeArch:    i586
Source0:        %{name}-%{version}.tar.gz
Source1001:	    %{name}.manifest

BuildRequires:  pkgconfig(hal-rootstrap)

%description
description: hal tbm backend module for drm shm

%global TZ_SYS_RO_SHARE  %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:/usr/share}

%prep
%setup -q
cp %{SOURCE1001} .

%build

%reconfigure --prefix=%{_prefix} --libdir=%{_libdir} \
			--with-hal-libdir=%{_hal_libdir} \
			--disable-cachectrl \
			FLAGS="${CFLAGS} -Wall -Werror" LDFLAGS="${LDFLAGS} -Wl,--hash-style=both -Wl,--as-needed"

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

# make rule and license files
mkdir -p %{buildroot}%{_hal_licensedir}/libhal-backend-tbm-shm
cp -af COPYING %{buildroot}%{_hal_licensedir}/libhal-backend-tbm-shm

%post
if [ -f %{_hal_libdir}/libhal-backend-tbm.so ]; then
    rm -rf %{_hal_libdir}/libhal-backend-tbm.so
fi
ln -s libhal-backend-tbm-shm.so %{_hal_libdir}/libhal-backend-tbm.so

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_hal_licensedir}/libhal-backend-tbm-shm/COPYING
%{_hal_libdir}/libhal-backend-*.so*
