Name:        singleo
Summary:     SingleO AI Service Framework
Version:     0.0.1
Release:     0
Group:       Multimedia/Framework
License:     Apache-2.0
Source0:     %{name}-%{version}.tar.gz
BuildRequires: cmake
BuildRequires: pkgconfig(capi-media-vision)
BuildRequires: pkgconfig(capi-media-tool)
BuildRequires: pkgconfig(capi-media-camera)
BuildRequires: pkgconfig(opencv)
BuildRequires: pkgconfig(dlog)
BuildRequires: gtest-devel
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(grpc++)
BuildRequires: pkgconfig(re2)

%define enable_visualizer 0

%description
SingleO AI Service Framework

%package devel
Summary:    SingleO AI Service Framework
Group:      Multimedia/Framework
Requires:   %{name}

%description devel
SingleO AI Service Framework (Dev)

%package test
Summary:    Test case for SingleO AI Service Framework
Group:      Multimedia/Framework
Requires:   %{name}

%description test
Test case for SingleO AI Service Framework (Dev)

%prep
%setup -q

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

export CFLAGS+=" -DPATH_LIBDIR=\\\"%{_libdir}\\\" -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export CXXFLAGS+=" -DPATH_LIBDIR=\\\"%{_libdir}\\\" -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DTZ_SYS_BIN=%TZ_SYS_BIN \
         -DPLATFORM_IS_TIZEN=ON \
         -DUSE_EXTERNAL_INFERENCE_SERVICE=OFF \
         -DUSE_INPUT_OPENCV_BACKEND=ON \
         -DUSE_AUTOZOOM_API=ON \
         -DUSE_FOCUSFINDER_API=ON \
         -DUSE_INPUT_CAMERA_API_BACKEND=ON \
		 -DUSE_VISUALIZER=%{enable_visualizer}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest singleo.manifest
%license LICENSE.APLv2
%{_libdir}/libsingleo_service.so
%if "%{enable_visualizer}" == "1"
%{_libdir}/libsingleo_visualizer.so
%endif

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/media/singleo/IInferenceTaskFactory.h
%{_includedir}/media/singleo/IInferenceTaskInterface.h
%{_includedir}/media/singleo/InferenceTaskFactory.h
%{_includedir}/media/singleo/SingleoInferenceTypes.h
%{_includedir}/media/singleo/SingleoCommonTypes.h
%{_includedir}/media/singleo/SingleoException.h
%{_includedir}/media/singleo/singleo_error.h
%{_includedir}/media/singleo/SharedBuffer.h
%{_includedir}/media/singleo/IService.h
%{_includedir}/media/singleo/AsyncManager.h
%{_includedir}/media/singleo/IPreprocessor.h
%{_includedir}/media/singleo/IPostprocessor.h
%{_includedir}/media/singleo/ImagePreprocessor.h
%{_includedir}/media/singleo/ServiceConfigParser.h
%{_includedir}/media/singleo/ServiceDataType.h
%{_includedir}/media/singleo/ServiceFactory.h
%{_includedir}/media/singleo/SingleoLog.h
%{_includedir}/media/singleo/SingleoLogBackend.h
%{_includedir}/media/singleo/SingleoLogType.h
%{_includedir}/media/singleo/IInputService.h
%{_includedir}/media/singleo/InputCamera.h
%{_includedir}/media/singleo/IInputObserver.h
%{_includedir}/media/singleo/InputTypes.h

%files test
%{_bindir}/test_singleo
%if "%{enable_visualizer}" == "1"
%{_bindir}/test_singleo_on_screen
%endif
%{_bindir}/test_singleo_task_manger
