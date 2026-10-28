%define name	hal-rootstrap-data-common
%define desc    HAL Rootstrap for Common Profile

%if "%{_with_da_profile}" == "1"
%define WITH_DA 1
%else
%define WITH_DA 0
%endif

%if "%{tizen_profile_name}" == "tv"
%define WITH_VD 1
%else
%define WITH_VD 0
%endif

%if "%{mv_prj}" == "1"
%define WITH_VD_MV 1
%else
%define WITH_VD_MV 0
%endif

Name:		%{name}
Summary:	%{desc}
Version:	10.0.0
Release:	1
#Group:
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
AutoReqProv:	no

Requires:	capi-base-common
BuildRequires:	capi-base-common
Requires:	capi-base-common-devel
BuildRequires:	capi-base-common-devel
Requires:	capi-base-utils
BuildRequires:	capi-base-utils
Requires:	capi-base-utils-devel
BuildRequires:	capi-base-utils-devel
Requires:	capi-system-info
BuildRequires:	capi-system-info
Requires:	capi-system-info-devel
BuildRequires:	capi-system-info-devel
Requires:	capi-system-runtime-info
BuildRequires:	capi-system-runtime-info
Requires:	capi-system-runtime-info-devel
BuildRequires:	capi-system-runtime-info-devel
Requires:	libtbm
BuildRequires:	libtbm
Requires:	libtbm-devel
BuildRequires:	libtbm-devel
Requires:	coregl
BuildRequires:	coregl
Requires:	coregl-devel
BuildRequires:	coregl-devel
Requires:	glib2-devel
BuildRequires:	glib2-devel
Requires:	glib2-devel-static
BuildRequires:	glib2-devel-static
Requires:	libgio
BuildRequires:	libgio
Requires:	libglib
BuildRequires:	libglib
Requires:	libgmodule
BuildRequires:	libgmodule
Requires:	libgobject
BuildRequires:	libgobject
Requires:	libgthread
BuildRequires:	libgthread

Requires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(alsa)
Requires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libusb-1.0)
Requires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(json-glib-1.0)
Requires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(libudev)
Requires:	pkgconfig(ttrace)
BuildRequires:	pkgconfig(ttrace)
Requires:	pkgconfig(libtzplatform-config)
BuildRequires:	pkgconfig(libtzplatform-config)
Requires:	pkgconfig(tpl-egl)
BuildRequires:	pkgconfig(tpl-egl)

Requires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(libdrm)

Requires:	pkgconfig(hal-api-audio)
BuildRequires:	pkgconfig(hal-api-audio)
Requires:	pkgconfig(hal-api-camera)
BuildRequires:	pkgconfig(hal-api-camera)
Requires:	pkgconfig(hal-api-common)
BuildRequires:	pkgconfig(hal-api-common)
Requires:	pkgconfig(hal-api-device)
BuildRequires:	pkgconfig(hal-api-device)
Requires:	pkgconfig(hal-api-nfc)
BuildRequires:	pkgconfig(hal-api-nfc)
Requires:	pkgconfig(hal-api-sensor)
BuildRequires:	pkgconfig(hal-api-sensor)
Requires:	pkgconfig(hal-api-tbm)
BuildRequires:	pkgconfig(hal-api-tbm)
Requires:	pkgconfig(hal-api-tdm)
BuildRequires:	pkgconfig(hal-api-tdm)

%if "%{WITH_VD}" == "0" && "%{WITH_VD_MV}" == "0"
Requires:	glibc
BuildRequires:	glibc
Requires:	glibc-devel
BuildRequires:	glibc-devel
Requires:	glibc-devel-static
BuildRequires:	glibc-devel-static
Requires:	glibc-devel-utils
BuildRequires:	glibc-devel-utils
Requires:	glibc-extra
BuildRequires:	glibc-extra
Requires:	glibc-locale
BuildRequires:	glibc-locale
Requires:	glibc-profile
BuildRequires:	glibc-profile
Requires:	linux-glibc-devel
BuildRequires:	linux-glibc-devel
Requires:	pkgconfig(capi-system-peripheral-io)
BuildRequires:	pkgconfig(capi-system-peripheral-io)
Requires:	pkgconfig(hal-api-bluetooth)
BuildRequires:	pkgconfig(hal-api-bluetooth)
Requires:	pkgconfig(hal-api-location)
BuildRequires:	pkgconfig(hal-api-location)
Requires:	pkgconfig(hal-api-power)
BuildRequires:	pkgconfig(hal-api-power)
Requires:	pkgconfig(hal-api-radio)
BuildRequires:	pkgconfig(hal-api-radio)
Requires:	pkgconfig(hal-api-wifi)
BuildRequires:	pkgconfig(hal-api-wifi)
Requires:	pkgconfig(hal-api-codec)
BuildRequires:	pkgconfig(hal-api-codec)
Requires:	pkgconfig(hal-api-drm)
BuildRequires:	pkgconfig(hal-api-drm)
Requires:	pkgconfig(hal-api-hdcp)
BuildRequires:	pkgconfig(hal-api-hdcp)
Requires:	pkgconfig(hal-api-security)
BuildRequires:	pkgconfig(hal-api-security)
Requires:	pkgconfig(hal-api-ml)
BuildRequires:	pkgconfig(hal-api-ml)
%endif

%if "%{WITH_DA}" == "0"
Requires:	pkgconfig(libdrm_vigs)
BuildRequires:	pkgconfig(libdrm_vigs)
%ifarch arm aarch64
Requires:	pkgconfig(libdrm_vc4)
BuildRequires:	pkgconfig(libdrm_vc4)
%endif
%endif

%description
%{desc}

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir %{buildroot}
mkdir -p %{buildroot}/tmp
ls -al
cp -R ./rs_resource %{buildroot}/tmp
%if "%{WITH_VD}" == "1" || "%{WITH_VD_MV}" == "1"
rm -f %{buildroot}/tmp/rs_resource/NativeAPI/capi-system-peripheral-io-rs.xml
rm -f %{buildroot}/tmp/rs_resource/HAL/hal-api-bluetooth-rs.xml
rm -f %{buildroot}/tmp/rs_resource/HAL/hal-api-location-rs.xml
rm -f %{buildroot}/tmp/rs_resource/HAL/hal-api-power-rs.xml
rm -f %{buildroot}/tmp/rs_resource/HAL/hal-api-radio-rs.xml
rm -f %{buildroot}/tmp/rs_resource/HAL/hal-api-wifi-rs.xml
%endif

%files
/tmp/*
