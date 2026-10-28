Name:        capi-media-vision
Summary:     Media Vision library for Tizen Native API
Version:     1.0.17
Release:     0
Group:       Multimedia/Framework
License:     Apache-2.0
Source0:     %{name}-%{version}.tar.gz
BuildRequires: cmake
BuildRequires: pkgconfig(capi-media-tool)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(opencv)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(iniparser)
BuildRequires: pkgconfig(inference-engine-interface-common)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(zbar)
# Change to the pkgconfig(zint) after zint package refactor
BuildRequires: zint
BuildRequires: zint-devel
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libswscale)
BuildRequires: libavutil-devel
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(gstreamer-base-1.0)
BuildRequires: pkgconfig(gstreamer-app-1.0)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(ncurses)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(glesv2)
BuildRequires: gtest-devel
BuildRequires: pkgconfig(dfs-adaptation)
BuildRequires: pkgconfig(capi-appfw-application)
%if 0%{?visualizer:1}
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(grpc++)
%endif

# Build options
# ENABLE_INFERENCE_PROFILER
# 0 : disable Mediavision inference engine profiler, 1 : enable Mediavision inference engine profiler.
%define enable_mv3d_pointcloud 0
%if "%{tizen_profile_name}" == "tv"
%define enable_ml_face_recognition 0
%define build_depth_stream_testsuite 0
%define enable_ml_gaze_tracking 0
%else
%define enable_ml_face_recognition 1
BuildRequires: pkgconfig(training-engine-interface-common)
Requires:      training-engine-interface-common

%define enable_ml_image_classification 1
%define enable_ml_object_detection 1
%define enable_ml_object_detection_3d 1
%define enable_ml_landmark_detection 1
%define enable_ml_image_segmentation 1
%define enable_ml_gaze_tracking 1

%define build_depth_stream_testsuite 1
BuildRequires: pkgconfig(vision-source)
%ifarch aarch64
%define enable_mv3d_pointcloud 1
BuildRequires: Open3D-devel
%endif
%endif
%define build_options -DENABLE_INFERENCE_PROFILER=0 -DBUILD_DEPTH_STREAM_TESTSUITE=%{build_depth_stream_testsuite} -DMV_3D_POINTCLOUD_IS_AVAILABLE=%{enable_mv3d_pointcloud}
%define task_group_options -DENABLE_ML_FACE_RECOGNITION=%{enable_ml_face_recognition} -DENABLE_ML_IMAGE_CLASSIFICATION=%{enable_ml_image_classification} -DENABLE_ML_OBJECT_DETECTION=%{enable_ml_object_detection} -DENABLE_ML_OBJECT_DETECTION_3D=%{enable_ml_object_detection_3d} -DENABLE_ML_LANDMARK_DETECTION=%{enable_ml_landmark_detection} -DENABLE_ML_IMAGE_SEGMENTATION=%{enable_ml_image_segmentation} -DENABLE_ML_GAZE_TRACKING=%{enable_ml_gaze_tracking}
Requires:   %{name}-machine_learning
Requires:   inference-engine-interface-common
Requires:   %{name}-barcode
Requires:   %{name}-face
Requires:   %{name}-image
Requires:   %{name}-surveillance
Requires:   %{name}-3d
Requires:   %{name}-roi_tracker

%description
Media Vision library for Tizen Native API. Includes barcode detecting, barcode generating, face and image modules.

%package devel
Summary:    Multimedia Vision Library (DEV)
Group:      Multimedia/Framework
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-barcode-devel
Requires:   %{name}-face-devel
Requires:   %{name}-image-devel
Requires:   %{name}-machine_learning-devel
Requires:   %{name}-surveillance-devel
Requires:   %{name}-3d-devel
Requires:   %{name}-roi_tracker-devel

%description devel
Media Vision library for Tizen Native API (DEV). Includes barcode detecting, barcode generating, face and image modules.

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Media Vision library for Tizen Native API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is teseted as gcov for a Media Vision for Tizen Native API
%endif

%package common
Summary:    Multimedia Vision common Library
Group:      Multimedia/Framework

%description common
Media Vision common library for Tizen Native API.

%package common-devel
Summary:    Multimedia Vision common Library
Group:      Multimedia/Framework
Requires:   %{name}-common

%description common-devel
Media Vision common library for Tizen Native API (DEV).

%package barcode
Summary:    Multimedia Vision Barcode Library
Group:      Multimedia/Framework
Requires:   %{name}-common

%description barcode
Media Vision barcode library for Tizen Native API.

%package barcode-devel
Summary:    Multimedia Vision Barcode Library
Group:      Multimedia/Framework
Requires:   %{name}-barcode
Requires:   %{name}-common-devel

%description barcode-devel
Media Vision barcode library for Tizen Native API (DEV).

%package face
Summary:    Multimedia Vision Library
Group:      Multimedia/Framework
Requires:   %{name}-common

%description face
Media Vision face library for Tizen Native API.

%package face-devel
Summary:    Multimedia Vision Face Library (DEV)
Group:      Multimedia/Framework
Requires:   %{name}-face
Requires:   %{name}-common-devel

%description face-devel
Media Vision face library for Tizen Native API (DEV).

%package image
Summary:    Multimedia Vision Image Library
Group:      Multimedia/Framework
Requires:   %{name}-common

%description image
Media Vision Image library for Tizen Native API.

%package image-devel
Summary:    Multimedia Vision Image Library
Group:      Multimedia/Framework
Requires:   %{name}-image
Requires:   %{name}-common-devel

%description image-devel
Media Vision Image library for Tizen Native API (DEV).

%package surveillance
Summary:    Multimedia Vision Surveillance Library
Group:      Multimedia/Framework
Requires:   %{name}-face

%description surveillance
Media Vision Surveillance library for Tizen Native API.

%package surveillance-devel
Summary:    Multimedia Vision Surveillance Library
Group:      Multimedia/Framework
Requires:   %{name}-surveillance
Requires:   %{name}-common-devel

%description surveillance-devel
Media Vision Surveillance library for Tizen Native API (DEV).

%package 3d
Summary:    Multimedia Vision 3d Library
Group:      Multimedia/Framework
Requires:   %{name}-common

%description 3d
Media Vision 3d library for Tizen Native API.

%package 3d-devel
Summary:    Multimedia Vision 3d Library
Group:      Multimedia/Framework
Requires:   %{name}-3d
Requires:   %{name}-common-devel

%description 3d-devel
Media Vision 3d library for Tizen Native API (DEV).

%package machine_learning
Summary:    Multimedia Vision Machine Learning Library
Group:      Multimedia/Framework
Requires:   %{name}-common

%description machine_learning
Media Vision Machine Learning library for Tizen Native API.

%package machine_learning-devel
Summary:    Multimedia Vision Machine Learning Library
Group:      Multimedia/Framework
Requires:   %{name}-machine_learning
Requires:   %{name}-common-devel

%description machine_learning-devel
Media Vision Machine Learning library for Tizen Native API (DEV).


%package roi_tracker
Summary:    Multimedia Vision Library
Group:      Multimedia/Framework
Requires:   %{name}-common

%description roi_tracker
Media Vision roi tracker library for Tizen Native API.

%package roi_tracker-devel
Summary:    Multimedia Vision ROI Tracker Library (DEV)
Group:      Multimedia/Framework
Requires:   %{name}-roi_tracker
Requires:   %{name}-common-devel

%description roi_tracker-devel
Media Vision roi_tracker library for Tizen Native API (DEV).

%package unittests
Summary:    Multimedia Vision Test Suite
Group:      Multimedia/Framework
Requires:   %{name}-barcode
Requires:   %{name}-face
Requires:   %{name}-image
Requires:   %{name}-surveillance
Requires:   %{name}-machine_learning
Requires:   %{name}-3d
Requires:   %{name}-roi_tracker

%description unittests
Media Vision Test Suite.

%prep
%setup -q

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

export CFLAGS+=" -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export CXXFLAGS+=" -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""

export CFLAGS+=" -DMV_CONFIG_PATH=\\\"%{TZ_SYS_RO_SHARE}/%{name}/\\\""
export CXXFLAGS+=" -DMV_CONFIG_PATH=\\\"%{TZ_SYS_RO_SHARE}/%{name}/\\\""

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

mkdir -p build
cd build
%cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo %{build_options} %{task_group_options} \
 -DTEST_RES_PATH="%{TZ_SYS_HOME}/%{TZ_SYS_DEFAULT_USER}/media/Others/mv_test" \
%if 0%{?_with_da_profile:1}
 -DWITH_DA_PROFILE=ON \
%endif
%if 0%{?visualizer:1}
 -DBUILD_VISUALIZER=ON \
%endif
%ifarch %arm aarch64
-DENABLE_NEON=ON
%endif

make %{?jobs:-j%jobs}

%install

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 script/run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}

cd build
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
pkg_version_path=$(basename "$(dirname $PWD)")
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$pkg_version_path"/${builddir}
mkdir -p "$gcno_obj_dir"

find . -name '*.gcno' -not -path "./test/*" -not -path "./mv_machine_learning/*" \
-exec cp --parents '{}' "$gcno_obj_dir" ';'

%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.APLv2

%files devel
%{_libdir}/pkgconfig/%{name}.pc

%files common
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_datadir}/%{name}/media-vision-config.json
%{_libdir}/libmv_common*.so

%files common-devel
%{_includedir}/media/mv_common.h
%{_libdir}/pkgconfig/*common.pc

%files barcode
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_libdir}/libmv_barcode*.so

%files barcode-devel
%{_includedir}/media/mv_barcode*.h
%{_libdir}/pkgconfig/*barcode.pc

%files face
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_libdir}/libmv_face*.so

%files face-devel
%{_includedir}/media/mv_face*.h
%{_libdir}/pkgconfig/*face.pc

%files image
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_libdir}/libmv_image.so

%files image-devel
%{_includedir}/media/mv_image*.h
%{_libdir}/pkgconfig/*image.pc

%files surveillance
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_libdir}/libmv_surveillance*.so

%files surveillance-devel
%{_includedir}/media/mv_surveillance*.h
%{_libdir}/pkgconfig/*surveillance.pc

%files 3d
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_libdir}/libmv_3d*.so

%files 3d-devel
%{_includedir}/media/mv_3d.h
%{_includedir}/media/mv_3d_type.h
%{_includedir}/media/mv_3d_internal.h
%{_includedir}/media/mv_3d_private.h
%{_libdir}/pkgconfig/*3d.pc

%files machine_learning
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_libdir}/libmv_inference*.so
%{_libdir}/libmv_ml_common.so
%if "%{enable_ml_face_recognition}" == "1"
%{_datadir}/%{name}/face_recognition.json
%{_libdir}/libmv_training.so
%{_libdir}/libmv_face_recognition.so
%endif
%if "%{enable_ml_image_classification}" == "1"
%{_datadir}/%{name}/image_classification.json
%{_libdir}/libmv_image_classification.so
%endif
%if "%{enable_ml_object_detection}" == "1"
%{_datadir}/%{name}/object_detection.json
%{_datadir}/%{name}/object_detection_plugin.json
%{_datadir}/%{name}/face_detection.json
%{_datadir}/%{name}/face_detection_plugin.json
%{_datadir}/%{name}/hand_detection.json
%{_datadir}/%{name}/hand_detection_plugin.json
%{_libdir}/libmv_object_detection.so
%endif
%if "%{enable_ml_object_detection_3d}" == "1"
%{_datadir}/%{name}/object_detection_3d.json
%{_libdir}/libmv_object_detection_3d.so
%endif
%if "%{enable_ml_landmark_detection}" == "1"
%{_datadir}/%{name}/facial_landmark.json
%{_datadir}/%{name}/pose_landmark.json
%{_datadir}/%{name}/hand_landmark.json
%{_libdir}/libmv_landmark_detection.so
%endif
%if "%{enable_ml_image_segmentation}" == "1"
%{_datadir}/%{name}/selfie_segmentation.json
%{_datadir}/%{name}/selfie_segmentation_plugin.json
%{_libdir}/libmv_image_segmentation.so
%endif
%if "%{enable_ml_gaze_tracking}" == "1"
%{_datadir}/%{name}/gaze_tracking.json
%{_datadir}/%{name}/gaze_tracking_plugin.json
%{_libdir}/libmv_gaze_tracking.so
%endif

%files machine_learning-devel
%{_includedir}/media/mv_infer*.h
%{_includedir}/media/MvMlException.h
%{_includedir}/media/MvMlConfig.h
%{_includedir}/media/mv_ml_types.h
%{_includedir}/media/MvMlPreprocess.h
%{_libdir}/pkgconfig/*inference.pc
%if "%{enable_ml_face_recognition}" == "1"
%{_includedir}/media/mv_face_recognition*.h
%{_libdir}/pkgconfig/*training.pc
%{_libdir}/pkgconfig/*face-recognition.pc
%endif
%if "%{enable_ml_image_classification}" == "1"
%{_includedir}/media/mv_image_classification_internal.h
%{_includedir}/media/mv_image_classification.h
%{_includedir}/media/mv_image_classification_type.h
%{_libdir}/pkgconfig/*image-classification.pc
%endif
%if "%{enable_ml_object_detection}" == "1"
%{_includedir}/media/mv_object_detection_internal.h
%{_includedir}/media/mv_object_detection.h
%{_includedir}/media/mv_object_detection_type.h
%{_includedir}/media/mv_face_detection_internal.h
%{_includedir}/media/mv_face_detection.h
%{_includedir}/media/mv_face_detection_type.h
%{_includedir}/media/IObjectDetection.h
%{_includedir}/media/object_detection_type.h
%{_libdir}/pkgconfig/*object-detection.pc
%{_includedir}/media/mv_hand_detection_internal.h
%{_includedir}/media/mv_hand_detection.h
%{_includedir}/media/mv_hand_detection_type.h

%endif
%if "%{enable_ml_object_detection_3d}" == "1"
%{_includedir}/media/mv_object_detection_3d_internal.h
%{_includedir}/media/mv_object_detection_3d_type.h
%{_libdir}/pkgconfig/*object-detection-3d.pc
%endif
%if "%{enable_ml_landmark_detection}" == "1"
%{_includedir}/media/mv_facial_landmark_internal.h
%{_includedir}/media/mv_facial_landmark.h
%{_includedir}/media/mv_facial_landmark_type.h
%{_includedir}/media/mv_pose_landmark_internal.h
%{_includedir}/media/mv_pose_landmark.h
%{_includedir}/media/mv_pose_landmark_type.h
%{_includedir}/media/mv_hand_landmark_internal.h
%{_includedir}/media/mv_hand_landmark.h
%{_includedir}/media/mv_hand_landmark_type.h
%{_libdir}/pkgconfig/*landmark-detection.pc
%endif
%if "%{enable_ml_image_segmentation}" == "1"
%{_includedir}/media/mv_selfie_segmentation_internal.h
%{_includedir}/media/mv_selfie_segmentation_type.h
%{_includedir}/media/IImageSegmentation.h
%{_includedir}/media/image_segmentation_type.h
%{_libdir}/pkgconfig/*image-segmentation.pc
%endif
%if "%{enable_ml_gaze_tracking}" == "1"
%{_includedir}/media/mv_gaze_tracking.h
%{_includedir}/media/mv_gaze_tracking_internal.h
%{_includedir}/media/mv_gaze_tracking_type.h
%{_includedir}/media/gaze_tracking_type.h
%{_libdir}/pkgconfig/*gaze-tracking.pc
%endif

%files roi_tracker
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_libdir}/libmv_roi_tracker.so

%files roi_tracker-devel
%{_includedir}/media/mv_roi_tracker*.h
%{_libdir}/pkgconfig/*tracker.pc

%files unittests
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_libdir}/libmv_*helper.so
%if 0%{?visualizer:1}
%{_libdir}/libmv_visualizer.so
%endif
%{_bindir}/mv_*
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
