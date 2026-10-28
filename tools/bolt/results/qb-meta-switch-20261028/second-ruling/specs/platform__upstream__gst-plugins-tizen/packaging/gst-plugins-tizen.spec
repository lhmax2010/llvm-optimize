%bcond_with wayland
%bcond_with x
%define gst_branch 1.0

Name:       gst-plugins-tizen
Version:    1.24.11
Summary:    GStreamer tizen plugins (common)
Release:    63
Group:      Multimedia/Framework
Url:        http://gstreamer.freedesktop.org/
License:    LGPL-2.1+
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-allocators-1.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(libexif)
%if %{with x}
BuildRequires:  pkgconfig(ecore-x)
BuildRequires:	pkgconfig(libdri2)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(dri2proto)
%endif
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(libdrm_exynos)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:	libdrm-devel
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(gles20)
BuildRequires:  pkgconfig(tpl-egl)
%if ("%{tizen_profile_name}" != "tv") && ("%{mv_prj}" != "1")
BuildRequires:  pkgconfig(tinycompress)
BuildRequires:  pkgconfig(hal-api-common)
# for tizencodec
BuildRequires:  pkgconfig(hal-api-codec)
# for tizenhdcp
BuildRequires:  pkgconfig(hal-api-hdcp)
%endif
%if %{with wayland}
BuildRequires:  pkgconfig(wayland-client) >= 1.0.0
BuildRequires:  pkgconfig(wayland-tbm-client)
BuildRequires:  pkgconfig(tizen-extension-client)
BuildRequires:  pkgconfig(wtz-video-shell-client)
%endif
%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif
BuildRequires:  pkgconfig(capi-media-sound-manager)
# for tizencamerasrc
BuildRequires:  pkgconfig(hal-api-camera)
# for tizenaudiosink
BuildRequires:  pkgconfig(hal-api-audio)

%description
GStreamer tizen plugins (common)


%if ("%{tizen_profile_name}" != "tv") && ("%{mv_prj}" != "1")
%package tinycompresssink
Summary: tinycompress audiosink plugin library

%description tinycompresssink
tinycompress audiosink plugin library


%package codec
Summary: tizen codec plugin

%description codec
codec plugin which uses tizen codec HAL interface.

%package hdcp
Summary: tizen hdcp plugin

%description hdcp
hdcp plugin which uses tizen HDCP HAL interface.
%endif


%package video360
Summary: video360 plugin library

%description video360
video360 plugin library


%package camera
Summary: tizen camera plugin

%description camera
camera plugin which uses tizen camera HAL interface.


%package audio
Summary: tizen audio sink plugin

%description audio
audio sink plugin which uses tizen audio HAL interface.


%prep
%setup -q


%build
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_WLSINK_ENHANCEMENT -DEXPORT_API=\"__attribute__((visibility(\\\"default\\\")))\" \
		-fstack-protector-strong -Wl,-z,relro -D_FORTIFY_SOURCE=2"
./autogen.sh --disable-static
%configure \
%if 0%{?gtests:1}
	--enable-tests \
%endif
%if 0%{?tinycompresstest:1}
	--enable-tinycompress_test\
%endif
%if ("%{tizen_profile_name}" != "tv") && ("%{mv_prj}" != "1")
	--enable-tinycompress\
	--enable-tizencodec\
	--enable-tizenhdcp\
	--enable-tizenaudiosink\
%endif
	--disable-drmdecryptor\
	--enable-ext-wfdtizenmanager\
	--enable-ext-alfec\
	--disable-tizenipc\
	--enable-tizencamerasrc\
	--disable-static\
	--with-tizen-platform \
	--with-native-formats \
	--with-gles2

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%files
%manifest gst-plugins-tizen1.0.manifest
%license COPYING
%defattr(-,root,root,-)
%{_libdir}/gstreamer-%{gst_branch}/*.so
%{_libdir}/libgstwfdbase.so*
%if ("%{tizen_profile_name}" != "tv") && ("%{mv_prj}" != "1")
%exclude %{_libdir}/gstreamer-%{gst_branch}/libgsttinycompress.so
%exclude %{_libdir}/gstreamer-%{gst_branch}/libgsttizenvideodec.so
%exclude %{_libdir}/gstreamer-%{gst_branch}/libgsttizenh264enc.so
%exclude %{_libdir}/gstreamer-%{gst_branch}/libgsttizenhdcp.so
%exclude %{_libdir}/gstreamer-%{gst_branch}/libgsttizenaudiosink.so
%endif
%exclude %{_libdir}/gstreamer-%{gst_branch}/libgstvideo360.so
%exclude %{_libdir}/gstreamer-%{gst_branch}/libgsttizencamerasrc.so
%if 0%{?gtests:1}
%{_bindir}/gtest*
%endif


%if ("%{tizen_profile_name}" != "tv") && ("%{mv_prj}" != "1")

%files tinycompresssink
%manifest gst-plugins-tizen1.0.manifest
%license COPYING
%defattr(-,root,root,-)
%{_libdir}/gstreamer-%{gst_branch}/libgsttinycompress.so
%if "%{tinycompresstest}" == "1"
%{_bindir}/tinycompress_test
%endif

%files codec
%manifest gst-plugins-tizen1.0.manifest
%license COPYING
%defattr(-,root,root,-)
%{_libdir}/gstreamer-%{gst_branch}/libgsttizenvideodec.so
%{_libdir}/gstreamer-%{gst_branch}/libgsttizenh264enc.so

%files hdcp
%manifest gst-plugins-tizen1.0.manifest
%license COPYING
%defattr(-,root,root,-)
%{_libdir}/gstreamer-%{gst_branch}/libgsttizenhdcp.so


%files audio
%manifest gst-plugins-tizen1.0.manifest
%license COPYING
%defattr(-,root,root,-)
%{_libdir}/gstreamer-%{gst_branch}/libgsttizenaudiosink.so

%endif


%files video360
%manifest gst-plugins-tizen1.0.manifest
%license COPYING
%defattr(-,root,root,-)
%{_libdir}/gstreamer-%{gst_branch}/libgstvideo360.so


%files camera
%manifest gst-plugins-tizen1.0.manifest
%license COPYING
%defattr(-,root,root,-)
%{_libdir}/gstreamer-%{gst_branch}/libgsttizencamerasrc.so

