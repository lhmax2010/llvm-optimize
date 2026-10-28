Name: chromium-efl
Summary: Chromium EFL
# Version: {TPK_VERSION}.{INTERNAL_API_REVISION}.{CHROMIUM_MAJOR_VERSION}
# The {INTERNAL_API_REVISION} is used for compatibility check with wrtjs.
Version: 1.1.130
# Set by ./tizen_src/scripts/update_chromium_version.sh
%define upstream_chromium_version 130.0.6723.116
Release: 1
# The 'Group' should be specified as one of the following valid group list.
# https://wiki.tizen.org/wiki/Packaging/Guidelines#Group_Tag
Group: Web Framework/Web Engine
# The 'License' should be specified as some of the following known license list.
# http://spdx.org/licenses/
License: LGPL-2.1 or BSD-2-Clause

Source0: %{name}-%{version}.tar.gz
Source1: content_shell.in
Source2: chromium-efl-engine.spec.in

# BUILD_TCORE_ENABLE: 0 (default) = ECORE, 1 = TCORE, for Tizen 11 only.
# Example: gbs build ... --define "BUILD_TCORE_ENABLE 1"
%define __use_ecore 1
%if "%{?BUILD_TCORE_ENABLE}" == "1"
%define __use_ecore 0
%endif
%if "%{?_use_ecore}" != ""
%define __use_ecore %{_use_ecore}
%endif

%ifarch aarch64 riscv64
%define __drm_mapi_aarch_64 1
%else
%define __drm_mapi_aarch_64 0
%endif

%if 0%{?asan}
BuildRequires: libasan
# Enable _nodebug by default for ASAN build
%if "%{?_nodebug}" == ""
%define _nodebug 1
%endif
%endif

%if 0%{?_nodebug} || "%{?_strip_option}" != ""
# Skip building the debug package for _nodebug option
%global __debug_install_post %{nil}
%global debug_package %{nil}
%endif

%if 0%{?_enable_unittests}
%define _debug_mode 1
%endif

# Do not use the hardcoded CPU numbers such as "jobs 20" or "_smp_mflags -j20"
# . The below statement is compatible with RPM 4.4.2.1+.
# . /usr/bin/getconf depends on the libc-common (or libc-bin) base package.
%if "%{?_costomized_smp_mflags}" != ""
%define _smp_mflags %{_costomized_smp_mflags}
%else
%define _smp_mflags -j%(echo $((`/usr/bin/getconf _NPROCESSORS_ONLN` / 2)))
%endif

%define _cpu_core_num %(echo $((`/usr/bin/getconf _NPROCESSORS_ONLN`)))
%if %{?_cpu_core_num} > 256
%define _use_core_num 256
%else
%define _use_core_num %(echo $((`/usr/bin/getconf _NPROCESSORS_ONLN`)))
%endif
%define tizen_version %{tizen_version_major}%{tizen_version_minor}

%define __build_wv 1
%if "%{?_build_wv}" != ""
%define __build_wv %{_build_wv}
%endif
%define __build_wv_shell_dali 0
%if 0%{__build_wv} && 0%{?_build_wv_shell_dali}
%define __build_wv_shell_dali 1
%endif

%if "%{?tizen_profile_name}" == "tv" || "%{?_with_da_profile}" == "1"
%define __is_tizen_product 1
%else
%define __is_tizen_product 0
%endif

# Enable gtests by default for TV profile
%if "%{?tizen_profile_name}" == "tv"
%define gtests 1
%endif

# Enable chrome by default except for x86_64,TV,DA.
%if "%{_arch}" != "x86_64" && "%{tizen_profile_name}" != "tv" && "%{_with_da_profile}" != "1" && "%{gcov}" != "1" && "%{asan}" != "1"
%define __build_chrome 1
%else
%define __build_chrome 0
%endif

%if "%{?_build_chrome}" != ""
%define __build_chrome %{_build_chrome}
%endif

%if 0%{?_create_next_browser_tpk:1}
 %define __create_next_browser_tpk 1
 %define __build_chrome 0
  %if 0%{?google_api_key:1}
    %define __google_api_key "%{?google_api_key}"
  %else
    %define __google_api_key ""
  %endif
Source4: org.tizen.next-browser.spec.in
%else
 %define __create_next_browser_tpk 0
%endif
%if 0%{?__build_chrome}
Source3: chromium-efl-browser.spec.in
%endif

%if 0%{?_tizen_release_build} || ("%{_local_build}" != "1" && 0%{__is_tizen_product} && "%{gcov}" != "1" && "%{asan}" != "1")
%define __tizen_release_build 1
%else
%define __tizen_release_build 0
%endif

%if 0%{__create_next_browser_tpk}
%define __browser_binary_name browser
%else
%define __browser_binary_name chrome_tizen
%endif

%if "%{?tizen_profile_name}" == "tv" && %{tizen_version} >= 70
# Tizen TV 7.0
%define __enable_capi_thread_booster 1
%else
%define __enable_capi_thread_booster 0
%endif

%if "%{?tizen_profile_name}" == "tv" && %{tizen_version} > 60
# Tizen TV 6.5
%define __enable_process_group 1
%else
%define __enable_process_group 0
%endif

%if "%{?tizen_profile_name}" == "tv" && %{tizen_version} > 60
# Tizen TV 6.5
%define __enable_network_camera 1
%else
%define __enable_network_camera 0
%endif

%define __disable_node_v8_component 0
%if 0%{?_disable_node_v8_component} || "%{?_arch}" == "aarch64" || "%{?_arch}" == "x86_64"
%define __disable_node_v8_component 1
%endif

%define __enable_platform_api_wrapper 0
%if 0%{?_enable_platform_api_wrapper}
%define __enable_platform_api_wrapper 1
%endif

%if "%{enable_gamepad_latency_test}" == "1"
%define __enable_gamepad_latency_test 1
%else
%define __enable_gamepad_latency_test 0
%endif

%if "%{_vd_cfg_product_type}" != "LFD" && "%{_vd_cfg_product_type}" != "IWB" && "%{?_with_emulator}" != "1" && "%{_vd_cfg_licensing}" == "n" && %{tizen_version} > 60
%define _tizen_atmos_decoder_enable 1
%endif

%if "%{?tizen_profile_name}" == "tv" && "%{_vd_cfg_product_type}" != "LFD" && "%{_vd_cfg_product_type}" != "IWB" && "%{?_with_emulator}" != "1" && "%{_vd_cfg_licensing}" == "n"
%define __tizen_auto_zoom_enable 1
%else
%define __tizen_auto_zoom_enable 0
%endif

%if "%{?tizen_profile_name}" == "tv" && "%{_vd_cfg_product_type}" != "AUDIO" &&  "%{_vd_cfg_product_type}" !="AV"
%define __tizen_tv_upstream_multimedia 1
%else
%define __tizen_tv_upstream_multimedia 0
%endif

%if "%{?tizen_profile_name}" == "tv" && %{tizen_version} >= 70
%define __tizen_tv_video_capture 1
BuildRequires: pkgconfig(video-capture)
%else
%define __tizen_tv_video_capture 0
%endif

%if "%{__tizen_tv_upstream_multimedia}" == "1" && "%{?_with_emulator}" != "1"
%if %{tizen_version} >= 90 && "%{?__tizen_tv_riscv64}" != "1"
%define __tizen_tv_upstream_multimedia_omx 0
%define __tizen_tv_upstream_multimedia_omx_ppi 1
%else
%if "%{_vd_cfg_licensing}" == "n"
%define __tizen_tv_upstream_multimedia_omx 1
%define __tizen_tv_upstream_multimedia_omx_ppi 0
%else
%define __tizen_tv_upstream_multimedia_omx 0
%define __tizen_tv_upstream_multimedia_omx_ppi 0
%endif
%endif
%else
%define __tizen_tv_upstream_multimedia_omx 0
%define __tizen_tv_upstream_multimedia_omx_ppi 0
%endif

# Multichannel PCM (MCH PCM) low-latency output.
%if "%{__tizen_tv_upstream_multimedia}" == "1" && %{tizen_version} >= 70 && "%{?_with_emulator}" != "1" && "%{_vd_cfg_licensing}" == "n"
%define __tizen_tv_use_mch_pcm 1
%if %{tizen_version} >= 90 && "%{?__tizen_tv_riscv64}" != "1"
%define __tizen_tv_mch_pcm_use_ppi 1
%define __tizen_tv_mch_pcm_use_tinycompress 0
%else
%define __tizen_tv_mch_pcm_use_ppi 0
%define __tizen_tv_mch_pcm_use_tinycompress 1
%endif
%else
%define __tizen_tv_use_mch_pcm 0
%define __tizen_tv_mch_pcm_use_ppi 0
%define __tizen_tv_mch_pcm_use_tinycompress 0
%endif

%if "%{__tizen_tv_upstream_multimedia}" == "1" && %{tizen_version} >= 100 && "%{?_with_emulator}" != "1"
%define __tizen_tv_use_hdr10_plus_gaming 1
%else
%define __tizen_tv_use_hdr10_plus_gaming 0
%endif

%define __use_system_icu 0
%if (%{tizen_version} >= 100 || "%{_use_system_icu}" == "1") && "%{?_with_emulator}" != "1"
%define __use_system_icu 1
%endif

%if "%{?tizen_profile_name}" == "tv" && %{tizen_version} >= 90 && "%{_vd_cfg_product_type}" != "LFD" && "%{_vd_cfg_product_type}" != "IWB" && "%{?_with_emulator}" != "1" && "%{_vd_cfg_licensing}" == "n"
%define __build_tizen_media_stream_processor 1
%define __build_tizen_mobile_microphone 1
%else
%define __build_tizen_media_stream_processor 0
%define __build_tizen_mobile_microphone 0
%endif

%if 0%{__create_next_browser_tpk}
%define __build_tizen_mobile_microphone 0
%endif
Requires: /usr/bin/systemctl
Requires(post): /sbin/ldconfig
Requires(post): xkeyboard-config
Requires(postun): /sbin/ldconfig
Requires: libatomic

%ifnarch riscv64
BuildRequires: binutils-gold
%endif
BuildRequires: at-spi2-atk-devel, bison, expat-devel, flex, gettext, gperf, libatk-bridge-2_0-0, libcap-devel, libcurl
%if 0%{?__use_ecore}
BuildRequires: edje-tools
%endif
BuildRequires: libjpeg-turbo-devel, ninja, perl, python3, python3-xml, which
%if 0%{?__enable_platform_api_wrapper}
BuildRequires: cmake
%endif
BuildRequires: pkgconfig(atk)
BuildRequires: pkgconfig(capi-appfw-application)
BuildRequires: pkgconfig(capi-appfw-app-manager)
BuildRequires: pkgconfig(capi-location-manager)
BuildRequires: pkgconfig(capi-media-audio-io)
BuildRequires: pkgconfig(capi-media-camera)
BuildRequires: pkgconfig(capi-media-player)
BuildRequires: pkgconfig(capi-media-tool)
BuildRequires: pkgconfig(capi-system-device)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(capi-system-sensor)
BuildRequires: pkgconfig(capi-system-system-settings)
BuildRequires: pkgconfig(capi-ui-autofill)
BuildRequires: pkgconfig(capi-ui-autofill-common)
BuildRequires: pkgconfig(capi-ui-autofill-service)
BuildRequires: pkgconfig(cynara-creds-self)
BuildRequires: pkgconfig(dlog)
%if 0%{?__use_ecore}
BuildRequires: pkgconfig(ecore)
BuildRequires: pkgconfig(ecore-evas)
BuildRequires: pkgconfig(ecore-imf)
BuildRequires: pkgconfig(ecore-imf-evas)
BuildRequires: pkgconfig(ecore-input)
BuildRequires: pkgconfig(efl-extension)
BuildRequires: pkgconfig(eldbus)
BuildRequires: pkgconfig(elementary)
BuildRequires: pkgconfig(evas)
%endif
BuildRequires: pkgconfig(feedback)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(gles20)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libexif)
BuildRequires: pkgconfig(libffi)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libtbm)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libusb-1.0)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(libxslt)
BuildRequires: pkgconfig(minizip)
BuildRequires: pkgconfig(mm-player)
BuildRequires: pkgconfig(notification)
BuildRequires: pkgconfig(nspr)
BuildRequires: pkgconfig(nss)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(scim)
BuildRequires: pkgconfig(security-manager)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(stt)
%if 0%{?__build_wv}
BuildRequires: pkgconfig(tizen-core)
%endif
%if 0%{?__build_wv_shell_dali}
BuildRequires: pkgconfig(dali2-adaptor)
BuildRequires: pkgconfig(dali2-core)
BuildRequires: pkgconfig(dali2-toolkit)
%endif
BuildRequires: pkgconfig(ttrace)
BuildRequires: pkgconfig(tts)
%if 0%{?__use_ecore}
BuildRequires: pkgconfig(ui-gadget-1)
%endif
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(jsoncpp)
%if 0%{?__create_next_browser_tpk}
#Added below pkg for Next Browser
BuildRequires: dapi-provider-devel
BuildRequires: pkgconfig(vd-elementary)
BuildRequires: pkgconfig(efl-assist)
BuildRequires: pkgconfig(uifw_misc)
BuildRequires: pkgconfig(was_db_api)
BuildRequires: pkgconfig(capi-window-tv)
BuildRequires: pkgconfig(VDCurl)
BuildRequires: pkgconfig(capi-media-image-util)
BuildRequires: pkgconfig(capi-ui-config-manager-tv)
BuildRequires: pkgconfig(smart-deadlock)
BuildRequires: pkgconfig(logger)
%endif

# Tizen system replacements for third_party libraries
BuildRequires: brotli, libbrotli-devel, libbrotlidec, libbrotlienc
BuildRequires: libfreetype
BuildRequires: pkgconfig(vpx)
BuildRequires: pkgconfig(libwebp)
BuildRequires: pkgconfig(opus)

%if "%{?profile}" == "tv"
BuildRequires: pkgconfig(libjpeg)
%endif

%if %{tizen_version} > 60
BuildRequires: pkgconfig(esplusplayer)
%endif

%if "%{?profile}" == "tv" && %{tizen_version} > 90
BuildRequires: pkgconfig(plusplayer)
BuildRequires: pkgconfig(drmmanager)
%endif

BuildRequires:  boost-devel
BuildRequires:  boost-filesystem
BuildRequires:  boost-system
BuildRequires:  boost-thread

# Applied python acceleration for generating gyp files.
%ifarch armv7l
BuildRequires: python-accel-armv7l-cross-arm
%endif
%ifarch armv7hl
BuildRequires: python-accel-armv7hl-cross-arm
%endif
%ifarch aarch64
BuildRequires: python-accel-aarch64-cross-aarch64
%endif
%ifarch riscv64
BuildRequires: python-accel-riscv64-cross-riscv64
%endif

%if "%{?_with_wayland}" == "1"
%if 0%{?__use_ecore}
%if %{tizen_version} >= 50
BuildRequires: pkgconfig(ecore-wl2)
%else
BuildRequires: pkgconfig(ecore-wayland)
%endif
%endif
%if %{tizen_version} >= 110
BuildRequires: pkgconfig(tizen-core-wl)
BuildRequires: pkgconfig(tizen-core-imf)
%endif
BuildRequires: pkgconfig(wayland-egl)
%else
BuildRequires: pkgconfig(ecore-x)
BuildRequires: pkgconfig(libdri2)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xt)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xtst)
%endif

%if "%{?tizen_profile_name}" == "tv"
BuildRequires: pkgconfig(launchpad)
BuildRequires: pkgconfig(autoinput)
BuildRequires: pkgconfig(aul-extension)
BuildRequires: pkgconfig(capi-media-sound-manager)
BuildRequires: pkgconfig(capi-stt-wrapper-tv)
BuildRequires: pkgconfig(capi-system-display-rotator)
BuildRequires: pkgconfig(capi-appfw-app-manager)
BuildRequires: pkgconfig(capi-network-bluetooth)
BuildRequires: pkgconfig(capi-network-bluetooth-tv)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(security-privilege-manager)
BuildRequires: pkgconfig(drmdecrypt)
BuildRequires: pkgconfig(efl-assist)
BuildRequires: pkgconfig(hdmicec-api)
BuildRequires: pkgconfig(lwipc)
BuildRequires: pkgconfig(privileged-service)
BuildRequires: pkgconfig(tv-resource-manager)
BuildRequires: pkgconfig(tv-resource-information)
BuildRequires: pkgconfig(vd-win-util)
BuildRequires: pkgconfig(audio-control)
BuildRequires: pkgconfig(video-dp-control)
%if "%{_tizen_atmos_decoder_enable}" == "1"
BuildRequires: pkgconfig(ais-control-settings)
%endif
%if %{tizen_version} >= 60
BuildRequires: pkgconfig(resource-center-api)
%endif
%endif

%if "%{__tizen_auto_zoom_enable}" == "1"
BuildRequires: pkgconfig(aifw-api)
BuildRequires: pkgconfig(aifw-core)
%endif

%if "%{__tizen_tv_upstream_multimedia}" == "1"
BuildRequires: libavoc-devel
BuildRequires: pkgconfig(capi-screensaver)
BuildRequires: pkgconfig(graphics-control)
BuildRequires: pkgconfig(tv-resource-information)
BuildRequires: pkgconfig(tv-resource-manager)
BuildRequires: pkgconfig(video-mm-control)
BuildRequires: pkgconfig(video-render-ctrl-c-glue)

%if %{tizen_version} >= 80
BuildRequires: pkgconfig(libvideoenhance)
%endif

%if "%{__tizen_tv_upstream_multimedia_omx}" == "1"
BuildRequires: pkgconfig(omxil-e4x12-v4l2)
%endif

%if "%{__tizen_tv_upstream_multimedia_omx_ppi}" == "1"
BuildRequires: pkgconfig(mm-omxil)
%endif

%if "%{__tizen_tv_mch_pcm_use_ppi}" == "1"
BuildRequires: pkgconfig(mm-audioout)
%endif

%if "%{__tizen_tv_mch_pcm_use_tinycompress}" == "1"
BuildRequires: pkgconfig(tinycompress)
%endif

%if "%{__tizen_tv_use_hdr10_plus_gaming}" == "1"
BuildRequires: pkgconfig(libhdr10plus-cloudgaming-api)
%endif

%if %{tizen_version} <= 70
BuildRequires: pkgconfig(libsec-video-set-display)
%endif%
%endif

%if "%{__enable_capi_thread_booster}" == "1"
BuildRequires: pkgconfig(capi-boost-tv)
%endif

%if %{tizen_version} >= 90
BuildRequires: libwebauthn-client, libwebauthn-client-devel, libwebauthn-common, webauthn, webauthn-ble
BuildRequires: pkgconfig(capi-media-vision)
BuildRequires: pkgconfig(capi-network-bluetooth)
%endif

# TODO(youngsoo): The binutils-gold crashes mini_browser on the Tizen v3.0 ARM 64 bit images.
#                 Once fixed, use binutils-gold for all targets on Tizen v3.0.
%ifnarch aarch64 %{arm} # [M48_2564] Temporary excluding arm architecture for fixing memory issue
                        #            FIXME: http://web.sec.samsung.net/bugzilla/show_bug.cgi?id=15383
#BuildRequires: binutils-gold
%endif

%ifarch armv7l
%define ARCHITECTURE armv7l
%endif
%ifarch armv7hl
%define ARCHITECTURE armv7hl
%endif
%ifarch aarch64
%define ARCHITECTURE aarch64
%endif
%ifarch i586 i686
%define ARCHITECTURE ix86
%endif
%ifarch x86_64
%define ARCHITECTURE x86_64
%endif
%ifarch riscv64
%define ARCHITECTURE riscv64
%endif

%{!?_clang: %define _clang 1}

%if "%{?gcov}" == "1"
%define __enable_gcov 1
%else
%define __enable_gcov 0
%endif

%if "%{?_clang}" == "1" && ("%{?_arch}" == "arm" || "%{?_arch}" == "aarch64" || "%{?_arch}" == "riscv64")  && "%{?gcov}" != "1" && "%{?asan}" != "1"
%define __use_clang 1
%else
%define __use_clang 0
%endif

%define __enable_wrt_js 1
%if 0%{?_disable_wrt_js}
%define __enable_wrt_js 0
%endif

# New Tizen HW Encoder API
%if "%{?tizen_profile_name}" == "tv" && %{tizen_version} >= 70
%define __enable_capi_encoder_tv_api 1
BuildRequires: pkgconfig(capi-encoder-tv)
%else
%define __enable_capi_encoder_tv_api 0
%endif

%if 0%{?__enable_gcov}
BuildRequires: lcov
%endif

%if 0%{?__enable_wrt_js}
BuildRequires: pkgconfig(appcore-agent)
BuildRequires: pkgconfig(appsvc)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(capi-appfw-package-manager)
BuildRequires: pkgconfig(capi-appfw-service-application)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-creds-pid)
BuildRequires: pkgconfig(launchpad)
BuildRequires: pkgconfig(libwebappenc)
BuildRequires: pkgconfig(message-port)
BuildRequires: pkgconfig(wgt-manifest-handlers)
%if "%{?profile}" == "tv"
BuildRequires: app-signer
BuildRequires: curl
BuildRequires: pkgmgr-extension-devel
BuildRequires: pkgconfig(capi-media-player)
BuildRequires: pkgconfig(capi-screensaver)
BuildRequires: pkgconfig(settings-api)
%endif
%endif

%define __xwalk_extension_path %{_libdir}/tizen-extensions-crosswalk
%define __xwalk_extension_service_path %{_libdir}/tizen-extensions-crosswalk-service
%define udev_rules_path %{_libdir}/udev/rules.d

# node module is required for nmt and category public features.
%if "%{?profile}" != "tv" && "%{?profile}" != "wearable" && "%{?_with_da_profile}" != "1"
%define _support_node_module 1
%endif

# Keep the loader in /usr/lib and the engine in CHROMIUM_LIB_DIR/lib for
# both backends. __use_ecore controls EWK APIs, not the loader layout.
%define __enable_ewk_interface 1

# Enable to support squashfs RPM and image by default
%define __enable_squashfs_image 1
%if "%{?profile}" == "tv" && "%{_vd_cfg_chip_vendor}" == "EMUL"
%define __package_signing 0
%else
%define __package_signing %{?__enable_squashfs_image}
%endif

# squashfs rpm isn't generated on local build by default.
%define __make_squashfs_rpm %{?_make_squashfs_rpm}%{!?_make_squashfs_rpm:%{?__enable_squashfs_image}}
%define __generate_tpk %{?__make_squashfs_rpm}

%if "%{?profile}" == "tv"
  %if 0%{?tpktype:1}
    %define __generate_tpk 1
    %define __make_squashfs_rpm 1
    %define __disable_node_v8_component 1
  %else
    %define __generate_tpk 0
    %define __make_squashfs_rpm 0
  %endif
%endif

%if 0%{?__enable_squashfs_image}
BuildRequires: squashfs
%endif

%if "%{?tizen_profile_name}" == "tv" && "%{_vd_cfg_product_type}" != "AUDIO" &&  "%{_vd_cfg_product_type}" != "AV"
BuildRequires: accessory-devel
%endif

%if 0%{?__generate_tpk} || 0%{?__package_signing}
BuildRequires: hash-signer, zip
%endif

%if "%{?__build_tizen_media_stream_processor}" == "1"
BuildRequires: pkgconfig(aifw-api)
BuildRequires: pkgconfig(aifw-core)
%endif

%if "%{__build_tizen_mobile_microphone}" == "1"
BuildRequires: pkgconfig(msfapi)
%endif

%if 0%{?__make_squashfs_rpm}
%package squashfs
Summary: Chromium EFL SquashFS Image
Requires: %{name} = %{version}-%{release}
%description squashfs
Browser Engine based on Chromium EFL (SquashFS Image)
%endif

%if 0%{?__generate_tpk}
%package tpk
Summary: Chromium EFL TPK
%description tpk
Browser Engine based on Chromium EFL (TPK)
%endif
%description
Browser Engine based on Chromium EFL (Shared Library)

%package devel
Summary: Chromium EFL
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
%description devel
Browser Engine dev library based on Chromium EFL (development files)

%if 0%{?_enable_unittests}
%package unittests
Summary: Chromium unittests
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
%description unittests
Chromium unite tests
%endif

%if 0%{?build_ewk_unittests}
%package ewktest
Summary: Chromium EWK unittests
Group: Development/UnitTests
Requires: %{name} = %{version}-%{release}
%description ewktest
Chromium EFL unit test utilities
%endif

%if 0%{?build_tizen_ppapi_extension_unittests}
%package tizen_ppapi_extension_unittests
Summary: Chromium tizen ppapi extension unittests
Group: Development/UnitTests
Requires: %{name} = %{version}-%{release}
%description tizen_ppapi_extension_unittests
Chromium tizen ppapi extension unit test utilities
%endif

%if 0%{?build_tizen_blink_unittests}
%package tizen_blink_unittests
Summary: Chromium Tizen Blink modules unittests
Group: Development/UnitTests
Requires: %{name} = %{version}-%{release}
%description tizen_blink_unittests
Chromium Tizen Blink modules unittests
%endif

%if 0%{?build_tizen_media_unittests}
%package tizen_media_unittests
Summary: Chromium Media Module unittests
Group: Development/UnitTests
Requires: %{name} = %{version}-%{release}
%description tizen_media_unittests
Chromium Media Module unittests
%endif

%if 0%{?build_rtc_unittests}
%package rtc_unittests
Summary: Chromium WebRTC unittests
Group: Development/UnitTests
Requires: %{name} = %{version}-%{release}
%description rtc_unittests
Chromium WebRTC unittests
%endif

%if 0%{?gtests}
%package ut-component-tomato
Summary: Chromium EFL Unit Tests for Tomato Framework
Group: Development/UnitTests
Requires: %{name} = %{version}-%{release}
%description ut-component-tomato
Chromium EFL unit test package for Tomato testing framework.
This package contains gtest-based automated test cases for Chromium EFL.
%endif

%if 0%{?__enable_gcov}
%package -n webkit2-gcov
Summary: Chromium gcov
Group: Development/UnitTests
Requires: %{name} = %{version}-%{release}
%description -n webkit2-gcov
Chromium gcov objects
%endif

%if 0%{?build_v8_unittests}
%package tizen_v8_unittests
Summary: Chromium Tizen V8 unittests
Group: Development/UnitTests
Requires: %{name} = %{version}-%{release}
%description tizen_v8_unittests
Chromium Tizen V8 unittests
%endif

# The macros '%TZ_' are valid from tizen v3.0
%define _pkgid org.tizen.%{name}
%define _xmldir %TZ_SYS_RO_PACKAGES

# Directory for chromium-efl tizen application package
%global CHROMIUM_APP_DIR %{TZ_SYS_RO_APP}/%{_pkgid}
# Directory for chromium-efl shared library
%global CHROMIUM_LIB_DIR %{_datadir}/%{name}

# Chromium unit tests install directory
%global CHROMIUM_UNITTESTS_DIR /opt/usr/chromium-unittests/
# Directory containing localization files
%global CHROMIUM_LOCALE_DIR %{_datadir}/%{name}/locale

%if 0%{?build_tizen_media_unittests}
%global TIZEN_MEDIA_UT_DIR /usr-ut/tizen_media_unittests
%global MEDIA_UT_DATA_DIR /media/test/data/
%endif

# Chromium-EFL TPK install directory
%global CHROMIUM_TPK_DIR /tmp

%if 0%{?build_tizen_blink_unittests}
# Tizen VD exec signer (kUEP) doesn't sign binaries in /opt directory,
# so choose other one.
%global TIZEN_BLINK_UT_DIR  /usr-ut/tizen_blink_unittests
%endif

%if 0%{?build_v8_unittests}
# Tizen VD exec signer (kUEP) doesn't sign binaries in /opt directory,
# so choose other one.
%global TIZEN_V8_UT_DIR  /usr-ut/tizen_v8_unittests

# List of extra v8 tests to unpack on the device
%global TIZEN_V8_EXTRA_TESTS \
    v8/test/wasm-spec-tests/tests.tar.gz \
    v8/test/wasm-js/tests.tar.gz
%endif

%if 0%{?build_rtc_unittests}
%global TIZEN_RTC_UT_DIR /usr-ut/tizen_rtc_unittests
%endif

# The tv profile has a different tpk generation policy.
# 2 types(update, upgrade) of tpk can be generated and used simultaneously.
# If tpktype is not defined and tizen version is less than 6.0, upgrade type is generated by default.
%if "%{?profile}" == "tv"
  %global CHROMIUM_LIB_UPGRADE_DIR  %{_datadir}/%{name}/upgrade
  %define _pkgid_upgrade %{_pkgid}-upgrade
  %if "%{?tpktype}" == "upgrade" || (0%{!?tpktype:1} && %{tizen_version} < 60)
    %define _tpkid %{_pkgid_upgrade}
  %endif
%endif
%if 0%{!?_tpkid:1}
%define _tpkid %{_pkgid}
%endif

# Include sub spec.in
%define include_sub_spec() %{expand:%(cat '%{1}')}
%if 0%{?__build_uwe_package}
%{include_sub_spec %{SOURCE2}}
%endif
%if 0%{?__build_chrome}
%{include_sub_spec %{SOURCE3}}
%endif

%if 0%{?__create_next_browser_tpk}
%define include_sub_spec() %{expand:%(cat '%{1}')}
%{include_sub_spec %{SOURCE4}}
%endif

%prep
%setup -q

%build
%if 0%{?asan}
%if "%{tizen_profile_name}" != "tv"
# from SR toolchain guide
export ASAN_OPTIONS=$(sed "s/start_deactivated=true/max_redzone=128/g" /ASAN_OPTIONS)
%endif
# from VD toolchain guide
export ASAN_OPTIONS="quarantine_size_mb=0:redzone=64:detect_stack_use_after_return=0:malloc_context_size=5:poison_heap=0:$ASAN_OPTIONS"
%endif

# The "_repository" flag was changed to "_vd_cfg_target_repository" in tizen 4.0 product tv.
%if "%{?tizen_profile_name}" == "tv"
#TO DO, onemain branch haven't defined _vd_cfg_target_repository, so add this hijack code
# to set repo_name to "MuseM" if not define _vd_cfg_target_repository, need to delete this
# code when defined _vd_cfg_target_repository in onemain.
%if "%{?_vd_cfg_target_repository}"
%define repo_name %{_vd_cfg_target_repository}
%else
%define repo_name MuseM
%endif
%else
%define repo_name %{_repository}
%endif

%if "%{?_tizen_release_build}" == "1"
%define _release_suffix .release
%endif

%if 0%{?__build_chrome} || %{__create_next_browser_tpk} == 1
%define OUTPUT_BASE_FOLDER out.chrome.tz_v%{tizen_version_major}.%{tizen_version_minor}.%{repo_name}.%{ARCHITECTURE}%{?_release_suffix}
%else
%define OUTPUT_BASE_FOLDER out.tz_v%{tizen_version_major}.%{tizen_version_minor}.%{repo_name}.%{ARCHITECTURE}%{?_release_suffix}
%endif

export GN_GENERATOR_OUTPUT=$PWD/%{OUTPUT_BASE_FOLDER}

export BUILD_ARCH=%{ARCHITECTURE}

#set build mode
%global OUTPUT_FOLDER %{OUTPUT_BASE_FOLDER}

# architecture related configuration + neon temporary workaround
%if %{?_skip_ninja:0}%{!?_skip_ninja:1}

%ifarch %{arm} aarch64
  export ADDITION_OPTION=" -finline-limit=64 -foptimize-sibling-calls -fno-unwind-tables -fno-exceptions -Os "

  export CFLAGS="$CFLAGS $ADDITION_OPTION"
  export CXXFLAGS="$CXXFLAGS $ADDITION_OPTION"
  export FFLAGS="$FFLAGS $ADDITION_OPTION"

  export CFLAGS="$(echo $CFLAGS | sed 's/-mfpu=[a-zA-Z0-9-]*/-mfpu=neon/g')"
  export CXXFLAGS="$(echo $CXXFLAGS | sed 's/-mfpu=[a-zA-Z0-9-]*/-mfpu=neon/g')"
  export FFLAGS="$(echo $FFLAGS | sed 's/-mfpu=[a-zA-Z0-9-]*/-mfpu=neon/g')"
%else
  export CFLAGS="$(echo $CFLAGS | sed 's/-Wl,--as-needed//g')"
  export CXXFLAGS="$(echo $CXXFLAGS | sed 's/-Wl,--as-needed//g')"
%endif

%if 0%{?_nodebug}
  CFLAGS="$(echo $CFLAGS | sed -E 's/-g[0-9] /-g0 /g')"
  CXXFLAGS="$(echo $CXXFLAGS | sed -E 's/-g[0-9] /-g0 /g')"
%endif

%if 0%{?__enable_platform_api_wrapper}
# Build platform api wrapper separately with gcc and cmake.
./tizen_src/platform_api_wrapper/build.sh %{?tizen_profile_name}
%endif

%if %{__use_clang} == 0
  ulimit -n 16384
%else
  ulimit -n 4096
%endif

%if 0%{?__enable_wrt_js}
  CFLAGS="$(echo $CFLAGS | sed -E 's/-O2/-Os/g')"
  CXXFLAGS="$(echo $CXXFLAGS | sed -E 's/-O2/-Os/g')"
  PATH="$PATH:$(cd third_party/node/tizen; pwd)"
  export PYTHONIOENCODING=utf-8
%endif

ccache_gn_arg=""
if type ccache &> /dev/null; then
  source tizen_src/build/ccache_env.sh tizen %{?_ccache_size}
  ccache_gn_arg="cc_wrapper=\"ccache\""
fi

%if 0%{!?_skip_gn:1}
%define macro_to_bool() %(if [ %{expand:%%{?%{1}}%%{!?%{1}:0}} -gt 0 ]; then echo true; else echo false; fi)
#gn generate

#run standard gn_chromiumefl wrapper
./tizen_src/build/gn_chromiumefl.sh \
  "is_tizen=true" \
  "lib_ro_root_dir=\"%{CHROMIUM_LIB_DIR}\"" \
  "app_ro_root_dir=\"%{TZ_SYS_RO_APP}/%{_pkgid}\"" \
  "app_rw_root_dir=\"%{TZ_SYS_RW_APP}/%{_pkgid}\"" \
%if "%{?profile}" == "tv"
  "lib_upgrade_root_dir=\"%{CHROMIUM_LIB_UPGRADE_DIR}\"" \
  "app_upgrade_root_dir=\"%{TZ_SYS_RW_APP}/%{_pkgid_upgrade}\"" \
%endif
  "package_id=\"%{_pkgid}\"" \
  "tizen_version=%{tizen_version}" \
  "tizen_version_major=%{tizen_version_major}" \
  "tizen_version_minor=%{tizen_version_minor}" \
  "tizen_version_patch=%{tizen_version_patch}" \
%ifarch armv7hl
  "arm_float_abi=\"hard\"" \
%endif
%if 0%{?_remove_webcore_debug_symbols:1}
  "remove_webcore_debug_symbols=true" \
%endif
%if %{tizen_version} >= 90
  "tizen_passkey_support=true" \
%endif
"exclude_unwind_tables=%{macro_to_bool __tizen_release_build}" \
"optimize_for_size=true" \
%if "%{?_enable_mlgo}" == "1"
  "enable_mlgo=true" \
%endif
%if "%{?_with_wayland}" == "1"
  "use_wayland=true" \
%endif
%if "%{?tizen_profile_name}" == "tv" && %{tizen_version} >= 60
  "tizen_vd_nga=true" \
%endif
%if "%{?_repository}" == "emulator" || "%{?_repository}" == "emulator32-x11" || "%{?_repository}" == "emulator32" || "%{?_repository}" == "emulator64"
  "tizen_emulator_support=true"  \
%endif
%if "%{?tizen_profile_name}" == "tv"
  "tizen_product_tv=true" \
%if 0%{?__create_next_browser_tpk}
  "is_samsung_next_browser=true" \
  "enable_lens_desktop=false" \
  "enable_background_mode=false" \
  "enable_background_contents=false" \
  "google_api_key=\"%{__google_api_key}\""\
  "version_next_browser=\"%{__next_browser_version}\""\
  "version_uwe=\"%{__uwe_version}\""\
  "app_samsung_next_browser_root_dir=\"%{TZ_SYS_RW_APP}/%{__browser_tpk_id}\"" \
%endif
%endif
%if "%{?_with_da_profile}" == "1"
  "tizen_product_da=true" \
%endif
%if 0%{?build_rtc_unittests}
  "tizen_rtc_unittests=true" \
%endif
%if "%{?tizen_profile_name}" == "tv" && "%{_vd_cfg_product_type}" != "AUDIO" &&  "%{_vd_cfg_product_type}" != "AV"
  "tizen_vd_accessory=true" \
  "tizen_vd_webhid=true" \
%endif
%if 0%{?tizen_media_logger_verbosity}
  "tizen_media_logger_verbosity=%{tizen_media_logger_verbosity}" \
%endif
%if 0%{?component_build}
 "component=\"shared_library\"" \
%endif
%if %{__use_clang} == 1
  "is_clang=true" \
%else
  "is_clang=false" \
%endif
%if "%{?__use_system_icu}" == "1"
  "use_system_icu=true" \
%else
  "use_system_icu=false" \
%endif
  "tizen_release_build=%{macro_to_bool __tizen_release_build}" \
%if 0%{?__build_chrome} || %{__create_next_browser_tpk} == 1
  "build_chrome=true" \
  "tizen_video_assistant=true" \
%else
  "build_chrome=false" \
%endif
  "build_wv=%{macro_to_bool __build_wv}" \
  "use_ecore=%{macro_to_bool __use_ecore}" \
  "wrt_loader_defer_init=false" \
%if "%{?tizen_profile_name}" == "tv"
  "lib_dir_path=\"%{_libdir}\"" \
%endif
%if "%{?_ttrace}" == "0"
  "use_ttrace=false" \
%else
  "use_ttrace_chrome_trace=%{macro_to_bool _ttrace}" \
%endif
%if "%{?asan}" == "1"
  "is_asan=true" \
%endif
%if 0%{?__enable_ewk_interface}
 "enable_ewk_interface=true" \
%endif
%if 0%{?__enable_capi_thread_booster}
 "tizen_thread_booster_service=true" \
%endif
  "ozone_auto_platforms=false" \
  "enable_wrt_js=%{macro_to_bool __enable_wrt_js}" \
  "enable_process_group=%{macro_to_bool __enable_process_group}" \
  "tizen_atmos_decoder_enable=%{macro_to_bool _tizen_atmos_decoder_enable}" \
  "xwalk_extension_path=\"%{__xwalk_extension_path}\"" \
  "xwalk_extension_service_path=\"%{__xwalk_extension_service_path}\"" \
%if %{__enable_network_camera}
  "enable_network_camera=true" \
%endif
%if 0%{?__enable_gcov}
  "enable_gcov=true" \
%endif
%if %{__enable_gamepad_latency_test}
  "enable_gamepad_latency_test=true" \
%endif
%if %{__tizen_tv_video_capture}
  "tizen_tv_video_capture=true" \
%endif
%if %{__enable_capi_encoder_tv_api}
  "enable_capi_encoder_tv_api=true" \
%endif
%if %{__drm_mapi_aarch_64} && "%{?tizen_profile_name}" == "tv" && %{tizen_version} >= 80
  "drm_mapi_aarch_64=true" \
%endif
%if %{__tizen_auto_zoom_enable}
 "tizen_auto_zoom_enable=true" \
%endif
%if %{__tizen_tv_upstream_multimedia}
  "tizen_tv_upstream_multimedia=true" \
%endif
%if %{__tizen_tv_upstream_multimedia_omx}
  "tizen_tv_upstream_multimedia_omx=true" \
%endif
%if %{__tizen_tv_upstream_multimedia_omx_ppi}
  "tizen_tv_upstream_multimedia_omx_ppi=true" \
%endif
%if "%{?_enable_memory_infra_heap_dumps}" == "1"
  "arm_use_thumb=false" \
  "enable_profiling=true" \
  "use_allocator_shim=true" \
%endif
%if "%{_vd_cfg_licensing}" == "y"
  "tizen_license_tv=true" \
%endif
%if %{__tizen_tv_use_mch_pcm}
  "tizen_tv_use_mch_pcm=true" \
%endif
%if %{__tizen_tv_mch_pcm_use_ppi}
  "tizen_tv_mch_pcm_use_ppi=true" \
%endif
%if %{__tizen_tv_mch_pcm_use_tinycompress}
  "tizen_tv_mch_pcm_use_tinycompress=true" \
%endif
%if %{__tizen_tv_use_hdr10_plus_gaming}
  "tizen_tv_use_hdr10_plus_gaming=true" \
%endif
%if "%{__build_tizen_mobile_microphone}" == "1"
  "tizen_mobile_microphone=true" \
%endif
%if "%{?__build_tizen_media_stream_processor}" == "1"
  "tizen_ai=true" \
%endif
%if 0%{?gtests}
  "enable_gtests=true" \
%endif
  "enable_platform_api_wrapper=%{macro_to_bool __enable_platform_api_wrapper}" \
  "disable_node_v8_component=%{macro_to_bool __disable_node_v8_component}" \
  $ccache_gn_arg
%endif  # _skip_gn

ninja %{?_ninja_debug:-v -d stats -d explain} %{_smp_mflags} -C "%{OUTPUT_FOLDER}" \
%if 0%{?build_ewk_unittests}
  ewk_unittests \
%endif
%if 0%{?build_tizen_ppapi_extension_unittests}
  efl_integration_unittests \
  ppapi_unittests \
%endif
%if 0%{?build_tizen_blink_unittests}
  tizen_blink_unittests \
%endif
%if 0%{?__enable_wrt_js}
  wrt wrt-service wrt-service-launcher \
%endif
%if ! 0%{?__disable_node_v8_component}
  node-runtime \
%endif
%if 0%{?build_tizen_media_unittests}
  tizen_media_unittests \
%endif
%if 0%{?__enable_ewk_interface}
  ewk-interface \
%endif
%if 0%{?__enable_squashfs_image} && "%{?tizen_profile_name}" == "tv"
  chromium-efl-install \
%endif
%if 0%{?build_v8_unittests}
  v8_tests \
%endif
%if 0%{?__build_chrome} || %{__create_next_browser_tpk} == 1
  %{__browser_binary_name} \
%endif
%if 0%{?build_rtc_unittests}
  webrtc_test_component \
%endif
%if 0%{?gtests}
  tizen_src/ewk/efl_integration:gtests_wrapper \
  ut:chromium_efl_gtests \
%endif
%if 0%{?__build_wv_shell_dali}
  wv_shell \
%endif
%if 0%{?__use_ecore}
  mini_browser \
%endif
  efl_webprocess chromium-ewk webview_samples

%if 0%{?_enable_unittests}
ninja %{_smp_mflags} -C"%{OUTPUT_FOLDER}" angle_unittests env_chromium_unittests cacheinvalidation_unittests \
  angle_unittests env_chromium_unittests cacheinvalidation_unittests \
  url_unittests sandbox_linux_unittests crypto_unittests sql_unittests accessibility_unittests \
  gfx_unittests printing_unittests events_unittests ppapi_unittests jingle_unittests \
  flip_in_mem_edsm_server_unittests breakpad_unittests dbus_unittests libphonenumber_unittests \
  base_unittests ffmpeg_unittests gin_unittests net_unittests snapshot_unittests \
  google_apis_unittests
# TODO: Fix compilation of the following tests content_unittests cc_unittests shell_dialogs_unittests
# gpu_unittests compos9itor_unittests media_unittests
%endif

%endif  # _skip_ninja


# XXX Workaround for using rpmlint with emulator build on Tizen_TV 3.0
#
# When using this repo http://download.tizen.org/snapshots/tizen/tv/latest/repos/emulator32-x11/packages/
# rpmlint-tizen-1.0-6.1 is installed in GBS-ROOT. So, after rpms are built
# gbs build script runs rpmlint to test created packages. There is some BUG in
# this script and directory /home/abuild/rpmbuild/OTHER/ isn't created. This
# directory is required for rpmlint's log file and its lack causes build error.
if [ ! -d %{buildroot}/../../OTHER/ -a -f /opt/testing/bin/rpmlint ]; then
   mkdir -p %{buildroot}/../../OTHER/
fi
# Running unittests
%if 0%{?run_unittests_in_gbs}

# Update library path to include libs from `/prd` directory
export LD_LIBRARY_PATH_ORIG=$LD_LIBRARY_PATH
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/prd/usr/lib:%{OUTPUT_FOLDER}"

%if 0%{?build_tizen_ppapi_extension_unittests}
%{OUTPUT_FOLDER}/efl_integration_unittests
%{OUTPUT_FOLDER}/ppapi_unittests
%endif

%if 0%{?build_tizen_blink_unittests}
%{OUTPUT_FOLDER}/tizen_blink_unittests --test-launcher-jobs=1
%endif

%if 0%{?build_tizen_media_unittests}
%{OUTPUT_FOLDER}/tizen_media_unittests --test-launcher-jobs=1 --test-data-dir-prefix=$PWD
%endif

# Restore original library path
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH_ORIG

%if 0%{?build_v8_unittests} && %{tizen_version} >= 80
v8/tools/run-tests.py --verbose --outdir=../%{OUTPUT_FOLDER} -j 1 --progress=verbose cctest/test-streaming-compilation-with-cache/*
%endif

%endif

%if 0%{?run_unittests_in_gbs}
%if 0%{?build_rtc_unittests}
./run_webrtc_unittests.sh %{OUTPUT_FOLDER}
%endif
%endif

echo %{version} > "%{OUTPUT_FOLDER}"/version

%define _base_version %{version}
# Prepare Tizen App Manifest
%if "%{?profile}" == "tv"
  %if 0%{?__create_next_browser_tpk}
    %define _next_browser_manifestname %{__browser_tpk_id}
    %define _base_version %{__uwe_version}
  %endif
  %if 0%{?__generate_tpk}
    %define _manifestname %{_pkgid}-vd-tpk
  %else
%define _manifestname %{_pkgid}-vd
  %endif
%else
%define _manifestname %{_pkgid}
%endif
sed -e 's#@TIZEN_VERSION@#%{tizen_version_major}.%{tizen_version_minor}#g' \
    -e 's#@CHROMIUM_VERSION@#%{version}#g' \
    -e 's#@PACKAGE_ID@#%{_pkgid}#g' \
    packaging/%{_manifestname}.xml.in \
    > "%{OUTPUT_FOLDER}"/tizen-manifest.xml
%if 0%{?__generate_tpk}
sed -e 's#@TIZEN_VERSION@#%{tizen_version_major}.%{tizen_version_minor}#g' \
    -e 's#@CHROMIUM_VERSION@#%{_base_version}#g' \
    -e 's#@PACKAGE_ID@#%{_tpkid}#g' \
    packaging/%{_manifestname}.xml.in \
    > "%{OUTPUT_FOLDER}"/tizen-manifest-tpk.xml
%endif

%if 0%{?__create_next_browser_tpk}
sed -e 's#@TIZEN_VERSION@#%{tizen_version_major}.%{tizen_version_minor}#g' \
    -e 's#@CHROMIUM_VERSION@#%{__next_browser_version}#g' \
    -e 's#@PACKAGE_ID@#%{__browser_tpk_id}#g' \
    -e 's#@UWE_VERSION@#%{__uwe_version}#g' \
    packaging/%{_next_browser_manifestname}.xml.in \
    > "%{OUTPUT_FOLDER}"/tizen-manifest-next-browser-tpk.xml
%endif

%if 0%{?__build_chrome}
sed -e 's#@TIZEN_VERSION@#%{tizen_version_major}.%{tizen_version_minor}#g' \
    -e 's#@CHROMIUM_VERSION@#%{version}#g' \
   packaging/%{_pkgid}-browser.xml.in \
    > "%{OUTPUT_FOLDER}"/tizen-manifest-browser.xml
%endif

%if 0%{?__generate_tpk} && "%{?profile}" == "tv"
# add build_id to tizen-manifest
python3 %{TZ_SYS_BIN}/set_build_info.py "%{OUTPUT_FOLDER}"/tizen-manifest-tpk.xml %{COSMOS_BUILD_ID}
%endif

# Generate pkg-confg file
mkdir -p "%{OUTPUT_FOLDER}"/pkgconfig/
    > "%{OUTPUT_FOLDER}"/pkgconfig/chromium-efl.pc
sed -e 's#@CHROMIUM_VERSION@#%{version}#' \
    -e 's#@LIBDIR@#%{_libdir}#' \
    -e 's#@INCLUDEDIR@#%{_includedir}#' \
    tizen_src/build/pkgconfig/chromium-efl.pc.in \
     > "%{OUTPUT_FOLDER}"/pkgconfig/chromium-efl.pc

%if 0%{?__enable_squashfs_image} && "%{?tizen_profile_name}" != "tv"
sed -e 's#@RO_APP_PATH@#%{TZ_SYS_RO_APP}/%{_pkgid}#g' \
    -e 's#@RW_APP_PATH@#%{TZ_SYS_RW_APP}/%{_pkgid}#g' \
    -e 's#@MOUNT_POINT@#%{CHROMIUM_LIB_DIR}#g' \
    tizen_src/downloadable/systemd/chromium-efl.service.in \
    > "%{OUTPUT_FOLDER}"/chromium-efl.service

sed -e 's#@RW_APP_PATH@#%{TZ_SYS_RW_APP}/%{_pkgid}#g' \
    -e 's#@MOUNT_POINT@#%{CHROMIUM_LIB_DIR}#g' \
    tizen_src/downloadable/systemd/chromium-efl-update.service.in \
    > "%{OUTPUT_FOLDER}"/chromium-efl-update.service
%endif

# Generate build report in output directory
python3 tizen_src/scripts/generate_build_report.py "%{OUTPUT_FOLDER}"

%install

%if "%{?tizen_profile_name}" == "tv"
mkdir -p %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts
install -p -m 500 packaging/chromium-efl.sh %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts/chromium-efl.sh

%if "%{_vd_cfg_product_type}" == "LFD"
# install udev rule for insmod
mkdir -p %{buildroot}%{udev_rules_path}
install -p -m 644 packaging/99-usbserial-pl2303.rules %{buildroot}%{udev_rules_path}/99-usbserial-pl2303.rules
%endif

%endif

# Make directory strucure for chromium-efl filesystem image
install -d "%{buildroot}"%{CHROMIUM_LIB_DIR}/bin/locales
install -d "%{buildroot}"%{CHROMIUM_LIB_DIR}/lib
install -d "%{buildroot}"%{CHROMIUM_LIB_DIR}/res/images
install -d "%{buildroot}"%{CHROMIUM_LIB_DIR}/res/locale
install -d "%{buildroot}"%{CHROMIUM_LIB_DIR}/res/themes
%if "%{?profile}" == "tv"
install -d "%{buildroot}"%{CHROMIUM_LIB_UPGRADE_DIR}
%endif

install -m 0644 "%{OUTPUT_FOLDER}"/version            "%{buildroot}"%{CHROMIUM_LIB_DIR}/
install -m 0644 "%{OUTPUT_FOLDER}"/snapshot_blob.bin  "%{buildroot}"%{CHROMIUM_LIB_DIR}/bin/
install -m 0644 "%{OUTPUT_FOLDER}"/ewk_efl_resources.pak  "%{buildroot}"%{CHROMIUM_LIB_DIR}/bin/

%if 0%{?__enable_gcov}
mkdir -p gcov-obj
find . -name '*.gcno' -exec cp '{}' gcov-obj ';'
%endif

install -d "%{buildroot}"%{_bindir}
install -d "%{buildroot}"%{_libdir}
install -d "%{buildroot}"%{CHROMIUM_APP_DIR}/bin

install -d "%{buildroot}"%{_includedir}/v8/cppgc
install -m 0644 v8/include/cppgc/common.h "%{buildroot}"%{_includedir}/v8/cppgc/

%if 0%{?_support_node_module}
install -d "%{buildroot}"%{_includedir}/node
install -m 0644 third_party/electron_node/src/*.h "%{buildroot}"%{_includedir}/node/
%endif

%if 0%{?__enable_gcov}
mkdir -p %{buildroot}%{_datadir}/gcov/obj
install -m 0644 gcov-obj/* %{buildroot}%{_datadir}/gcov/obj
%endif

  install -m 0644 "%{OUTPUT_FOLDER}"/locales/efl/*.pak  "%{buildroot}"%{CHROMIUM_LIB_DIR}/bin/locales/

  install -m 0755 "%{OUTPUT_FOLDER}"/efl_webprocess    "%{buildroot}"%{_bindir}/
  %if "%{?profile}" == "tv"
  ln -s efl_webprocess "%{buildroot}"%{_bindir}/efl_pluginprocess
  %endif
  %if 0%{?__enable_ewk_interface}
    install -m 0644 "%{OUTPUT_FOLDER}"/libchromium-ewk.so    "%{buildroot}"%{_libdir}/
  %else
    ln -s %{CHROMIUM_LIB_DIR}/lib/libchromium-ewk.so "%{buildroot}"%{_libdir}/libchromium-ewk.so
  %endif
  %if 0%{?__enable_squashfs_image}
    # mount service for chromium-efl.img
    install -d "%{buildroot}"%{_unitdir}/multi-user.target.wants
    install -d "%{buildroot}"%{_unitdir}/basic.target.wants

    %if "%{?tizen_profile_name}" == "tv"
      install -m 0755 "%{OUTPUT_FOLDER}"/chromium-efl-install "%{buildroot}"%{_bindir}/
      install -m 0644 tizen_src/downloadable/systemd/chromium-efl-vd.service "%{buildroot}"%{_unitdir}/chromium-efl-vd.service
      ln -s ../chromium-efl-vd.service "%{buildroot}"%{_unitdir}/basic.target.wants/
    %else
      install -m 0644 "%{OUTPUT_FOLDER}"/chromium-efl.service "%{buildroot}"%{_unitdir}
      ln -s ../chromium-efl.service "%{buildroot}"%{_unitdir}/multi-user.target.wants/

      install -m 0644 "%{OUTPUT_FOLDER}"/chromium-efl-update.service "%{buildroot}"%{_unitdir}
      ln -s ../chromium-efl-update.service "%{buildroot}"%{_unitdir}/multi-user.target.wants/
    %endif
  %endif

# org.tizen.chromium-efl Tizen App package
%if 0%{?__use_ecore}
install -m 0755 "%{OUTPUT_FOLDER}"/efl_webview_app   "%{buildroot}"%{CHROMIUM_APP_DIR}/bin/
install -m 0755 "%{OUTPUT_FOLDER}"/mini_browser      "%{buildroot}"%{CHROMIUM_APP_DIR}/bin/
install -m 0755 "%{OUTPUT_FOLDER}"/ubrowser          "%{buildroot}"%{CHROMIUM_APP_DIR}/bin/
%endif
%if 0%{?__build_wv} && %{tizen_version} >= 110 && "%{?_with_wayland}" == "1"
install -m 0755 "%{OUTPUT_FOLDER}"/wv_shell_tcore    "%{buildroot}"%{CHROMIUM_APP_DIR}/bin/
%endif
%if 0%{?__build_wv_shell_dali}
install -m 0755 "%{OUTPUT_FOLDER}"/wv_shell          "%{buildroot}"%{CHROMIUM_APP_DIR}/bin/
%endif

%if 0%{?__enable_ewk_interface}
  install -m 0644 "%{OUTPUT_FOLDER}"/libchromium-impl.so "%{buildroot}"%{CHROMIUM_LIB_DIR}/lib/
%else
  install -m 0644 "%{OUTPUT_FOLDER}"/libchromium-ewk.so  "%{buildroot}"%{CHROMIUM_LIB_DIR}/lib/
%endif
%if 0%{?__enable_platform_api_wrapper}
  install -m 0644 ./tizen_src/platform_api_wrapper/libchromium-efl-platform-api-wrapper.so "%{buildroot}"%{CHROMIUM_LIB_DIR}/lib/
%endif

%if ! 0%{?__disable_node_v8_component}
install -m 0644 "%{OUTPUT_FOLDER}"/libv8.so             "%{buildroot}"%{CHROMIUM_LIB_DIR}/lib/
%endif
%if 0%{?__use_ecore}
install -m 0644 "%{OUTPUT_FOLDER}"/resources/*.edj "%{buildroot}"%{CHROMIUM_LIB_DIR}/res/themes/
%endif

cp -r "%{OUTPUT_FOLDER}"/locale/* "%{buildroot}"%{CHROMIUM_LIB_DIR}/res/locale/
chmod -R a=r,u+w,a+X              "%{buildroot}"%{CHROMIUM_LIB_DIR}/res/locale/*

%if "%{?__use_system_icu}" != "1"
  install -m 0644 "%{OUTPUT_FOLDER}"/icudtl.dat           "%{buildroot}"%{CHROMIUM_LIB_DIR}/bin/
%endif

install -d "%{buildroot}"%{_xmldir}
install -m 0644 "%{OUTPUT_FOLDER}"/tizen-manifest.xml "%{buildroot}"%{_xmldir}/%{_pkgid}.xml

%if 0%{?__package_signing} && "%{?tizen_profile_name}" != "tv"
  %define tizen_sign 1
  %define tizen_sign_base %{CHROMIUM_APP_DIR}
  %define tizen_sign_level platform
  %define tizen_author_sign 1
  %define tizen_dist_sign 1
%endif

install -m 0644 "%{OUTPUT_FOLDER}"/images/*.png    "%{buildroot}"%{CHROMIUM_LIB_DIR}/res/images/
%if 0%{?__use_ecore}
install -m 0644 "%{OUTPUT_FOLDER}"/resources/*.edj "%{buildroot}"%{CHROMIUM_LIB_DIR}/res/themes/
%endif

%if "%{?__use_system_icu}" != "1"
  install -m 0644 "%{OUTPUT_FOLDER}"/icudtl.dat           "%{buildroot}"%{CHROMIUM_LIB_DIR}/bin/
%endif

install -d "%{buildroot}"%{_xmldir}
install -m 0644 "%{OUTPUT_FOLDER}"/tizen-manifest.xml "%{buildroot}"%{_xmldir}/%{_pkgid}.xml

%if 0%{?__package_signing} && "%{?tizen_profile_name}" != "tv"
  %define tizen_sign 1
  %define tizen_sign_base %{CHROMIUM_APP_DIR}
  %define tizen_sign_level platform
  %define tizen_author_sign 1
  %define tizen_dist_sign 1
%endif

%if 0%{?__package_signing} && "%{?tizen_profile_name}" == "tv"
  install -m 0644 tizen_src/downloadable/vd_sign/author-signature.xml "%{buildroot}"%{CHROMIUM_APP_DIR}
  install -m 0644 tizen_src/downloadable/vd_sign/signature1.xml "%{buildroot}"%{CHROMIUM_APP_DIR}
%endif

install -d "%{buildroot}"%{_libdir}/pkgconfig
install -m 0644 "%{OUTPUT_FOLDER}"/pkgconfig/chromium-efl.pc "%{buildroot}"%{_libdir}/pkgconfig/

install -d "%{buildroot}"%{_includedir}/chromium-ewk
%if 0%{?__use_ecore}
install -m 0644 tizen_src/ewk/efl_integration/public/*.h "%{buildroot}"%{_includedir}/chromium-ewk/
%endif
%if 0%{?__build_wv}
install -m 0644 tizen_src/wv/integration/public/*.h "%{buildroot}"%{_includedir}/chromium-ewk/
%endif

install -d "%{buildroot}"%{_includedir}/v8
install -m 0644 v8/include/*.h "%{buildroot}"%{_includedir}/v8/

# The native applications using ewk API from Tizen 2.x have a dependency about libewebkit2.so.
# The chromium-efl should support the backward compatibility of the native applications.
%if 0%{?__use_ecore}
ln -s %{_libdir}/libchromium-ewk.so %{buildroot}%{_libdir}/libewebkit2.so.0
ln -s %{_libdir}/libewebkit2.so.0   %{buildroot}%{_libdir}/libewebkit2.so
%endif

%if 0%{?build_tizen_blink_unittests}
mkdir -p %{buildroot}%{TIZEN_BLINK_UT_DIR}
install -m 0755 -p -D %{OUTPUT_FOLDER}/tizen_blink_unittests %{buildroot}%{TIZEN_BLINK_UT_DIR}
install -m 0644 -p -D %{OUTPUT_FOLDER}/content_shell.pak     %{buildroot}%{TIZEN_BLINK_UT_DIR}
install -m 0644 -p -D %{OUTPUT_FOLDER}/snapshot_blob.bin     %{buildroot}%{TIZEN_BLINK_UT_DIR}

%if ! 0%{?__disable_node_v8_component}
install -m 0644 "%{OUTPUT_FOLDER}"/libv8.so                  %{buildroot}%{TIZEN_BLINK_UT_DIR}
%endif

%if "%{?__use_system_icu}" != "1"
  install -m 0644 "%{OUTPUT_FOLDER}"/icudtl.dat              %{buildroot}%{TIZEN_BLINK_UT_DIR}
%endif
%endif
%if 0%{?__create_next_browser_tpk}
%{__next_browser_install_spec}
%endif
%if 0%{?__make_squashfs_rpm}
  install -d "%{buildroot}"%{CHROMIUM_APP_DIR}/res
  # Make squashfs image of chromium-efl after extracting debuginfo
  %if 0%{?__generate_tpk}
    %define _tpk_file_name %{_tpkid}-%{version}-v%{tizen_version_major}.%{tizen_version_minor}.%{repo_name}.%{ARCHITECTURE}
    %define __tpk_install_post \
      tizen_src/build/build_tpk.sh "%{buildroot}"%{CHROMIUM_APP_DIR} %{OUTPUT_FOLDER} %{_tpk_file_name} %{_tpkid} %{?profile} \
      install -d %{buildroot}%{CHROMIUM_TPK_DIR}/ \
      install -m 644 %{OUTPUT_FOLDER}/%{_tpk_file_name}.tpk %{buildroot}%{CHROMIUM_TPK_DIR}
  %else
    %define __tpk_install_post echo "No TPK generation"
  %endif
%if "%{?profile}" == "tv" && "%{__generate_tpk}" == "0"
  %define __squashfs_rpm_install_post \
    %{?__sandbox_chmod_cmd} \
    mksquashfs "%{buildroot}"%{CHROMIUM_LIB_DIR} "%{buildroot}"%{CHROMIUM_APP_DIR}/res/%{name}.img -all-root -processors %{_use_core_num} -action "uncompressed @ name(*.*)" \
    %{__tpk_install_post} \
    %{nil}
%else
  %define __squashfs_rpm_install_post \
    %{?__sandbox_chmod_cmd} \
    mksquashfs "%{buildroot}"%{CHROMIUM_LIB_DIR} "%{buildroot}"%{CHROMIUM_APP_DIR}/res/%{name}.img -all-root -processors %{_use_core_num} \
    %{__tpk_install_post} \
    %{nil}
%endif

 # Force stripping all symbols
  %if "%{?profile}" == "tv"
    # Clear %{_rpm_strip_option} macro to strip all symbols.
    echo "Clear _rpm_strip_option=%{?_rpm_strip_option} to strip all symbols."
    %define _rpm_strip_option %{nil}
    echo "_find_debuginfo_strip_opts=%{?_find_debuginfo_strip_opts}"
  %endif
%endif

%if 0%{?__create_next_browser_tpk}
  %if "%{?profile}" == "tv"
    # Clear %{_rpm_strip_option} macro to strip all symbols.
    echo "Clear _rpm_strip_option=%{?_rpm_strip_option} to strip all symbols."
    %define _rpm_strip_option %{nil}
    echo "_find_debuginfo_strip_opts=%{?_find_debuginfo_strip_opts}"
  %endif
%endif
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}} \
  %{__arch_install_post} \
  %{__os_install_post} \
  %{?__squashfs_rpm_install_post} \
  %{?__next_browser_rpm_install_post} \
  %{nil}

%if 0%{?_enable_unittests}
install -d "%{INSTALL_ROOT}%{CHROMIUM_UNITTESTS_DIR}"
for test in "%{OUTPUT_FOLDER}/*_unittests"; do
  install -m 0755 ${test} "%{INSTALL_ROOT}%{CHROMIUM_UNITTESTS_DIR}"
done
%endif

%if 0%{?build_ewk_unittests}
mkdir -p %{buildroot}/opt/usr/resources/
mkdir -p %{buildroot}/opt/usr/utc_exec/
cp -r tizen_src/ewk/unittest/resources/* %{buildroot}/opt/usr/resources/
install -m 0644 "%{OUTPUT_FOLDER}"/ewk_unittests %{buildroot}/opt/usr/utc_exec/
install -m 0755 tizen_src/ewk/utc_gtest_run.sh %{buildroot}/opt/usr/utc_exec/
%endif

%if 0%{?build_tizen_media_unittests}
mkdir -p %{buildroot}%{TIZEN_MEDIA_UT_DIR}
mkdir -p %{buildroot}%{TIZEN_MEDIA_UT_DIR}%{MEDIA_UT_DATA_DIR}
install -m 0755 -p -D %{OUTPUT_FOLDER}/tizen_media_unittests %{buildroot}%{TIZEN_MEDIA_UT_DIR}
%if "%{?__use_system_icu}" != "1"
install -m 0644 -p -D %{OUTPUT_FOLDER}/icudtl.dat %{buildroot}%{TIZEN_MEDIA_UT_DIR}
%endif
install -m 0664 -p -D $PWD%{MEDIA_UT_DATA_DIR}bear.h264 \
                      %{buildroot}%{TIZEN_MEDIA_UT_DIR}%{MEDIA_UT_DATA_DIR}
install -m 0664 -p -D $PWD%{MEDIA_UT_DATA_DIR}h264-320x180-frame-0 \
                      %{buildroot}%{TIZEN_MEDIA_UT_DIR}%{MEDIA_UT_DATA_DIR}
%endif

%if 0%{?build_rtc_unittests}
mkdir -p %{buildroot}%{TIZEN_RTC_UT_DIR}
install -m 0755 -p -D %{OUTPUT_FOLDER}/call_unittests %{buildroot}%{TIZEN_RTC_UT_DIR}
install -m 0755 -p -D %{OUTPUT_FOLDER}/modules_unittests %{buildroot}%{TIZEN_RTC_UT_DIR}
install -m 0755 -p -D %{OUTPUT_FOLDER}/peerconnection_unittests %{buildroot}%{TIZEN_RTC_UT_DIR}
install -m 0755 -p -D %{OUTPUT_FOLDER}/rtc_pc_unittests %{buildroot}%{TIZEN_RTC_UT_DIR}
install -m 0755 -p -D %{OUTPUT_FOLDER}/video_unittests %{buildroot}%{TIZEN_RTC_UT_DIR}
%if %{__use_clang} == 1
  # FIXME: This will copy 3 identical files under different names.
  #        Use symlink or add dependency to package provideing libatomic.
  install -m 0644 %{_libdir}/libatomic.so* %{buildroot}%{TIZEN_RTC_UT_DIR}
%endif
%endif

%if 0%{?gtests}
# Install gtests unit tests for Tomato framework
# Note: Binaries must be installed to /usr-ut/ directory for kUEP signing
# Tizen VD exec signer (kUEP) doesn't sign binaries in /opt directory
mkdir -p %{buildroot}/usr-ut/chromium-efl-ut-component-tomato/bin
mkdir -p %{buildroot}/opt/data/vdut
mkdir -p %{buildroot}/opt/data/tpk

# Copy executable with proper permissions
install -m 0755 -p -D %{OUTPUT_FOLDER}/chromium_efl_gtests %{buildroot}/usr-ut/chromium-efl-ut-component-tomato/bin/chromium-efl-ut-component-tomato

# Copy tizen-manifest.xml for TPK generation
install -m 0644 -p -D ut/tizen-manifest.xml %{buildroot}/usr-ut/chromium-efl-ut-component-tomato/tizen-manifest.xml

# Copy TC files for Tomato framework
mkdir -p %{buildroot}%{TZ_SYS_RW_APP}/tomato/testcase/chromium-efl-ut-component-tomato/tc
install -m 0644 -p -D ut/tc/TCList.dat %{buildroot}%{TZ_SYS_RW_APP}/tomato/testcase/chromium-efl-ut-component-tomato/tc/
install -m 0644 -p -D ut/tc/chromium-efl-ut-component-tomato-tomato.xml %{buildroot}%{TZ_SYS_RW_APP}/tomato/testcase/chromium-efl-ut-component-tomato/tc/
%endif

%if 0%{?build_tizen_ppapi_extension_unittests}
mkdir -p %{buildroot}/opt/usr/utc_exec/
install -m 0755 -p -D %{OUTPUT_FOLDER}/efl_integration_unittests %{buildroot}/opt/usr/utc_exec/
install -m 0755 -p -D %{OUTPUT_FOLDER}/ppapi_unittests %{buildroot}/opt/usr/utc_exec/
%endif

%if 0%{?build_v8_unittests}
mkdir -p %{buildroot}%{TIZEN_V8_UT_DIR}/bin
install -m 0644 -p -D "%{OUTPUT_FOLDER}"/snapshot_blob.bin               "%{buildroot}"%{TIZEN_V8_UT_DIR}/bin
install -m 0755 -p -D "%{OUTPUT_FOLDER}"/cctest                          "%{buildroot}"%{TIZEN_V8_UT_DIR}/bin
install -m 0755 -p -D "%{OUTPUT_FOLDER}"/d8                              "%{buildroot}"%{TIZEN_V8_UT_DIR}/bin
install -m 0755 -p -D "%{OUTPUT_FOLDER}"/generate-bytecode-expectations  "%{buildroot}"%{TIZEN_V8_UT_DIR}/bin
install -m 0755 -p -D "%{OUTPUT_FOLDER}"/inspector-test                  "%{buildroot}"%{TIZEN_V8_UT_DIR}/bin
install -m 0755 -p -D "%{OUTPUT_FOLDER}"/v8_unittests                    "%{buildroot}"%{TIZEN_V8_UT_DIR}/bin
install -m 0755 -p -D "%{OUTPUT_FOLDER}"/v8*fuzzer                       "%{buildroot}"%{TIZEN_V8_UT_DIR}/bin
install -m 0755 -p -D "%{OUTPUT_FOLDER}"/v8_build_config.json            "%{buildroot}"%{TIZEN_V8_UT_DIR}/bin
install -m 0755 -p -D "%{OUTPUT_FOLDER}"/wasm_api_tests                  "%{buildroot}"%{TIZEN_V8_UT_DIR}/bin

%if "%{?__use_system_icu}" != "1"
  install -m 0644 "%{OUTPUT_FOLDER}"/icudtl.dat  "%{buildroot}"%{TIZEN_V8_UT_DIR}/bin
%endif

# Use $(echo ...) to allow line breaks in TIZEN_V8_EXTRA_TESTS
for extra_test in $(echo "%{TIZEN_V8_EXTRA_TESTS}"); do
  echo "Verifying ${extra_test}..."
  sha1_exp=`cat ${extra_test}.sha1`
  sha1_got=`sha1sum ${extra_test} | awk '{print $1}'`
  if [[ "${sha1_exp}" != "${sha1_got}" ]]; then
    echo "Wrong SHA1 sum for ${extra_test} expected: ${sha1_exp} got: ${sha1_got}"
    exit 1
  fi
done

# Tar v8 test related directories to avoid hefty amount of file in rpm
# which will be processed very long.
tar -cj -f "%{buildroot}"%{TIZEN_V8_UT_DIR}/v8-test-data.tar.bz2 v8/tools/ v8/test/ v8/src/inspector
%endif

%if 0%{?__enable_wrt_js}
  %define __wrt_resourcedir %{CHROMIUM_LIB_DIR}/wrt
  %if "%{?tizen_profile_name}" != "tv"
    %define __wrt_localedir %{OUTPUT_FOLDER}/gen/wrt/resources/locales/
  %else
    %define __wrt_localedir %{OUTPUT_FOLDER}/gen/wrt/resources/tv_locales/
  %endif

  install -d %{buildroot}%{_bindir}
  install -d %{buildroot}%{_sysconfdir}/profile.d
  install -d %{buildroot}%{_unitdir_user}
  install -d %{buildroot}%{__wrt_resourcedir}
  install -d %{buildroot}%{__xwalk_extension_path}
  install -d %{buildroot}%{__xwalk_extension_service_path}
  install -d %{buildroot}%{_datadir}/locale
  install -d %{buildroot}%{_datadir}/edje/wrtjs
  %if "%{?profile}" == "wearable"
    install -d %{buildroot}%{_datadir}/icons/wrtjs
  %endif

  install -m 0755 %{OUTPUT_FOLDER}/wrt                            %{buildroot}%{_bindir}
  ln -s %{_bindir}/wrt                                            %{buildroot}%{_bindir}/wrt-client
  install -m 0755 wrt/wrt_env.sh                                  %{buildroot}%{_sysconfdir}/profile.d/
  install -m 0644 %{OUTPUT_FOLDER}/wrt_resources.pak              %{buildroot}%{CHROMIUM_LIB_DIR}/bin/
%if ! 0%{?__disable_node_v8_component}
  install -m 0644 %{OUTPUT_FOLDER}/libnode.so                 %{buildroot}%{CHROMIUM_LIB_DIR}/lib/
%endif
  install -m 0644 %{OUTPUT_FOLDER}/libsplash_screen_plugin.so     %{buildroot}%{__xwalk_extension_path}
  install -m 0644 %{OUTPUT_FOLDER}/libwidget_plugin.so            %{buildroot}%{__xwalk_extension_path}
  install -m 0644 %{OUTPUT_FOLDER}/libwrt-service-override.so     %{buildroot}%{__xwalk_extension_path}
  install -m 0644 %{OUTPUT_FOLDER}/gen/tizen_src/chromium_impl/components/xwalk_extensions/splash_screen_plugin/splash_screen.json \
                                                                  %{buildroot}%{__xwalk_extension_path}
  install -m 0644 %{OUTPUT_FOLDER}/gen/tizen_src/chromium_impl/components/xwalk_extensions/widget_plugin/widget.json \
                                                                  %{buildroot}%{__xwalk_extension_path}
%if "%{?profile}" == "tv"
  install -m 0644 %{OUTPUT_FOLDER}/libwrtservice_plugin.so        %{buildroot}%{__xwalk_extension_service_path}
%ifarch aarch64 riscv64 x86_64
  install -m 0644 %{OUTPUT_FOLDER}/gen/tizen_src/chromium_impl/components/xwalk_extensions/wrtservice_plugin/wrtservice_aarch64.json \
                                                                  %{buildroot}%{__xwalk_extension_service_path}/wrtservice.json
%else
  install -m 0644 %{OUTPUT_FOLDER}/gen/tizen_src/chromium_impl/components/xwalk_extensions/wrtservice_plugin/wrtservice.json \
                                                                  %{buildroot}%{__xwalk_extension_service_path}
%endif
%endif
%if 0%{?__use_ecore}
  install -m 0644 %{OUTPUT_FOLDER}/gen/wrt/resources/*.edj        %{buildroot}%{CHROMIUM_LIB_DIR}/res/themes/
%endif
  %if "%{?profile}" == "wearable"
    # Popup icons
    cp wrt/resources/icons/*.png                                  %{buildroot}%{_datadir}/icons/wrtjs/
  %endif
  %if "%{?profile}" != "tv"
    for file in $(find %{__wrt_localedir} -type f -name *.mo); do
      install -m 644 -D $file                                     %{buildroot}%{_datadir}/locale/${file#%{__wrt_localedir}}
    done

%if 0%{?__use_ecore}
    install -m 0644 %{OUTPUT_FOLDER}/gen/wrt/resources/*.edj      %{buildroot}%{_datadir}/edje/wrtjs
%endif
  %endif

  install -d %{buildroot}%{_datadir}/dbus-1/services
  install -m 0755 %{OUTPUT_FOLDER}/wrt-service                    %{buildroot}%{_bindir}
  install -m 0755 %{OUTPUT_FOLDER}/wrt-service-launcher           %{buildroot}%{_bindir}
  install -d %{buildroot}%{_sysconfdir}/wrt
  install -m 0644 wrt/resources/service_app.conf                 %{buildroot}%{_sysconfdir}/wrt/service_app.conf
%if ! 0%{?__disable_node_v8_component}
  install -m 0755 %{OUTPUT_FOLDER}/libnode-runtime.so             %{buildroot}%{__xwalk_extension_path}
  install -m 0755 wrt/src/service/node/node-runtime.js            %{buildroot}%{__xwalk_extension_path}
%endif
%if 0%{?__enable_platform_api_wrapper}
  install -m 0644 %{OUTPUT_FOLDER}/libwrt-c++wrapper.so           %{buildroot}%{CHROMIUM_LIB_DIR}/lib/
%endif

  %if "%{?profile}" == "tv"
    for file in $(find %{__wrt_localedir} -type f -name *.mo); do
      install -m 644 -D $file                                     %{buildroot}%{CHROMIUM_LIB_DIR}/res/locale/${file#%{__wrt_localedir}}
    done

%if 0%{?__use_ecore}
    install -m 0644 %{OUTPUT_FOLDER}/gen/wrt/resources/*.edj      %{buildroot}%{CHROMIUM_LIB_DIR}/res/themes/
%endif

    install -d %{buildroot}/etc/notstrip/
    install -m 644 packaging/wrt.notstrip                         %{buildroot}/etc/notstrip/wrt.notstrip
    %if 0%{?__generate_tpk}
      echo "start to get wrtjs package"
      install -d %{buildroot}%{__wrt_resourcedir}/app
      cd tizen_src/downloadable/wrtjs
      rpm2cpio wrtjs-1.1.1-1.armv7l.rpm | cpio -divm
      cp -rf usr/share/wrt/app/*                                  %{buildroot}%{__wrt_resourcedir}/app/
      cd -
    %endif
    mkdir -p %{buildroot}/etc/spolicy/
    %if 0%{?__generate_tpk}
      echo "start to get wrtjs package"
      install -d %{buildroot}%{__wrt_resourcedir}/app
      cd tizen_src/downloadable/wrtjs
      rpm2cpio wrtjs-1.1.1-1.armv7l.rpm | cpio -divm
      cp -rf usr/share/wrt/app/*                                  %{buildroot}%{__wrt_resourcedir}/app/
      cd -
    %endif
  %endif

  install -d %{buildroot}%{_includedir}/wrt
  install -m 0644 electron/electron.d.ts                          %{buildroot}%{_includedir}/wrt/
  install -m 0644 wrt/native_wrtjs.d.ts                           %{buildroot}%{_includedir}/wrt/
%endif

%if 0%{?__build_chrome}
  %{__browser_install_spec}
  # tizen_src/build/build_chromium_browser_tpk.sh %{_buildroot_next_browser} %{OUTPUT_FOLDER} %{_browser_tpk_file_name} %{__browser_tpk_id} %{?profile}
%endif

%if "%{?_strip_option}" != ""
  echo "Strip all symbols from all libraries in chromium-efl rpm package"
  find %{buildroot} -type f -name *.so | xargs strip --strip-%{_strip_option}
%endif

%pre
if (( $(rpm -qa | grep 'wrtjs-[[:digit:]]' | wc -l) > 1 )); then
  echo -e "\033[31m*****************************************************"
  echo -e "Please remove wrtjs rpm(s) except for one:\n"
  rpm -qa | grep 'wrtjs-[[:digit:]]'
  echo -e "*****************************************************\033[m"
  exit 1
fi

export CHROMIUM_REVISION=$(echo %{version} | awk -F. '{print $2}')
export WRTJS_REVISION=$(rpm -qa | grep wrtjs | awk -F. '{print $2}')
if [[ "${WRTJS_REVISION}" == "" ]]; then
  WRTJS_REVISION="not installed"
fi

echo -e "\033[32m*****************************************************"
echo -e "* chromium-efl revision : ${CHROMIUM_REVISION}"
echo -e "* wrtjs revision        : ${WRTJS_REVISION}"
echo -e "*"
if [[ "${WRTJS_REVISION}" == "not installed" ]] || \
    (( ${CHROMIUM_REVISION} == ${WRTJS_REVISION} )); then
  echo -e "* Succeeded to check rpm versions"
else
  if (( ${CHROMIUM_REVISION} < ${WRTJS_REVISION} )); then
    echo -e "\033[31m* You're trying to install too old chromium-efl."
    echo -e "* Please install chromium-efl as revision ${WRTJS_REVISION}"
    echo -e "* or"
  else
    echo -e "\033[31m* You have too old wrtjs."
  fi
  echo -e "* please re-install wrtjs as revision ${CHROMIUM_REVISION} first."
fi
echo -e "*****************************************************\033[m"

%post
%if 0%{?__enable_wrt_js}
# It's essential to drop thread privilege of service app
chsmack -e "System::Privileged" %{_bindir}/wrt-service
%if "%{?tizen_profile_name}" == "tv"
buxton2ctl -i -d create-int32 "memory" "memory/wrt-service/will-quit" 0 "http://tizen.org/privilege/internal/default/public" "http://tizen.org/privilege/internal/default/public"
%endif

%if "%{?_local_build}" == "1"
setcap cap_mac_admin=eip %{_bindir}/wrt-service
%endif
%endif

%if "%{__tizen_tv_upstream_multimedia}" == "1"
buxton2ctl -i -d create-string "memory" "memory/web/playinfo" "" "http://tizen.org/privilege/internal/default/public" "http://tizen.org/privilege/internal/default/public"
%endif

%if "%{?profile}" == "tv"
chsmack -e "User" /usr/bin/chromium-efl-install
chsmack -a "*" opt/usr/home/owner/.pki/nssdb/cert9.db
%endif

if [ -f %{CHROMIUM_APP_DIR}/res/%{name}.img ]; then
  echo "chromium-efl-squasfs image will be mounted on boot by chromium-efl-squasfs rpm."
  echo "If you want to use chromium-efl without squashfs, please uninstall chromium-efl-squashfs rpm."
fi

%if 0%{?gtests}
# Set SMACK label for gtests executable to allow direct execution
# Using "*" allows execution from any location
chsmack -a "*" /usr-ut/chromium-efl-ut-component-tomato/bin/chromium-efl-ut-component-tomato 2>/dev/null || true

# Set executable permissions (only if file exists to avoid errors when ut-component-tomato is in separate package)
if [ -f /usr-ut/chromium-efl-ut-component-tomato/bin/chromium-efl-ut-component-tomato ]; then
    chmod 755 /usr-ut/chromium-efl-ut-component-tomato/bin/chromium-efl-ut-component-tomato
fi

# Create test output directories
mkdir -p /opt/data/vdut
chmod 777 /opt/data/vdut

# Add library path to ldconfig for permanent library resolution
# This allows the binary to find libchromium-impl.so without setting LD_LIBRARY_PATH
echo "/usr/share/chromium-efl/lib" > /etc/ld.so.conf.d/chromium-efl-ut.conf
ldconfig
%endif

%preun
# Stop chromium-efl mount systemd unit if script called from target.
# "id -G" - helps to determine the current environment:
#   0     - called from image creation process
#   other - called form target
if [[ "$(id -G)" != "0" ]]; then
  if [ -f %{_unitdir}/chromium-efl.service ]; then
    echo "systemctl stop chromium-efl.service"
    systemctl stop chromium-efl.service
  fi
  if [ -f %{_unitdir}/basic.target.wants/chromium-efl-vd.service ]; then
    echo "systemctl stop chromium-efl-vd.service"
    systemctl stop chromium-efl-vd.service
  fi
fi

%postun
%if 0%{?__make_squashfs_rpm}
%preun squashfs
# Stop chromium-efl mount systemd unit if script called from target.
# "id -G" - helps to determine the current environment:
#   0     - called from image creation process
#   other - called form target
if [[ "$(id -G)" != "0" ]]; then
  if [ -f %{_unitdir}/chromium-efl.service ]; then
    echo "systemctl stop chromium-efl.service"
    systemctl stop chromium-efl.service
  fi
  if [ -f %{_unitdir}/basic.target.wants/chromium-efl-vd.service ]; then
    echo "systemctl stop chromium-efl-vd.service"
    systemctl stop chromium-efl-vd.service
  fi
fi

%pre squashfs

%post squashfs
rm -rf %{CHROMIUM_LIB_DIR}/*
echo "All regular files in /usr/share/chromium-efl have been removed."
echo "Note: It requries to reboot the device for mounting squashfs image!"
%endif

%if 0%{?__generate_tpk}
%preun tpk
pkgcmd -un %{_tpkid}

%post tpk
pkgcmd -i -t tpk -p %{CHROMIUM_TPK_DIR}/%{_tpk_file_name}.tpk
rm -rf %{CHROMIUM_TPK_DIR}/%{_tpk_file_name}.tpk
%endif

%if 0%{?build_v8_unittests}
%post tizen_v8_unittests
echo "Extracting v8 test data (please be patient this may take a while)..."
tar -C %{TIZEN_V8_UT_DIR} -jxf %{TIZEN_V8_UT_DIR}/v8-test-data.tar.bz2

echo "v8 test data extracted, extracting particular tests"
# Use $(echo ...) to allow line breaks in TIZEN_V8_EXTRA_TESTS
for extra_test in $(echo "%{TIZEN_V8_EXTRA_TESTS}"); do
  echo "Extracting ${extra_test}..."
  tar -C `dirname %{TIZEN_V8_UT_DIR}/${extra_test}` -zxf %{TIZEN_V8_UT_DIR}/${extra_test}
done

echo "Regenerating bytecode expectations"
pushd %{TIZEN_V8_UT_DIR}/v8/
%{TIZEN_V8_UT_DIR}/bin/generate-bytecode-expectations --rebaseline --verbose
popd

%preun tizen_v8_unittests
echo "Removing v8 test data"
rm -rf %{TIZEN_V8_UT_DIR}/v8
%endif

%files
%if "%{?tizen_profile_name}" == "tv"
%{_datadir}/upgrade/vd_scripts/additional_scripts/chromium-efl.sh

%if "%{_vd_cfg_product_type}" == "LFD"
%{udev_rules_path}/*.rules
%endif

%endif
%manifest packaging/chromium-efl.manifest
%if 0%{?__package_signing}
  %{CHROMIUM_APP_DIR}/author-signature.xml
  %{CHROMIUM_APP_DIR}/signature1.xml
%endif
%{_xmldir}/%{_pkgid}.xml
%defattr(-,root,root,-)

%{CHROMIUM_LIB_DIR}/version
%{CHROMIUM_LIB_DIR}/bin/snapshot_blob.bin
%{CHROMIUM_LIB_DIR}/bin/ewk_efl_resources.pak
%{CHROMIUM_LIB_DIR}/bin/locales/*.pak
%{CHROMIUM_LIB_DIR}/res/locale/*
  %{_libdir}/libchromium-ewk.so
%if 0%{?__use_ecore}
  %{_libdir}/libewebkit2.so*
%endif
%if 0%{?__enable_squashfs_image}
  %if "%{?tizen_profile_name}" == "tv"
    %{_bindir}/chromium-efl-install
    %{_unitdir}/chromium-efl-vd.service
    %{_unitdir}/basic.target.wants/chromium-efl-vd.service
    %dir %{CHROMIUM_LIB_UPGRADE_DIR}
  %else
    %{_unitdir}/chromium-efl.service
    %{_unitdir}/multi-user.target.wants/chromium-efl.service
    %{_unitdir}/chromium-efl-update.service
    %{_unitdir}/multi-user.target.wants/chromium-efl-update.service
  %endif
%endif
%if 0%{?__use_ecore}
%{CHROMIUM_APP_DIR}/bin/efl_webview_app
%{CHROMIUM_APP_DIR}/bin/mini_browser
%{CHROMIUM_APP_DIR}/bin/ubrowser
%endif
%if 0%{?__build_wv} && %{tizen_version} >= 110 && "%{?_with_wayland}" == "1"
%{CHROMIUM_APP_DIR}/bin/wv_shell_tcore
%endif
%if 0%{?__build_wv_shell_dali}
%{CHROMIUM_APP_DIR}/bin/wv_shell
%endif

%if "%{?tizen_profile_name}" == "tv"
  %caps(cap_mac_admin,cap_mac_override,cap_setgid=ei) %{_bindir}/efl_webprocess
  %{_bindir}/efl_pluginprocess
%else
  %{_bindir}/efl_webprocess
%endif

%if 0%{?__enable_ewk_interface}
  %{CHROMIUM_LIB_DIR}/lib/libchromium-impl.so
%else
  %{CHROMIUM_LIB_DIR}/lib/libchromium-ewk.so
%endif

%if 0%{?__enable_platform_api_wrapper}
  %{CHROMIUM_LIB_DIR}/lib/libchromium-efl-platform-api-wrapper.so
%endif

%if ! 0%{?__disable_node_v8_component}
%{CHROMIUM_LIB_DIR}/lib/libv8.so
%endif
%{CHROMIUM_LIB_DIR}/res/images/*.png
%if 0%{?__use_ecore}
%{CHROMIUM_LIB_DIR}/res/themes/*.edj
%endif

%if "%{?__use_system_icu}" != "1"
  %{CHROMIUM_LIB_DIR}/bin/icudtl.dat
%endif

%if 0%{?__enable_wrt_js}
  %if "%{?profile}" == "tv"
    %caps(cap_mac_admin,cap_mac_override,cap_setgid,cap_setpcap,cap_setuid,cap_sys_chroot,cap_sys_ptrace,cap_sys_admin,cap_dac_override,cap_sys_nice=eip) %{_bindir}/wrt
    /etc/notstrip/wrt.notstrip
    %if 0%{?__generate_tpk}
      %{__wrt_resourcedir}/app/*
    %endif
  %else
    %{_bindir}/wrt
%endif
  %{_bindir}/wrt-client
  %{_sysconfdir}/profile.d/wrt_env.sh
%if 0%{?__enable_platform_api_wrapper}
  %{CHROMIUM_LIB_DIR}/lib/libwrt-c++wrapper.so
%endif
  %{CHROMIUM_LIB_DIR}/bin/wrt_resources.pak
%if ! 0%{?__disable_node_v8_component}
  %{CHROMIUM_LIB_DIR}/lib/libnode.so
%endif
  %{__xwalk_extension_path}/libsplash_screen_plugin.so
  %{__xwalk_extension_path}/libwidget_plugin.so
  %{__xwalk_extension_path}/libwrt-service-override.so
  %{__xwalk_extension_path}/splash_screen.json
  %{__xwalk_extension_path}/widget.json
  %if "%{?profile}" == "tv"
    %{__xwalk_extension_service_path}/wrtservice.json
    %{__xwalk_extension_service_path}/libwrtservice_plugin.so
  %endif
  %if "%{?profile}" != "tv"
%if 0%{?__use_ecore}
    %{_datadir}/edje/wrtjs/*.edj
%endif
    %{_datadir}/locale/*
  %endif
  %if "%{?profile}" == "wearable"
    %{_datadir}/icons/wrtjs/*
  %endif

  %{_bindir}/wrt-service
  %{_bindir}/wrt-service-launcher
  %{_sysconfdir}/wrt/service_app.conf
%if ! 0%{?__disable_node_v8_component}
  %{__xwalk_extension_path}/libnode-runtime.so
  %{__xwalk_extension_path}/node-runtime.js
%endif
%endif

%if 0%{?__make_squashfs_rpm}
%files squashfs
%defattr(-,root,root,-)
%{CHROMIUM_APP_DIR}/res/%{name}.img
%endif

%if 0%{?__generate_tpk}
%files tpk
%defattr(-,root,root,-)
%{CHROMIUM_TPK_DIR}/*.tpk
%endif

%if 0%{?__enable_gcov}
%files -n webkit2-gcov
%{_datadir}/gcov/obj/*
%endif

%files devel
%defattr(-,root,root,-)
%{_includedir}/chromium-ewk/*.h
%{_libdir}/pkgconfig/*.pc
%{_includedir}/v8/*

%if 0%{?_support_node_module}
%{_includedir}/node/*
%endif

%if 0%{?__enable_wrt_js}
  %{_includedir}/wrt/*
%endif

%if 0%{?_enable_unittests}
%files unittests
%defattr(-,root,root,-)
%{CHROMIUM_UNITTESTS_DIR}/*
%endif

%if 0%{?build_ewk_unittests}
%files ewktest
%defattr(-,root,root,-)
%manifest ./packaging/chromium-ewktest.manifest
/opt/usr/utc_exec/*
/opt/usr/resources/*
%endif

%if 0%{?build_tizen_ppapi_extension_unittests}
%files tizen_ppapi_extension_unittests
%defattr(-,root,root,-)
%manifest ./packaging/chromium-tizen_ppapi_extension_unittests.manifest
/opt/usr/utc_exec/*
%endif

%if 0%{?build_tizen_blink_unittests}
%files tizen_blink_unittests
%manifest ./packaging/chromium-tizen_blink_unittests.manifest
%{TIZEN_BLINK_UT_DIR}/tizen_blink_unittests
%{TIZEN_BLINK_UT_DIR}/content_shell.pak
%{TIZEN_BLINK_UT_DIR}/snapshot_blob.bin

%if ! 0%{?__disable_node_v8_component}
%{TIZEN_BLINK_UT_DIR}/libv8.so
%endif

%if "%{?__use_system_icu}" != "1"
%{TIZEN_BLINK_UT_DIR}/icudtl.dat
%endif
%endif

%if 0%{?build_tizen_media_unittests}
%files tizen_media_unittests
%defattr(-,root,root,-)
%manifest ./packaging/chromium-tizen_media_unittests.manifest
%{TIZEN_MEDIA_UT_DIR}/tizen_media_unittests
%if "%{?__use_system_icu}" != "1"
%{TIZEN_MEDIA_UT_DIR}/icudtl.dat
%endif
%{TIZEN_MEDIA_UT_DIR}%{MEDIA_UT_DATA_DIR}
%endif

%if 0%{?build_v8_unittests}
%files tizen_v8_unittests
%manifest ./packaging/chromium-unittests.manifest
%{TIZEN_V8_UT_DIR}/bin
%{TIZEN_V8_UT_DIR}/v8-test-data.tar.bz2
%endif

%if 0%{?build_rtc_unittests}
%files rtc_unittests
%manifest ./packaging/chromium-tizen_rtc_unittests.manifest
%{TIZEN_RTC_UT_DIR}/call_unittests
%{TIZEN_RTC_UT_DIR}/modules_unittests
%{TIZEN_RTC_UT_DIR}/peerconnection_unittests
%{TIZEN_RTC_UT_DIR}/rtc_pc_unittests
%{TIZEN_RTC_UT_DIR}/video_unittests
%if %{__use_clang} == 1
%{TIZEN_RTC_UT_DIR}/libatomic.so*
%endif
%endif

%if 0%{?gtests}
%files ut-component-tomato
%defattr(-,root,root,-)
/usr-ut/chromium-efl-ut-component-tomato/
%{TZ_SYS_RW_APP}/tomato/testcase/chromium-efl-ut-component-tomato/tc/
%defattr(777,root,root,777)
%dir /opt/data/vdut/
%dir /opt/data/tpk/
%endif
