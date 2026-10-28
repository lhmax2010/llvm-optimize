Name:       hal-backend-drm-generic
Summary:    Tizen DRM Hal backend with clearkey
Version:    1.0.3
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Provides:   libhal-backend-drm.so

BuildRequires:  cmake
BuildRequires:  pkgconfig(hal-rootstrap)

%description
Tizen DRM Hal backend.

%prep
%setup -q -n %{name}-%{version}

%build
export CFLAGS="$CFLAGS -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export CXXFLAGS="$CXXFLAGS -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export FFLAGS="$FFLAGS -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""

%cmake . \
	-DSYSCONFDIR=%{_hal_sysconfdir} \
	-DCMAKE_HAL_LIBDIR_PREFIX=%{_hal_libdir} \
	-DCMAKE_HAL_LICENSEDIR_PREFIX=%{_hal_licensedir} \
	-DLIB_NAME="hal-backend-drm"

make %{?jobs:-j%jobs}

%install
%make_install

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest hal-backend-drm-generic.manifest
%defattr(-,root,root,-)
%{_hal_libdir}/libhal-backend-drm.so
%license LICENSE.APLv2
