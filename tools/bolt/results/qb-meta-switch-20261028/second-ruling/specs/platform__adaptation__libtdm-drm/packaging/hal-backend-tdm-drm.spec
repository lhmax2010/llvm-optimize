Name:           hal-backend-tdm-drm
Version:        2.2.5
Release:        0
Summary:        hal-backend-tdm module for drm
Group:          System/Libraries
License:        MIT
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires: pkgconfig(hal-rootstrap)

%description
description: hal tdm backend module for drm

%global TZ_SYS_RO_SHARE  %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:/usr/share}

%prep
%setup -q
cp %{SOURCE1001} .

%build
%reconfigure --prefix=%{_prefix} --libdir=%{_libdir}  --disable-static \
             --with-hal-libdir=%{_hal_libdir} \
             CFLAGS="${CFLAGS} -Wall -Werror" \
             LDFLAGS="${LDFLAGS} -Wl,--hash-style=both -Wl,--as-needed"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

# make lincense directory and move COPY to it.
mkdir -p %{buildroot}%{_hal_licensedir}/libhal-backend-tdm-drm
cp -af COPYING %{buildroot}%{_hal_licensedir}/libhal-backend-tdm-drm

%post
if [ -f %{_hal_libdir}/libhal-backend-tdm.so ]; then
    rm -rf %{_hal_libdir}/libhal-backend-tdm.so
fi
ln -s libhal-backend-tdm-drm.so %{_hal_libdir}/libhal-backend-tdm.so

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_hal_licensedir}/libhal-backend-tdm-drm/COPYING
%{_hal_libdir}/libhal-backend-*.so*
