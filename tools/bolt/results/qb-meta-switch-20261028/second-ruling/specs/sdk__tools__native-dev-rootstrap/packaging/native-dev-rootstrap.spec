Name:		native-dev-rootstrap
Summary:	make and package rootstrap
Version:	10.0
Release:	1
License:	Samsung
Source:		%{name}-%{version}.tar.gz
Source1:	%{name}.manifest

BuildRequires: xmlstarlet
BuildRequires: zip
BuildRequires: unzip
BuildRequires: libstdc++
BuildRequires: libstdc++-devel
BuildRequires: libgcc
BuildConflicts: libscl-common
Requires: zip
Requires: unzip

BuildRequires: SDL2
BuildRequires: SDL2-devel
BuildRequires: app-core-common
BuildRequires: app-core-common-devel
BuildRequires: appcore-agent
BuildRequires: appcore-widget
BuildRequires: askuser-notification-devel
BuildRequires: aul
BuildRequires: aul-devel
BuildRequires: aul-rsc-mgr
BuildRequires: aul-rsc-mgr-devel
BuildRequires: auth-fw
BuildRequires: badge
BuildRequires: badge-devel
BuildRequires: bundle
BuildRequires: bundle-devel
BuildRequires: cairo-devel
BuildRequires: calendar-service-devel
BuildRequires: capi-appfw-alarm
BuildRequires: capi-appfw-alarm-devel
BuildRequires: capi-appfw-app-common
BuildRequires: capi-appfw-app-common-devel
BuildRequires: capi-appfw-app-control
BuildRequires: capi-appfw-app-control-devel
BuildRequires: capi-appfw-app-manager
BuildRequires: capi-appfw-app-manager-devel
BuildRequires: capi-appfw-application
BuildRequires: capi-appfw-application-devel
BuildRequires: capi-appfw-component-manager
BuildRequires: capi-appfw-component-manager-devel
BuildRequires: capi-appfw-event
BuildRequires: capi-appfw-event-devel
BuildRequires: capi-appfw-job-scheduler
BuildRequires: capi-appfw-job-scheduler-devel
BuildRequires: capi-appfw-package-manager
BuildRequires: capi-appfw-package-manager-devel
BuildRequires: capi-appfw-preference
BuildRequires: capi-appfw-preference-devel
BuildRequires: capi-appfw-service-application-devel
BuildRequires: capi-appfw-united-service
BuildRequires: capi-appfw-united-service-devel
BuildRequires: capi-appfw-widget-application-devel
BuildRequires: capi-base-common
BuildRequires: capi-base-common-devel
BuildRequires: capi-base-utils
BuildRequires: capi-base-utils-devel
BuildRequires: capi-content-media-content
BuildRequires: capi-content-media-content-devel
BuildRequires: capi-content-mime-type
BuildRequires: capi-content-mime-type-devel
BuildRequires: capi-context
BuildRequires: capi-context-devel
BuildRequires: capi-context-engine
BuildRequires: capi-context-engine-devel
BuildRequires: capi-location-manager
BuildRequires: capi-location-manager-devel
BuildRequires: capi-machine-learning-common
BuildRequires: capi-machine-learning-common-devel
BuildRequires: capi-machine-learning-inference
BuildRequires: capi-machine-learning-inference-devel
BuildRequires: capi-machine-learning-inference-single
BuildRequires: capi-machine-learning-inference-single-devel
BuildRequires: capi-machine-learning-service
BuildRequires: capi-machine-learning-service-devel
BuildRequires: capi-machine-learning-training
BuildRequires: capi-machine-learning-training-devel
BuildRequires: capi-media-audio-io
BuildRequires: capi-media-audio-io-devel
BuildRequires: capi-media-camera
BuildRequires: capi-media-camera-devel
BuildRequires: capi-media-codec
BuildRequires: capi-media-codec-devel
BuildRequires: capi-media-controller
BuildRequires: capi-media-controller-devel
BuildRequires: capi-media-editor
BuildRequires: capi-media-editor-devel
BuildRequires: capi-media-image-util
BuildRequires: capi-media-image-util-devel
BuildRequires: capi-media-metadata-extractor
BuildRequires: capi-media-metadata-extractor-devel
BuildRequires: capi-media-player
BuildRequires: capi-media-player-devel
BuildRequires: capi-media-radio
BuildRequires: capi-media-radio-devel
BuildRequires: capi-media-recorder
BuildRequires: capi-media-recorder-devel
BuildRequires: capi-media-screen-mirroring
BuildRequires: capi-media-screen-mirroring-devel
BuildRequires: capi-media-sound-manager
BuildRequires: capi-media-sound-manager-devel
BuildRequires: capi-media-sound-pool
BuildRequires: capi-media-sound-pool-devel
BuildRequires: capi-media-thumbnail-util
BuildRequires: capi-media-thumbnail-util-devel
BuildRequires: capi-media-tone-player
BuildRequires: capi-media-tone-player-devel
BuildRequires: capi-media-tool
BuildRequires: capi-media-tool-devel
BuildRequires: capi-media-vision
BuildRequires: capi-media-vision-3d
BuildRequires: capi-media-vision-3d-devel
BuildRequires: capi-media-vision-barcode
BuildRequires: capi-media-vision-barcode-devel
BuildRequires: capi-media-vision-common
BuildRequires: capi-media-vision-common-devel
BuildRequires: capi-media-vision-devel
BuildRequires: capi-media-vision-face
BuildRequires: capi-media-vision-face-devel
BuildRequires: capi-media-vision-image
BuildRequires: capi-media-vision-image-devel
BuildRequires: capi-media-vision-machine_learning
BuildRequires: capi-media-vision-machine_learning-devel
BuildRequires: capi-media-vision-roi_tracker
BuildRequires: capi-media-vision-roi_tracker-devel
BuildRequires: capi-media-vision-surveillance
BuildRequires: capi-media-vision-surveillance-devel
BuildRequires: capi-media-wav-player
BuildRequires: capi-media-wav-player-devel
BuildRequires: capi-media-webrtc
BuildRequires: capi-media-webrtc-devel
BuildRequires: capi-mediademuxer
BuildRequires: capi-mediademuxer-devel
BuildRequires: capi-mediamuxer
BuildRequires: capi-mediamuxer-devel
BuildRequires: capi-network-asp
BuildRequires: capi-network-asp-devel
BuildRequires: capi-network-bluetooth
BuildRequires: capi-network-bluetooth-devel
BuildRequires: capi-network-connection
BuildRequires: capi-network-connection-devel
BuildRequires: capi-network-http
BuildRequires: capi-network-http-devel
BuildRequires: capi-network-inm
BuildRequires: capi-network-inm-devel
BuildRequires: capi-network-mtp
BuildRequires: capi-network-mtp-devel
BuildRequires: capi-network-nfc
BuildRequires: capi-network-nfc-devel
BuildRequires: capi-network-nsd
BuildRequires: capi-network-nsd-devel
BuildRequires: capi-network-smartcard
BuildRequires: capi-network-smartcard-devel
BuildRequires: capi-network-softap
BuildRequires: capi-network-softap-devel
BuildRequires: capi-network-stc
BuildRequires: capi-network-stc-devel
BuildRequires: capi-network-tethering
BuildRequires: capi-network-tethering-devel
BuildRequires: capi-network-ua
BuildRequires: capi-network-ua-devel
BuildRequires: capi-network-wifi-aware
BuildRequires: capi-network-wifi-aware-devel
BuildRequires: capi-network-wifi-direct
BuildRequires: capi-network-wifi-direct-devel
BuildRequires: capi-network-wifi-manager
BuildRequires: capi-network-wifi-manager-devel
BuildRequires: capi-privacy-privilege-manager
BuildRequires: capi-system-device
BuildRequires: capi-system-device-devel
BuildRequires: capi-system-info
BuildRequires: capi-system-info-devel
BuildRequires: capi-system-media-key
BuildRequires: capi-system-media-key-devel
BuildRequires: capi-system-peripheral-io
BuildRequires: capi-system-peripheral-io-devel
BuildRequires: capi-system-resource-monitor
BuildRequires: capi-system-resource-monitor-devel
BuildRequires: capi-system-runtime-info
BuildRequires: capi-system-runtime-info-devel
BuildRequires: capi-system-sensor
BuildRequires: capi-system-sensor-devel
BuildRequires: capi-system-system-settings
BuildRequires: capi-system-system-settings-devel
BuildRequires: capi-system-usbhost
BuildRequires: capi-system-usbhost-devel
BuildRequires: capi-telephony
BuildRequires: capi-telephony-devel
BuildRequires: capi-ui-autofill
BuildRequires: capi-ui-autofill-common
BuildRequires: capi-ui-autofill-common-devel
BuildRequires: capi-ui-autofill-devel
BuildRequires: capi-ui-autofill-manager
BuildRequires: capi-ui-autofill-manager-devel
BuildRequires: capi-ui-autofill-service
BuildRequires: capi-ui-autofill-service-devel
BuildRequires: capi-ui-efl-util
BuildRequires: capi-ui-efl-util-devel
BuildRequires: capi-ui-inputmethod
BuildRequires: capi-ui-inputmethod-devel
BuildRequires: capi-ui-inputmethod-manager
BuildRequires: capi-ui-inputmethod-manager-devel
BuildRequires: capi-ui-sticker
BuildRequires: capi-ui-sticker-devel
BuildRequires: capi-vpnsvc
BuildRequires: capi-vpnsvc-devel
BuildRequires: capi-web-url-download
BuildRequires: capi-web-url-download-devel
BuildRequires: chromium-efl
BuildRequires: chromium-efl-devel
BuildRequires: cion
BuildRequires: cion-devel
BuildRequires: component-based
BuildRequires: component-based-application
BuildRequires: component-based-application-devel
BuildRequires: component-based-devel
BuildRequires: contacts-service-devel
BuildRequires: coregl
BuildRequires: coregl-devel
BuildRequires: dali2
BuildRequires: dali2-adaptor
BuildRequires: dali2-adaptor-devel
BuildRequires: dali2-devel
BuildRequires: dali2-ui-foundation
BuildRequires: dali2-ui-foundation-devel
BuildRequires: data-control
BuildRequires: data-control-devel
BuildRequires: dbus-devel
BuildRequires: dbus-libs
BuildRequires: device-certificate-manager
BuildRequires: device-certificate-manager-devel
BuildRequires: diagnostics
BuildRequires: diagnostics-devel
BuildRequires: ecore
BuildRequires: ecore-buffer
BuildRequires: ecore-buffer-devel
BuildRequires: ecore-con
BuildRequires: ecore-con-devel
BuildRequires: ecore-core
BuildRequires: ecore-core-devel
BuildRequires: ecore-devel
BuildRequires: ecore-evas
BuildRequires: ecore-evas-devel
BuildRequires: ecore-file
BuildRequires: ecore-file-devel
BuildRequires: ecore-imf
BuildRequires: ecore-imf-devel
BuildRequires: ecore-imf-evas
BuildRequires: ecore-imf-evas-devel
BuildRequires: ecore-input
BuildRequires: ecore-input-devel
BuildRequires: ecore-input-evas
BuildRequires: ecore-input-evas-devel
BuildRequires: ecore-ipc
BuildRequires: ecore-ipc-devel
BuildRequires: ecore-wl2
BuildRequires: ecore-wl2-devel
BuildRequires: ector
BuildRequires: ector-devel
BuildRequires: edje
BuildRequires: edje-devel
BuildRequires: eet
BuildRequires: eet-devel
BuildRequires: efl
BuildRequires: efl-devel
BuildRequires: efl-extension
BuildRequires: efl-extension-devel
BuildRequires: efreet
BuildRequires: efreet-devel
BuildRequires: eina
BuildRequires: eina-devel
BuildRequires: eio
BuildRequires: eio-devel
BuildRequires: elementary
BuildRequires: elementary-devel
BuildRequires: embryo
BuildRequires: embryo-devel
BuildRequires: emile
BuildRequires: emile-devel
BuildRequires: eo
BuildRequires: eo-devel
BuildRequires: ethumb
BuildRequires: ethumb-devel
BuildRequires: evas
BuildRequires: evas-devel
BuildRequires: fontconfig
BuildRequires: fontconfig-devel
BuildRequires: freetype2-devel
BuildRequires: glib2-devel
BuildRequires: glib2-devel-static
BuildRequires: glibc
BuildRequires: glibc-devel
BuildRequires: glibc-devel-static
BuildRequires: glibc-devel-utils
BuildRequires: glibc-extra
BuildRequires: glibc-locale
BuildRequires: glibc-profile
BuildRequires: harfbuzz-devel
BuildRequires: iotcon
BuildRequires: iotcon-devel
BuildRequires: json-glib-devel
BuildRequires: libaccount-service
BuildRequires: libaccount-service-devel
BuildRequires: libalarm
BuildRequires: libalarm-devel
BuildRequires: libasan
BuildRequires: libauth-fw-client
BuildRequires: libauth-fw-client-admin
BuildRequires: libauth-fw-client-devel
BuildRequires: libcairo
BuildRequires: libcairo-gobject
BuildRequires: libcairo-script-interpreter
BuildRequires: libcalendar-service
BuildRequires: libcall-manager
BuildRequires: libcall-manager-devel
BuildRequires: libcontacts-service
BuildRequires: libcore-sync-client
BuildRequires: libcore-sync-client-devel
BuildRequires: libcurl
BuildRequires: libcurl-devel
BuildRequires: libdlog
BuildRequires: libdlog-devel
BuildRequires: libexif
BuildRequires: libexif-devel
BuildRequires: libfeedback
BuildRequires: libfeedback-devel
BuildRequires: libfreetype
BuildRequires: libgio
BuildRequires: libglib
BuildRequires: libgmodule
BuildRequires: libgobject
BuildRequires: libgthread
BuildRequires: libharfbuzz
BuildRequires: libicu
BuildRequires: libicu-devel
BuildRequires: libjson-glib
BuildRequires: libkey-manager-client
BuildRequires: libkey-manager-client-devel
BuildRequires: libkey-manager-common
BuildRequires: libnsd-dns-sd
BuildRequires: libnsd-ssdp
BuildRequires: liboauth
BuildRequires: liboauth-devel
BuildRequires: libode
BuildRequires: libode-devel
BuildRequires: libopenssl3
BuildRequires: libopenssl3-devel
BuildRequires: libpush
BuildRequires: libpush-devel
BuildRequires: librua
BuildRequires: librua-devel
BuildRequires: libsessiond
BuildRequires: libsessiond-devel
BuildRequires: libshortcut
BuildRequires: libshortcut-devel
BuildRequires: libsqlite
BuildRequires: libstorage
BuildRequires: libstorage-devel
BuildRequires: libtapi
BuildRequires: libtapi-devel
BuildRequires: libtbm
BuildRequires: libtbm-devel
BuildRequires: libwebauthn-client
BuildRequires: libwebauthn-client-devel
BuildRequires: libwebauthn-common
BuildRequires: libwidget_service
BuildRequires: libwidget_service-devel
BuildRequires: libxcrypt
BuildRequires: libxcrypt-devel
BuildRequires: libxml2
BuildRequires: libxml2-devel
BuildRequires: linux-glibc-devel
BuildRequires: message-port
BuildRequires: message-port-devel
BuildRequires: minizip
BuildRequires: minizip-devel
BuildRequires: mmi
BuildRequires: mmi-cli
BuildRequires: mmi-devel
BuildRequires: mmi-plugins
BuildRequires: multi-assistant
BuildRequires: multi-assistant-devel
BuildRequires: notification
BuildRequires: notification-devel
BuildRequires: notification-ex
BuildRequires: notification-ex-devel
BuildRequires: oauth2
BuildRequires: oauth2-devel
BuildRequires: openal-soft
BuildRequires: openal-soft-devel
BuildRequires: openssl3
BuildRequires: phonenumber-utils
BuildRequires: phonenumber-utils-devel
BuildRequires: pkgmgr-client
BuildRequires: pkgmgr-client-devel
BuildRequires: pkgmgr-installer
BuildRequires: pkgmgr-installer-devel
BuildRequires: privilege-info
BuildRequires: privilege-info-devel
BuildRequires: rpc-port
BuildRequires: rpc-port-devel
BuildRequires: sqlite
BuildRequires: sqlite-devel
BuildRequires: stt
BuildRequires: stt-devel
BuildRequires: stt-engine-devel
BuildRequires: syspopup-caller
BuildRequires: syspopup-caller-devel
BuildRequires: tizen-core
BuildRequires: tizen-core-devel
BuildRequires: tizen-core-imf
BuildRequires: tizen-core-imf-devel
BuildRequires: tizen-core-wl
BuildRequires: tizen-core-wl-devel
BuildRequires: ttrace
BuildRequires: ttrace-devel
BuildRequires: tts
BuildRequires: tts-devel
BuildRequires: tts-engine-devel
BuildRequires: tzsh
BuildRequires: tzsh-devel
BuildRequires: ui-gadget-1
BuildRequires: ui-gadget-1-devel
BuildRequires: update-control
BuildRequires: update-control-devel
BuildRequires: vconf-compat
BuildRequires: vconf-compat-devel
BuildRequires: pkgconfig(vconf-internal-keys)
#BuildRequires: vconf-internal-keys-devel
BuildRequires: voice-control
BuildRequires: voice-control-devel
BuildRequires: voice-control-elm
BuildRequires: voice-control-elm-devel
BuildRequires: voice-control-engine-devel
BuildRequires: voice-control-manager-devel
BuildRequires: voice-control-setting-devel
BuildRequires: voice-control-widget-devel
BuildRequires: vulkan-headers
BuildRequires: vulkan-loader
BuildRequires: vulkan-loader-devel
BuildRequires: yaca
BuildRequires: yaca-devel
BuildRequires: zlib
BuildRequires: zlib-devel

%define debug_package %{nil}
%define __strip /bin/true

%description
%{summary}

%prep
%setup -q
cp %{SOURCE1} .

%build

install -d output

#64bit
%ifarch aarch64 x86_64 riscv64
./script/convert64.sh
%endif

# Generate Private Rootstrap
%ifarch %arm
./make_rootstrap.sh -C rs-config ./rs_resource ./rs_resource_invisible ./rs_resource_rpm -t --internal --local --clean
%endif

%ifarch aarch64
./make_rootstrap_64.sh -C rs-config ./rs_resource ./rs_resource_invisible ./rs_resource_rpm -t --internal --local --clean
%endif

%ifarch x86_64
./make_rootstrap_64.sh -C rs-config ./rs_resource ./rs_resource_invisible ./rs_resource_rpm -e --internal --local --clean
%endif

%ifarch riscv64
./make_rootstrap_64.sh -C rs-config ./rs_resource ./rs_resource_invisible ./rs_resource_rpm -r --internal --local --clean
%endif


if [ $? -ne 0 ]; then
    echo "Failed to Generate Private Rootstrap"
    exit 127
fi

# Package Private Rootstrap
%ifarch aarch64 x86_64 riscv64
./package_rootstrap_64.sh -C rs-config --internal --64bit
%else
./package_rootstrap.sh -C rs-config --internal
%endif
if [ $? -ne 0 ]; then
    echo "Failed to Package Private Rootstrap"
    exit 127
fi

# Move Packaged Rootstrap
mv .pkg/*.zip output/

# Generate Public Rootstrap
%ifarch %arm
./make_rootstrap.sh -C rs-config ./rs_resource ./rs_resource_rpm -t --local --clean
%endif

%ifarch aarch64
./make_rootstrap_64.sh -C rs-config ./rs_resource ./rs_resource_rpm -t --local --clean
%endif

%ifarch x86_64
./make_rootstrap_64.sh -C rs-config ./rs_resource ./rs_resource_rpm -e --local --clean
%endif

%ifarch riscv64
./make_rootstrap_64.sh -C rs-config ./rs_resource ./rs_resource_rpm -r --local --clean
%endif


if [ $? -ne 0 ]; then
    echo "Failed to Generate Public Rootstrap"
    exit 127
fi

# Package Public Rootstrap
%ifarch aarch64 x86_64 riscv64
./package_rootstrap_64.sh -C rs-config --public --64bit
%else
./package_rootstrap.sh -C rs-config --public
%endif

if [ $? -ne 0 ]; then
    echo "Failed to Package Public Rootstrap"
    exit 127
fi

# Move Packaged Rootstrap
mv .pkg/*.zip output/

%install
install -d %{buildroot}/opt/
mv -f output/*.zip %{buildroot}/opt/

%post
unzip /opt/'*.zip' -d /opt/usr
chmod 755 -R /opt/usr/data/platforms

%clean
rm -rf %{buildroot}

%files
/opt/*.zip
