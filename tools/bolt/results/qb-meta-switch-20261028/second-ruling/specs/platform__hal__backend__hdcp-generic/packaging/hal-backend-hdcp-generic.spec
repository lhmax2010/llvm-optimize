Name:       hal-backend-hdcp-generic
Summary:    Tizen HDCP Hal backend
Version:    1.0.2
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Provides:   libhal-backend-hdcp.so

BuildRequires:  cmake
BuildRequires:  pkgconfig(hal-rootstrap)

%description
Tizen HDCP Hal backend.

%prep
%setup -q -n %{name}-%{version}

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE  -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE  -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""

%cmake . \
	-DSYSCONFDIR=%{_hal_sysconfdir} \
	-DCMAKE_HAL_LIBDIR_PREFIX=%{_hal_libdir} \
	-DCMAKE_HAL_LICENSEDIR_PREFIX=%{_hal_licensedir} \
	-DLIB_NAME="hal-backend-hdcp" \
	-DUSE_DLOG="1"

make %{?jobs:-j%jobs}

%install
%make_install

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest hal-backend-hdcp-generic.manifest
%defattr(-,root,root,-)
%{_hal_libdir}/libhal-backend-hdcp.so
%license LICENSE.APLv2
