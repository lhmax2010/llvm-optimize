Name:           hal-backend-tbm-vc4
Version:        3.2.1
Release:        1
License:        MIT
Summary:        hal-backend-tbm module for vc4
Group:          System/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(hal-rootstrap)
ExclusiveArch:  %{arm} aarch64

%description
description: hal tbm backend module for vc4

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

# make rule and license files
mkdir -p %{buildroot}%{_hal_libdir}/udev/rules.d/
cp -af rules/99-libhal-backend-tbm-vc4.rules %{buildroot}%{_hal_libdir}/udev/rules.d/
mkdir -p %{buildroot}%{_hal_licensedir}/libhal-backend-tbm-vc4
cp -af COPYING %{buildroot}%{_hal_licensedir}/libhal-backend-tbm-vc4

%post
if [ -f %{_hal_libdir}/libhal-backend-tbm.so ]; then
    rm -rf %{_hal_libdir}/libhal-backend-tbm.so
fi
ln -s libhal-backend-tbm-vc4.so %{_hal_libdir}/libhal-backend-tbm.so

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_hal_licensedir}/libhal-backend-tbm-vc4/COPYING
%{_hal_libdir}/libhal-backend-*.so*
%{_hal_libdir}/udev/rules.d/99-libhal-backend-tbm-vc4.rules
