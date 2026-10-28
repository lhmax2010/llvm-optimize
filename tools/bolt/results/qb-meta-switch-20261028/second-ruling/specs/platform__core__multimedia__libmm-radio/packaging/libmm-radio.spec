Name:       libmm-radio
Summary:    Multimedia Framework Radio Library
Version:    0.3.8
Release:    0
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	libmm-radio.manifest
BuildRequires:  pkgconfig(mm-common)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-media-sound-manager)
%ifnarch %{arm}
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
%endif
BuildRequires:  pkgconfig(resource-manager)
BuildRequires:  pkgconfig(resource-information)
BuildRequires:  pkgconfig(resource-center-api)
%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif
BuildRequires:  pkgconfig(hal-api-radio)

%description
Description: Multimedia Framework Radio Library


%package devel
Summary:    Multimedia Framework Radio Library (DEV)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Description: Multimedia Framework Radio Library (DEV)

%prep
%setup -q
cp %{SOURCE1001} .

%build
./autogen.sh

export CFLAGS="$CFLAGS %{optflags} -Wall"
%ifarch %{arm}
export CFLAGS="$CFLAGS -fPIC -DTIZEN_FEATURE_RADIO_HAL -DPATH_LIBDIR=\\\"%{_libdir}\\\""
export CXXFLAGS="$CXXFLAGS -fPIC"
%if 0%{?gtests:1}
export CXXFLAGS="$CXXFLAGS -DTIZEN_FEATURE_RADIO_HAL -DPATH_LIBDIR=\\\"%{_libdir}\\\""
%endif
%endif
export LDFLAGS="$LDFLAGS -Wl,--as-needed -Wl,--rpath=%{_libdir}/hal"

%configure \
%ifnarch %{arm}
--enable-emulator \
%endif
%if 0%{?gtests:1}
--enable-tests \
%endif
--enable-sound-vstream \
--disable-static --prefix=%{_prefix}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install


%post -p /sbin/ldconfig

%postun  -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libmmfradio.so.*
%license LICENSE.Apache-2.0
%if 0%{?gtests:1}
%{_bindir}/gtest_libmm_radio
%endif

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libmmfradio.so
%{_libdir}/pkgconfig/mm-radio.pc
%{_includedir}/mmf/mm_radio.h
