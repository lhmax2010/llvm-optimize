%define enable_zero_copy 0

Name:       hal-backend-camera-v4l2
Summary:    Tizen Camera Hal using generic V4L2 interface
Version:    1.4.1
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  pkgconfig(hal-rootstrap)

%description
Tizen Camera Hal using generic V4L2 interface.


%prep
%setup -q


%build
%if 0%{?enable_zero_copy}
export CFLAGS+=" -DTIZEN_FEATURE_ZERO_COPY_SUPPORT"
%endif
./autogen.sh
%configure \
	--disable-static\
	--libdir=%{_hal_libdir}
make %{?jobs:-j%jobs}

%install
%make_install
mkdir -p %{buildroot}%{_hal_licensedir}/%{name}
cp LICENSE.APLv2 %{buildroot}%{_hal_licensedir}/%{name}


%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_hal_licensedir}/%{name}/*
%defattr(-,root,root,-)
%{_hal_libdir}/*.so

