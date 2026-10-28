%bcond_with wayland

%define _manifestdir %{TZ_SYS_RW_PACKAGES}
%define _desktop_icondir %{TZ_SYS_SHARE}/icons/default/small

%define crosswalk_extensions tizen-extensions-crosswalk

%define crosswalk_extensions_path %{_libdir}/%{crosswalk_extensions}
%define tizen_ut_build                                       0
%define tizen_ut_build_and_run_in_gbs                        0
%{!?profile: %define profile common}

%ifarch aarch64
## for aarch64 there is a dlopen failure during dlopen of libcapi-media-image-util.so (one of its dependency):
## [  127s] Error >>/lib64/libgomp.so.1: cannot allocate memory in static TLS block
## to prevent this kind of error, we need to preload this library during runing desc_gentool program
%define ld_preload_library LD_PRELOAD=libcapi-media-image-util.so
%endif


Name:       webapi-plugins
Version:    2.92
Release:    0
License:    Apache-2.0 and BSD-3-Clause and MIT
Group:      Development/Libraries
Summary:    Tizen Web APIs implemented
Source0:    %{name}-%{version}.tar.gz

####################################################################
#       Common Profile : #TODO list devices                        #
####################################################################

%define tizen_common_privilege_engine                        CYNARA

%define tizen_common_feature_account_support                 1
%define tizen_common_feature_alarm_support                   1
%define tizen_common_feature_app_control_settings_support    1
%define tizen_common_feature_application_support             1
%define tizen_common_feature_archive_support                 1
%define tizen_common_feature_badge_support                   1
%define tizen_common_feature_bluetooth_support               1
%define tizen_common_feature_calendar_support                1
%define tizen_common_feature_contact_support                 1
%define tizen_common_feature_content_support                 1
%define tizen_common_feature_datacontrol_support             1
%define tizen_common_feature_datasync_support                0
%define tizen_common_feature_download_support                1
%define tizen_common_feature_exif_support                    1
%define tizen_common_feature_feedback_support                1
%define tizen_common_feature_filesystem_support              1

%ifarch aarch64
%define tizen_common_feature_fm_radio_support                0
%else
%define tizen_common_feature_fm_radio_support                1
%endif

%define tizen_common_feature_ham_support                     0
%define tizen_common_feature_inputdevice_support             1
%define tizen_common_feature_iotcon_support                  1
%define tizen_common_feature_key_manager_support             1
%define tizen_common_feature_location_batch                  0
%define tizen_common_feature_media_controller_support        1
%define tizen_common_feature_media_key_support               1
%define tizen_common_feature_message_port_support            1
%define tizen_common_feature_rpc_port_support                1
%define tizen_common_feature_metadata_support                1
%define tizen_common_feature_ml_support                      1
%define tizen_common_feature_ml_nntrainer_support            1
%define tizen_common_feature_nfc_support                     0
%define tizen_common_feature_nfc_emulation_support           0
%define tizen_common_feature_notification_support            1
%define tizen_common_feature_package_support                 1
%define tizen_common_feature_player_util_support             1
%define tizen_common_feature_power_support                   1
%define tizen_common_feature_ppm_support                     1
%define tizen_common_feature_preference_support              1
%define tizen_common_feature_push_support                    1

# secure element feature
%ifarch aarch64
%define tizen_common_feature_se_support                      0
%else
%define tizen_common_feature_se_support                      1
%endif

%define tizen_common_feature_sensor_support                  1
%define tizen_common_feature_sound_support                   1
%define tizen_common_feature_system_info_support             1
%define tizen_common_feature_system_setting_support          1

# telephony feature
%ifarch aarch64
%define tizen_common_feature_telephony_support               0
%define tizen_common_feature_callhistory_support             0
%define tizen_common_feature_nbs_support                     0
%else
%define tizen_common_feature_telephony_support               1
%define tizen_common_feature_callhistory_support             1
%define tizen_common_feature_nbs_support                     1
%endif

%define tizen_common_feature_time_support                    1
%define tizen_common_feature_tvinputdevice_support           0
%define tizen_common_feature_voicecontrol_support            1
%define tizen_common_feature_web_setting_support             1
%define tizen_common_feature_wi_fi_support                   1
%define tizen_common_feature_widget_service_support          1

## Common emulator


%define tizen_common_emulator_feature_bluetooth_support      0

# FM radio feature
%define tizen_common_emulator_feature_fm_radio_support       1

%define tizen_common_emulator_feature_ham_support            1
%define tizen_common_emulator_feature_media_key_support      0
%define tizen_common_emulator_feature_nfc_support            1
%define tizen_common_emulator_feature_nfc_emulation_support  0

# secure element feature
%define tizen_common_emulator_feature_se_support             0

# telephony feature
%define tizen_common_emulator_feature_telephony_support      1
%define tizen_common_emulator_feature_callhistory_support    1
%define tizen_common_emulator_feature_nbs_support            1

%define tizen_common_emulator_feature_wi_fi_support          0

####################################################################

# GBM Product Build Optimization. Not for 4.0 Public Unified Build.
%if "%{?profile}" == "common"
%define tizen_privilege_engine                        %{expand:%tizen_%{?profile}_privilege_engine}

%define tizen_feature_account_support                 %{expand:%tizen_%{?profile}_feature_account_support}
%define tizen_feature_alarm_support                   %{expand:%tizen_%{?profile}_feature_alarm_support}
%define tizen_feature_app_control_settings_support    %{expand:%tizen_%{?profile}_feature_app_control_settings_support}
%define tizen_feature_application_support             %{expand:%tizen_%{?profile}_feature_application_support}
%define tizen_feature_archive_support                 %{expand:%tizen_%{?profile}_feature_archive_support}
%define tizen_feature_badge_support                   %{expand:%tizen_%{?profile}_feature_badge_support}
%define tizen_feature_bluetooth_support               %{expand:%tizen_%{?profile}_feature_bluetooth_support}
%define tizen_feature_calendar_support                %{expand:%tizen_%{?profile}_feature_calendar_support}
%define tizen_feature_contact_support                 %{expand:%tizen_%{?profile}_feature_contact_support}
%define tizen_feature_content_support                 %{expand:%tizen_%{?profile}_feature_content_support}
%define tizen_feature_datacontrol_support             %{expand:%tizen_%{?profile}_feature_datacontrol_support}
%define tizen_feature_datasync_support                %{expand:%tizen_%{?profile}_feature_datasync_support}
%define tizen_feature_download_support                %{expand:%tizen_%{?profile}_feature_download_support}
%define tizen_feature_exif_support                    %{expand:%tizen_%{?profile}_feature_exif_support}
%define tizen_feature_feedback_support                %{expand:%tizen_%{?profile}_feature_feedback_support}
%define tizen_feature_filesystem_support              %{expand:%tizen_%{?profile}_feature_filesystem_support}
%define tizen_feature_fm_radio_support                %{expand:%tizen_%{?profile}_feature_fm_radio_support}
%define tizen_feature_ham_support                     %{expand:%tizen_%{?profile}_feature_ham_support}
%define tizen_feature_iotcon_support                  %{expand:%tizen_%{?profile}_feature_iotcon_support}
%define tizen_feature_location_batch                  %{expand:%tizen_%{?profile}_feature_location_batch}
%define tizen_feature_key_manager_support             %{expand:%tizen_%{?profile}_feature_key_manager_support}
%define tizen_feature_media_controller_support        %{expand:%tizen_%{?profile}_feature_media_controller_support}
%define tizen_feature_media_key_support               %{expand:%tizen_%{?profile}_feature_media_key_support}
%define tizen_feature_message_port_support            %{expand:%tizen_%{?profile}_feature_message_port_support}
%define tizen_feature_rpc_port_support                %{expand:%tizen_%{?profile}_feature_rpc_port_support}
%define tizen_feature_ml_support                      %{expand:%tizen_%{?profile}_feature_ml_support}
%define tizen_feature_ml_nntrainer_support            %{expand:%tizen_%{?profile}_feature_ml_nntrainer_support}
%define tizen_feature_nfc_emulation_support           %{expand:%tizen_%{?profile}_feature_nfc_emulation_support}
%define tizen_feature_nfc_support                     %{expand:%tizen_%{?profile}_feature_nfc_support}
%define tizen_feature_notification_support            %{expand:%tizen_%{?profile}_feature_notification_support}
%define tizen_feature_package_support                 %{expand:%tizen_%{?profile}_feature_package_support}
%define tizen_feature_player_util_support             %{expand:%tizen_%{?profile}_feature_player_util_support}
%define tizen_feature_power_support                   %{expand:%tizen_%{?profile}_feature_power_support}
%define tizen_feature_preference_support              %{expand:%tizen_%{?profile}_feature_preference_support}
%define tizen_feature_push_support                    %{expand:%tizen_%{?profile}_feature_push_support}
%define tizen_feature_se_support                      %{expand:%tizen_%{?profile}_feature_se_support}
%define tizen_feature_sensor_support                  %{expand:%tizen_%{?profile}_feature_sensor_support}
%define tizen_feature_sound_support                   %{expand:%tizen_%{?profile}_feature_sound_support}
%define tizen_feature_system_info_support             %{expand:%tizen_%{?profile}_feature_system_info_support}
%define tizen_feature_system_setting_support          %{expand:%tizen_%{?profile}_feature_system_setting_support}
%define tizen_feature_telephony_support               %{expand:%tizen_%{?profile}_feature_telephony_support}
%define tizen_feature_time_support                    %{expand:%tizen_%{?profile}_feature_time_support}
%define tizen_feature_web_setting_support             %{expand:%tizen_%{?profile}_feature_web_setting_support}
%define tizen_feature_widget_service_support          %{expand:%tizen_%{?profile}_feature_widget_service_support}
%define tizen_feature_wi_fi_support                   %{expand:%tizen_%{?profile}_feature_wi_fi_support}
%define tizen_feature_inputdevice_support             %{expand:%tizen_%{?profile}_feature_inputdevice_support}
%define tizen_feature_callhistory_support             %{expand:%tizen_%{?profile}_feature_callhistory_support}
%define tizen_feature_nbs_support                     %{expand:%tizen_%{?profile}_feature_nbs_support}
%define tizen_feature_tvinputdevice_support           %{expand:%tizen_%{?profile}_feature_tvinputdevice_support}
%define tizen_feature_voicecontrol_support            %{expand:%tizen_%{?profile}_feature_voicecontrol_support}
%define tizen_feature_ppm_support                     %{expand:%tizen_%{?profile}_feature_ppm_support}
%endif

BuildRequires: pkgconfig(security-privilege-manager)
BuildRequires: ninja
BuildRequires: pkgconfig(appcore-common)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(minizip)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(pkgmgr)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(pkgmgr-installer)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(storage)
BuildRequires: python
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(capi-system-runtime-info)
BuildRequires: pkgconfig(capi-network-connection)
BuildRequires: pkgconfig(capi-system-device)
BuildRequires: pkgconfig(capi-system-system-settings)
BuildRequires: pkgconfig(capi-network-bluetooth)
BuildRequires: pkgconfig(capi-network-wifi-manager)
BuildRequires: pkgconfig(tapi)
BuildRequires: pkgconfig(libpcrecpp)
BuildRequires: pkgconfig(capi-appfw-app-common)
BuildRequires: pkgconfig(capi-appfw-app-manager)
BuildRequires: pkgconfig(capi-appfw-package-manager)
BuildRequires: pkgconfig(capi-content-media-content)
BuildRequires: pkgconfig(capi-media-metadata-extractor)
# TODO check support on TV
BuildRequires: pkgconfig(capi-media-image-util)

BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(appsvc)

%if %{with wayland}
%define display_type wayland
BuildRequires: pkgconfig(wayland-client)
%else
%define display_type x11
#BuildRequires: pkgconfig(x11)
#BuildRequires: pkgconfig(xrandr)
%endif

%if "%{?tizen_privilege_engine}" == "ACE"
BuildRequires: pkgconfig(security-privilege-checker)
%endif

%if "%{?tizen_privilege_engine}" == "CYNARA"
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(libsmack)
%endif

%if "%{?tizen_feature_account_support}" == "1"
BuildRequires: pkgconfig(accounts-svc)
%endif

%if "%{?tizen_feature_alarm_support}" == "1"
BuildRequires: pkgconfig(capi-appfw-app-control)
BuildRequires: pkgconfig(capi-appfw-application)
BuildRequires: pkgconfig(capi-appfw-alarm)
BuildRequires: pkgconfig(alarm-service)
%endif

%if "%{?tizen_feature_application_support}" == "1"
BuildRequires: pkgconfig(capi-appfw-app-control)
BuildRequires: pkgconfig(capi-appfw-event)

%if "%{?profile}" == "common"
BuildRequires: pkgconfig(capi-context)
%endif

%endif

%if "%{?tizen_feature_bluetooth_support}" == "1"
BuildRequires: pkgconfig(capi-appfw-app-control)
%endif

%if "%{?tizen_feature_datacontrol_support}" == "1"
BuildRequires: pkgconfig(capi-data-control)
%endif

%if "%{?tizen_feature_download_support}" == "1"
BuildRequires: pkgconfig(capi-web-url-download)
%endif

%if "%{?tizen_feature_ham_support}" == "1" || ("%{?profile}" == "common" && "%{?tizen_common_emulator_feature_ham_support}" == "1")
BuildRequires: pkgconfig(motion)
BuildRequires: pkgconfig(capi-system-sensor)
BuildRequires: pkgconfig(capi-location-manager)
BuildRequires: pkgconfig(sensor)
%endif

%if "%{?tizen_feature_iotcon_support}" == "1"
BuildRequires: pkgconfig(iotcon)
%endif

%if "%{?tizen_feature_player_util_support}" == "1"
BuildRequires: pkgconfig(chromium-efl)
%endif

%if "%{?tizen_feature_power_support}" == "1"
BuildRequires: pkgconfig(capi-appfw-application)
%endif

%if "%{?tizen_feature_push_support}" == "1"
BuildRequires: pkgconfig(push)
BuildRequires: pkgconfig(capi-appfw-app-control)
%endif

%if "%{?tizen_feature_key_manager_support}" == "1"
BuildRequires: pkgconfig(key-manager)
%endif

%if "%{?tizen_feature_media_controller_support}" == "1"
BuildRequires: pkgconfig(capi-media-controller)
%endif

%if "%{?tizen_feature_ml_support}" == "1"
BuildRequires: pkgconfig(nnstreamer)
BuildRequires: pkgconfig(capi-ml-inference)
%endif

%if "%{?tizen_feature_ml_nntrainer_support}" == "1"
BuildRequires: pkgconfig(nntrainer)
BuildRequires: pkgconfig(capi-ml-training)
%endif


%if "%{?tizen_feature_badge_support}" == "1"
BuildRequires:  pkgconfig(badge)
%endif

%if "%{?tizen_feature_calendar_support}" == "1"
BuildRequires:  pkgconfig(calendar-service2)
%endif

%if "%{?tizen_feature_contact_support}" == "1"
BuildRequires:  pkgconfig(contacts-service2)
%endif

%if "%{?tizen_feature_callhistory_support}" == "1" || ("%{?profile}" == "common" && "%{?tizen_common_emulator_feature_callhistory_support}" == "1")
BuildRequires:  pkgconfig(contacts-service2)
%endif

%if "%{?tizen_feature_exif_support}" == "1"
BuildRequires:  pkgconfig(libexif)
%endif

%if "%{?tizen_feature_nfc_support}" == "1" || ("%{?profile}" == "common" && "%{?tizen_common_emulator_feature_nfc_support}" == "1")
BuildRequires:  pkgconfig(capi-network-nfc)
BuildRequires:  pkgconfig(capi-appfw-app-control)
%endif

%if "%{?tizen_feature_fm_radio_support}" == "1" || ("%{?profile}" == "common" && "%{?tizen_common_emulator_feature_fm_radio_support}" == "1")
BuildRequires: pkgconfig(capi-media-radio)
%endif

%if "%{?tizen_feature_feedback_support}" == "1"
BuildRequires: pkgconfig(feedback)
%endif

%if "%{?tizen_feature_se_support}" == "1"
BuildRequires:  pkgconfig(capi-network-smartcard)
%endif

%if "%{?tizen_feature_message_port_support}" == "1"
BuildRequires: pkgconfig(capi-message-port)
%endif

%if "%{?tizen_feature_rpc_port_support}" == "1"
BuildRequires: pkgconfig(rpc-port)
%endif

%if "%{?tizen_feature_notification_support}" == "1"
BuildRequires: pkgconfig(notification)
BuildRequires: pkgconfig(capi-appfw-app-control)
%endif

%if "%{?tizen_feature_preference_support}" == "1"
BuildRequires: pkgconfig(capi-appfw-preference)
%endif

%if "%{?tizen_feature_sound_support}" == "1"
BuildRequires:  pkgconfig(capi-media-sound-manager)
%endif

%if "%{?tizen_feature_sensor_support}" == "1"
BuildRequires: pkgconfig(capi-system-sensor)
%endif

%if "%{?tizen_feature_media_key_support}" == "1"
BuildRequires:  pkgconfig(capi-system-media-key)
%endif

%if "%{?tizen_feature_widget_service_support}" == "1"
BuildRequires: pkgconfig(widget_service)
%endif

%if "%{?tizen_feature_voicecontrol_support}" == "1"
BuildRequires: pkgconfig(voice-control)
%endif

%if "%{?tizen_feature_ppm_support}" == "1"
BuildRequires: pkgconfig(capi-privacy-privilege-manager)
%endif

Requires:      %{name}-compat = %{version}-%{release}
Recommends:    %{name}-profile_common = %{version}-%{release}

%description
Tizen Web APIs implemented.

%package profile_common
Summary:       webapi-plugin binaries for common profile
Provides:      %{name}-compat = %{version}-%{release}
%description profile_common
Tizen Web API implementation binaries for Tizen common profile.

%ifarch %{ix86} x86_64
%package common-extension-emulator
Summary:       webapi-plugin binaries for common emulator
Requires:      %{name}-profile_common = %{version}-%{release}
%description common-extension-emulator
Tizen Web API implementation binaries for Tizen common emulator.
%endif

%package devel
Summary:    webapi-plugins development headers
Group:      Development/Libraries
Requires:   %{name} = %{version}

%description devel
webapi-plugins development headers

%prep
%setup -q

%build

is_clang=0
%{?_toolchain:
%if %{toolchain_is clang}
is_clang=1
%endif
}

export GYP_GENERATORS='ninja'

%if "%{?profile}" == "common"
# COMMON
GYP_OPTIONS="--depth=. -Dtizen=1 -Dclang=$is_clang -Dextension_build_type=Debug -Dextension_host_os=common -Dprivilege_engine=%{tizen_common_privilege_engine}"
GYP_OPTIONS="$GYP_OPTIONS -Ddisplay_type=%{display_type}"
GYP_OPTIONS="$GYP_OPTIONS -Dcrosswalk_extensions_path=%{crosswalk_extensions_path}"

# ut flags
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_ut_build=%{tizen_ut_build}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_ut_build_and_run_in_gbs=%{tizen_ut_build_and_run_in_gbs}"

# feature flags
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_account_support=%{?tizen_common_feature_account_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_alarm_support=%{?tizen_common_feature_alarm_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_app_control_settings_support=%{?tizen_common_feature_app_control_settings_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_application_support=%{?tizen_common_feature_application_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_archive_support=%{?tizen_common_feature_archive_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_badge_support=%{?tizen_common_feature_badge_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_bluetooth_support=%{?tizen_common_feature_bluetooth_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_calendar_support=%{?tizen_common_feature_calendar_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_callhistory_support=%{?tizen_common_feature_callhistory_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_contact_support=%{?tizen_common_feature_contact_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_content_support=%{?tizen_common_feature_content_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_datacontrol_support=%{?tizen_common_feature_datacontrol_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_datasync_support=%{?tizen_common_feature_datasync_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_download_support=%{?tizen_common_feature_download_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_exif_support=%{?tizen_common_feature_exif_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_feedback_support=%{?tizen_common_feature_feedback_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_filesystem_support=%{?tizen_common_feature_filesystem_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_fm_radio_support=%{?tizen_common_feature_fm_radio_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_ham_support=%{?tizen_common_feature_ham_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_iotcon_support=%{?tizen_common_feature_iotcon_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_location_batch=%{?tizen_common_feature_location_batch}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_key_manager_support=%{?tizen_common_feature_key_manager_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_media_controller_support=%{?tizen_common_feature_media_controller_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_media_key_support=%{?tizen_common_feature_media_key_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_message_port_support=%{?tizen_common_feature_message_port_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_rpc_port_support=%{?tizen_common_feature_rpc_port_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_metadata_support=%{?tizen_common_feature_metadata_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_ml_support=%{?tizen_common_feature_ml_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_ml_nntrainer_support=%{?tizen_common_feature_ml_nntrainer_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_nbs_support=%{?tizen_common_feature_nbs_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_nfc_emulation_support=%{?tizen_common_feature_nfc_emulation_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_nfc_support=%{?tizen_common_feature_nfc_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_notification_support=%{?tizen_common_feature_notification_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_package_support=%{?tizen_common_feature_package_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_player_util_support=%{?tizen_common_feature_player_util_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_power_support=%{?tizen_common_feature_power_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_ppm_support=%{?tizen_common_feature_ppm_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_preference_support=%{?tizen_common_feature_preference_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_push_support=%{?tizen_common_feature_push_support}"
#GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_sap_support=%{?tizen_common_feature_sap_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_sensor_support=%{?tizen_common_feature_sensor_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_se_support=%{?tizen_common_feature_se_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_sound_support=%{?tizen_common_feature_sound_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_system_info_support=%{?tizen_common_feature_system_info_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_system_setting_support=%{?tizen_common_feature_system_setting_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_telephony_support=%{?tizen_common_feature_telephony_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_time_support=%{?tizen_common_feature_time_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_inputdevice_support=%{?tizen_common_feature_inputdevice_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_web_setting_support=%{?tizen_common_feature_web_setting_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_widget_service_support=%{?tizen_common_feature_widget_service_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_wi_fi_support=%{?tizen_common_feature_wi_fi_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_tvinputdevice_support=%{?tizen_common_feature_tvinputdevice_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_voicecontrol_support=%{?tizen_common_feature_voicecontrol_support}"

./tools/gyp/gyp $GYP_OPTIONS src/tizen-wrt.gyp

ninja -C out/Default %{?_smp_mflags}
(cd out || exit
mv Default bin_common
)

# common-extension-emulator
%ifarch %{ix86} x86_64

%define tizen_common_feature_bluetooth_support               %{?tizen_common_emulator_feature_bluetooth_support}

# FM radio feature
%define tizen_common_feature_fm_radio_support                %{?tizen_common_emulator_feature_fm_radio_support}

%define tizen_common_feature_ham_support                     %{?tizen_common_emulator_feature_ham_support}
%define tizen_common_feature_media_key_support               %{?tizen_common_emulator_feature_media_key_support}
%define tizen_common_feature_nfc_emulation_support           %{?tizen_common_emulator_feature_nfc_emulation_support}
%define tizen_common_feature_nfc_support                     %{?tizen_common_emulator_feature_nfc_support}

# secure element feature
%define tizen_common_feature_se_support                      %{?tizen_common_emulator_feature_se_support}

# telephony feature
%define tizen_common_feature_telephony_support               %{?tizen_common_emulator_feature_telephony_support}
%define tizen_common_feature_callhistory_support             %{?tizen_common_emulator_feature_callhistory_support}
%define tizen_common_feature_nbs_support                     %{?tizen_common_emulator_feature_nbs_support}

%define tizen_common_feature_wi_fi_support                   %{?tizen_common_emulator_feature_wi_fi_support}

GYP_OPTIONS="--depth=. -Dtizen=1 -Dclang=$is_clang -Dextension_build_type=Debug -Dextension_host_os=common -Dprivilege_engine=%{tizen_common_privilege_engine}"
GYP_OPTIONS="$GYP_OPTIONS -Ddisplay_type=%{display_type}"
GYP_OPTIONS="$GYP_OPTIONS -Dcrosswalk_extensions_path=%{crosswalk_extensions_path}"

# ut flags
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_ut_build=%{tizen_ut_build}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_ut_build_and_run_in_gbs=%{tizen_ut_build_and_run_in_gbs}"

# feature flags
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_account_support=%{?tizen_common_feature_account_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_alarm_support=%{?tizen_common_feature_alarm_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_app_control_settings_support=%{?tizen_common_feature_app_control_settings_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_application_support=%{?tizen_common_feature_application_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_archive_support=%{?tizen_common_feature_archive_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_badge_support=%{?tizen_common_feature_badge_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_bluetooth_support=%{?tizen_common_feature_bluetooth_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_calendar_support=%{?tizen_common_feature_calendar_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_callhistory_support=%{?tizen_common_feature_callhistory_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_contact_support=%{?tizen_common_feature_contact_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_content_support=%{?tizen_common_feature_content_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_datacontrol_support=%{?tizen_common_feature_datacontrol_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_datasync_support=%{?tizen_common_feature_datasync_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_download_support=%{?tizen_common_feature_download_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_exif_support=%{?tizen_common_feature_exif_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_feedback_support=%{?tizen_common_feature_feedback_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_filesystem_support=%{?tizen_common_feature_filesystem_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_fm_radio_support=%{?tizen_common_feature_fm_radio_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_ham_support=%{?tizen_common_feature_ham_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_iotcon_support=%{?tizen_common_feature_iotcon_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_location_batch=%{?tizen_common_feature_location_batch}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_key_manager_support=%{?tizen_common_feature_key_manager_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_media_controller_support=%{?tizen_common_feature_media_controller_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_media_key_support=%{?tizen_common_feature_media_key_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_message_port_support=%{?tizen_common_feature_message_port_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_rpc_port_support=%{?tizen_common_feature_rpc_port_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_metadata_support=%{?tizen_common_feature_metadata_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_ml_support=%{?tizen_common_feature_ml_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_ml_nntrainer_support=%{?tizen_common_feature_ml_nntrainer_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_nbs_support=%{?tizen_common_feature_nbs_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_nfc_emulation_support=%{?tizen_common_feature_nfc_emulation_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_nfc_support=%{?tizen_common_feature_nfc_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_notification_support=%{?tizen_common_feature_notification_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_package_support=%{?tizen_common_feature_package_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_player_util_support=%{?tizen_common_feature_player_util_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_power_support=%{?tizen_common_feature_power_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_ppm_support=%{?tizen_common_feature_ppm_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_preference_support=%{?tizen_common_feature_preference_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_push_support=%{?tizen_common_feature_push_support}"
#GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_sap_support=%{?tizen_common_feature_sap_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_sensor_support=%{?tizen_common_feature_sensor_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_se_support=%{?tizen_common_feature_se_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_sound_support=%{?tizen_common_feature_sound_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_system_info_support=%{?tizen_common_feature_system_info_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_system_setting_support=%{?tizen_common_feature_system_setting_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_telephony_support=%{?tizen_common_feature_telephony_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_time_support=%{?tizen_common_feature_time_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_inputdevice_support=%{?tizen_common_feature_inputdevice_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_web_setting_support=%{?tizen_common_feature_web_setting_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_widget_service_support=%{?tizen_common_feature_widget_service_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_wi_fi_support=%{?tizen_common_feature_wi_fi_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_tvinputdevice_support=%{?tizen_common_feature_tvinputdevice_support}"
GYP_OPTIONS="$GYP_OPTIONS -Dtizen_feature_voicecontrol_support=%{?tizen_common_feature_voicecontrol_support}"

./tools/gyp/gyp $GYP_OPTIONS src/tizen-wrt.gyp

ninja -C out/Default %{?_smp_mflags}
(cd out || exit
mv Default bin_common_emulator
)
%endif # common-extension-emulator

(cd out || exit
%if "%{?profile}" == "common"
ln -sf bin_common Default
%endif
)

%endif # COMMON

# run ut
%if "%{?tizen_ut_build_and_run_in_gbs}" == "1"
export LD_LIBRARY_PATH=out/Default/
out/Default/webapi_common_tests
%if "%{tizen_%{?profile}_feature_bluetooth_support}" == "1"
out/Default/webapi_bluetooth_tests gbs
%endif
%if "%{tizen_%{?profile}_feature_ml_support}" == "1"
out/Default/webapi_ml_tests gbs
%endif
%endif

%install

%if "%{?profile}" == "common"
mkdir -p %{buildroot}%{crosswalk_extensions_path}/common

# tizen ut common
%if "%{?tizen_ut_build}" == "1" || "%{?tizen_ut_build_and_run_in_gbs}" == "1"
mkdir -p %{buildroot}/usr/bin
install -p -m 755 out/bin_common/webapi_common_tests %{buildroot}/usr/bin/
%if "%{tizen_common_feature_bluetooth_support}" == "1"
install -p -m 755 out/bin_common/webapi_bluetooth_tests %{buildroot}/usr/bin/
%endif
%if "%{tizen_common_feature_ml_support}" == "1"
install -p -m 755 out/bin_common/webapi_ml_tests %{buildroot}/usr/bin/
%endif
%endif

install -p -m 644 out/bin_common/libtizen*.so %{buildroot}%{crosswalk_extensions_path}/common
# execute desc_gentool
LD_PRELOAD=libcapi-media-image-util.so LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{crosswalk_extensions_path}/common %{?ld_preload_library} out/Default/desc_gentool \
	%{crosswalk_extensions_path}/common \
	%{buildroot}%{crosswalk_extensions_path}/common > plugins.json

# temporary plugins description for lazy loading
install -p -m 644 plugins.json %{buildroot}%{crosswalk_extensions_path}/common/plugins.json

# common-extension-emulator
%ifarch %{ix86} x86_64
mkdir -p %{buildroot}%{crosswalk_extensions_path}/common_emulator
install -p -m 644 out/bin_common_emulator/libtizen*.so %{buildroot}%{crosswalk_extensions_path}/common_emulator
# execute desc_gentool
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{crosswalk_extensions_path}/common_emulator %{?ld_preload_library} out/Default/desc_gentool \
	%{crosswalk_extensions_path}/common_emulator \
	%{buildroot}%{crosswalk_extensions_path}/common_emulator > plugins.json

# temporary plugins description for lazy loading
install -p -m 644 plugins.json %{buildroot}%{crosswalk_extensions_path}/common_emulator/plugins.json
%endif // common-extension-emulator

%endif // common

# devel files
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp packaging/%{name}.pc.in %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
sed -i s,__LIB_DIR__,%{crosswalk_extensions_path},g %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
sed -i s,__INCLUDE_DIR__,%{_includedir}/%{name}/src,g %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
mkdir -p %{buildroot}%{_includedir}/%{name}/src/common
mkdir -p %{buildroot}%{_includedir}/%{name}/src/common/filesystem
install -p -m 644 src/common/*.h %{buildroot}%{_includedir}/%{name}/src/common
install -p -m 644 src/common/filesystem/*.h %{buildroot}%{_includedir}/%{name}/src/common/filesystem
install -p -m 644 src/common/*.gypi %{buildroot}%{_includedir}/%{name}/src/common
install -p -m 644 src/common/XW_Extension.cc %{buildroot}%{_includedir}/%{name}/src/common
mkdir -p %{buildroot}%{_includedir}/%{name}/tools
install -p -m 644 tools/generate_api.py %{buildroot}%{_includedir}/%{name}/tools
install -p -m 644 tools/mergejs.py %{buildroot}%{_includedir}/%{name}/tools
cp -a tools/gyp %{buildroot}%{_includedir}/%{name}/tools/gyp
cp -a tools/slimit %{buildroot}%{_includedir}/%{name}/tools/slimit
cp -a out/Default/desc_gentool %{buildroot}%{_includedir}/%{name}/tools/desc_gentool

%if "%{?profile}" == "common"
%post profile_common
ln -sf %{crosswalk_extensions_path}/common/* %{crosswalk_extensions_path}
%preun profile_common
# This is an un-installation.
if [ "$1" = "0" ]; then
  if [ -n "$(ls %{crosswalk_extensions_path}/ | grep libtizen*.so)" ]; then
    rm %{crosswalk_extensions_path}/libtizen*.so
  fi
  if [ -f %{crosswalk_extensions_path}/plugins.json ]; then
    rm %{crosswalk_extensions_path}/plugins.json
  fi
fi
%files
%license LICENSE
%manifest webapi-plugins.manifest

%files profile_common
%dir %{crosswalk_extensions_path}/common/
%{crosswalk_extensions_path}/common/libtizen*.so
%{crosswalk_extensions_path}/common/plugins.json
%manifest webapi-plugins.manifest

# UT files
%if "%{?tizen_ut_build}" == "1" || "%{?tizen_ut_build_and_run_in_gbs}" == "1"
%license GTEST.BSD-3-Clause
/usr/bin/webapi_common_tests
%if "%{tizen_common_feature_bluetooth_support}" == "1"
/usr/bin/webapi_bluetooth_tests
%endif
%if "%{tizen_common_feature_ml_support}" == "1"
/usr/bin/webapi_ml_tests
%endif
%endif

# common-extension-emulator
%ifarch %{ix86} x86_64
%post common-extension-emulator
ln -sf %{crosswalk_extensions_path}/common_emulator/* %{crosswalk_extensions_path}
%preun common-extension-emulator
# This is an un-installation.
if [ "$1" = "0" ]; then
  if [ -n "$(ls %{crosswalk_extensions_path}/ | grep libtizen*.so)" ]; then
    rm %{crosswalk_extensions_path}/libtizen*.so
  fi
  if [ -f %{crosswalk_extensions_path}/plugins.json ]; then
    rm %{crosswalk_extensions_path}/plugins.json
  fi
fi
%files common-extension-emulator
%dir %{crosswalk_extensions_path}/common_emulator/
%{crosswalk_extensions_path}/common_emulator/libtizen*.so
%{crosswalk_extensions_path}/common_emulator/plugins.json
%manifest webapi-plugins.manifest
%endif // common-extension-emulator
%endif // common

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*
