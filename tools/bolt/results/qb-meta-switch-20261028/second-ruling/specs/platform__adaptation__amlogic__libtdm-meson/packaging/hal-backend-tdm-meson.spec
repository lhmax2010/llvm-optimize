Name:           hal-backend-tdm-meson
Version:        1.1.2
Release:        0
Summary:        hal-backend-tdm module for meson
Group:          Development/Libraries
License:        MIT
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires: pkgconfig(hal-rootstrap)
ExclusiveArch: %{arm} aarch64

%description
description: hal tdm backend module for meson

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

%post
if [ -f %{_hal_libdir}/libhal-backend-tdm.so ]; then
    rm -rf %{_hal_libdir}/libhal-backend-tdm.so
fi
ln -s libhal-backend-tdm-meson.so %{_hal_libdir}/libhal-backend-tdm.so

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%{_hal_libdir}/libhal-backend-*.so*
