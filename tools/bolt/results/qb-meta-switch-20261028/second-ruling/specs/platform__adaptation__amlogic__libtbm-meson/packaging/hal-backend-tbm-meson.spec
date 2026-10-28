Name:           hal-backend-tbm-meson
Version:        1.1.1
Release:        1
License:        MIT
Summary:        hal-backend-tbm module for meson
Group:          System/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(hal-rootstrap)
BuildRequires:  kernel-headers-amlogic
BuildConflicts: linux-glibc-devel
ExclusiveArch:  %{arm} aarch64

%description
description: hal tbm backend module for meson

%prep
%setup -q
cp %{SOURCE1001} .

%build

%reconfigure --prefix=%{_prefix} --libdir=%{_libdir} \
			--with-hal-libdir=%{_hal_libdir} \
			CFLAGS="${CFLAGS} -Wall -Werror" LDFLAGS="${LDFLAGS} -Wl,--hash-style=both -Wl,--as-needed"

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

%make_install

%post
if [ -f %{_hal_libdir}/libhal-backend-tbm.so ]; then
    rm -rf %{_hal_libdir}/libhal-backend-tbm.so
fi
ln -s libhal-backend-tbm-meson.so %{_hal_libdir}/libhal-backend-tbm.so

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%{_hal_libdir}/libhal-backend-*.so*
